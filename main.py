<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', -apple-system, sans-serif; }
body { display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #121212; color: #fff; }

#game-container {
  width: 800px;
  height: 500px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  background: #222;
}

.scene-bg { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; filter: brightness(0.9); }
.character { height: 90%; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); transition: all 0.3s ease; }

.dialogue-box {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  background: rgba(20, 20, 25, 0.85);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 105, 180, 0.5);
  border-radius: 12px;
  padding: 20px;
  color: #fff;
}

.name-tag { font-weight: bold; font-size: 1.1rem; color: #ff69b4; margin-bottom: 8px; }
.text-content { font-size: 1rem; line-height: 1.5; min-height: 48px; }

.choices-container {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 10;
}

.choice-btn {
  background: rgba(255, 255, 255, 0.9);
  color: #222;
  border: none;
  padding: 14px 20px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.choice-btn:hover { background: #ff69b4; color: #fff; transform: translateY(-2px); }
.stats-overlay { position: absolute; top: 15px; right: 20px; background: rgba(0,0,0,0.6); padding: 8px 16px; border-radius: 20px; color: #ff69b4; }
</style>

<div id="game-container">
  <img id="bg" class="scene-bg" src="https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1000" alt="background">
  <img id="character" class="character" src="" alt="Marin">
  
  <div class="stats-overlay">
    ♥ 호감도: <span id="affection-score">0</span>
  </div>

  <div id="choices-container" class="choices-container" style="display: none;"></div>

  <div id="dialogue-box" class="dialogue-box">
    <div id="name-tag" class="name-tag">키타가와 마린</div>
    <div id="text-content" class="text-content"></div>
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
  agree: {
    name: '키타가와 마린',
    text: '진짜?! 역시 준서가 최고야! 그럼 원단 보고 맛있는 파페도 먹으러 가자!',
    choices: [
      { text: '마린이 네가 좋아하는 거라면 얼마든지.', nextScene: 'confess_setup', affectionDelta: 20 }
    ]
  },
  decline: {
    name
