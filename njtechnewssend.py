#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

allt=[]
def geth(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ''
def beauty(soup):
    postlines=''
    post=open('post.txt','w')
    a = soup.find('div', class_="txt")

    w=a.find('ul')

    d=w.find_all('a')
    nowtimes=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    posthead="今日教学新闻（ {1} 最新{0}条）:\n".format(len(d),nowtimes)
    post.writelines(posthead)
    for i in range(len(d)):
        postline=str(i+1) + ':' + d[i].string + '\n' + '网址为{}'.format(d[i].get('href').replace('..','jwb.njtech.edu.cn')) + '\n'
        #print(postline)
        post.writelines(postline)
        postlines+=postline
    post.close()

    postsend=posthead+postlines
    #print(postsend)
    return postsend

url='http://jwb.njtech.edu.cn/index/tzgg.htm'
html=geth(url)
soup=BS(html,'html.parser')
sendpost=beauty(soup)

sender='tabristrees@qq.com'
pwd='hfmaaifyjcrodhaj'#在开通相关的服务是会给你相应的密码，不是你自己登陆qq的密码

receivers=['2858795004@qq.com','3110263088@qq.com']#收件人的邮箱

#三个参数：第一个为文本内容，第二个为plain设置文本格式，第三个utf-8设置编码
message=MIMEText(sendpost,'plain','utf-8')
#标准邮件需要3个头部信息
message['From']=Header("伍先树",'utf-8')#发件人
message['To']=Header("所有人",'utf-8')#收件人
message['Subject']=Header('Njtech教务处网站新闻','utf-8')#邮件标题

try:
    #使用非本地服务器，需要使用ssl连接
    smtpObj=smtplib.SMTP_SSL("smtp.qq.com",465)
    smtpObj.login(sender,pwd)#登录第三方服务器
    smtpObj.sendmail(sender,receivers,message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("Error: 无法发送邮件，因为：%s"% e)


