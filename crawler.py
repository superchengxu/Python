# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:13:50 2016

@author: Xu.Cheng
"""
import re
import requests
import csv


def createListCSV(fileName="", dataList=[]):
    with open(fileName, "w",newline='') as csvFile:
        csvWriter = csv.writer(csvFile,delimiter=',')        
        for data in dataList:
            csvWriter.writerow(data)
        csvFile.close
    

#需要解决 1持续登录 2翻页 3数据抽取

url1 = 'hhttps://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'#登陆地址
url2 = "http://bj.lianjia.com/chengjiao/beiyuan2/"#需要登陆才能访问的地址


#北苑家园历史成交100页URL生成
url_base = "http://bj.lianjia.com/chengjiao/beiyuan2/pg"
url_list = []
n=0
while(n<100):
    url_list.append(url_base + str(n+1))
#    print(url_list[n])
    n=n+1
    
#爬取所有房子数据放在一个list中
houselist=[]
for each_url in url_list:
    print("Now we are fetching " + each_url)
    print("Current No. of house is "+ str(len(houselist)))
    cookie = 'lianjia_uuid=c37a8c4f-e9f7-4bf5-bf78-e2327d7c4722; lianjia_token=2.003e80ed044440bcc92f2dc4355031213c; miyue_hide=%20index%20%20index%20%20index%20%20index%20; cityCode=sh; ubt_load_interval_b=1463547095779; ubt_load_interval_c=1463547095779; ubta=2299869246.62609477.1463547096790.1463547096790.1463547096790.1; ubtb=2299869246.62609477.1463547096799.E2090CFC92DBF8656F190284CE4AFE96; ubtc=2299869246.62609477.1463547096799.E2090CFC92DBF8656F190284CE4AFE96; ubtd=1; select_city=110000; logger_session=bed93452d1f356540b065cf42c5746b2; lianjia_ssid=4b954e01-ba7c-42af-b840-efabb9869b38; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=573a94a4.41a4886e; CNZZDATA1253477573=422040716-1463452363-%7C1463543690; CNZZDATA1254525948=1205447239-1463452434-%7C1463544258; CNZZDATA1255633284=2028373821-1463453194-%7C1463544992; CNZZDATA1255604082=1214744714-1463455545-%7C1463542527; _ga=GA1.2.395491520.1463456932'
    headers = { 
            "Host":"bj.lianjia.com",
             "Connection":"keep-alive",
             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER" ,       
            "Referer":"http://bj.lianjia.com/chengjiao/",
             "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cookie":cookie
            }
    res = requests.get(each_url, headers=headers)
    res.encoding='utf-8'
    html = res.text
    pattern = '<div class="info-panel"><h2>.*? /></a></div>'
    houselist.extend(re.findall(pattern,html))
#append是把整体作为一个元素加入list    ，extend用来list合并
print(len(houselist))
#print(houselist[0])
#for each in houselist:
 #   print(each)

#数据提取
pattern_housename = 'target="_blank">(.*?)</a>'
pattern_height = '<div class="con">(.*?)</div>'
pattern_year = '<div class="introduce"><span>(.*?)</span>'
pattern_date='<div class="col-2 fr"><div class="dealType"><div class="fl"><div class="div-cun">(.*?)</div>'
pattern_price = '</p></div><div class="fl"><div class="div-cun">(.*?)<span>'
pattern_price_total = '<div class="fr"><div class="div-cun">(.*?)<span>'

final_list=[]

count=0
for each_house in houselist:
    print(count)
    count=count+1
    housename =re.findall(pattern_housename,each_house)
    if len(housename)==0:
        continue;
    split_house =str( housename[0]).strip().split()
    
    h=re.findall(pattern_height,each_house)
    length = len(h[0].strip().split('/'))
    if length == 3:
        split_house.append(str(h[0]).strip().split('/')[0].strip())
        split_house.append(str(h[0]).strip().split('/')[1].strip())
        split_house.append(str(h[0]).strip().split('/')[2].strip())
    elif length ==2:
        split_house.append(str(h[0]).strip().split('/')[0].strip())
        split_house.append(str(h[0]).strip().split('/')[1].strip())
    elif length ==1:
        split_house.append(str(h[0]).strip().split('/')[0].strip())    
    
    length = len(re.findall(pattern_year,each_house))
    if length ==1:
        split_house.append(str(re.findall(pattern_year,each_house)[0]).strip())
    elif length ==0:
        split_house.append('')
    
    split_house.append(str(re.findall(pattern_date,each_house)[0]).strip())
    split_house.append(str(re.findall(pattern_price,each_house)[0]).strip())
    split_house.append(str(re.findall(pattern_price_total,each_house)[0]).strip())
    print(split_house)
    final_list.append(split_house)

createListCSV('csvtest.csv',final_list)

