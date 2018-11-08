#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import speech_recognition as sr
import tempfile
from gtts import gTTS
from pygame import mixer
import requests
from time import ctime
import time
import pyttsx3
import cv2
import imutils
from bs4 import BeautifulSoup
import tkinter as tk
import os
from PIL import Image
from PIL import ImageTk
from pprint import pprint
import re
from SaraModules import *
def ReadAllCommand():
    from openpyxl import load_workbook
    wb=load_workbook('Sara指令表/Sara指令表.xlsx')
    ws=wb.get_active_sheet()
    SaraCommandDict=dict()
    for i in range(2,ws.max_column+1):
        SaraCommandDict[ws.cell(row=1,column=i).value]=[ws.cell(row=3,column=i).value,ws.cell(row=4,column=i).value]
    return SaraCommandDict
#Sara 的本體
def CreatGUI():
    SaraCommandDict=ReadAllCommand()
    def SearchCommand(talk):
        talk=talk.lower()
        for t in SaraCommandDict.keys():
            if re.findall(t,talk):
                print('aksldflkj')
                exec(SaraCommandDict[t][0])
                SpeakChinese(SaraCommandDict[t][1])
            else:
                print('no command')
    #爬取學校網站資料 獲得各科目公佈欄是否有公告
    def ConnectIlearnBroadCast():
        session = requests.Session()
        data = {'username': 'd0441258', 'password': 'MuMuShy850421'}
        r = session.post('https://ilearn2.fcu.edu.tw/login/index.php', data=data)
        print(r.cookies.get_dict())
        r = session.get("https://ilearn2.fcu.edu.tw/")
        soup = BeautifulSoup(r.text,'lxml')
        allClass=soup.find_all("a",title = re.compile(r'^1071(\w+)'))
        say=""
        for ul in allClass:
            print(ul['href'])
            r=session.get(ul['href'])
            soup=BeautifulSoup(r.text,'lxml')
            subjectName=soup.find("h1",{"class":"coursetitle"})
            subjectName=subjectName.text[5:-6]
            print(subjectName)
            broadcastURL=soup.find_all("a", href=re.compile(r"^https://ilearn2.fcu.edu.tw/mod/forum/view.php?(\w+)"))
            r=session.get(broadcastURL[2]['href'])
            soup=BeautifulSoup(r.content,'lxml')
            result=soup.find(class_="forumheaderlist")
            if result==None:
                print("no new broadcast")
            else:
                print(result)
                say+=subjectName
        SpeakChinese('以下科目有新的公告:')
        time.sleep(3)
        SpeakChinese(say)
        time.sleep(6)
        SpeakChinese('請趕快登入網站查詢')
        time.sleep(2)
        SpeakChinese('需要幫你打開ilearn嗎')
        time.sleep(2)
        data=Listen()
        if "yes" in data or "好" in data:
            SaraWeb.openWithURL('https://ilearn2.fcu.edu.tw/')
    #sara的耳朵
    def Listen():
        print('sara is listening...')
        r=sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio=r.listen(source)
        data=""
        #開始語音辨識
        try:
            data=r.recognize_google(audio,language='zh-TW')
            SearchCommand(data)
            print("you said"+data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            SetIText('無法辨識 請再說一遍')
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        SetIText(data)
        return data
    #Sara說英文
    def callback():
        print('a')
    def Speak(sentence):
        mixer.init()
        with tempfile.NamedTemporaryFile(delete=True)as fp:
            tts=gTTS(text=sentence,lang='en-US')
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load("{}.mp3".format(fp.name))
            mixer.music.play()
            SetSaraText(sentence)
    #Sara 中文
    def SpeakChinese(sentence):
        mixer.init()
        with tempfile.NamedTemporaryFile(delete=True)as fp:
            tts=gTTS(text=sentence,lang='zh-TW')
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load("{}.mp3".format(fp.name))
            mixer.music.play()
            SetSaraText(sentence)

    #爬取維基百科
    def SearchWiki(term):
        res=requests.get('https://zh.wikipedia.org/wiki/{}'.format(term))
        soup=BeautifulSoup(res.text,'lxml')
        result=soup.select_one('.mw-parser-output p').text
        print(result)
        return result
    def Speak2(sentence):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate)
        voices = engine.getProperty('voices')
        engine.setProperty('voice',voices[7].id)
        engine.say(sentence)
        engine.runAndWait()
    #Sara的大腦
    def Sara(data):
        #data=Listen()
        if(data==""):
            return
        if "天氣" in data:
            Speak('Searching Taichung weather... ')
            time.sleep(1)
            SearchingWeather()
        if "公告" in data:
            Speak('I will Help You To Check Please Wait....')
            ConnectIlearnBroadCast()
        if "時間" in data:
            Speak(ctime())
        if "time" in data:
            Speak(ctime())
        if "百科" in data:
            Speak("what do you want to search?")
            Searching=Listen()
            SpeakChinese(SearchWiki(Searching))  
        if "再見" in data:
            Speak('Goodbye nice to meet you')
            os._exit(0)
        if "school" in data:
            ConnectIlearnBroadCast()
        if "打開" in data or "學校網頁" in data:
            SaraWeb.openWithURL('https://ilearn2.fcu.edu.tw/')
    #查詢台中天氣
    def SearchingWeather():
        r = requests.get('https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
        soup=BeautifulSoup(r.content,'lxml')
        result=soup.find_all("td")
        speak="台中天氣"
        print(result[2].text)
        print(result[6].text)
        print(result[10].text)
        speak="台中天氣 今晚至明晨"+result[2].text+" 明天白天"+result[6].text+" 明天晚上"+result[10].text
        SpeakChinese(speak)
    #當視窗被關注 被調用(問候)
    def Onfocus(event):
        first=False
        if first==False:
            if event.widget==window:
                print('i am focus on')
                window.update()
                Speak('hi i am Sara')
                time.sleep(1)
                Speak('What can i help you?')
                time.sleep(1)
                SetSaraText('Hi i am Sara What Can I help You')
                time.sleep(1)
                first=True
    #sara 使用者文字輸入接口
    def SaraByText():
        command=UserEntry.get()
        
    def SetSaraText(saratext):
        canvas.delete('SaraText')
        canvas.create_text(400,100,fill="white",font="Times 30 italic bold",text=saratext,tag='SaraText')
        canvas.update()
    def SetIText(Itext):
        canvas.delete('Isay')
        canvas.create_text(400,500,fill="white",font="Times 20 italic bold",text=Itext,tag='Isay')
        canvas.update()
    def test():
        print('button test')
    def SaraMainLoop():
        if(mixer.music.get_busy()):
            print('')
        else:
            print('sara is not talking')
        window.after(1000, SaraMainLoop)
    #退出程序
    def on_closing():
        window.destroy()
        os._exit(0)
    #創建Tk window
    window=tk.Tk()
    window.title('Sara')
    window.geometry('800x600')
    #創建canvas並設置背景圖
    canvas=tk.Canvas(window,height=400,width=800)
    img = Image.open("sara.jpg")
    img = img.resize((800,600), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    canvas.create_image(0,0, image=photoImg,anchor='nw')
    master=window
    canvas.create_text(50,500,fill="white",font="Times 40 italic bold",text="",tag='SaraText')
    canvas.create_text(50,600,fill="white",font="Times 20 italic bold",text="",tag='Isay')
    canvas.pack()
    #使用者文本輸入
    UserEntry=tk.Entry(window)
    UserEntry.pack(padx=100,pady=0)
    #使用者輸入按鈕
    UserInputbutton=tk.Button(window,text="輸入",width=10,height=2,command=lambda:Sara(UserEntry.get()))
    UserInputbutton.pack(padx=50,pady=0)
    #使用者說話按鈕
    UserSaybutton=tk.Button(window,text='說話',width=10,height=2,command=lambda:Sara(Listen()))
    UserSaybutton.pack(padx=100,pady=30)
    #綁定event
    window.bind("<FocusIn>", Onfocus)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    #讓window 在最前視窗
    window.lift()
    window.attributes('-topmost', True)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    #window loop
    window.after(1000,SaraMainLoop)
    window.mainloop()
def main():
    CreatGUI()
if __name__ == '__main__':
    main()


# In[2]:


def ReadAllComand():
    from openpyxl import load_workbook
    wb=load_workbook('Sara指令表/Sara指令表.xlsx')
    ws=wb.get_active_sheet()
    print(ws.max_row)
    print(ws.max_column)
    for column in ws.columns:
        for cell in column:
            print(cell.value)
ReadAllComand()


# In[2]:





# In[ ]:




