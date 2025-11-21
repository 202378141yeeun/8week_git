@echo off
REM ===== 가상환경 생성 =====
python -m venv venv

REM ===== 가상환경 활성화 =====
call venv\Scripts\activate

REM ===== 패키지 설치 =====
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [INFO] 가상환경 셋팅 완료. (venv 활성화된 상태)
echo [INFO] 이 창에서 바로 서버 실행 명령을 입력할 수 있습니다.
echo.

REM 콘솔 창 유지
cmd /k
