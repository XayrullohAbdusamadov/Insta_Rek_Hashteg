@echo off
title Instagram Rek Hashtag Bot - Hayrulloh Abdusamadov
chcp 65001 > nul
cls

echo ===============================================================
echo     Instagram Rek Hashtag Telegram Bot
echo     Yaratuvchi: Hayrulloh Abdusamadov
echo ===============================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python main.py
) else (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" main.py
    ) else (
        echo [XATO] Python topilmadi! Iltimos, Python o'rnatilganligini tekshiring.
        pause
    )
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Bot to'xtadi yoki xatolik yuz berdi.
    pause
)
