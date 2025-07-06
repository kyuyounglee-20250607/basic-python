#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 패키지 사용 예시 - 남자/여자 음성 선택
고성능 TTS 패키지의 다양한 사용법을 보여줍니다.
"""

from tts_package import TTSPackage, VoiceGender, VoiceLanguage, quick_speak, demo_voices

def basic_usage_example():
    """기본 사용법 예시"""
    print("=" * 60)
    print("📖 기본 사용법 예시")
    print("=" * 60)
    
    # TTS 패키지 생성
    tts = TTSPackage()
    
    # 기본 음성 변환 (자동 성별 선택)
    print("\n1. 기본 음성 변환 (자동 성별):")
    tts.speak("안녕하세요! 이것은 기본 음성 변환 예시입니다.")
    
    # 남성 음성으로 변환
    print("\n2. 남성 음성으로 변환:")
    tts.speak("안녕하세요! 이것은 남성 음성입니다.", gender=VoiceGender.MALE)
    
    # 여성 음성으로 변환
    print("\n3. 여성 음성으로 변환:")
    tts.speak("안녕하세요! 이것은 여성 음성입니다.", gender=VoiceGender.FEMALE)

def language_examples():
    """다국어 사용 예시"""
    print("\n" + "=" * 60)
    print("🌍 다국어 사용 예시")
    print("=" * 60)
    
    tts = TTSPackage()
    
    # 한국어
    print("\n🇰🇷 한국어:")
    tts.speak("안녕하세요! 한국어 음성 테스트입니다.", 
              gender=VoiceGender.MALE, 
              language=VoiceLanguage.KOREAN)
    
    # 영어
    print("\n🇺🇸 영어:")
    tts.speak("Hello! This is an English voice test.", 
              gender=VoiceGender.FEMALE, 
              language=VoiceLanguage.ENGLISH)
    
    # 일본어
    print("\n🇯🇵 일본어:")
    tts.speak("こんにちは！これは日本語の音声テストです。", 
              gender=VoiceGender.MALE, 
              language=VoiceLanguage.JAPANESE)
    
    # 중국어
    print("\n🇨🇳 중국어:")
    tts.speak("你好！这是中文语音测试。", 
              gender=VoiceGender.FEMALE, 
              language=VoiceLanguage.CHINESE)

def file_saving_example():
    """파일 저장 예시"""
    print("\n" + "=" * 60)
    print("💾 파일 저장 예시")
    print("=" * 60)
    
    tts = TTSPackage()
    
    # MP3 파일로 저장
    print("\n1. MP3 파일로 저장:")
    success = tts.speak(
        text="이 음성은 MP3 파일로 저장됩니다.",
        gender=VoiceGender.MALE,
        save_to_file=True,
        filename="saved_voice.mp3",
        play_audio=True
    )
    
    if success:
        print("✅ 파일 저장 및 재생 완료!")
    
    # 여러 파일로 저장
    print("\n2. 여러 파일로 저장:")
    texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다."
    ]
    
    for i, text in enumerate(texts, 1):
        tts.speak(
            text=text,
            gender=VoiceGender.FEMALE if i % 2 == 0 else VoiceGender.MALE,
            save_to_file=True,
            filename=f"voice_{i}.mp3",
            play_audio=True
        )

def batch_processing_example():
    """일괄 처리 예시"""
    print("\n" + "=" * 60)
    print("🔄 일괄 처리 예시")
    print("=" * 60)
    
    tts = TTSPackage()
    
    # 여러 문장을 연속으로 처리
    texts = [
        "첫 번째 문장입니다. 남성 음성으로 변환됩니다.",
        "두 번째 문장입니다. 여성 음성으로 변환됩니다.",
        "세 번째 문장입니다. 다시 남성 음성으로 변환됩니다.",
        "네 번째 문장입니다. 마지막으로 여성 음성으로 변환됩니다."
    ]
    
    print("\n1. 연속 재생 (파일 저장 없음):")
    tts.batch_speak(
        texts=texts,
        gender=VoiceGender.AUTO,  # 자동으로 남성/여성 선택
        delay_between=1.5
    )
    
    print("\n2. 연속 재생 (파일 저장 포함):")
    tts.batch_speak(
        texts=texts,
        gender=VoiceGender.AUTO,
        save_to_files=True,
        delay_between=2.0
    )

def windows_tts_example():
    """Windows TTS 사용 예시"""
    print("\n" + "=" * 60)
    print("🖥️ Windows TTS 사용 예시")
    print("=" * 60)
    
    tts = TTSPackage()
    
    # Windows TTS 사용 (오프라인)
    print("\n1. Windows TTS - 남성 음성:")
    tts.speak(
        text="이것은 Windows TTS 남성 음성입니다.",
        gender=VoiceGender.MALE,
        use_google=False  # Windows TTS 사용
    )
    
    print("\n2. Windows TTS - 여성 음성:")
    tts.speak(
        text="이것은 Windows TTS 여성 음성입니다.",
        gender=VoiceGender.FEMALE,
        use_google=False  # Windows TTS 사용
    )

def quick_speak_example():
    """빠른 음성 변환 예시"""
    print("\n" + "=" * 60)
    print("⚡ 빠른 음성 변환 예시")
    print("=" * 60)
    
    # 간단한 사용법
    print("\n1. 기본 빠른 변환:")
    quick_speak("안녕하세요! 빠른 음성 변환입니다.")
    
    print("\n2. 남성 음성으로 빠른 변환:")
    quick_speak("안녕하세요! 남성 음성으로 빠른 변환입니다.", VoiceGender.MALE)
    
    print("\n3. 여성 음성으로 빠른 변환:")
    quick_speak("안녕하세요! 여성 음성으로 빠른 변환입니다.", VoiceGender.FEMALE)

def interactive_demo():
    """대화형 데모"""
    print("\n" + "=" * 60)
    print("🎮 대화형 TTS 데모")
    print("=" * 60)
    
    tts = TTSPackage()
    
    while True:
        print("\n" + "-" * 40)
        print("옵션 선택:")
        print("1. 텍스트 입력하여 음성 변환")
        print("2. 남성 음성으로 변환")
        print("3. 여성 음성으로 변환")
        print("4. 파일로 저장")
        print("5. Windows TTS 사용")
        print("6. 종료")
        print("-" * 40)
        
        choice = input("선택하세요 (1-6): ").strip()
        
        if choice == "1":
            text = input("음성으로 변환할 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "2":
            text = input("남성 음성으로 변환할 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, gender=VoiceGender.MALE)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "3":
            text = input("여성 음성으로 변환할 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, gender=VoiceGender.FEMALE)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "4":
            text = input("저장할 텍스트를 입력하세요: ").strip()
            if text:
                filename = input("파일명을 입력하세요 (기본: output.mp3): ").strip()
                if not filename:
                    filename = "output.mp3"
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
                
                tts.speak(text, save_to_file=True, filename=filename)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "5":
            text = input("Windows TTS로 변환할 텍스트를 입력하세요: ").strip()
            if text:
                gender = input("성별을 선택하세요 (male/female): ").strip().lower()
                if gender not in ['male', 'female']:
                    gender = VoiceGender.AUTO
                
                tts.speak(text, gender=gender, use_google=False)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "6":
            print("👋 데모를 종료합니다!")
            break
        
        else:
            print("❌ 잘못된 선택입니다.")

def main():
    """메인 함수"""
    print("🎵 TTS 패키지 사용 예시")
    print("=" * 60)
    
    # 사용 가능한 음성 확인
    tts = TTSPackage()
    voices = tts.get_available_voices()
    
    print("📋 사용 가능한 음성:")
    for engine, voice_list in voices.items():
        print(f"  {engine}: {len(voice_list)}개 음성")
        for voice in voice_list:
            print(f"    - {voice}")
    
    # 예시 실행
    basic_usage_example()
    language_examples()
    file_saving_example()
    batch_processing_example()
    windows_tts_example()
    quick_speak_example()
    
    # 대화형 데모
    demo_choice = input("\n대화형 데모를 실행하시겠습니까? (y/n): ").strip().lower()
    if demo_choice == 'y':
        interactive_demo()
    
    print("\n🎉 모든 예시 실행 완료!")

if __name__ == "__main__":
    main() 