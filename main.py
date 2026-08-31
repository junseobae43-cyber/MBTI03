import streamlit as st
import time

# 1. 페이지 기본 설정 (가장 위에 배치)
st.set_page_config(
    page_title="✨ MBTI 진로 탐색 가이드 ✨",
    page_icon="🌈",
    layout="wide"
)

# 2. 커스텀 CSS (화려한 배경, 애니메이션, 이미지 및 카드 스타일링)
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #a8c0ff 0%, #3f2b96 100%);
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 헤더 스타일링 */
    .main-title {
        text-align: center;
        font-size: 3.2rem !important;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.3);
        padding: 15px 0;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.3rem;
        color: #f0f3ff;
        margin-bottom: 25px;
        font-weight: 500;
    }

    /* 카드 스타일링 */
    .css-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* 직업 배지 스타일 */
    .job-badge {
        display: inline-block;
        background: linear-gradient(45deg, #FF512F, #DD2476);
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        font-weight: bold;
        margin: 6px 4px;
        box-shadow: 0 4px 12px rgba(221, 36, 118, 0.3);
        font-size: 1.05rem;
    }

    /* 이미지 커스텀 테두리 */
    .stImage img {
        border-radius: 20px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
        object-fit: cover;
    }

    /* Selectbox 커스텀 */
    .stSelectbox label {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. MBTI 데이터베이스 (직업, 강점, 이미지, 추천 환경)
mbti_db = {
    "INTJ": {
        "title": "🧠 용의주도한 전략가",
        "emoji": "🦅",
        "color": "🟣",
        "desc": "독립적이며 상상력이 풍부하고, 철저한 계획을 세우는 완벽주의자예요!",
        "image": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🔬 전략적 문제 해결 및 데이터/AI 연구",
        "jobs": ["💻 AI 연구원", "📊 데이터 분석가", "🏛️ 정책 기획자", "🧩 시스템 아키텍트", "🧪 과학자"],
        "strengths": ["💡 전략적 사고", "🎯 높은 집중력", "📐 논리적 문제 해결"],
        "advice": "혼자 몰입할 수 있고 지적 호기심을 자극하는 환경이 잘 맞아요!"
    },
    "INTP": {
        "title": "🔬 논리적인 사색가",
        "emoji": "🦉",
        "color": "🟣",
        "desc": "끊임없이 새로운 지식을 탐구하고 아이디어를 제안하는 원리원칙주의자예요!",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=800&auto=format&fit=crop",
        "image_caption": "💻 소프트웨어 및 첨단 기술 탐구",
        "jobs": ["💻 소프트웨어 개발자", "📐 이론물리학자", "🔍 보안 전문가", "🎓 교수/연구원", "🎮 게임 디자이너"],
        "strengths": ["🔎 객관적 분석", "🌌 창의적 상상력", "📚 끊임없는 탐구"],
        "advice": "자율성이 보장되고 복잡한 문제를 해결하는 분야를 추천해요!"
    },
    "ENTJ": {
        "title": "👑 대담한 통솔자",
        "emoji": "🦁",
        "color": "🟣",
        "desc": "대담하고 상상력이 풍부하며, 강한 의지로 길을 개척하는 리더예요!",
        "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=800&auto=format&fit=crop",
        "image_caption": "💼 비즈니스 경영 및 카리스마 리더십",
        "jobs": ["💼 경영 컨설턴트", "🚀 스타트업 창업가", "⚖️ 변호사", "📈 투자 은행가", "🏛️ 정치인"],
        "strengths": ["📢 카리스마 리더십", "🎯 목표 지향성", "⚡ 결단력"],
        "advice": "팀을 이끌고 단체나 조직의 목표를 달성하는 직무에서 빛을 발해요!"
    },
    "ENTP": {
        "title": "💡 뜨거운 논쟁을 즐기는 변론가",
        "emoji": "🦊",
        "color": "🟣",
        "desc": "호기심이 많고 지적인 도전을 두려워하지 않는 모험가예요!",
        "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?q=80&w=800&auto=format&fit=crop",
        "image_caption": "💡 창의적 브레인스토밍 및 신사업 기획",
        "jobs": ["📣 마케팅 기획자", "💡 벤처 투자자", "🎬 방송 PD", "🎙️ 시사 평론가", "🎨 기획 개발자"],
        "strengths": ["🔥 브레인스토밍", "🗣️ 설득력", "🔄 유연한 사고"],
        "advice": "변화가 무궁무진하고 새로운 아이디어를 마음껏 펼칠 수 있는 환경이 좋아요!"
    },
    "INFJ": {
        "title": "🔮 통찰력 있는 선의의 옹호자",
        "emoji": "🦄",
        "color": "🟢",
        "desc": "조용하고 신비로우며 샘솟는 영감으로 사람들에게 긍정적 영향을 주는 유형이에요!",
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?q=80&w=800&auto=format&fit=crop",
        "image_caption": "✍️ 심층적인 통찰과 창작/상담 활동",
        "jobs": ["📑 심리상담사", "✍️ 작가/시인", "🩺 한의사", "🕊️ 인권 활동가", "🎨 아트 디렉터"],
        "strengths": ["❤️ 깊은 공감 능력", "👁️ 예리한 통찰력", "🌱 진정성"],
        "advice": "사람들의 성장을 돕고 세상을 더 나은 곳으로 만드는 가치 있는 일이 맞아요!"
    },
    "INFP": {
        "title": "🎨 열정적인 중재자",
        "emoji": "🐰",
        "color": "🟢",
        "desc": "상냥하고 이타적이며, 나만의 이상적 세계를 꿈꾸는 낭만파예요!",
        "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🎨 감성과 신념을 담은 예술 창작",
        "jobs": ["🎨 일러스트레이터", "📚 웹툰 작가", "🎵 음악 프로듀서", "🧸 아동 상담사", "📝 에세이스트"],
        "strengths": ["🌈 풍부한 감수성", "💎 창의력", "🤝 따뜻한 이타심"],
        "advice": "개인의 신념과 창의성을 자유롭게 표현할 수 있는 환경이 최적이에요!"
    },
    "ENFJ": {
        "title": "☀️ 정의로운 사회운동가",
        "emoji": "🐬",
        "color": "🟢",
        "desc": "넘치는 카리스마와 열정으로 청중을 사로잡는 따뜻한 리더예요!",
        "image": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🎤 사람들을 고취시키는 교육 및 강연",
        "jobs": ["👩‍🏫 교사/강사", "🤝 HR(인사) 전문가", "🎤 아나운서", "🎪 행사 기획자", "🏥 사회복지사"],
        "strengths": ["✨ 동기부여 능력", "💬 뛰어난 소통력", "💖 타인에 대한 배려"],
        "advice": "사람들과 깊게 교류하며 타인의 잠재력을 이끌어내는 교육/상담 직무를 추천해요!"
    },
    "ENFP": {
        "title": "🎈 재발랄한 활동가",
        "emoji": "🐶",
        "color": "🟢",
        "desc": "창의적이고 열정적이며, 에너지가 넘치고 웃음이 많은 아이디어 크리에이터!",
        "image": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=800&auto=format&fit=crop",
        "image_caption": "📹 에너지와 호기심 가득한 미디어 콘텐츠 창작",
        "jobs": ["📹 크리에이터/유튜버", "🎨 광고 카피라이터", "✈️ 여행 가이드", "🎭 배우/엔터테이너", "🎉 이벤트 디렉터"],
        "strengths": ["⚡ 폭발적 친화력", "💡 마르지 않는 아이디어", "🌟 긍정 마인드"],
        "advice": "반복적이지 않고 재미있으며, 매일 새로운 사람과 만나는 일이 어울려요!"
    },
    "ISTJ": {
        "title": "🛡️ 청렴결백한 논리주의자",
        "emoji": "🐘",
        "color": "🔵",
        "desc": "실체적이고 두터운 원칙주의자로, 신뢰를 최우선으로 생각하는 현실주의자예요!",
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=800&auto=format&fit=crop",
        "image_caption": "📊 정교한 금융/데이터/행정 관리",
        "jobs": ["📊 회계사/세무사", "🏛️ 공무원", "📑 데이터 관리자", "⚖️ 판사/검사", "🛡️ 품질 관리자"],
        "strengths": ["📐 철저한 정직함", "🔍 꼼꼼한 디테일", "🏛️ 강한 책임감"],
        "advice": "체계가 잘 잡혀있고 데이터와 규칙이 명확한 환경에서 최고의 성과를 내요!"
    },
    "ISFJ": {
        "title": "🌷 용감한 수호자",
        "emoji": "🐧",
        "color": "🔵",
        "desc": "소중한 사람들을 지키는 데 진심이며, 헌신적이고 따뜻한 수호자예요!",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🏥 따뜻하고 세심한 보건/교육 서비스",
        "jobs": ["👩‍⚕️ 간호사", "🏫 초등학교 교사", "📜 사서", "🍰 파티시에", "🏥 영양사"],
        "strengths": ["🤝 세심한 배려", "🛡️ 안정감 제공", "🎯 성실함"],
        "advice": "타인을 직접적으로 돕고 실질적인 지원을 제공하는 따뜻한 분위기가 맞아요!"
    },
    "ESTJ": {
        "title": "🏛️ 엄격한 관리자",
        "emoji": "🦅",
        "color": "🔵",
        "desc": "사물과 사람을 관리하는 데 뛰어난 능력을 발휘하는 도덕적 가이드예요!",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🏭 효율적인 프로젝트 총괄 및 인프라 구축",
        "jobs": ["🏢 프로젝트 매니저(PM)", "👮 경찰/장교", "📈 금융 자산관리사", "🏭 공장 운영 관리자", "👨‍💼 경영자"],
        "strengths": ["📊 뛰어난 조직력", "⚡ 실천력", "🎯 명확한 목표 달성"],
        "advice": "명확한 규칙과 효율성을 바탕으로 체계적으로 팀을 관리하는 역할이 적합해요!"
    },
    "ESFJ": {
        "title": "🤝 사교적인 외교관",
        "emoji": "🦌",
        "color": "🔵",
        "desc": "타인에게 관심이 많고 친절하며, 항상 도울 준비가 되어있는 분위기 메이커예요!",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=800&auto=format&fit=crop",
        "image_caption": "✈️ 고객 매너와 최고의 호스피탈리티 서비스",
        "jobs": ["✈️ 승무원", "🏨 호텔 지배인", "🩺 고객만족(CS) 팀장", "🤝 뷰티 컨설턴트", "💌 고객 관리자"],
        "strengths": ["😊 뛰어난 공감력", "🎉 분위기 메이커", "🤝 협동심"],
        "advice": "화기애애한 팀워크 속에서 타인에게 적극적인 서비스를 제공하는 직업을 추천해요!"
    },
    "ISTP": {
        "title": "🛠️ 만능 재주꾼",
        "emoji": "🐯",
        "color": "🟡",
        "desc": "대담하고 실용적인 성향으로 온갖 도구를 자유자재로 다루는 장인이에요!",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🛠️ 정밀한 엔지니어링 및 기계/도구 다루기",
        "jobs": ["🏎️ 카레이서/정비사", "💻 네트워크 엔지니어", "✈️ 조종사", "🕵️ 보안 연구원", "🛠️ 로봇 공학자"],
        "strengths": ["🔧 위기 관리 능력", "🧩 실용적 문제 해결", "⚡ 임기응변"],
        "advice": "직접 몸으로 경험하고 도구나 기계를 다루는 활동적인 기술직이 잘 맞아요!"
    },
    "ISFP": {
        "title": "🎨 호기심 많은 예술가",
        "emoji": "🐱",
        "color": "🟡",
        "desc": "유연하고 매력 넘치며, 항상 새로운 가능성을 탐색하는 감각적인 예술가예요!",
        "image": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?q=80&w=800&auto=format&fit=crop",
        "image_caption": "📸 시각적 감각을 담아내는 패션 및 사진 예술",
        "jobs": ["📸 사진작가", "👗 패션 디자이너", "🌺 플로리스트", "💄 메이크업 아티스트", "🎵 음향 엔지니어"],
        "strengths": ["🎨 뛰어난 미적 감각", "🍃 자율성", "💖 따뜻한 감성"],
        "advice": "규율에 얽매이지 않고 감각과 미적 재능을 마음껏 발휘할 수 있는 분야가 좋아요!"
    },
    "ESTP": {
        "title": "⚡ 수완 좋은 모험가",
        "emoji": "🐆",
        "color": "🟡",
        "desc": "명석한 두뇌와 에너지, 그리고 직관으로 위험을 두려워하지 않는 개척자예요!",
        "image": "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🔥 박진감 넘치는 액션, 스릴, 빠른 판단력",
        "jobs": ["📊 주식 트레이더", "🚒 소방관", "🏋️ 스포츠 트레이너", "💼 세일즈 전문가", "🎬 액션 감독"],
        "strengths": ["🔥 강력한 행동력", "⚡ 빠른 판단력", "🎯 뛰어난 관찰력"],
        "advice": "스릴이 있고 빠르게 변하는 환경에서 직접 문제를 해결하는 직업이 최적이에요!"
    },
    "ESFP": {
        "title": "🎉 자유로운 영혼의 연예인",
        "emoji": "🦚",
        "color": "🟡",
        "desc": "주위 사람들을 절대 지루할 틈 없게 만드는 즉흥적이고 에너제틱한 주인공이에요!",
        "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=800&auto=format&fit=crop",
        "image_caption": "🎭 스포트라이트 중심에서의 공연 및 라이브 파티",
        "jobs": ["🎭 뮤지컬 배우", "🎤 MC/리포터", "🎨 이벤트 크리에이터", "🐾 동물 훈련사", "🎈 레크리에이션 강사"],
        "strengths": ["✨ 압도적 친화력", "🎉 긍정적 에너지", "🎭 탁월한 무대 매너"],
        "advice": "스포트라이트를 받으며 사람들에게 즐거움과 행복을 주는 무대가 가장 잘 어울려요!"
    }
}

# 4. 앱 헤더 및 소개
st.markdown("<h1 class='main-title'>✨ 🚀 MBTI 진로 탐색 가이드 🌟 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>나의 성격 유형에 꼭 맞는 찰떡 직업과 분위기 이미지를 확인해보세요! 🎈</p>", unsafe_allow_html=True)

st.write("---")

# 5. MBTI 선택 UI
col_select, _ = st.columns([2, 1])

with col_select:
    selected_mbti = st.selectbox(
        "🔮 **당신의 MBTI 유형을 선택하세요!**",
        list(mbti_db.keys()),
        index=0
    )

st.write("")

# 6. 결과 출력 영역
if selected_mbti:
    info = mbti_db[selected_mbti]
    
    # 선택 시 풍선 애니메이션 효과
    st.balloons()

    # 상단 요약 카드
    st.markdown(f"""
    <div class="css-card">
        <h2 style='color: #1a2a6c; margin-bottom: 5px;'>
            {info['color']} {selected_mbti} : {info['title']} {info['emoji']}
        </h2>
        <p style='font-size: 1.25rem; color: #444; font-weight: 500;'>"{info['desc']}"</p>
    </div>
    """, unsafe_allow_html=True)

    # 2열 레이아웃 (왼쪽: 대표 이미지, 오른쪽: 대표 직업 및 강점)
    col_img, col_info = st.columns([1, 1.2])

    with col_img:
        st.image(
            info['image'],
            caption=info['image_caption'],
            use_container_width=True
        )

    with col_info:
        # 추천 직업 카드
        st.markdown("""
        <div class="css-card">
            <h3 style='margin-bottom: 10px; color: #2C3E50;'>🎯 추천 대표 직업군</h3>
            <p style='color: #666; font-size: 0.95rem;'>당신의 성향과 시너지가 폭발하는 메인 직업들입니다!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 직업 배지 스타일 출력
        job_html = ""
        for job in info['jobs']:
            job_html += f"<span class='job-badge'>{job}</span> "
        st.markdown(job_html, unsafe_allow_html=True)
        st.write("")
        
        # 핵심 강점 출력
        st.markdown("""
        <div class="css-card">
            <h3 style='margin-bottom: 10px; color: #2C3E50;'>⭐ 당신의 핵심 강점</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for strength in info['strengths']:
            st.success(f"**{strength}**")

    # 진로 조언 하단 강조 카드
    st.info(f"💡 **진로 탐색 꿀팁:** {info['advice']}")

# 7. 푸터 안내
st.write("---")
st.markdown("""
<div style='text-align: center; color: #ffffff; padding: 20px;'>
    <p style='font-size: 1.1rem; font-weight: bold;'>🌈 MBTI는 진로 탐색을 위한 유용한 참고 도구입니다!</p>
    <p style='font-size: 0.9rem; opacity: 0.9;'>가장 중요한 건 여러분이 가진 꿈과 끊임없는 열정입니다 💪✨</p>
</div>
""", unsafe_allow_html=True)
