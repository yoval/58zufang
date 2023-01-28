# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 20:53:22 2023

@author: Administrator
"""
import pandas as pd
import re
import folium
from folium import CustomIcon

excel_file_name = r'zufang_20230126.xlsx' #抓取58租房的excel文件名
BD09_json_file_name = 'BD09_58_zufang.json' #excel转换成json的文件名，用于转换坐标 https://map.easyv.cloud/transform
def excel_to_json(excel_file_name):
    df = pd.read_excel(excel_file_name,sheet_name=0)
    df.to_json(BD09_json_file_name,orient='records',force_ascii=False,indent=4)
    print('已保存：%s ，上传至 https://map.easyv.cloud/transform 转换为GCJ坐标系'%BD09_json_file_name)

GCJII_json_file_name = r'GCJ02_zufang.json' #转换坐标系后的json文件名
df = pd.read_json(GCJII_json_file_name)
#通过链接获得house_id
def get_house_id(url):
    house_id = re.findall('houseId=(\d+)&', url)[0]
    return house_id
df['房屋ID'] = df['链接'].apply(get_house_id)
df.drop_duplicates(subset=['房屋ID'],keep='first',inplace=True)

def get_leixing(lianxiren):
    leixing = re.findall(('\((.*?)\)'), lianxiren)[0]
    return leixing

def parse_zhch(s):
    return str(str(s).encode('ascii' , 'xmlcharrefreplace'))[2:-1]

location = (32.902092,117.312116)
location_name = '甜啦啦运营中心'
m = folium.Map(
        location=location, 
        zoom_start=15, 
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}', # 高德街道图
        control_scale=True,#添加比例尺
        attr='default'
    )


icon_image = 'https://www.tianlala.com/favicon.ico'
icon = CustomIcon(
    icon_image,
    icon_size=(20, 20),
)


folium.Marker(location = location,
              popup = folium.Popup(html=parse_zhch(location_name)),
              icon = icon,
              tooltip="甜啦啦"
             ).add_to(m)

df.dropna(axis='index', how='all', subset=['经度','纬度']) #删除经纬度有空值的行
#缩短租房详情链接
def short_url(url):
    return url.split("?")[0]
#把手机号的小数点去掉
def int_phone_number(phone_number):
    try:
        phone_number = str(int(phone_number))
    except:
        pass
    return phone_number

df['短链接'] = df['链接'].apply(short_url)
df['联系电话'] = df['联系电话'].apply(int_phone_number)
price_list = list(df['价格'])
html_list = []
for row in df.itertuples():
    html = "<p>%s</p><p>%s，%s</p><p>%s，%s</p><p><a href='%s'>链接</a></p>"%(row.标题,row.房屋类型,row.价格,row.联系人,row.联系电话,row.短链接)
    html_list.append(html)

zufang_locations = list(zip(df['纬度'],df['经度']))
count=0
for zufang_location in zufang_locations:
    html = html_list[count]
    folium.Marker(zufang_location, 
                  popup=folium.Popup(html=html),
                  tooltip="%s元"%price_list[count] #hover
                  ).add_to(m)
    count+=1


m.save('zufang_bengbu.html') 
