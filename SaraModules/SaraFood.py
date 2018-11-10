
# coding: utf-8

# In[14]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re

def recommendation():
    food = input('欲查詢食譜:')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://icook.tw/")
    driver.find_element_by_name("q").click()
    driver.find_element_by_name("q").clear()
    driver.find_element_by_name("q").send_keys(food)
    driver.find_element_by_css_selector("button.btn.btn-search").click()
    #driver.close()
    titles=[]
    ingredients=[]
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    for a in soup.find_all('a',{'class':'browse-recipe-name'})[:5]:
        titles.append(a['title'])
    for p in soup.find_all('p',{'class':'browse-recipe-content-ingredient'})[:5]:
        ingredients.append(p.text)
    print('推薦以下餐點:')
    for i in range(0,5):
        print((i+1),titles[i])
        print(ingredients[i])
    driver.close()

