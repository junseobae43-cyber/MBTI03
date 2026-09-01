import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="마린과의 등교길", layout="centered")

# HTML/CSS/JS 코드 래핑
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <style>
    body {
      background-color: #1a1a1a;
      color: #ffffff;
      font-family: sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    #game-box {
      width: 100%;
      max-width: 600px;
      height: 420px;
      background-color: #2a2a3a;
      border: 3px solid #ff69b4;
      border-radius: 12px;
      padding: 20px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }
    #character-area {
      height: 140px;
      background-color: #3a3a5a;
      border-radius: 8px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 20px;
      font-weight: bold;
      color: #ff69b4;
    }
    #dialogue-area {
      background-color: rgba(0, 0, 0, 0.6);
      border: 1px solid #ff69b4;
      border-radius: 8px;
      padding: 15px;
      min-height: 100px;
      cursor: pointer;
    }
    #speaker {
      color: #ff69b4;
      font-weight: bold;
      margin-bottom: 5px;
    }
    #choices {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 10px;
    }
    .btn {
      background-color: #ff69b4;
      color: white;
      border: none;
      padding: 10px;
      border-radius: 5px;
      font-weight: bold;
      cursor: pointer;
    }
    .btn:hover { background-color: #ff1493; }
    #guide {
      font-size: 12px;
      color: #aaa;
      text-align: right;
      margin-top: 5px;
    }
  </style>
</head>
<body>

<div id="game-box">
  <div id="character-area">키타가와 마린 (등교 중)</div>
  <div id="choices"></div>
  <div id="dialogue-area" onclick="nextText()">
    <div id="speaker">키타가와 마린</div>
    <div id="text"></div>
    <div id="guide">클릭해서 계속 ▶</div>
  </div>
</div>

<script>
var story = {
  step1: { text: "야호~! 좋은 아침! 교문 앞에서 딱 만나다니 대박 완전 운 좋다~!", next: "step2", options: null },
  step2: { text: "같이 교실 올라가자! 어제 말했던 그 애니 최신화 봤어? 완전 대박이었는데!", next: null, options: [
    { msg: "응, 봤어! 연출 진짜 좋더라.", target: "step3_1" },
    { msg: "바빠서 아직 못 봤어.", target: "step3_2" }
  ]},
  step3_1: { text: "그치 그치?! 특히 주인공 변신 장면! 나 진짜 소름 돋아서 세 번이나 돌려봤잖아~!", next: "step4", options: null },
  step3_2: { text: "앗, 진짜?! 그럼 스포일러 안 하게 조심해야겠다! 오늘 집에 가자마자 꼭 봐!", next: "step4", options: null },
  step4: { text: "아 맞다! 교실 들어온 김에 말하는 건데, 다음 코스프레 캐릭터 의상 재료 말이야...", next: "step5", options: null },
  step5: { text: "원단이 생각보다 복잡해서 그런데, 혹시 쉬는 시간에 같이 인터넷으로 자재 좀 봐줄 수 있어?", next: null, options: [
    { msg: "좋아, 쉬는 시간에 같이 보자.", target: "end_happy" },
    { msg: "쉬는 시간엔 좀 자고 싶은데...", target: "end_pout" }
  ]},
  end_happy: { text: "아싸~! 역시 다정하다니까! 그럼 쉬는 시간 벨 울리자마자 바로 네 자리로 갈게!", next: null, options: null },
  end_pout: { text: "에~ 피곤한 거야? 어쩔 수 없지... 그럼 졸릴 때 깨워줄 테니까 편하게 쉬어! 히히~", next: null, options: null }
};

var currentStep = "step1";

function draw() {
  var data = story[currentStep];
  document.getElementById("text").innerText = data.text;
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

# 스트림릿에 HTML 렌더링
components.html(game_html, height=460)
