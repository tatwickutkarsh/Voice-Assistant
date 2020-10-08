import pyttsx3
import time
import speech_recognition as sr
import subprocess
from pydub import AudioSegment as a
from Wikipedia.wikipedia import wikipedia as w
from pydub.playback import play
import vlc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import selenium
import pafy
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
def hin_news(region):
    if region=='state':
        engine.say("क्या आप भारत के किसी राज्य का समाचार जानना चाहते हैं ?")
    elif region =='city':
        engine.say("क्या आप भारत के किसी शहर का समाचार जानना चाहते हैं ?")
    elif region=='country':
        engine.say("क्या आप भारत के अलावा किसी अन्य देश का समाचार जानना चाहते हैं ?")
    else:
        engine.say("क्या आप दुनिया भर की खबरें जानना चाहते हैं ?")
    engine.runAndWait()
    ans=sp2txt()    
    if 'ha' in ans.lower():
        if region=='state':
            engine.say('कृपया राज्य का नाम बोलें:')
            engine.runAndWait()
            q=sp2txt().lower()
            print(q)
            link='https://aajtak.intoday.in/'+('-'.join(q.split()))+'-news.html'
            engine.say('आज की '+q+' की ताज़ा खबरे कुछ इस प्रकार हैं:')
        elif region =='city':
            engine.say("कृपया शहर का नाम बोलें:")
            engine.runAndWait()
            q=sp2txt().lower()
            print(q)
            link='https://aajtak.intoday.in/topic/'+('-'.join(q.split()))+'-news.html'
            engine.say('आज की '+q+' की ताज़ा खबरे कुछ इस प्रकार हैं:')
        elif region=='country':
            engine.say("कृपया देश का नाम बोलें:")
            engine.runAndWait()
            q=sp2txt().lower()
            print(q)
            link='https://aajtak.intoday.in/topic/'+('-'.join(q.split()))+'-news.html'
            engine.say('आज की '+q+' की ताज़ा खबरे कुछ इस प्रकार हैं:')
        else:
            link='https://aajtak.intoday.in/world-news.html'
            engine.say('आज की दुनिया की ताज़ा खबरे कुछ इस प्रकार हैं:')
        engine.runAndWait()
        import requests
        response=requests.get(link)
        soup=BeautifulSoup(response.text,'html.parser')
        import re
        if region not in ['country','city']:
            p1= soup.find_all('a',href=re.compile(r'/story/'),class_=False,attrs={'title':True,'data-url':True,'target':False})
            p2= soup.find_all('a',href=re.compile(r'/story/'),class_=True,attrs={'title':True,'data-url':True,'target':False})
            p=p1+p2   
        else:
            p=soup.find_all('a',href=re.compile(r'/story/'),attrs={'target':False})
        # cnt=0
        
        for x in p:
            # if x.text:
                # print(x.attrs)
            flag=1    
            if region not in ['country','city']:
                print(x['title'])
                engine.say(x['title'])

            else:
                if x.text.strip():
                    print(x.text)
                    # print(x.attrs)   
                    engine.say(x.text) 
                else:
                    flag=0
            if flag:
                engine.say("क्या आप इस विषय में और जानना चाहते हैं?")
                engine.runAndWait()
                ans=sp2txt()
                print(ans)
                if 'ha' in ans.lower():
                    resp=requests.get('https://aajtak.intoday.in/'+x['href'])
                    sp=BeautifulSoup(resp.text,'html.parser')
                    q=sp.find('div',class_=True,attrs={'itemprop':"articleBody"}).find_all('p')
                    try:
                        text='. '.join(sp.find('ul',class_='highLightList').stripped_strings)
                        text+='. '
                    except:
                        text=''
                        pass    
                    for y in q:
                        # print(y.attrs)
                        # print(y.contents)
                        try:
                            y.ul.contents
                        except:
                            for z in y.stripped_strings:
                                if z not in text:
                                    if re.search(r'[a-zA-Z]',z):
                                        pass
                                    else:
                                        text+=z
                        else:
                            pass
                    # import ftfy        
                    # with open('news.txt','w') as file:        
                        # print(ftfy.fixes.fix_encoding(text))
                    print(text)
                    # file.write(text)
                    # engine.setProperty("rate",)
                    engine.say(text)
                    engine.runAndWait()
                    print()
            

