import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="그 비스크 돌은 사랑을 한다 - 연애 시뮬레이션", page_icon="🌸", layout="centered")

# 세션 상태 초기화
if "affection" not in st.session_state:
    st.session_state.affection = 50
if "step" not in st.session_state:
    st.session_state.step = 1

# 표정 이미지 경로 설정 (GitHub 레포지토리에 업로드한 파일명)
IMG_HAPPY = "marin_happy.png"
IMG_BLUSH = "marin_blush.png"
IMG_SAD = "marin_sad.png"

# 사이드바: 호감도 상태
st.sidebar.title("🎮 게임 상태")
st.sidebar.subheader("키타가와 마린")

st.session_state.affection = max(0, min(100, st.session_state.affection))
st.sidebar.progress(st.session_state.affection / 100)
st.sidebar.write(f"**현재 호감도:** {st.session_state.affection} / 100")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    st.session_state.affection = 50
    st.session_state.step = 1
    st.rerun()

st.title("🌸 방과 후 교실에서")

# ---------------------------------------------------------
# 시나리오 및 표정 변화 로직
# ---------------------------------------------------------

# [단계 1] 첫 만남 (기본/밝은 표정)
if st.session_state.step == 1:
    try:
        st.image(IMG_HAPPY, caption="방과 후 인사하는 마린")
    except Exception:
        st.info("🖼️ [밝게 웃는 마린]")

    st.chat_message("assistant").write("마린: 야~! 오늘 수업 진짜 지루했지 않냐? 방과 후에 옷 부자재 보러 가려고 했는데, 너 혹시 시간 있어?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. 당연히 있지! 같이 가자."):
            st.session_state.affection += 20
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("2. 미안, 오늘은 집에서 쉬고 싶어..."):
            st.session_state.affection -= 20
            st.session_state.step = 3
            st.rerun()

# [단계 2] 수락 시 (부끄러워하며 신나하는 표정)
elif st.session_state.step == 2:
    try:
        st.image(IMG_BLUSH, caption="얼굴을 붉히며 기뻐하는 마린")
    except Exception:
        st.info("🖼️ [부끄러워하는 마린]")

    st.chat_message("assistant").write("마린: 진짜?! 대박, 고마워! 사실 이번 코스프레 의상 재료 진짜 고민이었거든. 네가 골라주면 더 잘 될 것 같아!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. 네 열정은 항상 멋져. 완벽하게 도와줄게!"):
            st.session_state.affection += 30
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("2. 그냥 따라만 가는 거야, 너무 기대는 마."):
            st.session_state.affection -= 10
            st.session_state.step = 4
            st.rerun()

# [단계 3] 거절 시 (아쉬워하는 표정)
elif st.session_state.step == 3:
    try:
        st.image(IMG_SAD, caption="시무룩해진 마린")
    except Exception:
        st.info("🖼️ [시무룩한 마린]")

    st.chat_message("assistant").write("마린: 앗... 그렇구나. 엄청 피곤해 보이긴 했어! 그럼 어쩔 수 없지, 혼자 다녀올게. 조심히 들어가!")

    if st.button("다음날 학교에서 다시 말걸기"):
        st.session_state.step = 4
        st.rerun()

# [단계 4] 엔딩 (호감도에 따른 최종 표정 반영)
elif st.session_state.step == 4:
    st.subheader("🎬 결과")

    if st.session_state.affection >= 80:
        try:
            st.image(IMG_BLUSH, caption="수줍게 웃는 마린")
        except Exception:
            pass
        st.success("🎉 **해피 엔딩: 특별한 관계로!**")
        st.write("마린이 얼굴을 붉히며 당신의 소매를 살짝 잡습니다.")
        st.write("마린: '너랑 같이 있으니까 진짜 재미있다... 다음 주말에도 나랑 놀아줄래?'")
    elif st.session_state.affection >= 50:
        try:
            st.image(IMG_HAPPY, caption="밝게 인사하는 마린")
        except Exception:
            pass
        st.info("😊 **노멀 엔딩: 좋은 친구 사이**")
        st.write("마린이 손을 흔들며 밝게 인사합니다.")
        st.write("마린: '오늘 재미있었어! 내일 학교에서 또 보자!'")
    else:
        try:
            st.image(IMG_SAD, caption="서먹해진 마린")
        except Exception:
            pass
        st.error("💔 **배드 엔딩: 서먹해진 사이**")
        st.write("마린이 어색하게 미소 지으며 걸어 나갑니다.")
        st.write("마린: '아, 응... 그럼 나 먼저 가볼게.'")
