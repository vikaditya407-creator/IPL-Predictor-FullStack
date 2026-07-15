@echo off

start cmd /k "cd /d D:\Project A\IPL\backend && call venv\Scripts\activate && uvicorn app.main:app --reload"

timeout /t 5

start cmd /k "cd /d D:\Project A\IPL\frontend && npm start"