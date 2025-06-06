@echo off
echo Creating .env file...
del /Q .env 2>nul

echo # API Keys > .env
echo GEMINI_API_KEY=AIzaSyB1LBl9v8HQ2fH8dAnrPQHN_Hx8dReWJSE >> .env
echo. >> .env
echo # Browser Settings >> .env
echo BROWSER_HEADLESS=False >> .env
echo BROWSER_TIMEOUT=30 >> .env
echo. >> .env
echo # Automation Settings >> .env
echo MAX_RETRIES=3 >> .env
echo RETRY_DELAY=5 >> .env
echo ITERATION_DELAY=1 >> .env
echo. >> .env
echo # Git Settings >> .env
echo GIT_REPO_URL=https://github.com/appechomind/echo_loop_control.git >> .env
echo GIT_BRANCH=main >> .env
echo. >> .env
echo # Logging Settings >> .env
echo LOG_LEVEL=INFO >> .env

echo ✅ .env file created successfully!
echo.
echo 📝 Contents:
type .env 