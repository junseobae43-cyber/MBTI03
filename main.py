import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="그 비스크 돌은 사랑을 한다 - 연애 시뮬레이션", 
    page_icon="🌸", 
    layout="centered"
)

# 2. 세션 상태 초기화 (게임 진행 데이터)
if "affection" not in st.session_state:
    st.session_state.affection = 50  # 초기 호감도 (0 ~ 100)
if "step" not in st.session_state:
    st.session_state.step = 1       # 현재 대화 단계

# 3. 외부 이미지 URL (레포지토리에 파일을 넣지 않아도 되는 링크 방식)
# 필요시 원하시는 다른 마린 이미지 URL로 언제든 교체 가능합니다.
IMG_HAPPY = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000"
IMG_BLUSH = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000"
IMG_SAD = "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1000"

# 4. 사이드바: 게임 정보 및 호감도 관리
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
# 5. 시나리오 및 표정 변화 로직
# ---------------------------------------------------------

# [단계 1] 첫 만남 -> 밝은 표정
if st.session_state.step == 1:
    st.image(IMG_HAPPY, caption="방과 후, 신나서 인사하는 마린", use_container_width=True)

    st.chat_message("assistant").write(
        "마린: 야~! 오늘 수업 진짜 지루했지 않냐? 방과 후에 옷 부자재 보러 가려고 했는데, 너 혹시 시간 있어?"
    )

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

# [단계 2] 수락 시 -> 부끄러운/설레는 표정
elif st.session_state.step == 2:
    st.image(IMG_BLUSH, caption="얼굴을 붉히며 기뻐하는 마린", use_container_width=True)

    st.chat_message("assistant").write(
        "마린: 진짜?! 대박, 고마워! 사실 이번 코스프레 의상 재료 진짜 고민이었거든. 네가 골라주면 더 잘 될 것 같아!"
    )

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

# [단계 3] 거절 시 -> 시무룩한 표정
elif st.session_state.step == 3:
    st.image(IMG_SAD, caption="아쉬워하며 시무룩해진 마린", use_container_width=True)

    st.chat_message("assistant").write(
        "마린: 앗... 그렇구나. 엄청 피곤해 보이긴 했어! 그럼 어쩔 수 없지, 혼자 다녀올게. 조심히 들어가!"
    )

    if st.button("다음날 학교에서 다시 말걸기"):
        st.session_state.step = 4
        st.rerun()

# [단계 4] 엔딩 (호감도 결과에 따른 최종 표정)
elif st.session_state.step == 4:
    st.subheader("🎬 엔딩")

    if st.session_state.affection >= 80:
        st.image(IMG_BLUSH, caption="수줍게 웃는 마린", use_container_width=True)
        st.success("🎉 **해피 엔딩: 특별한 관계로!**")
        st.write("마린이 얼굴을 붉히며 당신의 옷소매를 살짝 잡습니다.")
        st.write("마린: '너랑 같이 있으니까 진짜 재미있다... 다음 주말에도 나랑 놀아줄래?'")
    elif st.session_state.affection >= 50:
        st.image(IMG_HAPPY, caption="밝게 인사하는 마린", use_container_width=True)
        st.info("😊 **노멀 엔딩: 좋은 친구 사이**")
        st.write("마린이 밝은 미소로 손을 흔들며 인사합니다.")
        st.write("마린: '오늘 재미있었어! 내일 학교에서 또 보자!'")
    else:
        st.image(IMG_SAD, caption="서먹해진 마린", use_container_width=True)
        st.error("💔 **배드 엔딩: 서먹해진 사이**")
        st.write("마린이 어색하게 미소 지으며 시선을 피합니다.")
        st.write("마린: '아, 응... 그럼 나 먼저 가볼게.'")
