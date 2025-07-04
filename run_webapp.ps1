# OptiPrice Streamlit Web Application Launcher
# PowerShell execution script

Write-Host "Starting OptiPrice Web Application..." -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "The web app will open in your default browser." -ForegroundColor Yellow
Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow
Write-Host ""

try {
    streamlit run app.py
}
catch {
    Write-Host "Error starting Streamlit: $_" -ForegroundColor Red
    Write-Host "Make sure Streamlit is installed: pip install streamlit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "OptiPrice web app stopped." -ForegroundColor Green
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
