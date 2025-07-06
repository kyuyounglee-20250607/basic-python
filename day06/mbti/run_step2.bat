@echo off
echo ========================================
echo 🌐 MBTI 성격유형 검사 - 2단계 (웹)
echo ========================================
echo.

cd step2_flask_mbti
echo 📁 디렉토리 이동: step2_flask_mbti
echo.

echo 🔧 의존성 확인 중...
python -c "import flask, pandas" 2>nul
if errorlevel 1 (
    echo ❌ 필요한 패키지가 설치되지 않았습니다.
    echo 📦 설치 중: pip install flask pandas
    pip install flask pandas
    echo.
)

echo 🚀 Flask 웹 애플리케이션을 시작합니다...
echo.
echo 🌐 웹 브라우저에서 http://localhost:5000 으로 접속하세요!
echo.
echo ⚠️  프로그램을 종료하려면 Ctrl+C를 누르세요.
echo.

python app.py

echo.
echo 👋 웹 서버가 종료되었습니다.
pause 