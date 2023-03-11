# -*- coding: utf-8 -*-

import netifaces
import time
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen
import win32serviceutil
import win32service
import win32event


def getInterface(): #确认连接公网的网卡
    interfaces=netifaces.interfaces()
    for interface in interfaces:
        addr=netifaces.ifaddresses(interface)
        if netifaces.AF_INET6 in addr.keys():
            tempIP=addr[netifaces.AF_INET6][0]['addr']
            if tempIP[:4]=='2409': #中国移动
                return interface
    return ''

def findIPv6(interface):
    addrs=netifaces.ifaddresses(interface)
    #ip=addrs[netifaces.AF_INET6][0]['addr'] #获取最靠上的地址
    ip=''
    for addr in addrs[netifaces.AF_INET6]: #获取最新的临时地址
        if addr['addr'][:4]=='2409':
            ip=addr['addr']
    return ip

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

def saveLog(fileName,log):
    try:
        f=open(fileName,'a+')
        f.write(log)
        f.close()
    except Exception as e:
        return e
    else:
        return True




class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "IPv6Check"
    _svc_display_name_ = "IPv6 DDNS updater"
    _svc_description_ = "Update IPv6 to DDNS service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        SAVED_IP="C:/Users/sample/OneDrive/IPv6.txt" #本地保存IP地址的文件
        SLEEP_TIME=10 #运行间隔，单位分钟
        INTERFACE=getInterface()
        oldIP=oldIPv6(SAVED_IP)
        loop=True
        while loop:
            oldIP=self.oneLoop(oldIP,INTERFACE)
            #time.sleep(SLEEP_TIME*60) 
            if win32event.WaitForSingleObject(self.hWaitStop,SLEEP_TIME*60*1000)==win32event.WAIT_OBJECT_0:
                break
    
    def oneLoop(self,oldIP,interface):
        SAVED_IP="C:/Users/sample/OneDrive/IPv6.txt" #本地保存IP地址的文件
        IP_LOG="C:/Users/sample/OneDrive/IPlog.txt" #本地记录文件
        HOSTNAME="sample.dynv6.net" #hostname 
        TOKEN="" #token
        tempIP=findIPv6(interface)
        if tempIP!=oldIP:
            newIP=tempIP
            sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" Notice:\tIPv6 changed\n"
            sentlog+=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" IPv6:\t"+newIP+"\n"
            saveLog(IP_LOG,sentlog)
            check=saveIPv6(SAVED_IP,newIP)
            if check!=True:
                sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' File:\t'+str(check)+'\n'
            else:
                sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" File:\tnew IPv6 saved\n"
            saveLog(IP_LOG,sentlog)
            res=updateIPv6(HOSTNAME,TOKEN,newIP)
            sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' DDNS:\t'+res+'\n'
            saveLog(IP_LOG,sentlog)
            return newIP
        else:
            #sentlog=datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Info:\tIPv6 no change\n'
            #saveLog(IP_LOG,sentlog)
            return oldIP

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)

