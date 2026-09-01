import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="마린과의 등교길", layout="centered")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      background-color: #121218;
      color: #ffffff;
      font-family: -apple-system, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    #game-box {
      width: 100%;
      max-width: 650px;
      height: 540px;
      background: linear-gradient(180deg, #2a2d42 0%, #181824 100%);
      border: 2px solid #ff69b4;
      border-radius: 16px;
      padding: 20px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* 캐릭터 영역 */
    #character-area {
      height: 260px;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      position: relative;
    }
    
    /* 대화 상자 */
    #dialogue-area {
      background-color: rgba(20, 20, 30, 0.88);
      border: 2px solid #ff69b4;
      border-radius: 12px;
      padding: 16px 20px;
      min-height: 110px;
      cursor: pointer;
      position: relative;
      z-index: 10;
    }
    #speaker {
      color: #ff69b4;
      font-weight: bold;
      font-size: 1.1rem;
      margin-bottom: 6px;
      text-shadow: 0 0 5px rgba(255, 105, 180, 0.5);
    }
    #text {
      font-size: 1.05rem;
      line-height: 1.5;
      color: #f0f0f0;
    }
    
    /* 선택지 */
    #choices {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 10px;
      z-index: 20;
    }
    .btn {
      background: rgba(255, 255, 255, 0.95);
      color: #111;
      border: 2px solid #ff69b4;
      padding: 12px;
      border-radius: 25px;
      font-weight: bold;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn:hover {
      background-color: #ff69b4;
      color: white;
      transform: translateY(-2px);
    }
    #guide {
      font-size: 0.8rem;
      color: #ff69b4;
      text-align: right;
      margin-top: 8px;
      animation: blink 1.2s infinite;
    }
    @keyframes blink {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }

    /* 표정 제어용 SVG 스타일 */
    .face-element { transition: all 0.2s ease; }
  </style>
</head>
<body>

<div id="game-box">
  <div id="character-area">
    <svg viewBox="0 0 240 280" width="220" height="260">
      <!-- 긴 금발 머리 (뒷머리) -->
      <path d="M 40,80 Q 10,180 30,280 L 210,280 Q 230,180 200,80 Z" fill="#ffe066"/>
      <!-- 투톤 핑크 피치 끝부분 -->
      <path d="M 32,200 Q 20,250 30,280 L 210,280 Q 220,250 208,200 Z" fill="#ff99c8"/>
      
      <!-- 몸통 / 흰색 셔츠 -->
      <path d="M 60,160 L 180,160 L 195,280 L 45,280 Z" fill="#ffffff"/>
      <polygon points="120,160 128,230 120,245 112,230" fill="#343a40"/>
      <polygon points="90,160 120,180 80,170" fill="#e9ecef"/>
      <polygon points="150,160 120,180 160,170" fill="#e9ecef"/>
      
      <!-- 목 & 흑색 초커 -->
      <rect x="105" y="130" width="30" height="35" fill="#ffede0"/>
      <rect x="105" y="145" width="30" height="6" fill="#111111"/>
      <circle cx="120" cy="154" r="3" fill="#ffd700"/>

      <!-- 얼굴 -->
      <ellipse cx="120" cy="100" rx="42" ry="46" fill="#ffede0"/>
      <!-- 앞머리 -->
      <path d="M 75,85 Q 120,55 165,85 Q 140,110 120,95 Q 100,110 75,85 Z" fill="#ffe066"/>

      <!-- 동적 변화 표정 레이어 -->
      <g id="eyes-layer"></g>
      <g id="blush-layer"></g>
      <g id="mouth-layer"></g>

      <!-- 브이 손가락 포즈 -->
      <g id="hand-pose">
        <path d="M 160,70 L 175,30 L 185,35 L 172,70 Z" fill="#ffede0"/>
        <path d="M 170,70 L 195,45 L 203,52 L 178,80 Z" fill="#ffede0"/>
        <rect x="155" y="75" width="20" height="8" rx="4" fill="#222222"/>
      </g>
    </svg>
  </div>
  
  <div id="choices"></div>

  <div id="dialogue-area" onclick="nextText()">
    <div id="speaker">키타가와 마린</div>
    <div id="text"></div>
    <div id="guide">클릭해서 계속 ▶</div>
  </div>
</div>

