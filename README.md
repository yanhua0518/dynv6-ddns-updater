# dynv6更新DDNS地址  
个人用  
Win版需要`pywin32`库，作为系统服务运行  
添加到服务并自动启动：  
```
python IPv6CheckWin.py --startup auto install
```
启动服务：
```
python IPv6CheckWin.py start
```

DSM版直接添加到任务计划
```
cd /存放目录/
python3 IPv6CheckDSM.py
```
自行设定运行频率
