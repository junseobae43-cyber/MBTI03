import io
from gtts import gTTS
import streamlit as st

# (기존 상단 설정 및 이미지 URL 변수 부분)
# ...

# 일본어 텍스트를 음성으로 재생하는 함수 정의
def play_voice(text):
    # gTTS를 사용해 일본어(ja) 음성 생성
    tts = gTTS(text=text, lang="ja")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    # Streamlit 오디오 플레이어로 자동 재생 설정
    st.audio(fp, format="audio/mp3", autoplay=True)


# --- 화면 출력 부분 ---
st.title("🌸 방과 후 교실에서")

# 1. 이미지 표시 (기존 파일명)
st.image("Gemini_Generated_Image_jc1x4pjc1x4pjc1x.png")

# 2. 마린 대사 설정 (일본어 & 한국어 번역)
marine_dialogue_ja = (
    "ねえねえ！今日の授業めっちゃ退屈じゃなかった？放課後, 資材 보러 가려고 했는데, 너 혹시 시간 있어?"
)
marine_dialogue_kr = "마린: 야야! 오늘 수업 진짜 지루했지 않아? 방과 후에 옷 부자재 보러 가려고 했는데, 너 혹시 시간 있어?"

# 3. 마린 대사 출력 및 목소리 재생
st.write(marine_dialogue_kr)
play_voice(marine_dialogue_ja)
