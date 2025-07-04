@echo off
echo Starting OptiPrice Web Application...
echo ====================================
echo.
echo The web app will open in your default browser.
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.

streamlit run app.py

echo.
echo OptiPrice web app stopped.
pause
