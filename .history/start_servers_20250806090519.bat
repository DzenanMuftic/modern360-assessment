@echo off
echo ============================================================
echo MODERN360 ASSESSMENT PLATFORM - DUAL SERVER LAUNCHER
echo ============================================================
echo.
echo Starting Modern360 Assessment Platform...
echo.
echo Main Application:
echo    URL: http://localhost:5000
echo    Purpose: User assessments, responses, dashboard
echo.
echo Admin Dashboard:
echo    URL: http://localhost:5001
echo    Username: admin
echo    Password: admin123
echo    Purpose: User management, assessment creation, reports
echo.
echo ============================================================
echo.

start "Modern360 Main App" python app.py
timeout /t 3 /nobreak >nul
start "Modern360 Admin App" python admin_app.py

echo Both servers are starting...
echo    Main App: http://localhost:5000
echo    Admin App: http://localhost:5001
echo.
echo Press any key to open admin dashboard in browser...
pause >nul
start http://localhost:5001

echo.
echo To stop the servers, close both terminal windows.
echo Press any key to exit this launcher...
pause >nul
