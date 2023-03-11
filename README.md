# dynv6更新DDNS地址  
个人用  
### Win版  
需要`pywin32`库，作为系统服务运行  
可以用网盘等方式把本地存储的文件进行云同步以便随时确认  

添加到服务并自动启动：  
```
python IPv6CheckWin.py --startup auto install
```
启动服务：  
```
python IPv6CheckWin.py start
```

### DSM版  
IP更新时自动发送邮件到设定好的邮箱  
如不需要发送邮件，删除两处`'''`前的`#`即可
直接添加到任务计划  
```
cd /存放目录/
python3 IPv6CheckDSM.py
```
自行设定运行频率  