def sp2txt():
    rec=sr.Recognizer()
    mic=sr.Microphone()
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        print("Speak now....................")
        audio=rec.listen(source)    
    z=rec.recognize_google(audio)
    return z

def news(region):
            if region=='country':
                engine.say("Do you want news of any particular "+region+" other than India?")
            elif region=='world':
                engine.say("Do you want news from all around the world?")    
            else:    
                engine.say("Do you want news of any particular "+region+" of India?")
            engine.runAndWait()
            ans=sp2txt()
            print(ans)
            if 'yes' in ans.lower():
                if region!='world':
                    engine.say("Please say the name of the "+region)
                    engine.runAndWait()
                    ans=sp2txt().lower()
                if region=="country":
                    link="https://timesofindia.indiatimes.com/"+"world/"+ans+"/"
                    response=requests.get("https://timesofindia.indiatimes.com/"+"world/"+ans)
                elif region=="state":
                    link="https://timesofindia.indiatimes.com/"+"india/"+ans+"/"
                    response=requests.get("https://timesofindia.indiatimes.com/"+"india/"+ans)
                elif region=="world":
                    link="https://timesofindia.indiatimes.com/world/"
                    response=requests.get(link)        
                else:
                    link="https://timesofindia.indiatimes.com/"+"city/"+ans+"/"
                    response=requests.get("https://timesofindia.indiatimes.com/"+"city/"+ans)    
                soup=BeautifulSoup(response.text,'html.parser')
                if region!='world':
                    engine.say("Today's Top News of "+ans+" are as follows:")
                else:
                    engine.say("Today's Top News from around the world are as follows:")    
                engine.runAndWait()
                import re    
                def fun(tag):
                    return tag.name=='a' and tag.has_attr('title') and tag.has_attr('pg') and re.search(r'Top News|Latest News',tag['pg'])       
                def fun2(tag):
                    return tag.name=='a' and tag.has_attr('title') and tag.has_attr('pg') and re.search(r'-world',tag['pg'])
                # u=soup.find_all('a',attrs={'pg':re.compile(r'^Latest_News')})
                # def fun1(pg):
                #     return pg and re.search(r'Top_News',pg)
                # u=soup.find_all('a',attrs={'pg':fun1})
                if region!='world':
                    u=soup.find_all(fun)
                else:
                    u=soup.find_all(fun2)    
                # for ele in u:
                # li=u.find_all('a')
                for x in u: 
                    if x.text:
                        print(x.text)
                        engine.say(x.text)
                        engine.say('Do you want to know more about this topic?')
                        engine.runAndWait()
                        ans=sp2txt()
                        print(ans)
                        if 'yes' in ans.lower():
                            resp=requests.get(link+x['href'])
                            sp=BeautifulSoup(resp.text,'html.parser')
                            try:
                                p=sp.find('div',class_='_1_Akb clearfix').stripped_strings
                            except:
                                engine.say('I am sorry! This topic doesn\'t have any article associated with it')
                                engine.runAndWait()
                                # print('\n')
                                continue    
                            
                            import ftfy
                            text=(' '.join(p))
                            text=ftfy.fixes.fix_encoding(text)
                            print(text)
                            engine.say(text)
                            engine.runAndWait()
                            print('\n')    

def select_media(path,inst,m_type,flag=0):
        cmd=["ls"]
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,cwd=path)
        for line in proc.stdout.readlines():
            if flag:
                break
            name=line.decode('utf-8')
            # print(name)
            import os
            # print(os.getcwd())
            # print(z+'\\'+name)
            key=path+'\\'+name
            if os.path.isfile(key.strip()):
                print(name.strip())
                # print(path)
                engine.say(name)
                engine.say('Do you want to play this '+m_type+'?')
                engine.runAndWait()
                ans=sp2txt()
                print(ans)
                if 'yes' in ans.lower():
                    flag=1
                    return inst.media_new(key.strip())
            else:  
                temp=key.strip()
                # print(path)
                select_media(temp,inst,m_type,flag)


