# 改用Flask
## PythonAnywhere

主程式source code (lv1codeman/mysite)  
[pythonanywhere/Files](https://www.pythonanywhere.com/user/lv1codeman/files/home/lv1codeman/mysite)


Web  
[pythonanywhere/Web](https://www.pythonanywhere.com/user/lv1codeman/webapps/#tab_id_lv1codeman_pythonanywhere_com)

# Web設置
## Code:
在Code:底下的Working directory路徑改成和Source code的一樣，才不會讀取不到static/data/message.json

## Virtualenv:
虛擬環境，作業系統是linux-based，用於安裝使用到的python module，路徑設置如下
/home/lv1codeman/.virtualenvs/myvirtualenv

可選擇[Start a console in this virtualenv](https://www.pythonanywhere.com/user/lv1codeman/consoles/virtualenv_console_in/lv1codeman.pythonanywhere.com/new)在新視窗開啟虛擬環境並輸入`pip list`可查看已安裝的modules

免費帳號只能開兩個console，開太多個的話需要去console介面關掉