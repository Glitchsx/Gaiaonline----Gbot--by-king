import hel
import threading
import re
import random
import json
import time
import mechanize

class gbot(threading.Thread):
    def __init__(self,username,password):
        '''/
        Initialize function
        Sets up browser with ease using helpy scripts
        stores url and some other user data
        '''
        threading.Thread.__init__(self)
        #- Build browser for web process
        self.helpy = hel.helpy()
        self.br = self.helpy.phttp(
            self.helpy.random_item("proxies.txt"),
            self.helpy.random_item("user-agents.txt") )
        #- Initialize Variables
        self.username = username
        self.password = password
        self.home = "http://www.gaiaonline.com"
        self.gsi = self.home + "/chat/gsi/?"
        self.gold_amt = ''
        self.ssid = ''
        self.tokens = ''
        self.tickets = ''

    #- Begin run program
    def run(self):
        '''/
        Main run method
        '''
        login_check = self.login()
        if login_check:
            self.sid()
            self.update_gold()
            self.helpy.display(self.username + " : " + self.gold_amt )
            self.grab_dailies()
            self.cashout()
            while True:
                self.pull()
                self.vote_arena()
                self.dumpster_dive()
        else:
            self.helpy.display(self.username + " failed to login")
    #- End run program
                         
    #- Begin login
    def login(self):
        '''/
        Login function using mechanize
        '''
        url = self.home + "/auth/login"
        try:
            self.br.open(url)
            self.br.select_form(nr=0) #this identifies what form to use.
            self.br["username"] = self.username
            self.br["password"] = self.password
            self.br.submit()# fill in login information.
            html = self.br.response().read()
            if "<title>Welcome to Gaia | Gaia Online</title>" in html:
                return True
        except:
            pass
        return False
    #- End login

    #- Begin SID
    def sid(self):
        '''/
        Sid is a session ID used for GSI method calls
        '''
        url = self.gsi + 'v=json&m=[[109]]'
        try:
            response = self.br.open( url ).read()
            self.ssid = str(json.loads(response)[0][2])
        except:
            pass
    #- End SID
        
    #- Begin Gold
    def update_gold(self):
        '''handy function used to track gold'''
        url = self.gsi + '''v=json&m=[[113,["'''+ self.ssid + '''"]]]'''
        try:
            response = self.br.open( url ).read()
            self.gold_amt = str(json.loads(response)[0][2])
        except:
            pass
    #- End Gold

    #- Begin daily chance
    def grab_dailies(self):
        '''grab the available daily chances'''
        for daily_id in [1,2,3,4,5,8]:
            url = self.home + "/dailycandy/?mode=ajax&action=issue&list_id=" + str(daily_id)
            try:
                self.br.open( url )
                response = self.br.response().get_data()
                if "success" in response:
                    reward = re.search('<name>(.*?)</name>', response ).group(1)
                    self.helpy.display(self.username+ ": found " + reward )
                else:
                    self.helpy.display(self.username + " : Dailies Failed...skipping...")
                    break
            except:
                pass
    #- End daily chance

    #- Being Dumpstr Dive
    def dumpster_dive(self):
        '''/
        Dumpster Dive function for getting random items for free
        '''
        url = self.home + "/dumpsterdive/"
        try:
            response = self.br.open(url, "mode=showConfirmed").read()
            reward = re.search('<div id="grant_text1">(.*?)</div>', response).group(1)
            self.helpy.display("|||||" + ": Found " + reward)
            Timer.sleep(random.randint(60*6))
        except:
            return None

    #- End Dumpster dive

    #- Being arena voter
    def vote_arena(self):
        '''/
        Simple gold-gen function for making money in arenas
        '''
        arenas = [
        "/arena/art/comics/vote/#title",
        "/arena/art/painting-and-drawing/vote/#title",
        "/arena/art/photography/vote/#title",
        "/arena/writing/fiction/vote/#title",
        "/arena/writing/non-fiction/vote/#title",
        "/arena/writing/poetry-and-lyrics/vote/#title",
        "/arena/writing/high-school-flashback/vote/#title",
        "/arena/gaia/homes/vote/#title",
        "/arena/gaia/original-avatar/vote/#title",
        "/arena/gaia/cosplay-avatar/vote/#title"
        ]
        url = self.home + random.choice(arenas)
        try:
            self.br.open(url)
            response = self.br.response().get_data()
            if "url:" in response:
                vote_url = re.search("url:'(.*?)'",response ).group(1) #get voting url
                vote_url = self.home + vote_url + str(random.randint(1,5) )
                self.br.open( vote_url )
        except:
            pass
        time.sleep(random.randint(3,15))
    #- End arena voter

    #- Being slots
    def slot_data(self):
        '''/
        This method reads your game data
        Sets Variables tickets and tokens
        '''
        url = self.gsi + '''v=json&m=[[801,["'''+ self.ssid + '''"]]]'''
        try:
            response = self.br.open(url).read()
            data = json.loads(response)
            self.tickets = data[0][2]['tickets'].replace("u'",'')
            self.tokens = data[0][2]['tokens'].replace("u'",'')
        except:
            pass

    def cashout(self):
        '''/
        Put winnings from slots into inventory
        '''
        url = self.gsi + '''v=json&m=[[803,["'''+ self.ssid + '''"]]]'''
        try:
            self.br.open(url) 
        except:
            pass
    
    def pull(self):
        '''/
        Call GSI 800, the only one I couldn't figure out how to clean up.
        Will pull slots for tickets
        '''
        url = self.gsi + 'v=phpobject&m=a:1:{i:0;a:2:{i:0;s:3:"800";i:1;a:6:{i:0;i:3;i:1;i:0;i:2;s:' + str(48) + ':"' + self.ssid + '";i:3;i:5794798;i:4;s:32:"746c80e1a272edc034abbdf090bdd715";i:5;i:1;}}}'
        try:
            self.br.open(url)
            time.sleep(random.randint(3,30))
        except:
            pass

    #def buy_tokens(self): scraped function
    #    '''
    #    url = self.home + "/gaia/shopping.php?key=ndroctlqvprghqqy"
    #    try:
    #        response = self.br.open(url)
    #        nonce = re.search('''&amp;nonce=(.*?)&amp;''',response.read()).group(1)
    #        data = urllib.urlencode({'item_id':100045,
    #            'quantity':100,
    #             'key':"ndroctlqvprghqqy",
    #             'nonce':nonce,
    #             'serial':'',
    #             'offerids':'',
    #             'mode':'buyq'})
    #        response = self.br.open(url,data)
    #    except:
    #        pass
    #- End Slots
                         
    ### Begin Poll Whore - SCRAPED FUNCTION
    #def poll(self):
    #    random_thread = str(random.randint(1000000,9000000))
    #    url = self.home + "/forum/chatterbox/t."+random_thread+"/"
    #    try:
    #        html = self.br.open(url)
    #        self.helpy.display(self.username + " - Voting in poll...")
    #        nonce = re.search('''name="nonce" value="(.*?)"''',line)
    #        post_data = {"optionid":0,"nonce":nonce,"t":random_thread}
    #        self.br.urlopen(request, urllib.urlencode(post_data))
    #        self.display(self.username + "...polling...")
    #        threading.Timer( random.randint(45,120), self.poll).start()
    #    except:
    #        self.poll()
    ### End Poll Whore                     
