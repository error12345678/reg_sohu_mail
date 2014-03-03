# -*- coding: utf-8 -*-

import base
import session.session as session
import random
import time
import copy
import tornado.ioloop
import json
import urllib
import md5

add_header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36",
                      }

class SohuMailbox(object):
    def __init__(self,username,password,posted_handler,err_list_handler,virtual_ip=""):
        self.__browser = session.AsyncSession()
        global add_header
        self.__username = username
        self.__password = password
        self.__add_header = copy.copy(add_header)
        if virtual_ip:
            self.__add_header["X-Forwarded-For"] = virtual_ip
            self.__add_header["X-Real-IP"] = virtual_ip
        self.__posted_handler = posted_handler
        self.__err_list_handler = err_list_handler

    def on_login(self,response):
        if response.error:
            deadline = time.time() + 10
            tornado.ioloop.IOLoop.instance().add_timeout(deadline,self.login)
        else:
            self.__browser.fetch("http://mail.sohu.com/","GET",self.__add_header,None,self.on_browser_redirect_page)

    def on_browser_redirect_page(self,response):
        global count
        global ok
        action = response.effective_url
        count += 1
        pos = self.__username.find("@")
        username = self.__username[:pos]
        if action.find("main") == -1:
            self.__err_list_handler.write("%s %s\n"% username,self.__password)
            self.__err_list_handler.flush()
        else:
            ok += 1
            action = action.replace("main","mail")
            self.__posted_handler.write("%s %s %s\n" % (username,self.__password,action))
            self.__posted_handler.flush()
        print "count:%d,ok:%d" % (count,ok)
                  
    def login(self):
        self.__browser.clear()
        user_field = {"userid":self.__username}
        user_arg = urllib.urlencode(user_field)
        action = "https://passport.sohu.com/sso/login.jsp?%s&password=%s&appid=1113&persistentcookie=0&s=%d&b=7&w=1920&pwdtype=1&v=26" %(
                   user_arg,md5.new(self.__password).hexdigest(),int(time.time()*1000))
        self.__browser.fetch(action,"GET",self.__add_header,None,self.on_login)

ip_list = []
count = 0
ok = 0

def get_virtual_ip():
    global ip_list
    first = 10
    while True:
        second = random.randint(2,250)
        third = random.randint(2,250)
        fourth = random.randint(2,250)
        ip = "%d.%d.%d.%d" % (first,second,third,fourth)
        if ip not in ip_list:
            ip_list.append(ip)
            break
    return ip

if __name__ == "__main__":
    account_file = open("reglist.txt","r")
    posted_handler = open("sohu_mail.txt","w")
    err_handler = open("err_list.txt","w")
    timespan = 0
    for line in account_file:
        line = line.strip()
        pos = line.find(" ")
        if pos == -1:
            continue
        username = line[:pos]
        password = line[pos:]
        password = password.strip()
        if not password:
            continue
        virtual_ip = get_virtual_ip()
        box = SohuMailbox("%s@sohu.com"%username,password,posted_handler,err_handler,virtual_ip)
        tornado.ioloop.IOLoop().instance().add_timeout(time.time()+timespan,box.login)
        timespan += 0.1
    #while True:
    #    ret = box.sendmail()
    #    count += 1
    #    seg = "<code>"
    #    pos = ret.find(seg)
    #    success = False
    #    if pos != -1:
    #        start = pos + len(seg)
    #        pos = ret.find("<",start)
    #        if pos != -1:
    #            if ret[start:pos] == "S_OK":
    #                ok += 1
    #                success = True
    #    print "total:%d,ok:%d" % (count,ok)
    #    if not success:
    #        print ret
    #    time.sleep(60*10)
    print "the server is running..."
    tornado.ioloop.IOLoop().instance().start()
