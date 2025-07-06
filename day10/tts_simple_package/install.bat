@echo off
echo ========================================
echo 간단한 TTS 패키지 설치 스크립트
echo ========================================
echo.

echo 🎵 간단한 TTS 패키지 설치를 시작합니다...
echo.

echo 1. pip 업그레이드 중...
python -m pip install --upgrade pip
echo.

echo 2. 필수 라이브러리 설치 중...
echo.

echo - gTTS (Google Text-to-Speech) 설치...
pip install gtts
echo.

echo - pygame (안정적인 음성 재생) 설치...
pip install pygame
echo.

echo ========================================
echo ✅ 간단한 TTS 패키지 설치 완료!
echo ========================================
echo.

echo 📋 사용 방법:
echo.
echo 1. 테스트 실행:
echo    python test_simple_tts.py
echo.
echo 2. 패키지 직접 사용:
echo    python -c "from tts_simple import speak_korean; speak_korean('안녕하세요!')"
echo.

echo 🎯 빠른 시작 예시:
echo    from tts_simple import speak_korean, speak_english
echo    speak_korean("안녕하세요!")
echo    speak_english("Hello!")
echo.

echo 📖 지원 언어:
echo    - 한국어 (ko)
echo    - 영어 (en)
echo    - 중국어 (zh)
echo    - 일본어 (ja)
echo.

pause 