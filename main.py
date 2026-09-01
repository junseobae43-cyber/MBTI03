import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="마린과의 등교길", layout="centered")

# 로컬 이미지 파일 읽기
image_filename = "marin.jpg"

if os.path.exists(image_filename):
    with open(image_filename, "rb") as f:
        encoded_img = base64.b64encode(f.read()).decode()
    img_data_url = f"data:image/jpeg;base64,{encoded_img}"
else:
    # 파일이 없을 경우 예외 처리
    st.error(f"폴더 안에 '{image_filename}' 파일이 없습니다. 마린 사진을 {image_filename} 이름으로 넣어주세요!")
    img_data_url = ""

game_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      background-color: #0d0d12;
      color: #ffffff;
      font-family: -apple-system, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }}
    #game-box {{
      width: 100%;
      max-width: 650px;
      height: 580px;
      background: linear-gradient(180deg, #232538 0%, #11111a 100%);
      border: 2px solid #ff69b4;
      border-radius: 16px;
      padding: 20px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }}
    
    #character-area {{
      height: 300px;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      overflow: hidden;
      border-radius: 12px;
      background-color: #1a1a24;
      border: 1px solid rgba(255, 105, 180, 0.4);
    }}

    #marin-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center 20%;
    }}
    
    #dialogue-area {{
      background-color: rgba(18, 18, 28, 0.92);
      border: 2px solid #ff69b4;
      border-radius: 12px;
      padding: 16px 20px;
      min-height: 100px;
      cursor: pointer;
      position: relative;
      z-index: 10;
    }}
    #speaker {{
      color: #ff69b4;
      font-weight: bold;
      font-size: 1.1rem;
      margin-bottom: 6px;
      text-shadow: 0 0 5px rgba(255, 105, 180, 0.5);
    }}
    #text {{
      font-size: 1.05rem;
      line-height: 1.5;
      color: #f0f0f0;
    }}
    
    #choices {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 10px;
      z-index: 20;
    }}
    .btn {{
      background: rgba(255, 255, 255, 0.95);
      color: #111;
      border: 2px solid #ff69b4;
      padding: 12px;
      border-radius: 25px;
      font-weight: bold;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn:hover {{
      background-color: #ff69b4;
      color: white;
      transform: translateY(-2px);
    }}
    #guide {{
      font-size: 0.8rem;
      color: #ff69b4;
      text-align: right;
      margin-top: 8px;
      animation: blink 1.2s infinite;
    }}
    @keyframes blink {{
      0%, 100% {{ opacity: 0.4; }}
      50% {{ opacity: 1; }}
    }}
  </style>
</head>
<body>

<div id="game-box">
  <div id="character-area">
    <img id="marin-img" src="{img_data_url}" alt="喜多川海夢">
  </div>
  
  <div id="choices"></div>

  <div id="dialogue-area" onclick="nextText()">
    <div id="speaker">喜多川 海夢 (키타가와 마린)</div>
    <div id="text"></div>
    <div id="guide">클릭해서 계속 ▶</div>
  </div>
</div>

