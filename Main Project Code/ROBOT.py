from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import wikipedia
import re
from playsound import playsound
import lyricwikia
import urllib
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import quote 
import random
import glob
import webbrowser
from weather import Weather
import requests, json 
import pyttsx3
from pocket import Pocket, PocketException
import pocket
import time
engine = pyttsx3.init()
engine.setProperty('rate', 155)

def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        engine.say(audio)
        engine.runAndWait()

    #  use the system's inbuilt say command instead of mpg123
    #  text_to_speech = gTTS(text=audio, lang='en')
    #  text_to_speech.save('audio.mp3')
    #  os.system('mpg123 audio.mp3')


def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()

    return command


def assistant(command):
    "if statements for executing commands"

    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'sing' in command:
            talkToMe('What Is The Name Of The Song?')
            SONG = myCommand()
            talkToMe('Who Sing That Song?')
            SINGER = myCommand()
            lyrics = lyricwikia.get_lyrics(SINGER,SONG)
            mystring = lyrics.replace('\n', ' ').replace('\r', '').replace('\'','').replace('(','').replace(')','')
            talkToMe(mystring)

    
    elif 'search for' in command:
        reg_ex = re.search('search for (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'say hi to' in command:
        reg_ex = re.search('say hi to (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            talkToMe('Hi '+domain)
        else:
            pass

    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.+)', command)
        if reg_ex:
            consumer_key = "84071-393fa2595527eaf671022012"
            access_token = "6f0441b8-3122-6194-706b-4ec7e6"
            pocket_instance = pocket.Pocket(consumer_key, access_token)
            p = Pocket(consumer_key="84071-393fa2595527eaf671022012",
            access_token="6f0441b8-3122-6194-706b-4ec7e6")
            topic = reg_ex.group(1)
            w = wikipedia.page(topic)
            u = w.url
            TopicPage = wikipedia.summary(topic, sentences=3)
            x = re.sub('[^ a-zA-Z0-9]', '', TopicPage)
            talkToMe(str(x))
            time.sleep(1)
            talkToMe('Do You Want Me To Save It To Your Pocket?')
            order = myCommand()
            if 'yes' in order:
                p.add(u)
                talkToMe('Great This Article Now In Your Pocket ')
            elif 'No' or 'no' or 'not' in order:
                talkToMe('Okay Maybe Another Time.')
            else:
                pass
        
        else:
            pass

    elif 'play' in command:
        talkToMe('what song do you want me to play ?')
        textToSearch = myCommand()
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,features="lxml")
        Links = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            Links.append('https://www.youtube.com' + vid['href']) 
        url2 = Links[0]
        webbrowser.open(url2)
        talkToMe('Playing'+query)


    elif 'random' in command:          
        L = (glob.glob("/home/mohamed/Music/*.mp3"))
        x= random.randint(0 , len(L))
        name = L[x]
        name2 = name[20:-4]
        webbrowser.open(L[x])
        talkToMe('Playing '+name2)

    elif 'what are you doing' in command:
        talkToMe('Just doing my thing')


    elif 'good morning' in command:
        talkToMe('Good Morning My Friend ')


    elif 'introduce yourself' in command:
        talkToMe('''Hello There , My Name Is Robot,I Was Created By Group Of Amazing Engineers In Nile Academy,You Can Call Me Hamo Bika If You Want!''')

    elif 'who is your friend' in command:
        talkToMe('my friend is ahmed emad')


    elif 'who is your creator' in command:
        talkToMe('i have been created with a group of amazing engineers From Nile Academy ')
        talkToMe('mohamed wael is one of them')

    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city_name = reg_ex.group(1)
            api_key = "42f0b6e848247352c0c59f6d72f05c69"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
            response = requests.get(complete_url) 
            x = response.json() 
            y = x["main"] 
            current_temperature = y["temp"] 
            current_pressure = y["pressure"] 
            current_humidiy = y["humidity"] 
            z = x["weather"] 
            weather_description = z[0]["description"] 
            tmp = str(int(current_temperature-273))
            wea = str(weather_description)
            talkToMe('The Weather In '+city_name+' City  ')
            talkToMe('It Seems To Be '+wea+' Day')
            talkToMe('And It Will Be '+tmp+' Celsius Degrees')

    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            city_name = reg_ex.group(1)
            api_key = "42f0b6e848247352c0c59f6d72f05c69"
            base_url = "http://api.openweathermap.org/data/2.5/forecast?"
            complete_url2 = base_url + "appid=" + api_key + "&q=" + city_name +"&cnt=1"
            response = requests.get(complete_url2) 
            x = response.json() 
            y = x["list"][0]['main'] 
            current_temperature = y["temp"] 
            z = x['list'][0]["weather"] 
            weather_description = z[0]["description"] 
            tmp = str(int(current_temperature-273))
            wea = str(weather_description)
            talkToMe('The Weather In The Next Three To Five Days In  '+city_name+' City  ')
            talkToMe('It Seems That It Will Be '+wea+' Days')
            talkToMe('And It Will Be About '+tmp+' Celsius Degrees')
    elif 'news' in command:
        NEWST = []
        NEWSD = []

        response = requests.get(' https://api.currentsapi.services/v1/search?keyword=Egypt',
        headers={'Authorization':'rpb2wnUpmm9gzCOAT8hKPuC1KJFnH_KvacMAz5YOpNNgUVuM'})

        length = len(response.json()['news'])

        for i in range(length):
            t = response.json()['news'][i]['title']
            d = response.json()['news'][i]['description']
            NEWST.append(t)
            NEWSD.append(d)

        O= random.randint(0 , len(NEWST))
        talkToMe(str(NEWST[O]).replace('\n', ' ').replace('\r', '').replace('\'','').replace('(','').replace(')','').replace('\"',''))
        talkToMe(str(NEWSD[O]).replace('\n', ' ').replace('\r', '').replace('\'','').replace('(','').replace(')','').replace('\"',''))

    elif 'quotation' in command:

        response = requests.get('http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1')
        x = response.json()[0]['content']
        y = response.json()[0]['title']
        label = (str(x).replace('\n', ' ').replace('8217','\"').replace('\r', '').replace('\'','').replace('(','').replace(')','').replace('\"','').replace('*','').replace('/','').replace('+','').replace('^','').replace('$','').replace('#','').replace('-','').replace('_','').replace('>','').replace('<','').replace(':','').replace(';','').replace('&',''))
        l = label[1:-2]
        talkToMe(y+' Said ')
        talkToMe(l)

    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'muhammad' or 'Mohamed' or 'Muhammad' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('mohamedwaelbishr@gmail.com', 'PASS')

            #send message
            mail.sendmail('mohamed', 'mohamedwaelbishr@gmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')

        else:
            talkToMe('I don\'t know what you mean!')

    else:
        talkToMe('I don\'t know what you mean!')

talkToMe('I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
