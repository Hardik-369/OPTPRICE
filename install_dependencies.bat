@echo off
echo Installing OptiPrice Web App Dependencies...
echo ==========================================
echo.

echo Installing required Python packages...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo You can now run the web application using:
echo   - run_webapp.bat
echo   - streamlit run app.py
echo.
echo The web app will be available at: http://localhost:8501
echo.
pause
