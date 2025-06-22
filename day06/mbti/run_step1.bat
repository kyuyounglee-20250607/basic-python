@echo off
echo ========================================
echo 🧠 MBTI 성격유형 검사 - 1단계 (콘솔)
echo ========================================
echo.

cd step1_mbti
echo 📁 디렉토리 이동: step1_mbti
echo.

echo 🔧 의존성 확인 중...
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo ❌ pandas가 설치되지 않았습니다.
    echo 📦 설치 중: pip install pandas
    pip install pandas
    echo.
)

echo 🚀 MBTI 검사 프로그램을 시작합니다...
echo.
python mbti_console.py

echo.
echo 👋 프로그램이 종료되었습니다.
pause 