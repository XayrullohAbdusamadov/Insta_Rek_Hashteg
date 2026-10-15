@echo off
title Instagram Rek Hashtag Bot - Hayrulloh Abdusamadov
chcp 65001 > nul
cls

echo ===============================================================
echo     Instagram Rek Hashtag Telegram Bot
echo     Yaratuvchi: Hayrulloh Abdusamadov
echo ===============================================================
echo.

:: O'rnatilgan Python 3.12 yo'lini PATH ga qo'shish (Windows Store stubini chetlab o'tish)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" main.py
    goto end
)

:: Agar boshqa papkada bo'lsa py orqali tekshirish
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -3 main.py
    goto end
)

:: Oddiy python buyrug'i
python main.py

:end
if %ERRORLEVEL% neq 0 (
    echo.
    echo ===============================================================
    echo [DIQQAT] Bot to'xtadi yoki xatolik yuz berdi.
    echo Yuqoridagi xabarni ko'rib chiqing.
    echo ===============================================================
)
pause
