#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 패키지 테스트 - 문제 진단
"""

def test_import():
    """import 테스트"""
    print("🔍 Import 테스트 중...")
    
    try:
        from tts_package import TTSPackage, VoiceGender, VoiceLanguage
        print("✅ Import 성공!")
        return True
    except Exception as e:
        print(f"❌ Import 실패: {e}")
        return False

def test_voice_gender():
    """VoiceGender 테스트"""
    print("\n🔍 VoiceGender 테스트 중...")
    
    try:
        from tts_package import VoiceGender
        print(f"✅ VoiceGender.MALE: {VoiceGender.MALE}")
        print(f"✅ VoiceGender.FEMALE: {VoiceGender.FEMALE}")
        print(f"✅ VoiceGender.AUTO: {VoiceGender.AUTO}")
        return True
    except Exception as e:
        print(f"❌ VoiceGender 테스트 실패: {e}")
        return False

def test_voice_language():
    """VoiceLanguage 테스트"""
    print("\n🔍 VoiceLanguage 테스트 중...")
    
    try:
        from tts_package import VoiceLanguage
        print(f"✅ VoiceLanguage.KOREAN: {VoiceLanguage.KOREAN}")
        print(f"✅ VoiceLanguage.ENGLISH: {VoiceLanguage.ENGLISH}")
        return True
    except Exception as e:
        print(f"❌ VoiceLanguage 테스트 실패: {e}")
        return False

def test_tts_package_creation():
    """TTSPackage 생성 테스트"""
    print("\n🔍 TTSPackage 생성 테스트 중...")
    
    try:
        from tts_package import TTSPackage
        tts = TTSPackage()
        print("✅ TTSPackage 생성 성공!")
        return tts
    except Exception as e:
        print(f"❌ TTSPackage 생성 실패: {e}")
        return None

def test_basic_speak(tts):
    """기본 음성 변환 테스트"""
    print("\n🔍 기본 음성 변환 테스트 중...")
    
    try:
        result = tts.speak("안녕하세요! 기본 테스트입니다.")
        print(f"✅ 기본 음성 변환 결과: {result}")
        return result
    except Exception as e:
        print(f"❌ 기본 음성 변환 실패: {e}")
        return False

def test_male_voice(tts):
    """남성 음성 테스트"""
    print("\n🔍 남성 음성 테스트 중...")
    
    try:
        from tts_package import VoiceGender
        result = tts.speak("안녕하세요! 남성 음성 테스트입니다.", gender=VoiceGender.MALE)
        print(f"✅ 남성 음성 변환 결과: {result}")
        return result
    except Exception as e:
        print(f"❌ 남성 음성 변환 실패: {e}")
        return False

def test_female_voice(tts):
    """여성 음성 테스트"""
    print("\n🔍 여성 음성 테스트 중...")
    
    try:
        from tts_package import VoiceGender
        result = tts.speak("안녕하세요! 여성 음성 테스트입니다.", gender=VoiceGender.FEMALE)
        print(f"✅ 여성 음성 변환 결과: {result}")
        return result
    except Exception as e:
        print(f"❌ 여성 음성 변환 실패: {e}")
        return False

def test_english_voice(tts):
    """영어 음성 테스트"""
    print("\n🔍 영어 음성 테스트 중...")
    
    try:
        from tts_package import VoiceGender, VoiceLanguage
        result = tts.speak(
            "Hello! This is an English voice test.",
            gender=VoiceGender.FEMALE,
            language=VoiceLanguage.ENGLISH
        )
        print(f"✅ 영어 음성 변환 결과: {result}")
        return result
    except Exception as e:
        print(f"❌ 영어 음성 변환 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🧪 TTS 패키지 문제 진단")
    print("=" * 50)
    
    # 1. Import 테스트
    if not test_import():
        print("\n❌ Import 문제가 있습니다. 라이브러리 설치를 확인하세요.")
        return
    
    # 2. VoiceGender 테스트
    if not test_voice_gender():
        print("\n❌ VoiceGender 문제가 있습니다.")
        return
    
    # 3. VoiceLanguage 테스트
    if not test_voice_language():
        print("\n❌ VoiceLanguage 문제가 있습니다.")
        return
    
    # 4. TTSPackage 생성 테스트
    tts = test_tts_package_creation()
    if not tts:
        print("\n❌ TTSPackage 생성 문제가 있습니다.")
        return
    
    # 5. 기능 테스트
    print("\n🎵 기능 테스트 시작...")
    
    test_basic_speak(tts)
    test_male_voice(tts)
    test_female_voice(tts)
    test_english_voice(tts)
    
    print("\n✅ 모든 테스트 완료!")

if __name__ == "__main__":
    main() 