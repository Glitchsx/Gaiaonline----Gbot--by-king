#!/usr/bin/env python
#   @author - king
#   @website - www.glitch.sx
#   @version - 0.1.200
#   
#   @keywords -/
#   help, main, test , functions, mechanize, lxml, python, 2.7.3, requests,
#   hacking,black,hat,glitch,multiplayer
#
#   @description -/
#   Hel.py
#   Working on a group of functions to re-use in daily hacking
#   along with general programing tests
#   Included function examples
#   -Display with timestamp
#   -timeout
#   -thirdparty library test
#   -Proxy list reader

import time
import sys
import random
import urllib

class helpy:
    def __init__(self):
        pass
    def display(self,str_message, display_time=True):
        '''/
        @args
        str_message - take a string message, and format it.
        [display_time] - if true will formate message with a timestamp
        '''
        if display_time is True:
            print("[ " + time.strftime('%X') + " ] " + str_message )
        else:
            print(set_message)

    def test_lib(self,name):
        '''/
            Check if a given third party library can be imported
        '''
        try:
            exec(str("import "+name))
            return True
        except:
            pip_url = "https://pypi.python.org/pypi/"
            self.display("Failed Importing " + str(name))
            self.display("Visit " + pip_url + str(name) + " for more information")
            return False

    def timeout(self):
        '''/
            some timer function
        '''
        quit_time = time.time() + 60
        while time.time() != quit_time:
            pass
            
    def terminate_process(self):
        '''/
            Display some messages and quit program
        '''
        self.display("Program will terminate in 60 seconds")
        self.timeout()
        self.display("Quiting...")
        sys.exit()      

    def list_builder(self,filename):
        '''/
            read file and build list
        '''
        _list = []
        fh = open(filename,'r+')
        for line in fh:
            _list.append(line.strip())
        return _list

    def random_item(self,filename):
        '''/
            return item from list
        '''
        _list = self.list_builder(filename)
        return _list[random.randint(0, len(_list)-1)]
                           
    def phttp(self,proxy,header):
        '''/
            phttp returns a mechanize browser
            @proxy - set and ip,and port to direct traffic
            @header - user agent data
        '''
        import mechanize
        browser = mechanize.Browser();
        browser.addheaders = [{'user-agent',header}]
        cookie_jar = mechanize.CookieJar()
        browser.set_cookiejar = cookie_jar
        try:
            if not eval(proxy) == None:
                browser.set_proxies({"http": proxy})
        except:
            pass #-not using proxy
        browser.set_handle_robots(False)
        browser.set_handle_refresh(False)
        return browser
    
    def require(self, module):
        '''/
            require is a method to check for a third party library
            kills terminate_process nicely if not
        '''
        if self.test_lib(module) is False:
            self.display(str(module) + " is required to run this script")
            self.terminate_process()
        else:
            self.display(str(module + " found"))
        
