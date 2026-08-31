import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="💖 마린과 나의 비스크 돌 러브스토리",
    page_icon="🎀",
    layout="centered"
)

# 2. 미연시 스타일 Custom CSS
st.markdown("""
<style>
    /* 전체 배경 그라데이션 (핑크 톤) */
    .stApp {
        background: linear-gradient(180deg, #ffdee9 0%, #b5fffc 100%);
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 대화창 UI 카드가 느껴지는 스타일 */
    .dialogue-box {
        background-color: rgba(255, 255, 255, 0.95);
        border: 4px solid #ff6b81;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 10px 25px rgba(255, 107, 129, 0.3);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* 캐릭터 이름 태그 */
    .character-name {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(45deg, #ff4757, #ff6b81);
        padding: 6px 18px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* 대화 텍스트 */
    .dialogue-text {
        font-size: 1.2rem;
        color: #2f3542;
        line-height: 1.7;
        font-weight: 500;
    }

    /* 이미지 커스텀 테두리 */
    .stImage img {
        border-radius: 20px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }

    /* 선택지 버튼 스타일링 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border:
