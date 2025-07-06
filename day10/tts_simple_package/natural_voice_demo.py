#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자연스러운 여성 음성 데모 프로그램
tts_simple 패키지의 자연스러운 여성 음성 기능을 시연합니다.
"""

from tts_simple import (
    speak_natural_korean, speak_natural_english, speak_natural_chinese, speak_natural_japanese,
    VoiceSpeed, SimpleTTS, Language
)

def demo_natural_female_voice():
    """자연스러운 여성 음성 데모"""
    print("🎵 자연스러운 여성 음성 데모")
    print("=" * 50)
    print("Google TTS의 자연스러운 여성 음성을 시연합니다.")
    print("느린 속도(slow=True)로 더 자연스러운 발음을 제공합니다.")
    print()
    
    # 1. 한국어 자연스러운 여성 음성
    print("🇰🇷 한국어 자연스러운 여성 음성:")
    print("텍스트: '안녕하세요! 오늘은 정말 좋은 날씨네요.'")
    speak_natural_korean("안녕하세요! 오늘은 정말 좋은 날씨네요.")
    print()
    
    # 2. 영어 자연스러운 여성 음성
    print("🇺🇸 영어 자연스러운 여성 음성:")
    print("Text: 'Hello! The weather is really nice today.'")
    speak_natural_english("Hello! The weather is really nice today.")
    print()
    
    # 3. 중국어 자연스러운 여성 음성
    print("🇨🇳 중국어 자연스러운 여성 음성:")
    print("文本: '你好！今天天气真好。'")
    speak_natural_chinese("你好！今天天气真好。")
    print()
    
    # 4. 일본어 자연스러운 여성 음성
    print("🇯🇵 일본어 자연스러운 여성 음성:")
    print("テキスト: 'こんにちは！今日は天気がとても良いです。'")
    speak_natural_japanese("こんにちは！今日は天気がとても良いです。")
    print()

def compare_voice_speeds():
    """음성 속도 비교 데모"""
    print("🔄 음성 속도 비교 데모")
    print("=" * 50)
    
    tts = SimpleTTS()
    test_text = "안녕하세요! 이것은 음성 속도 비교 테스트입니다."
    
    # 일반 속도
    print("1️⃣ 일반 속도 (VoiceSpeed.NORMAL):")
    tts.speak(test_text, language=Language.KOREAN, speed=VoiceSpeed.NORMAL)
    print()
    
    # 자연스러운 속도
    print("2️⃣ 자연스러운 속도 (VoiceSpeed.SLOW):")
    tts.speak(test_text, language=Language.KOREAN, speed=VoiceSpeed.SLOW)
    print()

def interactive_natural_voice():
    """대화형 자연스러운 음성 테스트"""
    print("🎮 대화형 자연스러운 음성 테스트")
    print("=" * 50)
    
    while True:
        print("\n옵션 선택:")
        print("1. 한국어 자연스러운 여성 음성")
        print("2. 영어 자연스러운 여성 음성")
        print("3. 중국어 자연스러운 여성 음성")
        print("4. 일본어 자연스러운 여성 음성")
        print("5. 음성 속도 비교")
        print("6. 종료")
        print("-" * 30)
        
        choice = input("선택하세요 (1-6): ").strip()
        
        if choice == "1":
            text = input("한국어 텍스트를 입력하세요: ").strip()
            if text:
                speak_natural_korean(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "2":
            text = input("영어 텍스트를 입력하세요: ").strip()
            if text:
                speak_natural_english(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "3":
            text = input("중국어 텍스트를 입력하세요: ").strip()
            if text:
                speak_natural_chinese(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "4":
            text = input("일본어 텍스트를 입력하세요: ").strip()
            if text:
                speak_natural_japanese(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "5":
            compare_voice_speeds()
        
        elif choice == "6":
            print("👋 자연스러운 음성 데모를 종료합니다!")
            break
        
        else:
            print("❌ 잘못된 선택입니다.")

def main():
    """메인 함수"""
    print("🎵 자연스러운 여성 음성 TTS 데모 프로그램")
    print("=" * 60)
    print()
    
    # 1. 자연스러운 여성 음성 데모
    demo_natural_female_voice()
    
    # 2. 음성 속도 비교
    compare_voice_speeds()
    
    # 3. 대화형 테스트
    demo_choice = input("\n대화형 자연스러운 음성 테스트를 실행하시겠습니까? (y/n): ").strip().lower()
    if demo_choice == 'y':
        interactive_natural_voice()
    
    print("\n🎉 자연스러운 여성 음성 데모 완료!")
    print("\n💡 팁:")
    print("- VoiceSpeed.SLOW를 사용하면 더 자연스러운 발음을 얻을 수 있습니다.")
    print("- Google TTS는 기본적으로 여성 음성을 제공합니다.")
    print("- 느린 속도는 발음이 더 명확하고 자연스럽습니다.")

if __name__ == "__main__":
    main() 