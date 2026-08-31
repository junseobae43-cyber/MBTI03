import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="💖 마린과 나의 비스크 돌 러브스토리",
    page_icon="🎀",
    layout="centered"
)

# 2. 게임 커스텀 CSS (미소녀 연애 시뮬레이션 UI)
st.markdown("""
<style>
    /* 배경 그라데이션 */
    .stApp {
        background: linear-gradient(180deg, #ffdde1 0%, #ee9ca7 100%);
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 대화창 카드 스타일 (게임 메인 창) */
    .dialogue-box {
        background-color: rgba(255, 255, 255, 0.92);
        border: 4px solid #ff6b81;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(255, 107, 129, 0.4);
        margin-top: 10px;
    }
    
    /* 캐릭터 이름 태그 */
    .character-name {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ff4757;
        background-color: #ffeaa7;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    
    /* 대화 텍스트 */
    .dialogue-text {
        font-size: 1.2rem;
        color: #2f3542;
        line-height: 1.6;
        font-weight: 500;
    }

    /* 선택지 버튼 커스텀 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: 2px solid #ffffff !important;
        padding: 12px !important;
        margin-top: 5px !important;
        box-shadow: 0 5px 15px rgba(255, 117, 140, 0.4) !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# 3. 마린 반응별 이미지 DB (Unsplash 감성 고화질 이미지)
MARIN_IMAGES = {
    "happy": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=800&auto=format&fit=crop", # 밝은 미소
    "excited": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=800&auto=format&fit=crop", # 신남/코스프레 이야기
    "blush": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=800&auto=format&fit=crop", # 부끄러움/설렘
    "heart": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=800&auto=format&fit=crop"  # 심쿵/감동
}

# 4. 세션 상태 초기화 (게임 진행 상황 관리)
if "scene" not in st.session_state:
    st.session_state.scene = 0
if "affection" not in st.session_state:
    st.session_state.affection = 0

def next_scene(scene_id, points=0):
    st.session_state.scene = scene_id
    st.session_state.affection += points

def restart_game():
    st.session_state.scene = 0
    st.session_state.affection = 0

# 5. 게임 헤더 및 상태바
st.title("🎀 그 비스크 돌은 사랑을 한다 💖")
st.caption("~ 방과 후 의상실에서 마린과의 달달한 시간 ~")

# 호감도 게이지 표시
affection_score = min(st.session_state.affection, 100)
st.progress(affection_score / 100)
st.write(f"❤️ **마린과의 호감도:** `{affection_score} / 100` Point")
st.write("---")

# 6. 시나리오 분기 (비주얼 노벨 핵심 로직)
scene = st.session_state.scene

# [장면 0: 오프닝]
if scene == 0:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["happy"], caption="✨ 반짝거리는 눈으로 나를 바라보는 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "야호~! 오늘 방과 후에도 남아줘서 진짜 고마워!<br><br>
                저기 있잖아... 지난번에 부탁한 <b>새로운 코스프레 의상</b> 말인데, 혹시 작업은 잘 진행되어 가고 있어? 🥺"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 당연하지! 마린이 입을 의상인데 최선을 다해 만드는 중이야!"):
            next_scene(1, 20)
            st.rerun()
        if st.button("💬 음... 치수 재는 게 조금 까다로워서 아직 고민 중이야."):
            next_scene(2, 10)
            st.rerun()

# [장면 1: 의상 칭찬 route]
elif scene == 1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["excited"], caption="🔥 감동받아 흥분한 마린!", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "꺄앗-! 진짜?! 역시 너 최고야!! 😭✨<br><br>
                네가 만들어주는 의상은 진짜 캐릭터에 대한 사랑이 느껴진단 말이지...<br>
                있잖아, 완성되면 네 앞에서 <b>가장 먼저</b> 입고 보여줄게!"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 고마워 마린! 마린이 기뻐해 주니까 나도 너무 행복해."):
            next_scene(3, 30)
            st.rerun()
        if st.button("💬 얼른 입은 모습 보고 싶다. 마린한테 진짜 잘 어울릴 거야."):
            next_scene(3, 40)
            st.rerun()

# [장면 2: 치수 재기 route]
elif scene == 2:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["blush"], caption="😳 순간 당황해서 붉어진 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "아... 치수...! 😳 (얼굴이 살짝 붉어지며)<br><br>
                맞다, 핏을 딱 맞추려면 치수를 정확히 재야 하지...<br>
                그럼... 지금 바로 재볼래? 부끄럽지만 네 앞이라면 괜찮아!"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("💬 (조심스럽게 어깨와 허리 치수를 잰다)"):
            next_scene(3, 30)
            st.rerun()

# [장면 3: 클라이맥스 - 고백 전야]
elif scene == 3:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["blush"], caption="💌 붉어진 얼굴로 진지하게 바라보는 마린", use_container_width=True)
    with col2:
        st.markdown("""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "...저기 말야. 항상 내 멋대로인 요청 다 들어주고...<br><br>
                함께 코스프레할 수 있어서 진짜 매일매일이 꿈같아.<br>
                근데 있잖아, 난 이제 단순히 '코스프레 파트너' 이상으로... <b>너에 대해 알고 싶어.</b>"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("❤️ 나도 그래, 마린. 처음 본 순간부터 너를 좋아했어."):
            next_scene(4, 40)
            st.rerun()
        if st.button("🍦 그럼 이번 주말에 둘이서 첫 데이트 하러 갈래?"):
            next_scene(5, 30)
            st.rerun()

# [장면 4: 해피 엔딩 A - 고백 성공]
elif scene == 4:
    st.balloons()
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["heart"], caption="💖 최고의 해피 엔딩!", use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "거짓말...! 진짜로...?! 🥺❤️<br><br>
                아하하, 너무 행복해서 눈물 나올 것 같아!!<br>
                앞으로 내 코스프레 의상도, <b>그리고 내 마음도 평생 네가 독점해 줘! 사랑해!</b> 💕"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"🎉 **HAPPY ENDING 1: 찰떡궁합 연인 성립!** (최종 호감도: {st.session_state.affection})")
        if st.button("🔄 처음부터 다시 플레이하기"):
            restart_game()
            st.rerun()

# [장면 5: 해피 엔딩 B - 데이트 약속]
elif scene == 5:
    st.snow()
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(MARIN_IMAGES["happy"], caption="🌟 설렘 가득한 데이트 약속!", use_container_width=True)
    with col2:
        st.markdown(f"""
        <div class="dialogue-box">
            <div class="character-name">👑 키타가와 마린</div>
            <div class="dialogue-text">
                "좋아 좋아! 주말 데이트 확정~! 🍦✨<br><br>
                맛있는 파페도 먹고, 코스프레 재료도 새로 사러 가자!<br>
                나... 옷 엄청 예쁘게 입고 나올 테니까 기대해야 해?"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"🎉 **HAPPY ENDING 2: 달달한 첫 데이트!** (최종 호감도: {st.session_state.affection})")
        if st.button("🔄 처음부터 다시 플레이하기"):
            restart_game()
            st.rerun()
