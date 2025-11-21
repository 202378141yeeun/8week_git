@echo off

REM ===== FastAPI 서버 실행 =====
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo [INFO] 서버가 종료되었습니다.
echo.

REM 콘솔 창 유지
pause
