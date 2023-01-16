import requests
import re
import pandas as pd
import json
import time
def get_level(mid):
    url='https://api.bilibili.com/x/space/wbi/acc/info'
    headers = {'Refer': 'https://www.bilibili.com/','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'}
    params ={'mid':mid}
    response = requests.get(url=url,headers=headers,params=params)
    res=response.json()
    level=res['data']['level']
    return level

def get_next(res):
    zhen_ze2=re.compile('"next":(.*?),"total":')
    next1=zhen_ze2.findall(res)
    return next1
url='https://api.bilibili.com/pgc/review/short/list'
headers = {
    'Refer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}
params = {
    'media_id': 4315402,
    'ps': 20,
    'sort': 0,
    'cursor': 0
}

response = requests.get(url=url,headers=headers,params=params)
res=response.text

data={'score':[],'likes':[],'mid':[],"uname":[],"vipStatus":[],"content":[]}
# data={'score':[],'likes':[],'mid':[],"uname":[],"vipStatus":[],"content":[],'level':[]}
df1=pd.DataFrame(data,columns=['mid',"uname",'score',"content",'likes',"vipStatus"])
# df1=pd.DataFrame(data,columns=['mid',"uname",'score',"content",'likes',"vipStatus",'level'])
 

total=requests.get(url=url,headers=headers,params=params).json()['data']['total']
n=0
while n<total:
    response = requests.get(url=url,headers=headers,params=params)
    res=response.json()
    for number in range(len(res['data']['list'])):
        score=res['data']['list'][number]['score']
        likes=res['data']['list'][number]['stat']['likes']
        mid=res['data']['list'][number]['mid']
        uname=res['data']['list'][number]['author']["uname"]
        vipStatus=res['data']['list'][number]['author']['vip']["vipStatus"]
        content=res['data']['list'][number]["content"]
#         try:
#             level=get_level(mid)
#         except:
#             level=0
        df1=df1.append({'score':score,'likes':likes,'mid':mid,"content":content,'uname':uname,"vipStatus":vipStatus},ignore_index=True)
#         df1=df1.append({'score':score,'likes':likes,'mid':mid,"content":content,'uname':uname,"vipStatus":vipStatus,'level':level},ignore_index=True)
        n=n+1
    time.sleep(0.3)
    print((n/total)*100)
    next1=get_next(response.text)
    params['cursor']=next1
df1.to_excel('三体评分1.16.xlsx')        
    
 #   'uname':uname,"vipStatus":vipStatus
    
