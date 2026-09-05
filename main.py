import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="그 비스크 돌 - 키타가와 마린 연애 시뮬레이션",
    page_icon="🌸",
    layout="centered",
)

# 2. 이미지 파일 경로 설정 (저장소 내 이미지 파일명)
IMG_HAPPY = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x.png"
IMG_BLUSH = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x (1).png"
IMG_SAD = "Gemini_Generated_Image_jc1x4pjc1x4pjc1x (2).png"


# 3. Web Speech API (브라우저 내장 TTS) 기반 음성 재생 함수
def speak_js(text):
    js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.lang = 'ja-JP';
            msg.rate = 1.0;
            msg.pitch = 1.1; // 약간 높은 마린 톤
            window.speechSynthesis.cancel(); // 이전 음성 취소
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)


# 4. 게임 데이터 초기화
if "affection" not in st.session_state:
    st.session_state.affection = 50
if "scene" not in st.session_state:
    st.session_state.scene = "start"

# 5. 사이드바 - 호감도 및 상태
st.sidebar.title("🎮 게임 상태")
st.sidebar.subheader("키타가와 마린")
st.sidebar.progress(st.session_state.affection / 100)
st.sidebar.write(f"**연애 호감도:** {st.session_state.affection} / 100")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    st.session_state.affection = 50
    st.session_state.scene = "start"
    st.rerun()

# 6. 메인 스토리 진행
st.title("🌸 그 비스크 돌은 사랑을 한다")

# --- 장면 1: 시작 (방과 후 교실) ---
if st.session_state.scene == "start":
    st.subheader("📍 1장: 방과 후 교실")
    st.image(IMG_HAPPY, caption="방과 후, 당신에게 다가오는 마린")

    jp_voice = "ねえねえ！今日の授業めっちゃ退屈じゃなかった？放課後、資材見に行こうと思ってたんだけど、一緒に行く？"
    kr_text = "마린: 야야! 오늘 수업 진짜 지루했지 않아? 방과 후에 옷 부자재 보러 가려고 했는데, 너 혹시 같이 갈래?"

    st.markdown(f"**{kr_text}**")
    speak_js(jp_voice)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 좋아! 원단 상점 같이 가자."):
            st.session_state.affection += 15
            st.session_state.scene = "shop"
            st.rerun()
    with col2:
        if st.button("🏫 오늘은 가정실에서 의상 치수부터 재자."):
            st.session_state.affection += 10
            st.session_state.scene = "clubroom"
            st.rerun()

# --- 장면 2-A: 동아리실(가정실) 치수 재기 ---
elif st.session_state.scene == "clubroom":
    st.subheader("📍 2장: 방과 후 가정실")
    st.image(IMG_BLUSH, caption="얼굴이 붉어진 마린")

    jp_voice = "えっ…？サイズ測るの…？あ、うん！いいけど…ちょっと恥ずかしいかも…丁寧に測ってね？"
    kr_text = "마린: 에...? 치수 잰다고...? 아, 응! 괜찮긴 한데... 조금 부끄러울지도... 조심해서 재줘?"

    st.markdown(f"**{kr_text}**")
    speak_js(jp_voice)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 진지하게
