#!/usr/bin/env python
# coding: utf-8

# In[20]:
import webbrowser
import platform
import requests
from bs4 import BeautifulSoup
import re
from SaraModules import SaraSpeak
import time
# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# Linux
# chrome_path = '/usr/bin/google-chrome %s'  
def __init__(self):
    if platform.system()==Darwin:
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    if platform.system()==Windows:
        chrome_path='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
#開啟網頁
def openWithURL():
    url=input()
    webbrowser.get(chrome_path).open(url)
def openURL(url):
    webbrowser.get(chrome_path).open(url)
#爬取逢甲大學ilearn公布欄
def SearchilearnBroadcast():
    session = requests.Session()
    SaraSpeak.SpeakChinese('請給我你的學校帳號密碼')
    account=input('請輸入帳號:')
    password=input('請輸入密碼:')
    print('請稍等')
    data = {'username': account, 'password': password}
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
    SaraSpeak.SpeakChinese('以下科目有新的公告 請趕快登入網站查詢  須要幫你打開ilearn嗎？')
    time.sleep(3)
    print('以下科目有新的公告 請趕快登入網站查詢:'+say)
    data=input('要幫你打開ilearn嗎？ y/n')
    if data is 'y':
         webbrowser.get(chrome_path).open('https://ilearn2.fcu.edu.tw/')
#查詢台中天氣
def SearchingWeather():
    SaraSpeak.SpeakChinese("正在搜尋天氣狀況...")
    r = requests.get('https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
    soup=BeautifulSoup(r.content,'lxml')
    result=soup.find_all("td")
    time.sleep(1)
    speak="台中天氣 今晚至明晨"+result[2].text+" 明天白天"+result[6].text+" 明天晚上"+result[10].text
    print(speak)
#爬取維基百科
def SearchWiki():
    SaraSpeak.SpeakChinese("請給我你要搜尋的名稱")
    searching=input('請輸入你要搜索什麼:')
    res=requests.get('https://zh.wikipedia.org/wiki/{}'.format(searching))
    soup=BeautifulSoup(res.text,'lxml')
    result=soup.select_one('.mw-parser-output p').text
    time.sleep(1)
    SaraSpeak.SpeakChinese("以上為維基百科搜尋結果")
    print(result)
#星座運勢
def constellationLuck():
    SaraSpeak.SpeakChinese('你是什麼星座?')
    choose=input("請問你的星座是？(1)牡羊 (2)金牛 (3)雙子 (4)巨蟹 (5)獅子 (6)處女 (7)天秤 (8)天蠍 (9)射手 (10)摩羯 (11)水瓶 (12)雙魚)")
    r=requests.get('https://m.click108.com.tw/astro/index.php?astroNum='+choose)
    soup=BeautifulSoup(r.content,'lxml')
    dayluktitle=soup.find(id='astroDailyWording')
    print('今日運勢:'+dayluktitle.text)
    dayloveluk=soup.find(id='astroDailyData_love')
    print('愛情運:'+dayloveluk.text)
#電影推薦
def MovieRecommand():
    SaraSpeak.SpeakChinese('我來幫你看看有什麼最新電影')
    r=requests.get('https://movies.yahoo.com.tw/movie_intheaters.html')
    soup=BeautifulSoup(r.content,'lxml')
    result=soup.find("ul",{"class":"ranking_list_r"})
    time.sleep(3)
    SaraSpeak.SpeakChinese('這些是我推薦的電影~')
    time.sleep(2)
    print("以下是我推薦的電影 :")
    print(result.text.replace("\n",""))
def ListenMusic():
    import youtube_dl
    SaraSpeak.SpeakChinese('請問你要聽什麼音樂')
    searchMusic=input('請問你想聽什麼音樂?')
    url='https://www.youtube.com/results?search_query='+searchMusic
    print(url)
    r=requests.get(url)
    soup=BeautifulSoup(r.content,'lxml')
    downloadTarget=soup.select('h3')[3].select('a')[0]['href']
    url="https://www.youtube.com"+downloadTarget
    openURL(url)


# In[ ]:




