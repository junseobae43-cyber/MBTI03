import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="💖 마린과 나의 비스크 돌 러브스토리",
    page_icon="🎀",
    layout="centered"
)

# 2. 커스텀 CSS (미연시 스타일 UI)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #ffdee9 0%, #b5fffc 100%);
        font-family: 'Pretendard', sans-serif;
    }
    
    .dialogue-box {
        background-color: rgba(255, 255, 255, 0.95);
        border: 4px solid #ff6b81;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(255, 107, 129, 0.3);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    .character-name {
        font-size: 1.3rem;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(45deg, #ff4757, #ff6b81);
        padding: 6px 18px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    .dialogue-text {
        font-size: 1.15rem;
        color: #2f3542;
        line-height: 1.7;
        font-weight: 500;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: white !important;
        font-size: 1.05rem !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: 2px solid #ffffff !important;
        padding: 12px !important;
        margin-top: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 마린 이미지 DB
MARIN_IMAGES = {
    "happy": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=800&auto=format&fit=crop",
    "excited": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=800&auto=format&fit=crop",
    "blush": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=800&auto=format&fit=crop",
    "heart": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=800&auto=format&fit=crop"
}

# 4. 세션 상태 관리 (에러 방지용 안전 재실행 함수 포함)
if "scene" not in st.session_state:
    st.session_state.scene = 0
if "affection" not in st.session_state:
    st.session_state.affection = 0

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def next_scene(scene_id, points=0):
    st.session_state.scene = scene_id
    st.session_state.affection += points
    safe_rerun()

def restart_game():
    st.session_state.scene = 0
    st.session_state.affection = 0
    safe_rerun()

# 5. 헤더 및 호감도 표시
st.title("🎀 그 비스크 돌은 사랑을 한다 💖")
st.caption("~ 키타가와 마린과의 방과 후 코스프레 로맨스 ~")

affection_score = min(st.session_state.affection, 100)
st.progress(affection_score / 100)
st.write(f"❤️ **마린과의 호감도:** `{affection_score} / 100` Point")
st.write("---")

# 6. 장면 분기 및 스토리 진행
scene = st.session_state.scene

# [장면 0: 오프닝]
if scene == 0:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["happy"], caption="✨ 마린과의 만남", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "야호~! 기다리고 있었다고! 💕<br><br>
                저기 있잖아... 지난번에 얘기했던 <b>그 캐릭터 코스프레 의상</b> 말인데...<br>
                치수 재는 거 오늘 바로 도와줄 수 있어? 🥺"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 당연하지! 마린이 입을 의상인데 완벽하게 만들어줄게."):
            next_scene(1, 30)
        if st.button("💬 음... 조금 부끄러운데 괜찮을까?"):
            next_scene(2, 20)

# [장면 1: 의상 제작 약속]
elif scene == 1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["excited"], caption="🔥 감동받은 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "꺄앗-! 진짜?! 역시 너 최고야 대박-!! 😭✨<br><br>
                네가 만드는 의상은 디테일이 장난 아니잖아!<br>
                완성되면 <b>너한테 제일 먼저 입은 모습</b> 보여줄 거니까 기대해!"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 마린이 입으면 어떤 캐릭터든 진짜 잘 어울릴 거야."):
            next_scene(3, 30)
        if st.button("💬 빨리 완성해서 같이 행사 가자!"):
            next_scene(3, 40)

# [장면 2: 수줍은 치수 재기]
elif scene == 2:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["blush"], caption="😳 얼굴이 붉어진 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "앗... 부, 부끄럽다고...? 😳<br><br>
                바보야, 나도 살짝 쑥스럽지만... 너라면 상관없는걸!<br>
                자, 조심해서 치수 재 줘..."
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 (진지하게 조심스럽게 치수를 잰다)"):
            next_scene(3, 30)

# [장면 3: 고백 직전]
elif scene == 3:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["blush"], caption="💌 진지한 표정의 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "...저기 있잖아.<br><br>
                항상 내 억지 다 들어주고, 이렇게 같이 있어서 고마워.<br>
                근데 나 말이지... 요즘엔 <b>너랑 함께 있는 시간</b>이 더 기다려져."
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("❤️ 나도 그래 마린, 계속 좋아하고 있었어."):
            next_scene(4, 40)
        if st.button("🍦 그럼 이번 주말에 둘이서 첫 데이트 하러 갈래?"):
            next_scene(5, 30)

# [장면 4: 엔딩 A - 고백 성공]
elif scene == 4:
    st.balloons()
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["heart"], caption="💖 행복해하는 마린", use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "진짜로...?! 🥺❤️ 대박, 나 울 것 같아!!<br><br>
                좋아해! 엄청 엄청 좋아해!<br>
                앞으로 <b>내 마음도 전부 네가 독점하는 거다?!</b> 💕"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"🎉 **HAPPY ENDING 1: 찰떡궁합 커플!** (호감도: {st.session_state.affection})")
        if st.button("🔄 처음부터 다시 하기"):
            restart_game()

# [장면 5: 엔딩 B - 데이트 약속]
elif scene == 5:
    st.snow()
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["happy"], caption="🌟 설레는 마린", use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "좋았어! 주말 데이트 결정이다~! 🍦✨<br><br>
                맛있는 것도 먹고, 쇼핑도 가자!<br>
                나 완전 제일 예쁘게 꾸미고 나올 테니까 각오해? 😉"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"🎉 **HAPPY ENDING 2: 첫 데이트 약속!** (호감도: {st.session_state.affection})")
        if st.button("🔄 처음부터 다시 하기"):
            restart_game()
