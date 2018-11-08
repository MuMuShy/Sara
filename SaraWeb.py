#!/usr/bin/env python
# coding: utf-8

# In[29]:


import webbrowser
import platform
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
def openWithURL():
    url=input()
    webbrowser.get(chrome_path).open(url)
def mult(a,b):
    return a*b


# In[28]:





# In[ ]:




