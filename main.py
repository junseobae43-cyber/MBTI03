<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>그 비스크 돌은 사랑을 한다 - 등교편</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', -apple-system, sans-serif; user-select: none; }
    body { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #0f0f12; color: #fff; }

    #game-container {
      width: 800px;
      height: 500px;
      position: relative;
      overflow: hidden;
      border-radius: 16px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8);
      background: linear-gradient(135deg, #2b1055, #7597de);
    }

    /* SVG 배경 */
    .scene-bg { 
      width: 100%; 
      height: 100%; 
      position: absolute; 
      top: 0; 
      left: 0; 
    }

    /* SVG 마린 캐릭터 */
    .character-container {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      width: 280px;
      height: 380px;
      pointer-events: none;
      transition: all 0.3s ease;
    }

    /* 대화창 */
    .dialogue-box {
      position: absolute;
      bottom: 15px;
      left: 50%;
      transform: translateX(-50%);
      width: 92%;
      height: 135px;
      background: rgba(15, 15, 22, 0.92);
      backdrop-filter: blur(10px);
      border: 2px solid rgba(255, 105, 180, 0.7);
      border-radius: 14px;
      padding: 18px 24px;
      color: #fff;
      cursor: pointer;
      z-index: 20;
    }

    .name-tag { 
      font-weight: 700; 
      font-size: 1.15rem; 
      color: #ff69b4; 
      margin-bottom: 8px; 
      text-shadow: 0 0 8px rgba(255, 105, 180, 0.5);
    }

    .text-content { 
      font-size: 1.05rem; 
      line-height: 1.6; 
      color: #f0f0f0;
    }

    .click-prompt {
      position: absolute;
      bottom: 12px;
      right: 20px;
      font-size: 0.8rem;
      color: #ff69b4;
      animation: blink 1.2s infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 1; }
    }

    /* 선택지 메뉴 */
    .choices-container {
      position: absolute;
      top: 40%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 75%;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 30;
    }

    .choice-btn {
      background: rgba(255, 255, 255, 0.95);
      color: #111;
      border: 2px solid #ff69b4;
      padding: 14px 20px;
      border-radius: 30px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .choice-btn:hover { 
      background: #ff69b4; 
      color: #fff; 
      transform: scale(1.02); 
    }

    /* 상단 호감도 바 */
    .stats-overlay { 
      position: absolute; 
      top: 15px; 
      right: 20px; 
      background: rgba(0, 0, 0, 0.7); 
      padding: 8px 18px; 
      border-radius: 20px; 
      color: #ff69b4; 
      font-weight: bold;
      border: 1px solid rgba(255, 105, 180, 0.5);
      z-index: 10;
    }
  </style>
</head>
<body>

<div id="game-container">
  <!-- 배경 SVG -->
  <svg class="scene-bg" viewBox="0 0 800 500">
    <rect width="800" height="500" fill="#1e1e2f"/>
    <!-- 학교 건물 표현 -->
    <rect x="100" y="100" width="600" height="400" fill="#2d2d44" rx="10"/>
    <rect x="140" y="140" width="80" height="60" fill="#ffd700" opacity="0.6" rx="5"/>
    <rect x="260" y="140" width="80" height="60" fill="#ffd700" opacity="0.8" rx="5"/>
    <rect x="380" y="140" width="80" height="60" fill="#ffd700" opacity="0.4" rx="5"/>
    <rect x="500" y="140" width="80" height="60" fill="#ffd700" opacity="0.7" rx="5"/>
  </svg>
  
  <!-- 마린 캐릭터 SVG 일러스트 -->
  <div class="character-container">
    <svg viewBox="0 0 200 300" width="100%" height="100%">
      <!-- 긴 금발 머리 -->
      <path d="M 30,80 Q 10,180 35,290 L 165,290 Q 190,180 170,80 Z" fill="#ffe066"/>
      <!-- 핑크 그라데이션 포인트 (투톤) -->
      <path d="M 32,220 Q 25,260 35,290 L 165,290 Q 175,260 168,220 Z" fill="#ff99c8"/>
      <!-- 얼굴 구조 -->
      <ellipse cx="100" cy="100" rx="45" ry="50" fill="#ffede0"/>
      <!-- 앞머리 -->
      <path d="M 55,85 Q 100,60 145,85 Q 120,110 100,95 Q 80,110 55,85 Z" fill="#ffe066"/>
      <!-- 눈 (적자색) -->
      <ellipse cx="80" cy="100" rx="7" ry="10" fill="#d63384"/>
      <ellipse cx="120" cy="100" rx="7" ry="10" fill="#d63384"/>
      <circle cx="82" cy="98" r="2.5" fill="#fff"/>
      <circle cx="122" cy="98" r="2.5" fill="#fff"/>
      <!-- 입 (웃는 모양) -->
      <path d="M 90,120 Q 100,130 110,120" stroke="#ff4d6d" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- 교복/셔츠 -->
      <path d="M 55,145 L 145,145 L 160,290 L 40,290 Z" fill="#ffffff"/>
      <!-- 넥타이 -->
      <polygon points="100,145 106,210 100,225 94,210" fill="#495057"/>
    </svg>
  </div>
  
  <div class="stats-overlay">
    ♥ 호감도: <span id="affection-score">0</span>
  </div>

  <div id="choices-container" class="choices-container" style="display: none;"></div>

  <div id="dialogue-box" class="dialogue-box">
    <div id="name-tag" class="name-tag">키타가와 마린</div>
    <div id="text-content" class="text-content"></div>
    <div id="click-prompt" class="click-prompt">클릭하여 계속 ▼</div>
  </div>
</div>

<script>
// 게임 스토리 데이터
const storyData = {
  school_gate: {
    name: '키타가와 마린',
    text: '야호~! 좋은 아침! 교문 앞에서 딱 만나다니 대박 완전 운 좋다~!',
    nextScene: 'gate_talk',
    choices: []
  },
  gate_talk: {
    name: '키타가와 마린',
    text: '같이 교실 올라가자! 어제 말했던 그 애니 최신화 봤어? 완전 대박이었는데!',
    choices: [
      { text: '응, 봤어! 연출 진짜 좋더라.', nextScene: 'hallway_excited', affectionDelta: 10 },
      { text: '바빠서 아직 못 봤어.', nextScene: 'hallway_spoil', affectionDelta: 5 }
    ]
  },
  hallway_excited: {
    name: '키타가와 마린',
    text: '그치 그치?! 특히 3분쯤에 나온 주인공 변신 장면! 나 진짜 소름 돋아서 세 번이나 돌려봤잖아~!',
    nextScene: 'classroom_in',
    choices: []
  },
  hallway_spoil: {
    name: '키타가와 마린',
    text: '앗, 진짜?! 그럼 스포일러 안 하게 조심해야겠다! 오늘 집에 가자마자 꼭 봐야 해, 약속~!',
    nextScene: 'classroom_in',
    choices: []
  },
  classroom_in: {
    name: '키타가와 마린',
    text: '아 맞다! 교실 들어온 김에 말하는 건데, 다음 코스프레 캐릭터 의상 재료 말이야...',
    nextScene: 'classroom_talk2',
    choices: []
  },
  classroom_talk2: {
    name: '키타가와 마린',
    text: '원단이 생각보다 복잡해서 고민이었거든? 혹시 쉬는 시간에 같이 인터넷으로 자재 좀 봐줄 수 있어?',
    choices: [
      { text: '좋아, 쉬는 시간에 같이 보자.', nextScene: 'ending_happy', affectionDelta: 15 },
      { text: '쉬는 시간엔 좀 자고 싶은데...', nextScene: 'ending_pout', affectionDelta: -5 }
    ]
  },
  ending_happy: {
    name: '키타가와 마린',
    text: '아싸~! 역시 다정하다니까! 그럼 쉬는 시간 벨 울리자마자 바로 네 자리로 갈게!',
    nextScene: null,
    choices: []
  },
  ending_pout: {
    name: '키타가와 마린',
    text: '에~ 피곤한 거야? 어쩔 수 없지... 그럼 졸릴 때 깨워줄 테니까 편하게 쉬어! 히히~',
    nextScene: null,
    choices: []
  }
};

let affection = 0;
let currentSceneKey = 'school_gate';

function renderScene() {
  const scene = storyData[currentSceneKey];
  if (!scene) return;

  document.getElementById('name-tag').innerText = scene.name;
  document.getElementById('text-content').innerText = scene.text;
  document.getElementById('affection-score').innerText = affection;

  const choicesContainer = document.getElementById('choices-container');
  const clickPrompt = document.getElementById('click-prompt');
  choicesContainer.innerHTML = '';

  if (scene.choices && scene.choices.length > 0) {
    choicesContainer.style.display = 'flex';
    clickPrompt.style.display = 'none';

    scene.choices.forEach(choice => {
      const button = document.createElement('button');
      button.className = 'choice-btn';
      button.innerText = choice.text;
      button.onclick = (e) => {
        e.stopPropagation();
        affection += choice.affectionDelta;
        currentSceneKey = choice.nextScene;
        renderScene();
      };
      choicesContainer.appendChild(button);
    });
  } else {
    choicesContainer.style.display = 'none';
    clickPrompt.style.display = scene.nextScene ? 'block' : 'none';
  }
}

// 화면 대화창 클릭 진행
document.getElementById('dialogue-box').onclick = function() {
  const scene = storyData[currentSceneKey];
  if (scene && scene.nextScene && (!scene.choices || scene.choices.length === 0)) {
    currentSceneKey = scene.nextScene;
    renderScene();
  }
};

// 시작 실행
renderScene();
</script>

</body>
</html>
