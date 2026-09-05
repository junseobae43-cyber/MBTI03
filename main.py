import urllib.parse
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


# 3. 브라우저 차단을 우회하는 오디오 플레이어 함수
def play_voice_button(text, button_label="🔊 마린 목소리 듣기"):
    encoded_text = urllib.parse.quote(text)
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl=ja&client=tw-ob"

    # HTML audio 태그를 사용하여 플레이어 생성 (autoplay 제외)
    audio_html = f"""
        <audio controls style="width: 100%; height: 40px; margin-top: 10px;">
            <source src="{tts_url}" type="audio/mp3">
            브라우저가 오디오 재생을 지원하지 않습니다.
        </audio>
    """
    st.components.v1.html(audio_html, height=60)


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
    play_voice_button(jp_voice)

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
    play_voice_button(jp_voice)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 진지하게 꼼꼼하게 치수를 잰다."):
            st.session_state.affection += 15
            st.session_state.scene = "rooftop"
            st.rerun()
    with col2:
        if st.button("😳 부끄러워하며 어물쩡거린다."):
            st.session_state.affection -= 5
            st.session_state.scene = "rooftop"
            st.rerun()

# --- 장면 2-B: 부자재 상가 방문 ---
elif st.session_state.scene == "shop":
    st.subheader("📍 2장: 부자재 상가 데이트")
    st.image(IMG_HAPPY, caption="신나서 원단을 고르는 마린")

    jp_voice = "見て見て！この生地、めっちゃ質感良くない！？これで衣装作ったら絶対ヤバいって！"
    kr_text = "마린: 이것 좀 봐! 이 재질, 진짜 대박이지 않아?! 이걸로 의상 만들면 완전 대박일 거야!"

    st.markdown(f"**{kr_text}**")
    play_voice_button(jp_voice)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ 마린이 좋아하는 코스프레 이야기로 호응해준다."):
            st.session_state.affection += 20
            st.session_state.scene = "rooftop"
            st.rerun()
    with col2:
        if st.button("🥤 힘들어서 공차 마시러 가자고 한다."):
            st.session_state.affection += 5
            st.session_state.scene = "rooftop"
            st.rerun()

# --- 장면 3: 노을 지는 옥상 ---
elif st.session_state.scene == "rooftop":
    st.subheader("📍 3장: 노을 지는 학교 옥상")

    if st.session_state.affection >= 80:
        st.image(IMG_BLUSH, caption="노을 빛을 받으며 미소 짓는 마린")
        jp_voice = "あのね…私、君と衣装作ってる時が一番楽しいんだ。…これからも、ずっと隣にいてくれる？"
        kr_text = "마린: 있잖아... 나, 너랑 의상 만들 때가 제일 즐거워. ...앞으로도 계속 내 옆에 있어줄래?"

        st.markdown(f"**{kr_text}**")
        play_voice_button(jp_voice)

        if st.button("❤️ 마린에게 고백한다"):
            st.session_state.scene = "happy_ending"
            st.rerun()

    else:
        st.image(IMG_SAD, caption="아쉬운 표정의 마린")
        jp_voice = (
            "今日は楽しかったよ！…でも、なんだかちょっと寂しいな。また明日ね！"
        )
        kr_text = "마린: 오늘 즐거웠어! ...하지만 어쩐지 조금 아쉽네. 내일 또 봐!"

        st.markdown(f"**{kr_text}**")
        play_voice_button(jp_voice)

        if st.button("👋 인사를 나누고 집으로 간다"):
            st.session_state.scene = "normal_ending"
            st.rerun()

# --- 엔딩 화면 ---
elif st.session_state.scene == "happy_ending":
    st.balloons()
    st.success("🎉 **HAPPY ENDING: 마린과 연인이 되었습니다!**")
    st.image(IMG_BLUSH)
    st.write(
        "마린: 고마워! 앞으로도 코스프레 의상 많이 만들어줘, 내 전속 디자이너님! 💖"
    )

elif st.session_state.scene == "normal_ending":
    st.info("✉️ **NORMAL ENDING: 좋은 친구 사이로 남았습니다.**")
    st.image(IMG_SAD)
    st.write("마린과의 호감도를 더 올려서 해피 엔딩에 도전해보세요!")
