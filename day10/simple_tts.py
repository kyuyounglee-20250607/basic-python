#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 TTS 사용법
가장 쉽고 빠른 방법으로 텍스트를 음성으로 변환합니다.
"""

from tts_package import TTSPackage, VoiceGender, VoiceLanguage

def simple_speak():
    """가장 간단한 음성 변환"""
    tts = TTSPackage()
    
    # 기본 사용법
    tts.speak("안녕하세요! 이것은 간단한 TTS 예시입니다.")

def male_voice():
    """남성 음성으로 변환"""
    tts = TTSPackage()
    tts.speak("안녕하세요! 이것은 남성 음성입니다.", gender=VoiceGender.MALE)

def female_voice():
    """여성 음성으로 변환"""
    tts = TTSPackage()
    tts.speak("안녕하세요! 이것은 여성 음성입니다.", gender=VoiceGender.FEMALE)

def save_to_file():
    """파일로 저장"""
    tts = TTSPackage()
    tts.speak(
        "이 음성은 파일로 저장됩니다.",
        gender=VoiceGender.MALE,
        save_to_file=True,
        filename="my_voice.mp3"
    )

def english_voice():
    """영어 음성"""
    tts = TTSPackage()
    tts.speak(
        "Hello! This is an English voice test.",
        gender=VoiceGender.FEMALE,
        language=VoiceLanguage.ENGLISH
    )

def multiple_sentences():
    """여러 문장 연속 변환"""
    tts = TTSPackage()
    
    texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다."
    ]
    
    tts.batch_speak(texts, gender=VoiceGender.AUTO)

if __name__ == "__main__":
    print("🎵 TTS 패키지 - 남성/여성 음성 및 다국어 예시")
    print("=" * 50)
    
    print("\n1. 남성 음성:")
    male_voice()
    
    print("\n2. 여성 음성:")
    female_voice()
    
    print("\n3. 영어 음성 (여성):")
    english_voice()
    
    print("\n4. 파일로 저장 (남성 음성):")
    save_to_file()
    
    print("\n5. 여러 문장 연속 변환:")
    multiple_sentences()
    
    print("\n✅ 모든 예시 완료!") 