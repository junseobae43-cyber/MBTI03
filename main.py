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
st.sidebar.progress(st.session_state.affection / 100)
st.sidebar.write(f"**현재 호감도:** {st.session_state.affection} / 100")

if st.sidebar.button("🔄 처음부터 다시 시작"):
    st.session_state.affection = 50
    st.session_state.step = 1
    st.rerun()

st.title("🌸 방과 후 교실에서")

# ---------------------------------------------------------
# 시나리오 단계별 로직
# ---------------------------------------------------------

# [단계 1] 등교/방과 후 첫 만남
if st.session_state.step == 1:
    st.image(
        "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000", # 임시 이미지 (원하는 마린 이미지 URL로 변경 가능)
        caption="방과 후, 창가에 앉아있는 마린",
        use_container_width=True
    )
    
    st.chat_message("assistant").write("마린: 야~! 오늘 수업 진짜 지루했지 않냐? 방과 후에 옷 부자재 보러 동대문 가려고 했는데, 너 혹시 시간 있어?")
    
    # 음성 파일 재생 (원하는 mp3 파일 URL이나 로컬 경로로 교체 가능)
    # st.audio("https://example.com/marin_voice1.mp3") 

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
    st.image(
        "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000",
        caption="신나서 미소 짓는 마린",
        use_container_width=True
    )
    
    st.chat_message("assistant").write("마린: 진짜?! 대박, 고마워! 사실 이번에 만들 코스프레 의상 재료 진짜 고민이었거든. 네가 골라주면 더 잘 될 것 같아!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("1. 네 열정은 항상 멋져. 완벽하게 도와줄게!"):
            st.session_state.affection += 30
            st.session_state.step = 4
            st.
