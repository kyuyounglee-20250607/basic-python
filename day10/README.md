# 🎵 텍스트 음성 변환 (TTS) 프로그램

윈도우 환경에서 무료로 사용할 수 있는 텍스트 음성 변환 프로그램입니다.

## 📋 기능

- **Google TTS**: 인터넷 연결 시 매우 자연스러운 음성 제공
- **Windows TTS**: 오프라인 사용 가능, 윈도우 기본 음성 엔진 사용
- **MP3 저장**: Google TTS로 변환한 음성을 MP3 파일로 저장
- **다국어 지원**: 한국어, 영어 등 다양한 언어 지원
- **사용자 친화적 인터페이스**: 직관적인 메뉴 시스템

## 🚀 설치 방법

### 1. 기본 라이브러리 설치

PowerShell이나 명령 프롬프트에서 다음 명령어를 실행하세요:

```bash
pip install gtts pyttsx3 playsound
```

### 2. 고급 기능 (안정적인 음성 재생)

연속 음성 재생 시 발생하는 자원 해제 문제를 해결하려면 pygame을 추가로 설치하세요:

```bash
pip install pygame
```

또는 자동 설치 스크립트를 사용하세요:
- `install_requirements.bat` - 기본 라이브러리 설치
- `install_advanced_requirements.bat` - 고급 라이브러리 포함 설치

### 3. 개별 라이브러리 설명

- **gTTS (Google Text-to-Speech)**: Google의 고품질 TTS 서비스
- **pyttsx3**: 윈도우 기본 TTS 엔진 사용
- **playsound**: 음성 파일 재생 (기본)
- **pygame**: 안정적인 음성 재생 (고급 기능)

## 📁 파일 구조

```
day10/
├── tts_package.py                    # 🆕 고성능 TTS 패키지 (남자/여자 음성 선택)
├── tts_package_example.py            # 🆕 패키지 사용 예시
├── simple_tts.py                     # 🆕 간단한 사용법
├── tts_program.py                    # 메인 TTS 프로그램
├── tts_advanced.py                   # 고급 TTS 프로그램 (pygame 사용)
├── tts_example.py                    # 사용 예시
├── test_tts.py                       # 테스트 프로그램
├── install_tts_package.bat           # 🆕 TTS 패키지 설치
├── install_requirements.bat          # 기본 라이브러리 설치
├── install_advanced_requirements.bat # 고급 라이브러리 설치
└── README.md                         # 이 파일
```

## 🎯 사용 방법

### 1. TTS 패키지 사용 (권장)

```bash
# 패키지 설치
install_tts_package.bat

# 간단한 사용법
python simple_tts.py

# 상세한 사용 예시
python tts_package_example.py

# 패키지 직접 사용
python tts_package.py
```

### 2. 기존 프로그램 실행

```bash
# 기본 프로그램
python tts_program.py

# 고급 프로그램 (안정적인 음성 재생)
python tts_advanced.py
```

### 2. 예시 프로그램 실행

```bash
python tts_example.py
```

### 3. 테스트 프로그램 실행

```bash
python test_tts.py
```

## 📖 프로그램 기능

### 🆕 TTS 패키지 (`tts_package.py`) - 권장

#### 주요 기능
1. **남자/여자 음성 선택**
   - `VoiceGender.MALE` - 남성 음성
   - `VoiceGender.FEMALE` - 여성 음성
   - `VoiceGender.AUTO` - 자동 선택

2. **다국어 지원**
   - 한국어, 영어, 일본어, 중국어
   - 각 언어별 남성/여성 음성 선택

3. **안정적인 음성 재생**
   - pygame 기반 안정적인 재생
   - 연속 재생 시 자원 해제 문제 해결

4. **파일 저장 및 일괄 처리**
   - MP3 파일로 저장
   - 여러 문장 연속 처리

#### 사용법
```python
from tts_package import TTSPackage, VoiceGender

# 패키지 생성
tts = TTSPackage()

# 남성 음성으로 변환
tts.speak("안녕하세요!", gender=VoiceGender.MALE)

# 여성 음성으로 변환
tts.speak("안녕하세요!", gender=VoiceGender.FEMALE)

# 파일로 저장
tts.speak("저장할 텍스트", gender=VoiceGender.MALE, save_to_file=True)
```

### 기존 프로그램

#### 기본 프로그램 (`tts_program.py`)
1. **Google TTS 사용**
   - 인터넷 연결 필요
   - 매우 자연스러운 음성
   - MP3 파일로 저장 가능

2. **Windows TTS 사용**
   - 오프라인 사용 가능
   - 윈도우 기본 음성 엔진
   - 실시간 음성 재생

3. **예시 문장 테스트**
   - 미리 준비된 예시 문장으로 테스트
   - 두 TTS 엔진 모두 테스트 가능

#### 고급 프로그램 (`tts_advanced.py`)
1. **pygame을 사용한 안정적인 음성 재생**
   - 연속 음성 재생 시 자원 해제 문제 해결
   - 여러 파일 연속 재생 가능
   - 더 안정적인 음성 재생

2. **playsound와 pygame 선택 가능**
   - 사용자가 원하는 재생 방식을 선택
   - 각각의 장단점 비교 가능

### 예시 프로그램 (`tts_example.py`)

- 간단한 Google TTS 사용법
- 간단한 Windows TTS 사용법
- 여러 문장 일괄 처리 예시

## 🔧 문제 해결

### 1. 라이브러리 설치 오류

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 기본 라이브러리 재설치
pip install --upgrade gtts pyttsx3 playsound

# 고급 기능을 위한 pygame 설치
pip install pygame
```

### 2. 음성 재생 오류

- **Windows TTS**: 윈도우 설정에서 음성 인식 기능 활성화
- **Google TTS**: 인터넷 연결 확인
- **연속 재생 오류**: pygame을 사용한 고급 프로그램 사용 권장

### 3. 한국어 음성 문제

- Windows TTS에서 한국어 음성이 없는 경우 영어 음성으로 대체
- Google TTS는 한국어를 완벽하게 지원

## 🌐 지원 언어

### Google TTS
- 한국어 (ko)
- 영어 (en)
- 일본어 (ja)
- 중국어 (zh)
- 기타 100개 이상의 언어

### Windows TTS
- 시스템에 설치된 음성에 따라 다름
- 한국어 음성 팩 설치 권장

## 📝 사용 예시

### Google TTS 사용

```python
from gtts import gTTS
from playsound import playsound

# 텍스트를 음성으로 변환
text = "안녕하세요! 이것은 TTS 예시입니다."
tts = gTTS(text=text, lang='ko', slow=False)

# MP3 파일로 저장
tts.save("output.mp3")

# 음성 재생
playsound("output.mp3")
```

### Windows TTS 사용

```python
import pyttsx3

# TTS 엔진 초기화
engine = pyttsx3.init()

# 음성 속도 설정
engine.setProperty('rate', 150)

# 텍스트를 음성으로 변환
text = "안녕하세요! 이것은 Windows TTS 예시입니다."
engine.say(text)
engine.runAndWait()
```

## ⚠️ 주의사항

1. **Google TTS**: 인터넷 연결이 필요하며, 일일 사용량 제한이 있을 수 있습니다.
2. **Windows TTS**: 시스템에 설치된 음성에 따라 품질이 달라집니다.
3. **음성 파일**: MP3 파일은 현재 디렉토리에 저장됩니다.
4. **연속 재생**: 여러 파일을 연속으로 재생할 때는 고급 프로그램(`tts_advanced.py`)을 사용하세요.

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**즐거운 TTS 사용하세요! 🎵** 