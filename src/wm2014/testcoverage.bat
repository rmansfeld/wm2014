@ECHO OFF
call ..\..\venv\Scripts\activate.bat
coverage run manage.py test
coverage report
