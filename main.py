import urllib.parse
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="그 비스크 돌은 사랑을 한다 - 연애 시뮬레이션",
    page_icon="🌸",
    layout="centered",
)

# 2. 호감도 및 진행 상태 초기화
if "affection" not in st.session_state:
    st.session_state.affection = 50
if "step" not in st.session_state:
    st.session_state.step = 1

# 3. 마린 이미지 파일명 (저장소 내 이미지)
IMG_HAPPY = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x.png"
IMG_BLUSH = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x (1).png"
IMG_SAD = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x (2).png"


# 4. 일본어 음성 재생 함수 (Google Translate TTS 링크 활용)
def play_japanese_voice(text):
    encoded_text = urllib.parse.quote(text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl=ja&client=tw-ob"
    st.audio(tts_url, format="audio/mp3", autoplay=True)


# 5. 사이드바 - 호감도 표시
st.sidebar.title("🎮 게임 상태")
st.sidebar.subheader("키타가와 마린")
st.sidebar.progress(st.session_state.affection / 100)
st.sidebar.write(f"**연애 호감도:** {st.session_state.affection} / 100")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    st.session_state.affection = 50
    st.session_state.step = 1
    st.rerun()

# 6. 메인 화면 출력
st.title("🌸 방과 후 교실에서")

# 7. 대사 및 이미지 설정
japanese_text = "ねえねえ！今日の授業めっちゃ退屈じゃなかった？放課後、資材見に行こうと思ってたんだけど, 너 혹시 시간 있어?"
korean_text = "마린: 야야! 오늘 수업 진짜 지루했지 않아? 방과 후에 부자재 보러 가려고 했는데, 너 혹시 시간 있어?"

# 이미지 출력
st.image(IMG_HAPPY, caption="방과 후, 신나서 대화하는 마린")

# 대사 출력
st.markdown(f"**{korean_text}**")

# 일본어 음성 재생
play_japanese_voice("ねえねえ！今日の授業めっちゃ退屈じゃなかった？")

# 8. 선택지 버튼
st.subheader("선택지를 골라주세요:")
col1, col2 = st.columns(2)

with col1:
    if st.button("👍 좋아, 같이 가자!"):
        st.session_state.affection = min(100, st.session_state.affection + 10)
        st.success("마린이 기뻐합니다! (호감도 +10)")

with col2:
    if st.button("👎 미안, 오늘은 바빠..."):
        st.session_state.affection = max(0, st.session_state.affection - 10)
        st.error("마린이 아쉬워합니다... (호감도 -10)")
