@echo off
start cmd /k "python cursor_agent.py"
timeout /t 2 >nul
start cmd /k "python chatgpt_agent.py"
timeout /t 2 >nul
start cmd /k "python llama3_agent.py"
