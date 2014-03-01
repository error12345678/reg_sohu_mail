import os

class AccountMgr(object):
    def __init__(self):
        self.__handler_history = open("lastline.txt","r+")
        self.__last_num = int(self.__handler_history.readline().strip())
        self.__src_account_file = open("namelist.txt","r")
        for i in range(self.__last_num):
            self.__src_account_file.readline()
        self.__active_account_file = open("reglist.txt","a")
        self.__bad_account_file = open("badlist.txt","a")

    def get_new_account(self):
        line = self.__src_account_file.readline()
        line = line.strip()
        pos = line.find(" ")
        username = line[:pos]
        password = line[pos:]
        password = password.strip()
        self.__last_num += 1
        self.__handler_history.seek(0)
        self.__handler_history.write(str(self.__last_num)+"\n")
        self.__handler_history.flush()
        os.fsync(self.__handler_history)
        return (username,password)

    def add_account(self,username,password,is_ok=True):
        if is_ok:
            handler = self.__active_account_file
        else:
            handler = self.__bad_account_file
        handler.seek(0,os.SEEK_END)
        handler.write("%s %s\n"%(username,password))
        handler.flush()
        os.fsync(handler)

    def quit(self):
        self.__handler_history.close()
        self.__active_account_file.close()
        self.__bad_account_file.close()

account_mgr = AccountMgr()

if __name__ == "__main__":
    print "Get Two Account:"
    account1 = account_mgr.get_new_account()
    account2 = account_mgr.get_new_account()
    print account1
    print account2

    print "Add a registered account:\n"
    print account2
    account_mgr.add_account(account2[0],account2[1])

    print "Add a bad account:\n"
    print account1
    account_mgr.add_account(account1[0],account1[1],False)

    raw_input("press")
    account_mgr.quit()
