@echo off

start "" cmd /c server.bat
echo Waiting for server HTTP endpoint to respond...

:waitloop
:: Check if Flask server (port 5000) is up
powershell -Command "try { $res = Invoke-WebRequest -Uri http://127.0.0.1:5000/status -UseBasicParsing -TimeoutSec 1; if ($res.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
if errorlevel 1 (
    echo Flask server is not ready. Waiting...
    timeout /t 1 >nul
    goto waitloop
)

:: Check if Go server (port 8080) is up
powershell -Command "try { $res = Invoke-WebRequest -Uri http://127.0.0.1:8080/status -UseBasicParsing -TimeoutSec 1; if ($res.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
if errorlevel 1 (
    echo Go server is not ready. Waiting...
    timeout /t 1 >nul
    goto waitloop
)

echo Both servers are ready. Launching UI...
call ui.bat