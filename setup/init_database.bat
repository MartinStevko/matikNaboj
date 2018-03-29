@echo off
title Naboj

REM Project directory
cd %~dp0
cd ..
pause

REM Migrations
manage.py makemigrations obdlznik
manage.py makemigrations trojuholnik

manage.py migrate

echo Migrations successfully created!
pause

REM Superuser
manage.py createsuperuser
pause

REM Database creation
cd %~dp0
python base.py

cd ..
manage.py shell < .\setup\base_data.txt
del .\setup\base_data.txt
echo Database successfully created!
pause

REM Server initiation
manage.py runserver 0.0.0.0:80
