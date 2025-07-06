#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 TTS 패키지 사용 예시
"""

from tts_simple import SimpleTTS, Language, speak_korean, speak_english, speak_chinese, speak_japanese

def main():
    """메인 예시 함수"""
    print("🎵 간단한 TTS 패키지 사용 예시")
    print("=" * 40)
    
    # 1. 기본 사용법
    print("\n1️⃣ 기본 사용법:")
    tts = SimpleTTS()
    
    # 한국어
    print("   🇰🇷 한국어: 안녕하세요!")
    tts.speak("안녕하세요!", language=Language.KOREAN)
    
    # 영어
    print("   🇺🇸 영어: Hello!")
    tts.speak("Hello!", language=Language.ENGLISH)
    
    # 중국어
    print("   🇨🇳 중국어: 你好！")
    tts.speak("你好！", language=Language.CHINESE)
    
    # 일본어
    print("   🇯🇵 일본어: こんにちは！")
    tts.speak("こんにちは！", language=Language.JAPANESE)
    
    # 2. 편의 함수 사용
    print("\n2️⃣ 편의 함수 사용:")
    
    print("   🇰🇷 한국어 편의 함수:")
    speak_korean("안녕하세요! 편의 함수로 음성 변환합니다.")
    
    print("   🇺🇸 영어 편의 함수:")
    speak_english("Hello! This is using convenience function.")
    
    print("   🇨🇳 중국어 편의 함수:")
    speak_chinese("你好！这是使用便利函数。")
    
    print("   🇯🇵 일본어 편의 함수:")
    speak_japanese("こんにちは！これは便利関数を使用しています。")
    
    # 3. 파일 저장 예시
    print("\n3️⃣ 파일 저장 예시:")
    
    # 한국어 파일 저장
    print("   🇰🇷 한국어 파일 저장:")
    tts.speak(
        "이 음성은 파일로 저장됩니다.",
        language=Language.KOREAN,
        save_to_file=True,
        filename="korean_example.mp3"
    )
    
    # 영어 파일 저장
    print("   🇺🇸 영어 파일 저장:")
    tts.speak(
        "This voice will be saved to a file.",
        language=Language.ENGLISH,
        save_to_file=True,
        filename="english_example.mp3"
    )
    
    # 4. 일괄 처리 예시
    print("\n4️⃣ 일괄 처리 예시:")
    
    korean_texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다."
    ]
    
    print("   연속으로 3개 문장을 처리합니다...")
    tts.batch_speak(korean_texts, language=Language.KOREAN, delay_between=2.0)
    
    # 5. 외부 텍스트 입력 예시
    print("\n5️⃣ 외부 텍스트 입력 예시:")
    
    # 사용자 입력 받기
    user_text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
    
    if user_text:
        print("언어를 선택하세요:")
        print("1. 한국어")
        print("2. 영어")
        print("3. 중국어")
        print("4. 일본어")
        
        choice = input("선택 (1-4): ").strip()
        
        if choice == "1":
            speak_korean(user_text)
        elif choice == "2":
            speak_english(user_text)
        elif choice == "3":
            speak_chinese(user_text)
        elif choice == "4":
            speak_japanese(user_text)
        else:
            print("기본값으로 한국어로 변환합니다.")
            speak_korean(user_text)
    else:
        print("텍스트가 입력되지 않았습니다.")
    
    print("\n🎉 예시 완료!")

if __name__ == "__main__":
    main() 