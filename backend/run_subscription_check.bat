@echo off
cd /d "e:\AgaShop\Frontend\backend"
call venv\Scripts\activate.bat
python manage.py check_subscriptions
