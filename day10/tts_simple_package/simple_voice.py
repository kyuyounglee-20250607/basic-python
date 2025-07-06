#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 음성 출력 프로그램
tts_simple 패키지를 사용하여 문장과 언어를 받아 음성을 출력합니다.
자연스러운 여성 음성과 속도 조절 기능을 제공합니다.
"""

from tts_simple import SimpleTTS, Language, VoiceSpeed, speak_natural_korean, speak_natural_english, speak_natural_chinese, speak_natural_japanese

def speak_text(sentence, language="ko", natural=True):
    """
    문장과 언어를 받아서 음성으로 출력하는 함수
    
    Args:
        sentence (str): 음성으로 변환할 문장
        language (str): 언어 코드 (ko, en, zh, ja)
        natural (bool): 자연스러운 여성 음성 사용 여부 (기본값: True)
    
    Returns:
        bool: 성공 여부
    """
    # TTS 객체 생성
    tts = SimpleTTS()
    
    # 언어 코드 매핑
    language_map = {
        "ko": Language.KOREAN,
        "en": Language.ENGLISH,
        "zh": Language.CHINESE,
        "ja": Language.JAPANESE
    }
    
    # 언어 코드 확인 및 변환
    if language not in language_map:
        print(f"❌ 지원하지 않는 언어입니다: {language}")
        print("지원 언어: ko(한국어), en(영어), zh(중국어), ja(일본어)")
        return False
    
    # 음성 속도 설정 (자연스러운 여성 음성)
    speed = VoiceSpeed.SLOW if natural else VoiceSpeed.NORMAL
    speed_text = "자연스러운 여성" if natural else "일반"
    
    # 음성 변환 및 재생
    print(f"🎤 '{sentence}' (언어: {language}, 음성: {speed_text})")
    success = tts.speak(sentence, language=language_map[language], speed=speed)
    
    if success:
        print("✅ 음성 출력 완료!")
    else:
        print("❌ 음성 출력 실패!")
    
    return success

def speak_natural_voice(sentence, language="ko"):
    """
    자연스러운 여성 음성으로 문장을 출력하는 함수
    
    Args:
        sentence (str): 음성으로 변환할 문장
        language (str): 언어 코드 (ko, en, zh, ja)
    
    Returns:
        bool: 성공 여부
    """
    # 자연스러운 여성 음성 전용 함수들 사용
    natural_functions = {
        "ko": speak_natural_korean,
        "en": speak_natural_english,
        "zh": speak_natural_chinese,
        "ja": speak_natural_japanese
    }
    
    if language not in natural_functions:
        print(f"❌ 지원하지 않는 언어입니다: {language}")
        print("지원 언어: ko(한국어), en(영어), zh(중국어), ja(일본어)")
        return False
    
    print(f"🎤 자연스러운 여성 음성: '{sentence}' (언어: {language})")
    success = natural_functions[language](sentence)
    
    if success:
        print("✅ 자연스러운 음성 출력 완료!")
    else:
        print("❌ 음성 출력 실패!")
    
    return success

# 사용 예시
if __name__ == "__main__":
    print("🎵 간단한 음성 출력 프로그램 (자연스러운 여성 음성)")
    print("=" * 50)
    
    # 예시 1: 자연스러운 한국어 여성 음성
    print("\n1. 자연스러운 한국어 여성 음성:")
    speak_natural_voice("안녕하세요! 오늘 날씨가 정말 좋네요.", "ko")
    
    # 예시 2: 자연스러운 영어 여성 음성
    print("\n2. 자연스러운 영어 여성 음성:")
    speak_natural_voice("Hello! The weather is really nice today.", "en")
    
    # 예시 3: 자연스러운 중국어 여성 음성
    print("\n3. 자연스러운 중국어 여성 음성:")
    speak_natural_voice("你好！今天天气真好。", "zh")
    
    # 예시 4: 자연스러운 일본어 여성 음성
    print("\n4. 자연스러운 일본어 여성 음성:")
    speak_natural_voice("こんにちは！今日は天気がとても良いです。", "ja")
    
    # 사용자 입력 받기
    print("\n" + "-" * 50)
    print("직접 테스트해보세요!")
    
    while True:
        sentence = input("\n음성으로 변환할 문장을 입력하세요 (종료: q): ").strip()
        
        if sentence.lower() == 'q':
            print("👋 프로그램을 종료합니다!")
            break
        
        if not sentence:
            print("❌ 문장을 입력해주세요.")
            continue
        
        print("언어를 선택하세요:")
        print("1. 한국어 (ko)")
        print("2. 영어 (en)")
        print("3. 중국어 (zh)")
        print("4. 일본어 (ja)")
        
        choice = input("선택 (1-4): ").strip()
        
        language_map = {
            "1": "ko",
            "2": "en", 
            "3": "zh",
            "4": "ja"
        }
        
        if choice in language_map:
            # 자연스러운 여성 음성으로 출력
            speak_natural_voice(sentence, language_map[choice])
        else:
            print("❌ 잘못된 선택입니다. 기본값(한국어)으로 실행합니다.")
            speak_natural_voice(sentence, "ko") 