@echo off
echo ========================================
echo 고성능 TTS 패키지 설치 스크립트
echo ========================================
echo.

echo 🎵 TTS 패키지 설치를 시작합니다...
echo.

echo 1. pip 업그레이드 중...
python -m pip install --upgrade pip
echo.

echo 2. 필수 라이브러리 설치 중...
echo.

echo - gTTS (Google Text-to-Speech) 설치...
pip install gtts
echo.

echo - pyttsx3 (Windows TTS) 설치...
pip install pyttsx3
echo.

echo - pygame (안정적인 음성 재생) 설치...
pip install pygame
echo.

echo - playsound (대안 음성 재생) 설치...
pip install playsound
echo.

echo ========================================
echo ✅ TTS 패키지 설치 완료!
echo ========================================
echo.

echo 📋 사용 가능한 프로그램:
echo.
echo 1. TTS 패키지 메인:
echo    python tts_package.py
echo.
echo 2. 간단한 사용법:
echo    python simple_tts.py
echo.
echo 3. 상세한 사용 예시:
echo    python tts_package_example.py
echo.
echo 4. 기존 프로그램들:
echo    python tts_program.py
echo    python tts_advanced.py
echo.

echo 🎯 빠른 시작:
echo    from tts_package import TTSPackage, VoiceGender
echo    tts = TTSPackage()
echo    tts.speak("안녕하세요!", gender=VoiceGender.MALE)
echo.

echo 📖 자세한 사용법은 README.md 파일을 참조하세요.
echo.

pause 