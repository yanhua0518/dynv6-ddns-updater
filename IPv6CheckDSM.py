# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen

def updateIPv6(hostname,token,ip):
    #addr=ip[:ip.rfind('/')]
    #prefix=ip[ip.rfind('/')+1:]
    parameters={'hostname':hostname,'token':token,'ipv6':ip}
    url='https://dynv6.com/api/update?'
    url+=urlencode(parameters)
    try:
        res=urlopen(url)
        data=res.read().decode()
    except Exception as e:
    	return str(e)
    else:
    	return data


def oldIPv6(fileName):
    try:
        f=open(fileName,'r')
        ip=f.readline()
        f.close()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return e
    else:
        return ip

def saveIPv6(fileName,ip):
    try:
        f=open(fileName,'w')
        f.write(ip)
        f.close()
    except Exception as e:
        return e
    else:
        return True

def findIPv6():
    output=os.popen('ip -f inet6 addr show eth0').readlines()
    for line in output:
        if line.find('global')>-1:
            ip=line[line.find('inet6')+6:line.find('/')]
            #ip=line[line.find('inet6')+6:line.find('scope')-1]
            return ip
    return False

def saveLog(fileName,log):
    try:
        f=open(fileName,'a+')
        f.write(log)
        f.close()
    except Exception as e:
        return e
    else:
        return True

SAVED_IP="IPv6.txt" #本地保存IP地址的文件
IP_LOG="IPlog.txt" #本地记录文件
HOSTNAME="sample.dynv6.net" #hostname 
TOKEN="" #token

tempIP=findIPv6()
if tempIP:
    oldIP=oldIPv6(SAVED_IP)
    if tempIP!=oldIP:
        newIP=tempIP
        sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\tNotice: IPv6 changed\n"
        
        #'''
        import smtplib
        from email.mime.text import MIMEText
        msg=MIMEText(newIP,'plain','utf-8')
        msg['From']='a@qq.com' #发件人
        msg['To']='b@qq.com' #收件人
        msg['Subject']='IP changed' #邮件主题
        text=msg.as_string()
        try:
            smtp=smtplib.SMTP('smtp.qq.com',25) #SMTP服务器地址、端口
            smtp.login('username','password') #用户名或邮箱地址、密码或授权码
            smtp.sendmail("a@qq.com","b@qq.com",text) #发件地址、收件地址
        except Exception as e:
            sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\tE-mail: '+str(e)+'\n'
        #else:
            #sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\tE-mail: sent\n"
        #'''
        
        check=saveIPv6(SAVED_IP,newIP)
        if check!=True:
            sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\tfile: '+str(check)+'\n'
        #else:
            #sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\tfile: new IPv6 saved\n"
        res=updateIPv6(HOSTNAME,TOKEN,newIP)
        sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\tDDNS: '+res+'\n'
        saveLog(IP_LOG,sentlog)
    else:
        print("IPv6 no change")
else:
    sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\tglobal IPv6 not found!\n"
    saveLog(IP_LOG,sentlog)
