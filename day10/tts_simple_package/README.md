# 🎵 간단한 TTS 패키지

가장 자연스러운 Google TTS 엔진을 사용한 간단하고 강력한 텍스트 음성 변환 패키지입니다.

## 🌟 특징

- **4개 언어 지원**: 한국어, 영어, 중국어, 일본어
- **가장 자연스러운 음성**: Google TTS 엔진 사용
- **안정적인 재생**: pygame 기반 안정적인 음성 재생
- **간단한 사용법**: 한 줄로 음성 변환 가능
- **파일 저장**: MP3 파일로 저장 가능
- **일괄 처리**: 여러 문장 연속 처리

## 🚀 설치

### 자동 설치
```bash
install.bat
```

### 수동 설치
```bash
pip install gtts pygame
```

## 📖 사용법

### 1. 기본 사용법

```python
from tts_simple import SimpleTTS, Language

# TTS 객체 생성
tts = SimpleTTS()

# 한국어 음성 변환
tts.speak("안녕하세요! 이것은 한국어 음성입니다.", language=Language.KOREAN)

# 영어 음성 변환
tts.speak("Hello! This is English voice.", language=Language.ENGLISH)

# 중국어 음성 변환
tts.speak("你好！这是中文语音。", language=Language.CHINESE)

# 일본어 음성 변환
tts.speak("こんにちは！これは日本語の音声です。", language=Language.JAPANESE)
```

### 2. 편의 함수 사용

```python
from tts_simple import speak_korean, speak_english, speak_chinese, speak_japanese

# 더 간단한 사용법
speak_korean("안녕하세요!")
speak_english("Hello!")
speak_chinese("你好！")
speak_japanese("こんにちは！")
```

### 3. 파일로 저장

```python
from tts_simple import SimpleTTS, Language

tts = SimpleTTS()

# 음성을 MP3 파일로 저장
tts.speak(
    text="이 음성은 파일로 저장됩니다.",
    language=Language.KOREAN,
    save_to_file=True,
    filename="my_voice.mp3"
)
```

### 4. 여러 문장 일괄 처리

```python
from tts_simple import SimpleTTS, Language

tts = SimpleTTS()

texts = [
    "첫 번째 문장입니다.",
    "두 번째 문장입니다.",
    "세 번째 문장입니다."
]

# 연속으로 음성 변환
tts.batch_speak(texts, language=Language.KOREAN, delay_between=1.5)
```

### 5. 빠른 변환

```python
from tts_simple import quick_speak, Language

# 빠른 음성 변환
quick_speak("안녕하세요!", Language.KOREAN)
quick_speak("Hello!", Language.ENGLISH)
```

## 📁 파일 구조

```
tts_simple_package/
├── tts_simple.py           # 메인 TTS 패키지
├── test_simple_tts.py      # 종합 테스트 파일
├── install.bat             # 설치 스크립트
└── README.md              # 이 파일
```

## 🧪 테스트

### 전체 테스트 실행
```bash
python test_simple_tts.py
```

### 개별 테스트
```python
# 한국어 테스트
from tts_simple import speak_korean
speak_korean("안녕하세요! 테스트입니다.")

# 영어 테스트
from tts_simple import speak_english
speak_english("Hello! This is a test.")
```

## 🌐 지원 언어

| 언어 | 코드 | 예시 |
|------|------|------|
| 한국어 | `ko` | "안녕하세요!" |
| 영어 | `en` | "Hello!" |
| 중국어 | `zh` | "你好！" |
| 일본어 | `ja` | "こんにちは！" |

## ⚙️ API 참조

### SimpleTTS 클래스

#### `__init__()`
TTS 객체를 초기화합니다.

#### `speak(text, language=Language.KOREAN, save_to_file=False, filename=None, play_audio=True)`
텍스트를 음성으로 변환하고 재생합니다.

**매개변수:**
- `text` (str): 변환할 텍스트
- `language` (str): 언어 코드 (기본값: 한국어)
- `save_to_file` (bool): 파일 저장 여부 (기본값: False)
- `filename` (str): 저장할 파일명
- `play_audio` (bool): 음성 재생 여부 (기본값: True)

**반환값:**
- `bool`: 성공 여부

#### `batch_speak(texts, language=Language.KOREAN, save_to_files=False, delay_between=1.0)`
여러 텍스트를 연속으로 음성 변환합니다.

**매개변수:**
- `texts` (list): 변환할 텍스트 리스트
- `language` (str): 언어 코드
- `save_to_files` (bool): 각각 파일로 저장 여부
- `delay_between` (float): 문장 간 대기 시간 (초)

### 편의 함수들

#### `speak_korean(text)`
한국어 음성 변환

#### `speak_english(text)`
영어 음성 변환

#### `speak_chinese(text)`
중국어 음성 변환

#### `speak_japanese(text)`
일본어 음성 변환

#### `quick_speak(text, language=Language.KOREAN)`
빠른 음성 변환

## 🔧 문제 해결

### 1. 라이브러리 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 라이브러리 재설치
pip install --upgrade gtts pygame
```

### 2. 음성 재생 오류
- 인터넷 연결 확인
- pygame 설치 확인
- 시스템 볼륨 확인

### 3. 언어 인식 오류
- 텍스트가 해당 언어로 올바르게 작성되었는지 확인
- 언어 코드가 정확한지 확인

## 📝 예시

### 기본 예시
```python
from tts_simple import SimpleTTS, Language

tts = SimpleTTS()

# 한국어
tts.speak("안녕하세요! 오늘 날씨가 정말 좋네요.", Language.KOREAN)

# 영어
tts.speak("Hello! The weather is really nice today.", Language.ENGLISH)

# 중국어
tts.speak("你好！今天天气真好。", Language.CHINESE)

# 일본어
tts.speak("こんにちは！今日は天気がとても良いです。", Language.JAPANESE)
```

### 파일 저장 예시
```python
from tts_simple import SimpleTTS, Language

tts = SimpleTTS()

# 여러 언어로 파일 저장
tts.speak("안녕하세요!", Language.KOREAN, save_to_file=True, filename="korean.mp3")
tts.speak("Hello!", Language.ENGLISH, save_to_file=True, filename="english.mp3")
tts.speak("你好！", Language.CHINESE, save_to_file=True, filename="chinese.mp3")
tts.speak("こんにちは！", Language.JAPANESE, save_to_file=True, filename="japanese.mp3")
```

### 일괄 처리 예시
```python
from tts_simple import SimpleTTS, Language

tts = SimpleTTS()

# 한국어 문장들
korean_texts = [
    "첫 번째 문장입니다.",
    "두 번째 문장입니다.",
    "세 번째 문장입니다."
]

# 연속으로 음성 변환
tts.batch_speak(korean_texts, language=Language.KOREAN, delay_between=2.0)
```

## ⚠️ 주의사항

1. **인터넷 연결**: Google TTS를 사용하므로 인터넷 연결이 필요합니다.
2. **사용량 제한**: Google TTS는 일일 사용량 제한이 있을 수 있습니다.
3. **텍스트 길이**: 너무 긴 텍스트는 분할하여 처리하는 것을 권장합니다.
4. **파일 저장**: MP3 파일은 현재 디렉토리에 저장됩니다.

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**즐거운 TTS 사용하세요! 🎵** 