def create_media_list(path,lis,m_type,flag=0):
        cmd=["ls"]
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,cwd=path)
        for line in proc.stdout.readlines():
            if flag:
                break
            else:    
                name=line.decode('utf-8')
                # print(name)
                import os
                # print(os.getcwd())
                # print(z+'\\'+name)
                key=path+'\\'+name
                if os.path.isfile(key.strip()):
                    print(name.strip())
                    # print(path)
                    engine.say(name)
                    engine.say('Do you want to add this '+m_type+' to your playlist?')
                    engine.runAndWait()
                    ans=input()
                    print(ans)
                    if 'yes' in ans.lower():
                        lis.add_media(key.strip())
                        engine.say('This '+m_type+' has been added to your playlist')
                        engine.say('Do you want to add more '+m_type+'s to your playlist?')
                        engine.runAndWait()
                        ans=input()
                        print(ans)
                        if ('no' in ans.lower()):
                            flag=1
                    #print(player.is_playing())
                    
                else:  
                    temp=key.strip()
                    # print(path)
                    create_media_list(temp,lis,m_type,flag)



    
if __name__=="__main__":
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    engine= pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[3].id)
    engine.setProperty('rate',150)
    # engine.say("Which topic do you want to know about?")
    # engine.runAndWait()
    # srq=sp2txt()
    # print(srq)
    # try:
    #     flag=False
    #     # w.set_lang("hi")
    #     summary=w.summary(srq,sentences=5)
    #     if '=' in summary:
    #         summary=summary[:summary.index('=')].strip()
    #     print(summary)
    # except:
    #     alt=w.suggest(srq)
    #     engine.say("Do you mean "+alt+"?")
    #     engine.runAndWait()
    #     z=sp2txt()
    #     print(z)
    #     if "yes" in z.lower():
    #         srq=alt
    #         summary=w.summary(srq,sentences=5)
    #         if '=' in summary:
    #             summary=summary[:summary.index('=')].strip()
    #         print(summary)
    #     else:
    #         engine.say("Sorry! I can't provide you any information regarding this topic.")  
    #         engine.runAndWait()
    #         flag=True
    # finally:
    #     if not flag:   
    #         # engine.setProperty('voice',voices[1].id)
    #         engine.say(summary)
    #         engine.runAndWait()
    #         engine.say("Do you want to learn more about this topic?")
    #         engine.runAndWait()
    #         q=sp2txt()
    #         print(q)
    #         if "yes" in q.lower().split():
    #             soup=BeautifulSoup(w.page(srq).html(),'html.parser')
    #             # print(soup.prettify())
    #             sections=[]
    #             for x in soup.find_all('h2',id=False):
    #                 if '[' in x.text:
    #                     sections.append(x.text[:x.text.index('[')])
    #                 else:
    #                     sections.append(x.text)    
    #             orig_sections=[]
    #             engine.say("This topic has the following sections:")
    #             engine.runAndWait()
    #             for i,x in enumerate(sections):
    #                 print(x)
    #                 orig_sections.append(x)
    #                 sections[i]=x.lower()
    #                 engine.say(x)
    #                 engine.runAndWait()
            
    #             engine.say("Which section do you specifically want to learn about? Or do you want me to read out all the sections?")
    #             engine.runAndWait()
    #             t=sp2txt()
    #             if t.lower() in sections:
    #                 src=w.page(srq).content
    #                 indx=sections.index(t.lower())
    #                 if indx!=(len(sections)-1):
    #                     text=src[src.index(orig_sections[sections.index(t.lower())]):src.index(orig_sections[sections.index(t.lower())+1])]
    #                 else:
    #                     text=src[src.index(orig_sections[sections.index(t.lower())]):]
    #                 text=text.replace('=','').strip()    
    #                 print(text)    
    #                 engine.say(text)
    #                 engine.runAndWait()
    #             elif "all" in t.lower().split():
    #                 src=w.page(srq).content
    #                 text=src[src.index(orig_sections[0]):]
    #                 text=text.replace('=','').strip()    
    #                 print(text)    
    #                 engine.say(text)
    #                 engine.runAndWait()
    #             else:
    #                 engine.say("This is an invalid section")
    #                 engine.runAndWait()


    
    ##print(x for x in w.page(srq).sections)
    ##engine.say(w.page(srq).sections)
    # engine.say("Do you want to play an audio or a video?")
    # engine.runAndWait()
    # ans=sp2txt()
    # print(ans)
    # cond=1
    # if 'audio' in ans.lower():
    #     m_type="audio"
    # elif 'video' in ans.lower():
    #     m_type="video"
    # else:
    #     m_type=None
    # # engine.say("Which song do you like to hear?")
    # if m_type=='audio':
    #     engine.say("Please enter the absolute path to your audio folder")
    # elif m_type=='video':
    #     engine.say("Please enter the absolute path to your video folder")  
    # else:
    #     engine.say("I am Sorry! This is an invalid response")
    #     cond=0       
    # engine.runAndWait()
    # if cond:
    #     path=input()
    #     engine.say("Do you want to play a single "+m_type+" or a playlist of "+m_type+"s?")
    #     engine.runAndWait()
    #     ans=input()
    #     print(ans)
    # #     #     import os
    # #     #     print(os.getcwd())
    #     if 'playlist' in ''.join(ans.lower().strip().split()):
    #         Instance = vlc.Instance('--quiet')
    #         player = Instance.media_list_player_new()
    #         Media = Instance.media_list_new()
    #         create_media_list(path,Media,m_type)
    #         # print("oginal psth is",path)
    #         player.set_media_list(Media)
    #         flag=0  
    #         # print(flag)
    #         engine.say("Playing your Playlist")
    #         engine.runAndWait()
    #         player.get_media_player().toggle_fullscreen()
    #         player.play()
    #         while(player.get_state()!=vlc.State.Ended):
    #             # player.get_media_player().toggle_fullscreen()
    #             # print("Pher se kr")
    #             while(not player.is_playing()):
    #                 # print("Not Playing")
    #                 time.sleep(1)
                
    #             ##    print(length)
    #             ##print(player.is_playing())
    #             # print(player.get_state())
    #             while(player.is_playing()):
    #                 # print(player.get_state())
    #                 time.sleep(1)
    #                 # player.next()
    #                 # print(player.get_state())
    #                 if (player.get_state()==vlc.State.Opening):
    #                     break
    #                     # engine.say("Playing next song")    
    #                     # engine.runAndWait()
    #                 # flag=player.next()#this will be -1 if the media is the last one in your playlist and will not do anything so I have to break the loop to close the player instance
    #                 # print(flag)
    #                 # break
    #             if (player.get_state()==vlc.State.Opening):
    #                 engine.say("Playing next "+m_type)    
    #                 engine.runAndWait()
    #             elif (player.get_state()==vlc.State.Ended):
    #                 engine.say("Closing the Media Player")    
    #                 engine.runAndWait()
    #         player.release()
    #         # print(player.next())       
    #         # player.pause()
    #         # print(player.next())    
    #         # player.release()    

    #     else:

    #         Instance = vlc.Instance('--quiet','--play-and-stop')
    #         player = Instance.media_player_new()
    #         Media=select_media(path,Instance,m_type)
    #         Media.get_mrl()
    #         player.set_media(Media)
    #         engine.say("Playing the selected "+m_type)
    #         engine.runAndWait()
    #         player.toggle_fullscreen()
    #         player.play()
    #         while(not player.is_playing()):
    #             time.sleep(1)
    #     ##    print(length)
    #     ##print(player.is_playing())
    #         while(player.is_playing()):
    #             time.sleep(2)
    #         engine.say("Closing the player")
    #         engine.runAndWait()            
    #         player.release()
        
        # m_list(path)
        # Media.get_mrl()
        # player.set_media(Media)
   
        
    # Media = Instance.media_new(key.strip())
    # Media.get_mrl()
    # player.set_media(Media)
    # player.toggle_fullscreen()
    # ##print(player.is_playing())
    # player.play()
    # while(not player.is_playing()):
    #     time.sleep(1)
    #     ##    print(length)
    #     ##print(player.is_playing())
    # while(player.is_playing()):
    #     time.sleep(2)
                
    # engine.say("Do you want to play an audio or a video?")
    # engine.runAndWait()
    # z=sp2txt()
    # print(z)
    # ex=1
    # if 'audio' in z.lower():
    #     arg='audio'
    # elif 'video' in z.lower():
    #     arg=''
    # else:
    #     ex=0  
    #     engine.say("I am sorry! That's an invalid response")
    #     engine.runAndWait()       
    # ##z=input()
    # if ex:
        # engine.say("Say the name of the song or the video that you want to play")
        # engine.runAndWait()
        # z=sp2txt()
        # print(z)
        # z+=" "+arg
        # driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
        # driver.get("https://www.youtube.com/results?search_query="+('+'.join(z.strip().split())))
        # ##time.sleep(15)
        # ##print("https://www.youtube.com/results?search_query="+('+'.join(z.split())))
        # ##for w in range(30,-1,-1):
        # ##    engine.say(w)
        # ##    engine.runAndWait()
        # ##    time.sleep(1)
        # html= driver.execute_script("return document.documentElement.outerHTML")
        # driver.quit()
        # soup=BeautifulSoup(html,'html.parser')
        # ##print(soup.prettify())
        # for hi in soup.find_all(id='video-title'):
        #     try:
        #         h= hi['href']
        #     except KeyError:
        #         pass
        #     else:
        #         break
        # vid=pafy.new("https://www.youtube.com"+h)
        # url=vid.getbest().url
        # if not arg:
        #     Instance = vlc.Instance('--quiet','--play-and-stop')
        # else:
        #     # url=vid.getbestaudio().url    
        #     Instance = vlc.Instance('--quiet','--play-and-stop','--no-video')
        # ##a.converter = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
        # ##a.ffmpeg = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"
        # ##a.ffprobe ="C:\\Program Files\\ffmpeg\\bin\\ffprobe.exe"
        # file=a.from_file(r"C:\Users\Ishwar\Desktop\Please-Don't-Go.mp3",format="mp3")
        # rev=file.reverse()
    # ##file.export(r"C:\Users\Ishwar\Downloads\Main Hoon.wav",format="wav")

    # ##subprocess.call(['ffmpeg', '-i', r"C:\Users\Ishwar\Desktop\Please-Don't-Go.mp3",r"C:\Users\Ishwar\Desktop\Please-Don't-Go.wav"])

    # from playsound import playsound

    
        # player = Instance.media_player_new()
        # Media = Instance.media_new(url)
        # Media.get_mrl()
        # player.set_media(Media)
        # player.toggle_fullscreen()
        # #print(player.is_playing())
        # engine.say("Playing the requested media")
        # engine.runAndWait()
        # player.play()
        # ##print(player.is_playing())
        # length=0
        # while(length==0):
        #     time.sleep(1.5)
        #     length=player.get_length()
        # while(not player.is_playing()):
        #     time.sleep(1)
        # ##    print(length)
        # ##print(player.is_playing())
        # while(player.is_playing()):
        #     time.sleep(2)
        # engine.say("Closing the Media Player")
        # engine.runAndWait()    
        # ##length/=1000
        # ##time.sleep(length)
        # player.release()    
    ##player= vlc.MediaPlayer("https://gaana.com/song/onemorenight")
    ##fi=a.from_file("https://gaana.com/song/onemorenight",format="mp3")
    ##player.play()
    # engine.say("Playing song Please Don't Go in reverse")
    # ##print(player.is_playing())
    # engine.runAndWait()
    # play(file)
    # play(rev)
    ##for voice in voices:
    ##    print("Voice: %s" % voice.name)
    ##    print(" - ID: %s" % voice.id)
    ##    print(" - Languages: %s" % voice.languages)
    ##    print(" - Gender: %s" % voice.gender)
    ##    print(" - Age: %s" % voice.age)
    ##    print("\n")
    ##for voice in voices:
    ##engine.setProperty('voice',voices[3].id)
    ##rate=engine.getProperty('rate')
    ##print(rate)
    ##    engine.setProperty('voice.age',60)
    # engine.setProperty('rate',150)
    # rate=engine.getProperty('rate')
    ##print(rate)
    ##v=pyttsx3.voice.Voice(voices[1].id)
    ##v.age=60
    ##print(v.age)
    ##engine.say("For English, press 1")
    ##engine.setProperty('voice',voices[1].id)
    ##engine.say("हिंदी के लिए दो दबाए")
    ##engine.runAndWait()
    # rec=sr.Recognizer()
    # ##rec.energy_threshold=4000
    # mic=sr.Microphone()
    # with mic as source:
    # ##    rec.adjust_for_ambient_noise(source)
    #     print("Speak now....................")  
    #     audio=rec.listen(source)
    # x= rec.recognize_google(audio)
    # engine.say('To get the news in English, say "English News"')
    # engine.setProperty('voice',voices[1].id)
    # engine.say("हिंदी में समाचार पाने के लिए 'हिंदी न्यूज़' बोलें")
    # engine.runAndWait()
    x='hindi'   
    print(x)
    if 'hindi' in x.lower().split():
        engine.setProperty('voice',voices[1].id)
        # engine.say('नमस्कार!! मैं अलेक्सा हूँ | मैं आपके लिए क्या कर सकती हूँ ?')
        # engine.runAndWait()

        from bs4 import BeautifulSoup
        import requests
        response=requests.get("https://aajtak.intoday.in/national.html")
        soup=BeautifulSoup(response.text,'html.parser')
    ##    print(soup.prettify())
        # t=soup.find_all('div',class_="imglazy")
        ##print(t)
        ##engine= pyttsx3.init()
        ##voices=engine.getProperty('voices')
        ##engine.setProperty('voice',voices[1].id)
        ##    rate=engine.getProperty('rate')
        ##    print(rate)
        ##engine.setProperty('rate',150)
        engine.say("आज की देश की ताज़ा खबरें कुछ इस प्रकार हैं : ")
        engine.runAndWait()
    ##    print(t)
        import re
        p1= soup.find_all('a',href=re.compile(r'/story/'),class_=False,attrs={'title':True,'data-url':True,'target':False})
        p2= soup.find_all('a',href=re.compile(r'/story/'),class_=True,attrs={'title':True,'data-url':True,'target':False})
        cnt=0
        p=p1+p2
        for x in p:
            # if x.text:
            print(x.attrs)    
            cnt+=1
            print(cnt)
            # print(x['title'])
            # engine.say(x['title'])
            # engine.say("क्या आप इस विषय में और जानना चाहते हैं?")
            # engine.runAndWait()
            # ans=sp2txt()
            # print(ans)
            # if 'ha' in ans.lower():
            #     resp=requests.get('https://aajtak.intoday.in/'+x['href'])
            #     sp=BeautifulSoup(resp.text,'html.parser')
                # q=sp.find('div',class_=True,attrs={'itemprop':"articleBody"}).find_all('p')
                # try:
                #     text='. '.join(sp.find('ul',class_='highLightList').stripped_strings)
                #     text+='. '
                # except:
                #     text=''
                #     pass    
                # for y in q:
            #         # print(y.attrs)
            #         # print(y.contents)
            #         try:
            #             y.ul.contents
            #         except:
            #             for z in y.stripped_strings:
            #                 if z not in text:
            #                     if re.search(r'[a-zA-Z]',z):
            #                         pass
            #                     else:
            #                         text+=z
            #         else:
            #             pass
                # with open('news.txt','w') as file:        
                # print(text)
                # # # file.write(text)
                # # engine.setProperty("rate",200)
                # engine.say(text)
                # engine.runAndWait()
                # print()

        hin_news('state')
        hin_news('city')
        hin_news('country')
        hin_news('world')
                # cnt+=1
                # print(cnt)
    #     for data in t:
    #     ##    rate=engine.getProperty('rate')
    #     ##    print(rate)
    #         if "सो सॉरी" not in data['data-alt'] and len(data['data-alt'])>8:
    #             print(data['data-alt'])
    #             engine.say(data['data-alt'])
    #             engine.runAndWait()
    # ##            time.sleep(3)
    # ##            print(".........")
    # ##            with mic as source:
    # ####                rec.adjust_for_ambient_noise(source)
    # ##                audio=rec.listen(source)
    # ##            try:
    ##                z=rec.recognize_google(audio,language='hi-IN')
    ##            except:
    ##                continue
    ##            if 'चुप' in z.split():
    ##                engine.say("धन्यवाद् ")
    ##                engine.runAndWait()
    ##                break
    else:
        engine.setProperty('voice',voices[3].id)
        # engine.say("Hello!! I am Alexa! What can I do for you?")
        # engine.runAndWait()
        from bs4 import BeautifulSoup
        import requests
        response=requests.get("https://timesofindia.indiatimes.com/")
        soup=BeautifulSoup(response.text,'html.parser')
    ##    print(soup.prettify())
        # t=soup.find_all('a',class_='list8')
        ##print(t)
        ##engine= pyttsx3.init()
        ##voices=engine.getProperty('voices')
        ##engine.setProperty('voice',voices[1].id)
        ##    rate=engine.getProperty('rate')
        ##    print(rate)
        ##engine.setProperty('rate',150)
        # engine.say("Today's Top News of the country are as follows:")
        # engine.runAndWait()
        # # for text in t.stripped_strings:
        # # ##    rate=engine.getProperty('rate')
        # # ##    print(rate)
        # #     print(text)
        # #     engine.say(text)
        # #     engine.runAndWait()
        # import re    
        # def fun(tag):
        #     return tag.name=='a' and tag.has_attr('title') and tag.has_attr('pg') and re.search(r'Top_News|Latest_News',tag['pg'])       
        # # u=soup.find_all('a',attrs={'pg':re.compile(r'^Latest_News')})
        # # def fun1(pg):
        # #     return pg and re.search(r'Top_News',pg)
        # # u=soup.find_all('a',attrs={'pg':fun1})
        # u=soup.find_all(fun)
        # # for ele in u:
        # # li=u.find_all('a')
        # for x in u: 
        #     if x.text:
        #         print(x.text)
        #         engine.say(x.text)
        #         engine.say('Do you want to know more about this topic?')
        #         engine.runAndWait()
        #         ans=sp2txt()
        #         print(ans)
        #         import ftfy
        #         if 'yes' in ans.lower():
        #             resp=requests.get("https://timesofindia.indiatimes.com/"+x['href'])
        #             sp=BeautifulSoup(resp.text,'html.parser')
        #             try:
        #                 p=sp.find('div',class_='_1_Akb clearfix').stripped_strings
        #             except:
        #                 engine.say('I am sorry! This topic doesn\'t have any article associated with it')
        #                 engine.runAndWait()
        #                 # print('\n')
        #                 continue
        #             # text=''
        #             # import unidecode    
        #             # for x in p:
        #             #     alt=unidecode.unidecode(x)
        #             #     text+=alt.encode('unicode_escape').decode('ascii')+" "          
        #             text=(' '.join(p))
        #             text=ftfy.fixes.fix_encoding(text)
        #             # text=text.replace('â',"")
        #             # text=text.replace('\x80\x98',"'")
        #             # text=text.replace('\x80\x99',"'")
        #             print(text)
        #             engine.say(text)
        #             engine.runAndWait()
        #             print()    
        

        news('state')
        news('city')
        news('country')
        news('world')
    ##    print(u.contents)
    ##    c=1
        # for text in u.contents:
        # ##    rate=engine.getProperty('rate')
        # ##    print(rate)
        #     try:
        #         print(text.a['title'])
        #     except:
        #         continue
        #     engine.say(text.a['title'])
        #     engine.runAndWait()
            
