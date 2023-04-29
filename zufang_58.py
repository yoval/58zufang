# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 08:57:38 2023

@author: Administrator
"""
import time,re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


url = 'https://bengbu.58.com/chuzu/pn58/?PGTID=0d3090a7-00d8-e854-629d-ebdbbae6b237&ClickID=162'

browser = webdriver.Chrome() 
browser.get(url)
handle = browser.current_window_handle
time.sleep(5)
df = pd.DataFrame() #生成df
input('如需登录，请在打开网页登录，不登录可能验证码比较多。按回车键继续……')
while True:
#    btns = browser.find_elements_by_xpath("//div[@class='des']/h2/a[@class='strongbox']")
    btns = browser.find_elements(By.XPATH, "//div[@class='des']/h2/a[@class='strongbox']")
    for btn in btns:
        browser.switch_to.window(handle)
        time.sleep(8)
        try:
            btn.click()#进入租房详情页
        except Exception as e:
            print(e)
            continue
        allWindows = browser.window_handles
        browser.switch_to.window(allWindows[-1])
        Current_url = browser.current_url #详情页链接
        soup = BeautifulSoup(browser.page_source,'lxml')
        if '请输入验证码' in soup.title:
            input('被限制了，解决后按回车键继续')
            browser.refresh()
            soup = BeautifulSoup(browser.page_source,'lxml')
        title = soup.find_all('div',class_='house-title')[0]
        title = title.h1.get_text() #标题
        price = soup.find_all('b',class_='f36 strongbox')[0]
        price = price.get_text()
        price = price.strip() #价格
        instructions = soup.find_all('span',class_='instructions')[0]
        instructions = instructions.get_text() #支付方式
        zuling_type = soup.find_all('span',class_='c_888 mr_15')
        zuling = zuling_type[0].next_sibling.get_text() #租赁方式
        leixing = zuling_type[1].next_sibling.get_text()
        leixing = leixing.strip()
        leixing = leixing.replace('\xa0\xa0','-') #房屋类型
        chaoixang = zuling_type[2].next_sibling.next_sibling.get_text()
        chaoixang = chaoixang.replace('\xa0\xa0','-') #朝向楼层
        xiaoqu = soup.find_all('a',class_='c_333 ah')[0]
        xiaoqu = xiaoqu.get_text()
        xiaoqu = xiaoqu.strip() #所在小区
        quyu =  zuling_type[4].next_sibling.get_text()
        quyu = re.sub(r'(\s|\x00)', '', quyu)#所属区域
        address = zuling_type[5].next_sibling.next_sibling.get_text()
        address = re.sub(r'(\s|\x00)', '', address)
        lianxiren = soup.find_all('a',class_='c_000')[0]
        lianxiren = re.sub(r'(\s|\x00)', '', lianxiren.get_text())#联系人
        try:
            phone = soup.find_all('p',class_='phone-num strongbox')[0]
            phone = phone.get_text()
        except:
            phone = ''
        try:
            agent_company = soup.find_all('p',class_='agent-company')[0]
            agent_company = re.sub(r'(\s|\x00)', '', agent_company.get_text())
        except:
            agent_company = ''
        try:
            map_url = soup.find_all('div',class_='view-more-detailmap view-more')[0]    
            map_url = map_url.a.get('href')
            location = re.findall('location=(.*?)&', map_url)[0]
        except:
            jingdu = ''
            weidu = ''
        [weidu,jingdu] = location.split(',')
        data = {'标题':title,'价格':price,'租赁方式':zuling,'房屋类型':leixing,'朝向':chaoixang,'小区':xiaoqu,'所属区域':quyu,'地址':address,'纬度':weidu,'经度':jingdu,'联系人':lianxiren,'联系电话':phone,'公司':agent_company,'链接':Current_url}
        df = df.append(data, ignore_index = True)#保存数据
        print('已添加：%s'%title)
        time.sleep(5)
        browser.close()
    time.sleep(5)
    try:
        print('翻下一页')
        browser.switch_to.window(handle)
#        next_btn = browser.find_elements_by_css_selector("[class='next']")[0]
        next_btn = browser.find_elements(By.CSS_SELECTOR,"[class='next']")[0]
        next_btn.click()
        time.sleep(5)
    except:
        break
fileName = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
df.to_excel('%s.xlsx'%fileName,index=False)
browser.quit()    
