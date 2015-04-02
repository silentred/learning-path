@echo off
title [IP地址设置和ARP绑定]
color F9
ver|find /i "5.1." >nul && set ETHERNET=本地连接 && set SYSTEM=WinXP 
ver|find /i "6.1." >nul && set ETHERNET=本地连接 && set SYSTEM=Win7
ver|find /i "6.2." >nul && set ETHERNET=以太网 &&set SYSTEM=Win8
ver|find /i "6.3." >nul && set ETHERNET=以太网 &&set SYSTEM=Win8.1
@echo ======================================================================
@echo ""
@echo 当前系统为：%SYSTEM%
@echo ""
@echo 注意：Win7、WIN8、Win8.1系统，请右键选择以管理员身份运行！
@echo 注意：如果出现360弹窗，选择允许！
@echo 注意：出现 [设置完毕] 表示设置完毕，请耐心等待，中途不要执行其他操作！
@echo ""
@echo ======================================================================
@ping 127.0.0.1 -n 8 >nul
@echo ""
@echo ************************第一步，设置 ip 地址！************************
@echo ""
@set IP=172.16.1.19
@set MASK=255.255.254.0
@set GATEWAY=172.16.0.1
@set DNS1=114.114.114.114
@set DNS2=8.8.4.4
@echo ==========================[开始设置 ip 地址]==========================
@echo 正在设置IP地址，请稍等......
netsh interface ip set address %ETHERNET% static %IP% %MASK% %GATEWAY% 1 >nul
@echo ""
@echo IP地址为：%IP%
@echo 子网掩码：%MASK%
@echo 默认网关：%GATEWAY%
@echo ==========================[开始设置 dns地址]==========================
@echo 正在设置DNS地址，请稍等......
netsh interface ip set dns %ETHERNET% source=static address=%DNS1% primary >nul
netsh interface ip add dns %ETHERNET% address=%DNS2% >nul
@echo ""
@echo 主DNS地址为：%DNS1%
@echo 辅DNS地址为：%DNS2%
@echo ==========================[完成 ip 地址设置]==========================
@echo ""
@echo ======================================================================
@echo ""
@echo ************************第二步，arp 网关绑定！************************
@echo ""
if /i "%SYSTEM%"=="WinXP" goto NT5
if /i "%SYSTEM%"=="Win7" goto NT6
if /i "%SYSTEM%"=="Win8" goto NT6
if /i "%SYSTEM%"=="Win8.1" goto NT6
:NT5
@echo ==========================[开始 arp网关绑定]==========================
@echo NT5网关绑定
arp -s %GATEWAY% 00-22-19-d4-18-79
@echo ==========================[创建 arp绑定文件]==========================
@echo 开始创建开机启动arp绑定文件，请稍等......
echo cd \ > "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\arp.cmd"
echo arp -a >> "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\arp.cmd"
echo arp -d >> "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\arp.cmd"
echo arp -s %GATEWAY% 00-22-19-d4-18-79 >> "C:\Documents and Settings\All Users\「开始」菜单\程序\启动\arp.cmd"
@echo ==========================[完成 arp网关绑定]==========================
goto END
:NT6
@echo ==========================[开始 arp网关绑定]==========================
@echo NT6网关绑定
netsh i i show in
@echo ==========================[获取网卡 idx编号]==========================
@echo 正在获取网卡idx编号，请稍等......
for /f "tokens=1 delims= " %%i in ('netsh i i show in^|findstr %ETHERNET%') do set Idx=%%i >nul
@echo ""
@echo 你的网卡idx编号是:[%Idx%]
@echo ==========================[绑定 arp网关地址]==========================
@echo 正在绑定arp网关地址，请稍等......
arp -d >nul
netsh i i delete neighbors >nul
netsh -c "i i" add neighbors %Idx% %GATEWAY% "00-22-19-d4-18-79" >nul
@echo ""
@echo 显示网关绑定状态:
arp -a | find /i "%GATEWAY%"
@echo ==========================[完成 arp网关绑定]==========================
goto END
:END
@ping 127.0.0.1 -n 3 >nul
@echo ""
@echo ******************************[设置完毕]******************************
@echo ""
@echo 请按任意键关闭窗口！ &pause>nul