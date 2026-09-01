<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>그 비스크 돌은 사랑을 한다 - 준서 루트</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', -apple-system, sans-serif; user-select: none; }
    body { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #0a0a0c; color: #fff; }

    /* 게임 화면 컨테이너 */
    #game-container {
      width: 800px;
      height: 500px;
      position: relative;
      overflow: hidden;
      border-radius: 16px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
      background: #1a1a1a;
    }

    /* 배경 이미지 */
    .scene-bg { 
      width: 100%; 
      height: 100%; 
      object-fit: cover; 
      position: absolute; 
      top: 0; 
      left: 0; 
      filter: brightness(0.85);
    }

    /* 캐릭터 일러스트 */
    .character { 
      height: 95%; 
      position: absolute; 
      bottom: 0; 
      left: 50%; 
      transform: translateX(-50%); 
      transition: all 0.3s ease-in-out;
      pointer-events: none;
    }

    /* 대화창 상자 */
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

    /* 선택지 메뉴 */
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

    /* 호감도 표시 */
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
  <img id="bg" class="scene-bg" src="https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1000" alt="배경">
  
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
  currentScene: 'start'
};

const storyData = {
  start: {
    name: '키타가와 마린',
    text: '준서야! 오늘 방과 후에 시간 있어? 같이 코스프레 의상 재료 보러 가자!',
    choices: [
      { text: '좋아! 같이 가자.', nextScene: 'agree', affectionDelta: 10 },
      { text: '미안, 오늘은 좀 바쁜데...', nextScene: 'decline', affectionDelta: -5 }
    ]
  },
