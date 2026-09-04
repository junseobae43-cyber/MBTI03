import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="그 비스크 돌은 사랑을 한다 - 연애 시뮬레이션", page_icon="🌸", layout="centered")

# 세션 상태 초기화 (게임 진행 상황 저장)
if "affection" not in st.session_state:
    st.session_state.affection = 50  # 초기 호감도 (0 ~ 100)
if "step" not in st.session_state:
    st.session_state.step = 1       # 현재 대화 단계

# 사이드바: 게임 정보 및 호감도 표시
st.sidebar.title("🎮 게임 상태")
st.sidebar.subheader("키타가와 마린")

# 호감도 범위 제한 (0 ~ 100)
st.session_state.affection = max(0, min(100, st.session_state.affection))
st.sidebar.progress(st.session_state.affection / 100)
st.sidebar.write(f"**현재 호감도:** {st.session_state.affection} / 100")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    st.session_state.affection = 50
    st.session_state.step = 1
    st.rerun()

st.title("🌸 방과 후 교실에서")

# 이미지 경로 (GitHub 레포지토리에 marin.jpg 파일이 있을 경우 "marin.jpg"로 변경)
IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000"

# ---------------------------------------------------------
# 시나리오 단계별 로직
# ---------------------------------------------------------

# [단계 1] 등교/방과 후 첫 만남
if st.session_state.step == 1:
    try:
        st.image(IMAGE_URL, caption="방과 후, 창가에 앉아있는 마린")
    except Exception:
        st.info("🖼️ [마린의 모습]")
    
    st.chat_message("assistant").write("마린: 야~! 오늘 수업 진짜 지루했지 않냐? 방과 후에 옷 부자재 보러 동대문 가려고 했는데, 너 혹시 시간 있어?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. 당연히 있지! 같이 가자."):
            st.session_state.affection += 20
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("2. 미안, 오늘은 집에서 쉬고 싶어..."):
            st.session_state.affection -= 15
            st.session_state.step = 3
            st.rerun()

# [단계 2] 수락 시 (쇼핑/코스프레 이야기)
elif st.session_state.step == 2:
    try:
        st.image(IMAGE_URL, caption="신나서 미소 짓는 마린")
    except Exception:
        st.info("🖼️ [기뻐하는 마린]")
    
    st.chat_message("assistant").write("마린: 진짜?! 대박, 고마워! 사실 이번에 만들 코스프레 의상 재료 진짜 고민이었거든. 네가 골라주면 더 잘 될 것 같아!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. 네 열정은 항상 멋져. 완벽하게 도와줄게!"):
            st.session_state.affection += 30
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("2. 그냥 따라만 가는 거야, 기대는 하지 마."):
            st.session_state.affection -= 5
            st.session_state.step = 4
            st.rerun()

# [단계 3] 거절 시
elif st.session_state.step == 3:
    try:
        st.image(IMAGE_URL, caption="아쉬워하는 마린")
    except Exception:
        st.info("🖼️ [아쉬워하는 마린]")
    
    st.chat_message("assistant").write("마린: 앗... 그렇구나. 엄청 피곤해 보이긴 했어! 그럼 어쩔 수 없지, 혼자 다녀올게. 조심히 들어가!")

    if st.button("다음날 학교에서 다시 말걸기"):
        st.session_state.step = 4
        st.rerun()

# [단계 4] 엔딩 판정
elif st.session_state.step == 4:
    st.subheader("🎬 결과")
    
    if st.session_state.affection >= 80:
        st.success("🎉 **해피 엔딩: 특별한 관계로!**")
        st.write("마린이 당신의 손을 잡으며 얼굴을 붉힙니다.")
        st.write("마린: '너랑 같이 있으니까 진짜 재미있다... 다음 주말에도 같이 놀러 갈래?'")
    elif st.session_state.affection >= 50:
        st.info("😊 **노멀 엔딩: 좋은 친구 사이**")
        st.write("마린이 밝게 웃으며 인사합니다.")
        st.write("마린: '오늘 재미있었어! 내일 학교에서 또 봐!'")
    else:
        st.error
