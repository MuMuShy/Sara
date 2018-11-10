#!/usr/bin/env python
# coding: utf-8

# In[81]:


import webbrowser
import platform
import requests
from bs4 import BeautifulSoup
import re
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
#爬取逢甲大學ilearn公布欄
def SearchilearnBroadcast():
    session = requests.Session()
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
    print('以下科目有新的公告 請趕快登入網站查詢:'+say)
    data=input('要幫你打開ilearn嗎？ y/n')
    if data is 'y':
         webbrowser.get(chrome_path).open('https://ilearn2.fcu.edu.tw/')
#查詢台中天氣
def SearchingWeather():
    r = requests.get('https://www.cwb.gov.tw/V7/forecast/taiwan/Taichung_City.htm')
    soup=BeautifulSoup(r.content,'lxml')
    result=soup.find_all("td")
    speak="台中天氣 今晚至明晨"+result[2].text+" 明天白天"+result[6].text+" 明天晚上"+result[10].text
    print(speak)
#爬取維基百科
def SearchWiki():
    searching=input('請輸入你要搜索什麼:')
    res=requests.get('https://zh.wikipedia.org/wiki/{}'.format(searching))
    soup=BeautifulSoup(res.text,'lxml')
    result=soup.select_one('.mw-parser-output p').text
    print(result)
#星座運勢
def constellationLuck():
    choose=input("請問你的星座是？(1)牡羊 (2)金牛 (3)雙子 (4)巨蟹 (5)獅子 (6)處女 (7)天秤 (8)天蠍 (9)射手 (10)摩羯 (11)水瓶 (12)雙魚)")
    r=requests.get('https://m.click108.com.tw/astro/index.php?astroNum='+choose)
    soup=BeautifulSoup(r.content,'lxml')
    dayluktitle=soup.find(id='astroDailyWording')
    print('今日運勢:'+dayluktitle.text)
    dayloveluk=soup.find(id='astroDailyData_love')
    print('愛情運:'+dayloveluk.text)
#電影推薦
def MovieRecommand():
    r=requests.get('https://movies.yahoo.com.tw/movie_intheaters.html')
    soup=BeautifulSoup(r.content,'lxml')
    result=soup.find("ul",{"class":"ranking_list_r"})
    print("以下是我推薦的電影 :")
    print(result.text.replace("\n",""))


# In[ ]:




