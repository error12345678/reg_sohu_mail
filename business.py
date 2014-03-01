import base
import session.session as session
import random
import account_mgr
import time
import json

add_header = {
              "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36",
              }

class SohuMailbox(object):
    def __init__(self):
        self.__browser = session.Session()
        self.__prev_username = None
        self.__prev_password = None

    def submit(self,code):
        mgr = account_mgr.account_mgr
        if not self.__prev_username:
            while True:
                self.__prev_username,self.__prev_password = mgr.get_new_account()
                self.__prev_username = self.__prev_username[0:16]
                if not self.is_registered(self.__prev_username):
                    break
                else:
                    mgr.add_account(self.__prev_username,self.__prev_password,False)
        action = "http://passport.sohu.com/web/Passportregister.action"
        data = {
            "shortname":self.__prev_username,
            "domainName":"sohu.com",
            "user.password": self.__prev_password,
            "password2": self.__prev_password,
            "validate":code.encode("gbk"),
            "uuidCode":"",
            "app_para":"appid=1113",
            "ot_registerid":"",
            "registerid":"",
            "appid":"1113",
            "autologin":"1",
            "ru":"http://mail.sohu.com/reg/signup_success.jsp",
            "registerType":"Passport",
            "showAllType":"0"
         }
        print "########## SUBMIT #########################"
        import copy
        new_add_header = copy.copy(add_header)
        #new_add_header["Referer"] = "http://passport.sohu.com/web/Passportregister.action"
        response = self.__browser.send_form(action,"POST",data,new_add_header)
        html = response.body
        if not html:
            return (False,response.error)
        html = html.decode("gbk")
        if html.find(u"验证码不正确，请重新输入") != -1:
            return (False,u"验证码不正确，请重新输入")
        if html.find(u"恭喜您，已经成功注册搜狐通行证") != -1:
            mgr.add_account(self.__prev_username,self.__prev_password)
            self.__prev_username,self.__prev_password = None,None
            return (True,None)
        self.__prev_username,self.__prev_password = None,None
        return (False,html)

    def is_registered(self,username):
        test_url = "http://passport.sohu.com/jsonajax/checkusername.action?shortname=%s&domain=sohu.com&appid=1000&_t=%d&mobileReg=false" %(
                    username,int(time.time()*1000))
        response = self.__browser.fetch(test_url,"GET",add_header,None)
        try:
            ret = json.loads(response.body)
            if ret["status"] == "1":
                return True
        except Exception,e:
            pass
        return False

    def get_next(self):
        self.__browser.fetch("http://mail.sohu.com/","GET",add_header,None)
        code_img_url = "http://passport.sohu.com/servlet/Captcha?time=%f" % random.random()
        response = self.__browser.fetch(code_img_url,"GET",add_header,None)
        code_img_url = "http://passport.sohu.com/servlet/Captcha?time=%f" % random.random()
        response = self.__browser.fetch(code_img_url,"GET",add_header,None)
        print "##########GET NEW PICTURE#########################"
        self.__browser.report()
        if response.body:
            handler = open("code.png","wb")
            handler.write(response.body)
            handler.close()
            return True
        return (False,response.error)

