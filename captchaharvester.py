# coding=utf-8
import random
import sys
import threading
import time
import requests, json, datetime, time, BeautifulSoup, pickle

# How many threads?
Hthreads = 2
sitekeyEnabled = False
repeat = True
repeatTime = '12:30' 

CaptchaList = []
active_threads = 0
sitekey = '6LfYhz0UAAAAAJFKp28Sg0NnAEIPMfKI1RJSGsdB' 
API_KEY = '' # INPUT YOUR API KEY HERE
captcha_url = 'https://slamjamsocialism-drops.com/graphql' 


def main():
    global CaptchaList
    global sitekey
    global API_KEY
    global captcha_url
    global headers

    log('Welcome')
    if sitekeyEnabled == True:
        log('Retriving Sitekey')
        sitekey = get_sitekey(captcha_url)

    d = datetime.datetime.now().strftime('%H:%M') # print -> 16:18
    # Shitty coding
    if repeat == True: 
        while not str(d) == repeatTime:
            for i in range(0,Hthreads):
                t = threading.Thread(target=get_captcha, args=(API_KEY,sitekey,captcha_url))
                t.daemon = True
                t.start()
                time.sleep(0.1)
            # ce while empêche le while repeatTime de se terminer...
            while not active_threads == 0 or active_threads == 1:
                log('Active Threads ---------- ' + str(active_threads))
                timeout = []
                timeout.append(active_threads)
                if timeout.count(active_threads) == 10:
                    break
                time.sleep(5)
                d = datetime.datetime.now().strftime('%H:%M')
            timeout = []

    else: 
        for i in range(0,Hthreads):
            t = threading.Thread(target=get_captcha, args=(API_KEY,sitekey,captcha_url))
            t.daemon = True
            t.start()
            time.sleep(0.1)
        while not active_threads == 0 or active_threads == 1:
            log('Active Threads ---------- ' + str(active_threads))
            timeout = []
            timeout.append(active_threads)
            if timeout.count(active_threads) == 20:
                break
            time.sleep(5)

    # Only tests to check if it's saving and working good
    """print CaptchaList
    d = datetime.datetime.now().strftime('%H:%M')
    with open(str(d)+'.txt','r') as f:
        trump = pickle.load(f)
        item = random.choice(trump)
    print trump
    print item"""

def log(event):
    print('Captcha by Azerpas :: ' + str(datetime.datetime.now().strftime('%H:%M:%S')) + ' :: ' + str(event))


def get_sitekey(url):
        if sitekeyEnabled == False:
            log('Sitekey scraping is disabled, using the default value') 
        else:
            session = requests.session()   
            log('Scraping sitekey')
            session.get(url, headers=headers)
            ##### finding captcha sitekey with BeautifulSoup ####

def get_captcha(API_KEY,sitekey,captcha_url):
    global active_threads

    active_threads += 1

    session = requests.session()
    session.cookies.clear()
    randomID = random.getrandbits(16)
    log('Generating Captcha for task ID: ' + str(randomID))
    captcha_id = session.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, sitekey, captcha_url)).text.split('|')[1]
    recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        print(recaptcha_answer)
        time.sleep(3)
        recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    try:
        recaptcha_answer = recaptcha_answer.split('|')[1]
    except IndexError:
        print("Captcha error")
        return
    log('Captcha successfully obtained, task ID: ' + str(randomID))
    saveCaptcha(recaptcha_answer,randomID)
    log('Task ID ' + str(randomID) + ' is closing...')
    active_threads -= 1

def saveCaptcha(recaptcha_answer, ID):
    d = datetime.datetime.now().strftime('%H:%M')
    log("Saving Captcha into '" + str(d) + ".txt', valid for 2 minutes")
    try : 
        file = open(str(d)+'.txt','r')
        print('Txt already exists, task ID: ' + str(ID))
        try:
            Filelist = pickle.load(file)
        except EOFError:
            print("--------------------")
            print("Captcha error")
            print("--------------------")
            return
        Filelist.append(recaptcha_answer)
        file = open(str(d)+'.txt','w')
        pickle.dump(Filelist,file)
        #file.write(Filelist)
        #file.write(str(recaptcha_answer))
        #file.write('\n')
    except IOError as e:
        print('Creating txt, task ID: ' + str(ID))
        file = open(str(d)+'.txt','w')
        Filelist = []
        Filelist.append(recaptcha_answer)
        #file.write(Filelist)
        pickle.dump(Filelist,file)
        #file.write('\n')
    print('Captcha successfuly saved, task ID: ' + str(ID))
    CaptchaList.append(recaptcha_answer)

if __name__ == "__main__":
    main()
