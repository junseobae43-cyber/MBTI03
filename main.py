import streamlit as st
import time

# 1. 페이지 기본 설정 (가장 위에 배치)
st.set_page_config(
    page_title="✨ MBTI 진로 탐색 가이드 ✨",
    page_icon="🌈",
    layout="wide"
)

# 2. 커스텀 CSS (화려한 배경, 애니메이션, 카드 스타일링)
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 헤더 스타일링 */
    .main-title {
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        padding: 20px 0;
        animation: fadeIn 2s;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.3rem;
        color: #ffffff;
        margin-bottom: 30px;
        font-weight: 500;
    }

    /* 카드 스타일링 */
    .css-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .job-badge {
        display: inline-block;
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* 버튼 스타일링 */
    .stButton>button {
        background: linear-gradient(45deg, #4FACFE 0%, #00F2FE 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. MBTI 데이터베이스 (직업, 강점, 추천 환경)
mbti_db = {
    "INTJ": {
        "title": "🧠 용의주도한 전략가",
        "emoji": "🦅",
        "color": "🟣",
        "desc": "독립적이며 상상력이 풍부하고, 철저한 계획을 세우는 완벽주의자예요!",
        "jobs": ["💻 AI 연구원", "📊 데이터 분석가", "🏛️ 정책 기획자", "🧩 시스템 아키텍트", "🧪 과학자"],
        "strengths": ["💡 전략적 사고", "🎯 높은 집중력", "📐 논리적 문제 해결"],
        "advice": "혼자 몰입할 수 있고 지적 호기심을 자극하는 환경이 잘 맞아요!"
    },
    "INTP": {
        "title": "🔬 논리적인 사색가",
        "emoji": "🦉",
        "color": "🟣",
        "desc": "끊임없이 새로운 지식을 탐구하고 끊임없이 아이디어를 제안하는 원리원칙주의자예요!",
        "jobs": ["💻 소프트웨어 개발자", "📐 이론물리학자", "🔍 보안 전문가", "🎓 교수/연구원", "🎮 게임 디자이너"],
        "strengths": ["🔎 객관적 분석", "🌌 창의적 상상력", "📚 끊임없는 탐구"],
        "advice": "자율성이 보장되고 복잡한 문제를 해결하는 분야를 추천해요!"
    },
    "ENTJ": {
        "title": "👑 대담한 통솔자",
        "emoji": "🦁",
        "color": "🟣",
        "desc": "대담하고 상상력이 풍부하며, 강한 의지로 길을 개척하는 리더예요!",
        "jobs": ["💼 경영 컨설턴트", "🚀 스타트업 창업가", "⚖️ 변호사", "📈 투자 은행가", "🏛️ 정치인"],
        "strengths": ["📢 카리스마 리더십", "🎯 목표 지향성", "⚡ 결단력"],
        "advice": "팀을 이끌고 단체나 조직의 목표를 달성하는 직무에서 빛을 발해요!"
    },
    "ENTP": {
        "title": "💡 뜨거운 논쟁을 즐기는 변론가",
        "emoji": "🦊",
        "color": "🟣",
        "desc": "호기심이 많고 지적인 도전을 두려워하지 않는 모험가예요!",
        "jobs": ["📣 마케팅 기획자", "💡 벤처 투자자", "🎬 방송 PD", "🎙️ 시사 평론가", "🎨 기획 개발자"],
        "strengths": ["🔥 브레인스토밍", "🗣️ 설득력", "🔄 유연한 사고"],
        "advice": "변화가 무궁무진하고 새로운 아이디어를 마음껏 펼칠 수 있는 환경이 좋아요!"
    },
    "INFJ": {
        "title": "🔮 통찰력 있는 선의의 옹호자",
        "emoji": "🦄",
        "color": "🟢",
        "desc": "조용하고 신비로우며 샘솟는 영감으로 사람들에게 긍정적 영향을 주는 유형이에요!",
        "jobs": ["📑 심리상담사", "✍️ 작가/시인", "🩺 한의사", "🕊️ 인권 활동가", "🎨 아트 디렉터"],
        "strengths": ["❤️ 깊은 공감 능력", "👁️ 예리한 통찰력", "🌱 진정성"],
        "advice": "사람들의 성장을 돕고 세상을 더 나은 곳으로 만드는 가치 있는 일이 맞아요!"
    },
    "INFP": {
        "title": "🎨 잔망스러운 열정적인 중재자",
        "emoji": "🐰",
        "color": "🟢",
        "desc": "상냥하고 이타적이며, 나만의 이상적 세계를 꿈꾸는 낭만파예요!",
        "jobs": ["🎨 일러스트레이터", "📚 웹툰 작가", "🎵 음악 프로듀서", "🧸 아동 상담사", "📝 에세이스트"],
        "strengths": ["🌈 넘치는 풍부한 감수성", "💎 창의력", "🤝 따뜻한 이타심"],
        "advice": "개인의 신념과 창의성을 자유롭게 표현할 수 있는 환경이 최적이에요!"
    },
    "ENFJ": {
        "title": "☀️ 정의로운 사회운동가",
        "emoji": "🐬",
        "color": "🟢",
        "desc": "넘치는 카리스마와 열정으로 청중을 사로잡는 따뜻한 리더예요!",
        "jobs": ["👩‍🏫 교사/강사", "🤝 HR(인사) 전문가", "🎤 아나운서", "🎪 행사 기획자", "🏥 사회복지사"],
        "strengths": ["✨ 동기부여 능력", "💬 뛰어난 소통력", "💖 타인에 대한 배려"],
        "advice": "사람들과 깊게 교류하며 타인의 잠재력을 이끌어내는 교육/상담 직무를 추천해요!"
    },
    "ENFP": {
        "title": "🎈 재발랄한 활동가",
        "emoji": "🐶",
        "color": "🟢",
        "desc": "창의적이고 열정적이며, 에너지가 넘치고 웃음이 많은 아이디어 파티시엘!",
        "jobs": ["📹 크리에이터/유튜버", "🎨 광고 카피라이터", "✈️ 여행 가이드", "🎭 배우/엔터테이너", "🎉 이벤트 디렉터"],
        "strengths": ["⚡ 폭발적인 에너지를 바탕으로 한 친화력", "💡 마르지 않는 아이디어", "🌟 긍정 마인드"],
        "advice": "반복적이지 않고 재미있으며, 매일 새로운 사람과 만나는 일이 어울려요!"
    },
    "ISTJ": {
        "title": "🛡️ 청렴결백한 논리주의자",
        "emoji": "🐘",
        "color": "🔵",
        "desc": "실체적이고 두터운 원칙주의자로, 신뢰를 최우선으로 생각하는 현실주의자예요!",
        "jobs": ["📊 회계사/세무사", "🏛️ 공무원", "📑 데이터 관리자", "⚖️ 판사/검사", "🛡️ 품질 관리자"],
        "strengths": ["📐 철저한 정직함", "🔍 꼼꼼한 디테일", "🏛️ 강한 책임감"],
        "advice": "체계가 잘 잡혀있고 데이터와 규칙이 명확한 환경에서 최고의 성과를 내요!"
    },
    "ISFJ": {
        "title": "🌷 용감한 수호자",
        "emoji": "🐧",
        "color": "🔵",
        "desc": "소중한 사람들을 지키는 데 진심이며, 헌신적이고 따뜻한 수호자예요!",
        "jobs": ["👩‍⚕️ 간호사", "🏫 초등학교 교사", "📜 사서", "🍰 파티시에", "🏥 영양사"],
        "strengths": ["🤝 세심한 배려", "🛡️ 안정감 제공", "🎯 성실함"],
        "advice": "타인을 직접적으로 돕고 실질적인 지원을 제공하는 따뜻한 분위기가 맞아요!"
    },
    "ESTJ": {
        "title": "🏛️ 엄격한 관리자",
        "emoji": "🦅",
        "color": "🔵",
        "desc": "사물과 사람을 관리하는 데 뛰어난 능력을 발휘하는 도덕적 가이드예요!",
        "jobs": ["🏢 프로젝트 매니저(PM)", "👮 경찰/장교", "📈 금융 자산관리사", "🏭 공장 운영 관리자", "👨‍💼 경영자"],
        "strengths": ["📊 뛰어난 조직력", "⚡ 실천력", "🎯 명확한 목표 달성"],
        "advice": "명확한 규칙과 효율성을 바탕으로 체계적으로 팀을 관리하는 역할이 적합해요!"
    },
    "ESFJ": {
        "title": "🤝 사교적인 외교관",
        "emoji": "🦌",
        "color": "🔵",
        "desc": "타인에게 관심이 많고 친절하며, 항상 도울 준비가 되어있는 인싸형 수호자예요!",
        "jobs": ["✈️ 승무원", "🏨 호텔 지배인", "🩺 고객만족(CS) 팀장", "🤝 뷰티 컨설턴트", "💌 고객 관리자"],
        "strengths": ["😊 뛰어난 공감력", "🎉 분위기 메이커", "🤝 협동심"],
        "advice": "화기애애한 팀워크 속에서 타인에게 적극적인 서비스를 제공하는 직업을 추천해요!"
    },
    "ISTP": {
        "title": "🛠️ 만능 재주꾼",
        "emoji": "🐯",
        "color": "🟡",
        "desc": "대담하고 실용적인 성향으로 온갖 도구를 자유자재로 다루는 장인이에요!",
        "jobs": ["🏎️ 카레이서/정비사", "💻 네트워크 엔지니어", "✈️ 조종사", "🕵️ 데이터 침투 테스트 전문가", "🛠️ 로봇 공학자"],
        "strengths": ["🔧 위기 관리 능력", "🧩 실용적 문제 해결", "⚡ 임기응변"],
        "advice": "직접 몸으로 경험하고 도구나 기계를 다루는 활동적인 기술직이 잘 맞아요!"
    },
    "ISFP": {
        "title": "🎨 호기심 많은 예술가",
        "emoji": "🐱",
        "color": "🟡",
        "desc": "유연하고 매력 넘치며, 항상 새로운 가능성을 탐색하는 감각적인 예술가예요!",
        "jobs": ["📸 사진작가", "👗 패션 디자이너", "🌺 플로리스트", "💄 메이크업 아티스트", "🎵 음향 엔지니어"],
        "strengths": ["🎨 뛰어난 미적 감각", "🍃 자율성", "💖 따뜻한 감성"],
        "advice": "규율에 얽매이지 않고 감각과 미적 재능을 마음껏 발휘할 수 있는 분야가 좋아요!"
    },
    "ESTP": {
        "title": "⚡ 수완 좋은 모험가",
        "emoji": "🐆",
        "color": "🟡",
        "desc": "명석한 두뇌와 에너지, 그리고 직관으로 위험을 두려워하지 않는 개척자예요!",
        "jobs": ["📊 주식 트레이더", "🚒 소방관", "🏋️ 스포츠 트레이너", "💼 세일즈 전문가", "🎬 액션 감독"],
        "strengths": ["🔥 행동력", "⚡ 빠른 판단력", "🎯 뛰어난 관찰력"],
        "advice": "스릴이 있고 빠르게 변하는 환경에서 직접 문제를 해결하는 직업이 최적이에요!"
    },
    "ESFP": {
        "title": "🎉 자유로운 영혼의 연예인",
        "emoji": "🦚",
        "color": "🟡",
        "desc": "주위 사람들을 절대 지루할 틈 없게 만드는 즉흥적이고 에너제틱한 주인공이에요!",
        "jobs": ["🎭 뮤지컬 배우", "🎤 MC/리포터", "🎨 이벤트 크리에이터", "🐾 동물 훈련사", "🎈 레크리에이션 강사"],
        "strengths": ["✨ 압도적 친화력", "🎉 긍정적 에너지", "🎭 연출/스타일링 능재"],
        "advice": "스포트라이트를 받으며 사람들에게 즐거움과 행복을 주는 무대가 가장 잘 어울려요!"
    }
}

# 4. 앱 헤더 및 소개
st.markdown("<h1 class='main-title'>✨ 🚀 MBTI 진로 탐색 가이드 🌟 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>나의 성격 유형에 딱 맞는 찰떡 직업은 무엇일까요? 아래에서 MBTI를 선택해보세요! 🎈</p>", unsafe_allow_html=True)

st.write("---")

# 5. MBTI 선택 UI
col_select, col_space = st.columns([2, 1])

with col_select:
    selected_mbti = st.selectbox(
        "🔮 **당신의 MBTI 유형을 선택하세요!**",
        list(mbti_db.keys()),
        index=0
    )

st.write("")

# 6. 결과 출력 영역 (선택 시 화려한 애니메이션 연출)
if selected_mbti:
    info = mbti_db[selected_mbti]
    
    # 로딩 애니메이션
    with st.spinner("✨ 성격 데이터 분석 및 직업 매칭 중... 🔍"):
        time.sleep(0.3)

    st.balloons()  # 풍선 효과!

    # 결과 카드 출력
    st.markdown(f"""
    <div class="css-card">
        <h2 style='color: #2C3E50; margin-bottom: 5px;'>
            {info['color']} {selected_mbti} : {info['title']} {info['emoji']}
        </h2>
        <p style='font-size: 1.2rem; color: #555;'>"{info['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)

    # 2열 레이아웃으로 상세 정보 표시
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="css-card">
            <h3>🎯 추천 대표 직업군</h3>
            <p style='color: #666;'>당신의 성향과 시너지가 폭발하는 직업들입니다!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 직업 배지 스타일로 출력
        job_html = ""
        for job in info['jobs']:
            job_html += f"<span class='job-badge'>{job}</span> "
        st.markdown(job_html, unsafe_allow_html=True)
        st.write("")

    with col2:
        st.markdown("""
        <div class="css-card">
            <h3>⭐ 당신의 핵심 강점</h3>
            <p style='color: #666;'>직업 세계에서 빛나는 핵심 능력치입니다!</p>
        </div>
        """, unsafe_allow_html=True)
        
        for strength in info['strengths']:
            st.success(f"**{strength}**")

    # 진로 조언 하단 카드
    st.info(f"💡 **진로 탐색 꿀팁:** {info['advice']}")

# 7. 푸터 (하단 안내 메시지)
st.write("---")
st.markdown("""
<div style='text-align: center; color: #ffffff; padding: 20px;'>
    <p>🌈 MBTI는 진로 탐색을 위한 참고용일 뿐! 가장 중요한 건 여러분의 열정과 관심사입니다 💪✨</p>
    <p style='font-size: 0.8rem; opacity: 0.8;'>Educational Career Guide Tool built with Streamlit ❤️</p>
</div>
""", unsafe_allow_html=True)
