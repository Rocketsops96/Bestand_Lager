@echo off
taskkill /IM VVO.exe /F /FI "MODULES eq _bcrypt.pyd"
taskkill /f /im VVO.exe
update.exe
exit