<script>
var story = {{
  step1: {{ 
    text: "야호~! 좋은 아침! 교문 앞에서 딱 만나다니 대박 완전 운 좋다~!", 
    jaText: "ヤッホー！おはよう！校門の前でピッタリ会えるなんて、超ウケる、運良すぎ！",
    next: "step2", 
    options: null 
  }},
  step2: {{ 
    text: "같이 교실 올라가자! 어제 말했던 그 애니 최신화 봤어? 완전 대박이었는데!", 
    jaText: "一緒に教室行こ！昨日言ってたあのアニメの最新話見た？マジでヤバかったんだけど！",
    next: null, 
    options: [
      {{ msg: "응, 봤어! 연출 진짜 좋더라.", target: "step3_1" }},
      {{ msg: "바빠서 아직 못 봤어.", target: "step3_2" }}
    ]
  }},
  step3_1: {{ 
    text: "그치 그치?! 특히 주인공 변신 장면! 나 진짜 소름 돋아서 세 번이나 돌려봤잖아~!", 
    jaText: "でしょでしょ！？特に主人公の変身シーン！マジで鳥肌立って３回も見直しちゃったし！",
    next: "step4", 
    options: null 
  }},
  step3_2: {{ 
    text: "앗, 진짜?! 그럼 스포일러 안 하게 조심해야겠다! 오늘 집에 가자마자 꼭 봐!", 
    jaText: "あ、マジで！？じゃあネタバレしないように気をつけるね！今日家に帰ったら絶対見てよ！",
    next: "step4", 
    options: null 
  }},
  step4: {{ 
    text: "아 맞다! 교실 들어온 김에 말하는 건데, 다음 코스프레 캐릭터 의상 재료 말이야...", 
    jaText: "あ、そうだ！せっかく教室入ったから言うんだけど、次のコスプレキャラの衣装の材料なんだけどね…",
    next: "step5", 
    options: null 
  }},
  step5: {{ 
    text: "원단이 생각보다 복잡해서 그런데, 혹시 쉬는 시간에 같이 인터넷으로 자재 좀 봐줄 수 있어?", 
    jaText: "生地が思ったより複雑でさ…もし良かったら休み時間に一緒にネットで資材見てくれない？",
    next: null, 
    options: [
      {{ msg: "좋아, 쉬는 시간에 같이 보자.", target: "end_happy" }},
      {{ msg: "쉬는 시간엔 좀 자고 싶은데...", target: "end_pout" }}
    ]
  }},
  end_happy: {{ 
    text: "아싸~! 역시 다정하다니까! 그럼 쉬는 시간 벨 울리자마자 바로 네 자리로 갈게!", 
    jaText: "やった〜！やっぱり優しい！じゃあ休み時間のチャイムが鳴ったらすぐ席行くね！",
    next: null, 
    options: null 
  }},
  end_pout: {{ 
    text: "에~ 피곤한 거야? 어쩔 수 없지... 그럼 졸릴 때 깨워줄 테니까 편하게 쉬어! 히히~", 
    jaText: "え〜疲れてるの？しゃーないなー…じゃあ眠そうな時起こしてあげるからゆっくり休んでね！ヘヘッ！",
    next: null, 
    options: null 
  }}
}};

var currentStep = "step1";

function speak(text) {{
  if ('speechSynthesis' in window) {{
    window.speechSynthesis.cancel();
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ja-JP';
    utterance.pitch = 1.45; 
    utterance.rate = 1.15;

    var voices = window.speechSynthesis.getVoices();
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang.includes('ja') || voices[i].lang.includes('JP')) {{
        utterance.voice = voices[i];
        break;
      }}
    }}
    window.speechSynthesis.speak(utterance);
  }}
}}

function draw() {{
  var data = story[currentStep];
  document.getElementById("text").innerText = data.text;
  speak(data.jaText);

  var choiceDiv = document.getElementById("choices");
  var guideDiv = document.getElementById("guide");
  choiceDiv.innerHTML = "";

  if (data.options) {{
    guideDiv.style.display = "none";
    for (var i = 0; i < data.options.length; i++) {{
      (function(opt) {{
        var button = document.createElement("button");
        button.className = "btn";
        button.innerText = opt.msg;
        button.onclick = function() {{ currentStep = opt.target; draw(); }};
        choiceDiv.appendChild(button);
      }})(data.options[i]);
    }}
  }} else {{
    guideDiv.style.display = data.next ? "block" : "none";
  }}
}}

function nextText() {{
  var data = story[currentStep];
  if (!data.options && data.next) {{
    currentStep = data.next;
    draw();
  }}
}}

if (speechSynthesis.onvoiceschanged !== undefined) {{
  speechSynthesis.onvoiceschanged = draw;
}}

draw();
</script>
</body>
</html>
"""

components.html(game_html, height=620)
