<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>그 비스크 돌은 사랑을 한다 - 학교 등교편</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', -apple-system, sans-serif; user-select: none; }
    body { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #0a0a0c; color: #fff; }

    #game-container {
      width: 800px;
      height: 500px;
      position: relative;
      overflow: hidden;
      border-radius: 16px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
      background: #1a1a1a;
    }

    .scene-bg { 
      width: 100%; 
      height: 100%; 
      object-fit: cover; 
      position: absolute; 
      top: 0; 
      left: 0; 
      filter: brightness(0.85);
      transition: background-image 0.5s ease;
    }

    .character { 
      height: 95%; 
      position: absolute; 
      bottom: 0; 
      left: 50%; 
      transform: translateX(-50%); 
      transition: all 0.3s ease-in-out;
      pointer-events: none;
    }

    .dialogue-box {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      width: 90%;
      height: 130px;
      background: rgba(18, 18, 24, 0.88);
      backdrop-filter: blur(12px);
      border: 2px solid rgba(255, 105, 180, 0.6);
      border-radius: 14px;
      padding: 18px 24px;
      color: #fff;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }

    .name-tag { 
      font-weight: 700; 
      font-size: 1.15rem; 
      color: #ff69b4; 
      margin-bottom: 8px; 
      text-shadow: 0 0 8px rgba(255, 105, 180, 0.4);
    }

    .text-content { 
      font-size: 1.05rem; 
      line-height: 1.6; 
      color: #eaeaea;
    }

    .click-prompt {
      position: absolute;
      bottom: 12px;
      right: 20px;
      font-size: 0.8rem;
      color: rgba(255, 255, 255, 0.5);
      animation: blink 1.2s infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 1; }
    }

    .choices-container {
      position: absolute;
      top: 45%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 75%;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 10;
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
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .choice-btn:hover { 
      background: #ff69b4; 
      color: #fff; 
      transform: scale(1.02); 
    }

    .stats-overlay { 
      position: absolute; 
      top: 15px; 
      right: 20px; 
      background: rgba(0, 0, 0, 0.65); 
      padding: 8px 18px; 
      border-radius: 20px; 
      color: #ff69b4; 
      font-weight: bold;
      border: 1px solid rgba(255, 105, 180, 0.4);
      z-index: 5;
    }
  </style>
</head>
<body>

<div id="game-container">
  <img id="bg" class="scene-bg" src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1000" alt="학교">
  <img id="character" class="character" src="https://i.imgur.com/3932j64.png" alt="키타가와 마린" onerror="this.style.display='none'">
  
  <div class="stats-overlay">
    ♥ 호감도: <span id="affection-score">0</span>
  </div>

  <div id="choices-container" class="choices-container" style="display: none;"></div>

  <div id="dialogue-box" class="dialogue-box" onclick="handleDialogueClick()">
    <div id="name-tag" class="name-tag">키타가와 마린</div>
    <div id="text-content" class="text-content"></div>
    <div id="click-prompt" class="click-prompt">클릭하여 진행 ▼</div>
  </div>
</div>

<script>
const gameState = {
  affection: 0,
  currentScene: 'school_gate'
};

// 스토리 데이터 구성
const storyData = {
  // 1. 교문 앞 Encounter
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

  // 2. 복도 이동 (리액션)
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

  // 3. 교실 도착 후 연속 대화
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

  // 4. 엔딩 분기
  ending_happy: {
    name: '키타가와 마린',
    text: '아싸~! 역시 다정하다니까! 그럼 쉬는 시간 벨 울리자마자 바로 네 자리로 갈게!',
    choices: []
  },
  ending_pout: {
    name: '키타가와 마린',
    text: '에~ 피곤한 거야? 어쩔 수 없지... 그럼 졸릴 때 깨워줄 테니까 쉬어! 히히~',
    choices: []
  }
};

function renderScene(sceneKey) {
  const scene = storyData[sceneKey];
  if (!scene) return;

  document.getElementById('name-tag').innerText = scene.name;
  document.getElementById('text-content').innerText = scene.text;
  document.getElementById('affection-score').innerText = gameState.affection;

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
        selectChoice(choice);
      };
      choicesContainer.appendChild(button);
    });
  } else {
    choicesContainer.style.display = 'none';
    clickPrompt.style.display = scene.nextScene ? 'block' : 'none';
  }
}

function selectChoice(choice) {
  gameState.affection += choice.affectionDelta;
  gameState.currentScene = choice.nextScene;
  renderScene(choice.nextScene);
}

function handleDialogueClick() {
  const current = storyData[gameState.currentScene];
  // 선택지가 없는 대화창 클릭 시 다음 장면으로 이동
  if (current && current.nextScene && (!current.choices || current.choices.length === 0)) {
    gameState.currentScene = current.nextScene;
    renderScene(current.nextScene);
  }
}

// 게임 시작
renderScene('school_gate');
</script>

</body>
</html>
