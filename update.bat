@echo off
taskkill /IM VVO.exe /F /FI "MODULES eq _bcrypt.pyd"

update.exe
VVO.exe
exit
