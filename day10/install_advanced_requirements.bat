@echo off
echo ========================================
echo 고급 TTS 프로그램 라이브러리 설치 스크립트
echo ========================================
echo.

echo 1. pip 업그레이드 중...
python -m pip install --upgrade pip
echo.

echo 2. 기본 라이브러리 설치 중...
echo - gTTS (Google Text-to-Speech) 설치...
pip install gtts
echo.

echo - pyttsx3 (Windows TTS) 설치...
pip install pyttsx3
echo.

echo - playsound (음성 재생) 설치...
pip install playsound
echo.

echo 3. 고급 라이브러리 설치 중...
echo - pygame (안정적인 음성 재생) 설치...
pip install pygame
echo.

echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo 이제 다음 명령어로 프로그램을 실행할 수 있습니다:
echo.
echo 기본 프로그램:
echo python tts_program.py
echo.
echo 고급 프로그램 (pygame 사용):
echo python tts_advanced.py
echo.
echo 예시 프로그램:
echo python tts_example.py
echo.
echo 테스트 프로그램:
echo python test_tts.py
echo.
pause 