<script>
// 상황별 스토리 및 표정 설정 (expression: wink, happy, excited, shy, pout)
var story = {
  step1: { 
    text: "야호~! 좋은 아침! 교문 앞에서 딱 만나다니 대박 완전 운 좋다~!", 
    expression: "wink", 
    next: "step2", 
    options: null 
  },
  step2: { 
    text: "같이 교실 올라가자! 어제 말했던 그 애니 최신화 봤어? 완전 대박이었는데!", 
    expression: "happy", 
    next: null, 
    options: [
      { msg: "응, 봤어! 연출 진짜 좋더라.", target: "step3_1" },
      { msg: "바빠서 아직 못 봤어.", target: "step3_2" }
    ]
  },
  step3_1: { 
    text: "그치 그치?! 특히 주인공 변신 장면! 나 진짜 소름 돋아서 세 번이나 돌려봤잖아~!", 
    expression: "excited", 
    next: "step4", 
    options: null 
  },
  step3_2: { 
    text: "앗, 진짜?! 그럼 스포일러 안 하게 조심해야겠다! 오늘 집에 가자마자 꼭 봐!", 
    expression: "wink", 
    next: "step4", 
    options: null 
  },
  step4: { 
    text: "아 맞다! 교실 들어온 김에 말하는 건데, 다음 코스프레 캐릭터 의상 재료 말이야...", 
    expression: "shy", 
    next: "step5", 
    options: null 
  },
  step5: { 
    text: "원단이 생각보다 복잡해서 그런데, 혹시 쉬는 시간에 같이 인터넷으로 자재 좀 봐줄 수 있어?", 
    expression: "shy", 
    next: null, 
    options: [
      { msg: "좋아, 쉬는 시간에 같이 보자.", target: "end_happy" },
      { msg: "쉬는 시간엔 좀 자고 싶은데...", target: "end_pout" }
    ]
  },
  end_happy: { 
    text: "아싸~! 역시 다정하다니까! 그럼 쉬는 시간 벨 울리자마자 바로 네 자리로 갈게!", 
    expression: "excited", 
    next: null, 
    options: null 
  },
  end_pout: { 
    text: "에~ 피곤한 거야? 어쩔 수 없지... 그럼 졸릴 때 깨워줄 테니까 편하게 쉬어! 히히~", 
    expression: "pout", 
    next: null, 
    options: null 
  }
};

var currentStep = "step1";

// 표정 렌더링 함수
function setExpression(type) {
  var eyes = document.getElementById("eyes-layer");
  var blush = document.getElementById("blush-layer");
  var mouth = document.getElementById("mouth-layer");

  // 기본 볼터치
  blush.innerHTML = `
    <ellipse cx="88" cy="112" rx="8" ry="4" fill="#ff85a2" opacity="${type === 'shy' ? '0.9' : '0.5'}"/>
    <ellipse cx="145" cy="112" rx="8" ry="4" fill="#ff85a2" opacity="${type === 'shy' ? '0.9' : '0.5'}"/>
  `;

  // 눈표정 분기
  if (type === "wink") {
    eyes.innerHTML = `
      <path d="M 90,102 Q 100,96 105,102" stroke="#d63384" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <ellipse cx="138" cy="102" rx="8" ry="11" fill="#d63384"/>
      <circle cx="140" cy="99" r="3" fill="#ffffff"/>
    `;
  } else if (type === "excited") {
    eyes.innerHTML = `
      <ellipse cx="82" cy="102" rx="8" ry="11" fill="#d63384"/>
      <circle cx="84" cy="99" r="3.5" fill="#ffffff"/>
      <ellipse cx="138" cy="102" rx="8" ry="11" fill="#d63384"/>
      <circle cx="140" cy="99" r="3.5" fill="#ffffff"/>
    `;
  } else if (type === "shy") {
    eyes.innerHTML = `
      <ellipse cx="82" cy="103" rx="7" ry="9" fill="#d63384"/>
      <circle cx="84" cy="101" r="2.5" fill="#ffffff"/>
      <ellipse cx="138" cy="103" rx="7" ry="9" fill="#d63384"/>
      <circle cx="140" cy="101" r="2.5" fill="#ffffff"/>
    `;
  } else if (type === "pout") {
    eyes.innerHTML = `
      <path d="M 75,98 Q 82,104 90,98" stroke="#d63384" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <path d="M 130,98 Q 138,104 145,98" stroke="#d63384" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    `;
  } else { // happy
    eyes.innerHTML = `
      <ellipse cx="82" cy="102" rx="8" ry="10" fill="#d63384"/>
      <circle cx="84" cy="99" r="3" fill="#ffffff"/>
      <ellipse cx="138" cy="102" rx="8" ry="10" fill="#d63384"/>
      <circle cx="140" cy="99" r="3" fill="#ffffff"/>
    `;
  }

  // 입표정 분기
  if (type === "excited") {
    mouth.innerHTML = `<path d="M 105,118 Q 120,138 135,118 Z" fill="#ff4d6d"/>`;
  } else if (type === "shy") {
    mouth.innerHTML = `<path d="M 110,122 Q 120,126 130,122" stroke="#ff4d6d" stroke-width="3" fill="none" stroke-linecap="round"/>`;
  } else if (type === "pout") {
    mouth.innerHTML = `<path d="M 110,125 Q 120,120 130,125" stroke="#ff4d6d" stroke-width="3" fill="none" stroke-linecap="round"/>`;
  } else {
    mouth.innerHTML = `<path d="M 108,120 Q 120,132 132,120 Z" fill="#ff4d6d"/>`;
  }
}

function draw() {
  var data = story[currentStep];
  document.getElementById("text").innerText = data.text;
  setExpression(data.expression);

  var choiceDiv = document.getElementById("choices");
  var guideDiv = document.getElementById("guide");
  choiceDiv.innerHTML = "";

  if (data.options) {
    guideDiv.style.display = "none";
    for (var i = 0; i < data.options.length; i++) {
      (function(opt) {
        var button = document.createElement("button");
        button.className = "btn";
        button.innerText = opt.msg;
        button.onclick = function() { currentStep = opt.target; draw(); };
        choiceDiv.appendChild(button);
      })(data.options[i]);
    }
  } else {
    guideDiv.style.display = data.next ? "block" : "none";
  }
}

function nextText() {
  var data = story[currentStep];
  if (!data.options && data.next) {
    currentStep = data.next;
    draw();
  }
}

draw();
</script>
</body>
</html>
"""

components.html(game_html, height=580)
