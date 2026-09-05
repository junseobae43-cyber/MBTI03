import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 철권 스타일 격투 - GOD 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (최종 완벽 수정 버전)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    body { background-color: #08080c; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; user-select: none; }
    canvas { background: #0f0d1a; border: 3px solid #3b82f6; display: block; margin: 10px auto; outline: none; box-shadow: 0 0 30px rgba(59,130,246,0.5); }
    .notice { color: #c084fc; font-weight: bold; margin: 8px 0; font-size: 15px; text-shadow: 0 0 10px #a855f7; }
    .info { font-size: 13px; color: #cbd5e1; background: #1e1b2e; padding: 8px 16px; display: inline-block; border-radius: 6px; border: 1px solid #475569; }
    #yt-player { position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
</style>
</head>
<body>
    <div class="notice">⚡ 완벽 구동 보장! 철권 8 스타일 선택 화면 & 대사 극대화 ⚡</div>
    <div class="info">
        <b>[1P 조작]</b> 이동: A, D | 점프: W | 공격: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, → | 점프: ↑ | 공격: K | 궁극기: L <br>
        <span style="color: #60a5fa;"><b>[게임 종료 후]</b> <b>R</b> 키를 누르면 재시작!</span>
    </div>
    
    <iframe id="yt-player" src="https://www.youtube.com/embed/YXxdETZ9npU?enablejsapi=1&autoplay=0&loop=1&playlist=YXxdETZ9npU" allow="autoplay"></iframe>

    <canvas id="gameCanvas" width="960" height="520" tabindex="0"></canvas>

<script>
window.addEventListener('DOMContentLoaded', function() {
    var canvas = document.getElementById("gameCanvas");
    if(!canvas) return;
    var ctx = canvas.getContext("2d");

    var audioCtx = null;
    var ytPlayer = document.getElementById("yt-player");

    var GOD_PRAISE_EXACT = "전지전능하신 천지신 세계의 왕 배준서님이 강림하셨다";

    var GOD_PRAISES_ATTACK = [
        "신벌이다!",
        "어디 감히!",
        "무릎 꿇어라!",
        "배준서 님의 일격!"
    ];

    var GOD_PRAISES_ULT = [
        "전지전능한 창세의 권능!",
        "우주 파괴의 신벌을 받아라!",
        "배준서 님 앞에 모든 만물은 소멸한다!"
    ];

    var GOD_PRAISES_WIN = [
        "전지전능하신 세계의 왕 배준서 님의 당연한 승리다!",
        "승자는 오직 절대존엄 배준서 님뿐이다!",
        "배준서 님의 위대함 앞에 패배자만 남았도다."
    ];

    function getRandomItem(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function initAudio() {
        try {
            if (!audioCtx) {
                var AudioContextClass = window.AudioContext || window.webkitAudioContext;
                if (AudioContextClass) audioCtx = new AudioContextClass();
            }
            if (audioCtx && audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        } catch(e) {}
    }

    function speakText(text, pitch, rate) {
        try {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = 'ko-KR';
                msg.pitch = pitch || 0.1;
                msg.rate = rate || 0.85;
                msg.volume = 1.0;
                window.speechSynthesis.speak(msg);
            }
        } catch(e) {}
    }

    function playBGM() {
        try {
            if (ytPlayer && ytPlayer.contentWindow) {
                ytPlayer.contentWindow.postMessage(JSON.stringify({event: 'command', func: 'setVolume', args: [20]}), '*');
                ytPlayer.contentWindow.postMessage(JSON.stringify({event: 'command', func: 'playVideo', args: ''}), '*');
            }
        } catch(e) {}
    }

    function stopBGM() {
        try {
            if (ytPlayer && ytPlayer.contentWindow) {
                ytPlayer.contentWindow.postMessage(JSON.stringify({event: 'command', func: 'pauseVideo', args: ''}), '*');
            }
        } catch(e) {}
    }

    function playSound(type, pitchMultiplier) {
        initAudio();
        if (!audioCtx) return;

        try {
            var osc = audioCtx.createOscillator();
            var gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            var now = audioCtx.currentTime;
            var pitch = pitchMultiplier || 1.0;

            if (type === 'hit') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(160 * pitch, now);
                osc.frequency.exponentialRampToValueAtTime(30 * pitch, now + 0.12);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.start(now);
                osc.stop(now + 0.12);
            } else if (type === 'godHit') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(220, now);
                osc.frequency.exponentialRampToValueAtTime(15, now + 0.35);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now);
                osc.stop(now + 0.35);
            } else if (type === 'ult') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(90 * pitch, now);
                osc.frequency.linearRampToValueAtTime(650 * pitch, now + 0.4);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
                osc.start(now);
                osc.stop(now + 0.4);
            }
        } catch(e) {}
    }

    var CHARACTERS = [
        { name: "⚡배준서 (GOD)⚡", color: "#A855F7", beltColor: "#FFD700", hairColor: "#E2E8F0", skinColor: "#FFF0E5", eyeColor: "#EF4444", hp: 1000, speed: 15, atk: 100, ult: 500, isGod: true },
        { name: "카즈야", color: "#DC2626", beltColor: "#000000", hairColor: "#1E293B", skinColor: "#F3D2C1", eyeColor: "#FF0000", hp: 100, speed: 5, atk: 10, ult: 30 },
        { name: "진 카자마", color: "#16A34A", beltColor: "#000000", hairColor: "#0F172A", skinColor: "#FFE5D9", eyeColor: "#38BDF8", hp: 90, speed: 6, atk: 8, ult: 25 },
        { name: "폴 피닉스", color: "#CA8A04", beltColor: "#000000", hairColor: "#FACC15", skinColor: "#FDE047", eyeColor: "#1E293B", hp: 120, speed: 4, atk: 15, ult: 40 },
        { name: "마샬 로우", color: "#DB2777", beltColor: "#000000", hairColor: "#18181B", skinColor: "#EAB308", eyeColor: "#000000", hp: 85, speed: 7, atk: 7, ult: 22 },
        { name: "킹", color: "#0891B2", beltColor: "#FFFFFF", hairColor: "#D97706", skinColor: "#B45309", eyeColor: "#000000", hp: 110, speed: 5, atk: 12, ult: 35 },
        { name: "니나 윌리엄스", color: "#E11D48", beltColor: "#FFFFFF", hairColor: "#FEF08A", skinColor: "#FFF0F5", eyeColor: "#2563EB", hp: 95, speed: 7, atk: 9, ult: 28 },
        { name: "화랑", color: "#EA580C", beltColor: "#000000", hairColor: "#F97316", skinColor: "#FFE4E6", eyeColor: "#1E293B", hp: 90, speed: 8, atk: 8, ult: 26 },
        { name: "요시미츠", color: "#0D9488", beltColor: "#FFD700", hairColor: "#64748B", skinColor: "#0284C7", eyeColor: "#FACC15", hp: 105, speed: 6, atk: 11, ult: 32 },
        { name: "브라이언 퓨리", color: "#475569", beltColor: "#000000", hairColor: "#94A3B8", skinColor: "#E2E8F0", eyeColor: "#DC2626", hp: 115, speed: 4, atk: 14, ult: 38 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var p1 = {}, p2 = {};

    window.addEventListener("click", function() { 
        canvas.focus();
        initAudio();
    });

    window.addEventListener("keydown", function(e) {
        initAudio();
        keys[e.key] = true;
        keys[e.code] = true;

        if (gameState === "SELECT") {
            if (!p1Ready) {
                if (e.key === 'a' || e.key === 'A' || e.code === 'KeyA') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'd' || e.key === 'D' || e.code === 'KeyD') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (e.key === 'f' || e.key === 'F' || e.code === 'KeyF') {
                    p1Ready = true;
                    if (CHARACTERS[p1Sel].isGod) {
                        playBGM();
                        speakText(GOD_PRAISE_EXACT, 0.1, 0.75);
                    }
                }
            }
            if (!p2Ready) {
                if (e.key === 'ArrowLeft' || e.code === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'ArrowRight' || e.code === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
                if (e.key === 'k' || e.key === 'K' || e.code === 'KeyK') {
                    p2Ready = true;
                    if (CHARACTERS[p2Sel].isGod) {
                        playBGM();
                        speakText(GOD_PRAISE_EXACT, 0.1, 0.75);
                    }
                }
            }
            if (p1Ready && p2Ready) startGame();
        } else if (gameState === "END") {
            if (e.key === 'r' || e.key === 'R' || e.code === 'KeyR') {
                resetToSelect();
            }
        }
    });

    window.addEventListener("keyup", function(e) {
        keys[e.key] = false;
        keys[e.code] = false;
    });

    function resetToSelect() {
        p1Ready = false;
        p2Ready = false;
        gameState = "SELECT";
        stopBGM();
    }

    function startGame() {
        var c1 = CHARACTERS[p1Sel];
        var c2 = CHARACTERS[p2Sel];

        p1 = {
            x: 150, y: 320, w: 50, h: 110, color: c1.color, beltColor: c1.beltColor,
            hairColor: c1.hairColor, skinColor: c1.skinColor, eyeColor: c1.eyeColor,
            name: c1.name, hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            isGod: c1.isGod, facing: 1, vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        p2 = {
            x: 760, y: 320, w: 50, h: 110, color: c2.color, beltColor: c2.beltColor,
            hairColor: c2.hairColor, skinColor: c2.skinColor, eyeColor: c2.eyeColor,
            name: c2.name, hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
            isGod: c2.isGod, facing: -1, vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        gameState = "PLAY";
    }

    function updatePlayer(p, enemy, l1, l2, r1, r2, j1, j2, a1, a2, u1, u2) {
        if (keys[l1] || keys[l2]) { p.x -= p.speed; p.facing = -1; }
        if (keys[r1] || keys[r2]) { p.x += p.speed; p.facing = 1; }

        if ((keys[j1] || keys[j2]) && !p.isJumping) {
            p.vy = -15;
            p.isJumping = true;
        }

        p.vy += 0.85;
        p.y += p.vy;

        if (p.y >= 320) {
            p.y = 320;
            p.isJumping = false;
        }

        p.x = Math.max(20, Math.min(canvas.width - p.w - 20, p.x));

        if ((keys[a1] || keys[a2]) && !p.attacking) {
            doAttack(p, enemy, p.atk, 85, false);
        }
        if ((keys[u1] || keys[u2]) && !p.attacking && p.ultGauge >= 100) {
            doAttack(p, enemy, p.ultAtk, 160, true);
            p.ultGauge = 0;
        }
    }

    function doAttack(p, enemy, damage, range, isUlt) {
        p.attacking = true;
        var box = {
            x: p.facing === 1 ? p.x + p.w : p.x - range,
            y: p.y + 20,
            w: range,
            h: 60
        };
        p.attackBox = box;

        if (box.x < enemy.x + enemy.w && box.x + box.w > enemy.x &&
            box.y < enemy.y + enemy.h && box.y + box.h > enemy.y) {
            enemy.hp = Math.max(0, enemy.hp - damage);
            if (!isUlt) p.ultGauge = Math.min(100, p.ultGauge + 50);

            if (p.isGod) {
                if (isUlt) {
                    playSound('ult', 0.5);
                    speakText(getRandomItem(GOD_PRAISES_ULT), 0.1, 0.8);
                } else {
                    playSound('godHit', 1.0);
                    speakText(getRandomItem(GOD_PRAISES_ATTACK), 0.1, 1.0);
                }
            } else {
                if (isUlt) playSound('ult', 1.0);
                else playSound('hit', 1.0);
            }
        }

        setTimeout(function() {
            p.attacking = false;
            p.attackBox = null;
        }, 150);
    }

    function drawFacePortrait(c, x, y, width, height) {
        ctx.fillStyle = "#111827";
        ctx.fillRect(x, y, width, height);

        if (c.isGod) {
            var grad = ctx.createRadialGradient(x + width/2, y + height/2, 5, x + width/2, y + height/2, width/1.2);
            grad.addColorStop(0, "rgba(168, 85, 247, 0.8)");
            grad.addColorStop(1, "rgba(15, 23, 42, 0)");
            ctx.fillStyle = grad;
            ctx.fillRect(x, y, width, height);
        }

        ctx.fillStyle = c.skinColor;
        ctx.beginPath();
        ctx.arc(x + width/2, y + height/2 + 5, 20, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = c.hairColor;
        if (c.isGod) {
            ctx.beginPath();
            ctx.moveTo(x + width/2 - 25, y + height/2 - 5);
            ctx.lineTo(x + width/2 - 8, y + height/2 - 30);
            ctx.lineTo(x + width/2, y + height/2 - 20);
            ctx.lineTo(x + width/2 + 12, y + height/2 - 32);
            ctx.lineTo(x + width/2 + 25, y + height/2 - 5);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = c.eyeColor;
            ctx.fillRect(x + width/2 - 12, y + height/2 + 4, 5, 4);
            ctx.fillRect(x + width/2 + 7, y + height/2 + 4, 5, 4);
        } else {
            ctx.beginPath();
            ctx.arc(x + width/2, y + height/2 - 5, 22, Math.PI, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = c.eyeColor;
            ctx.fillRect(x + width/2 - 10, y + height/2 + 2, 4, 4);
            ctx.fillRect(x + width/2 + 6, y + height/2 + 2, 4, 4);
        }
    }

    function drawPixelFighter(p) {
        var x = p.x;
        var y = p.y;
        var f = p.facing;

        if (p.isGod) {
            ctx.fillStyle = "rgba(168, 85, 247, 0.3)";
            ctx.beginPath();
            ctx.arc(x + 25, y + 55, 65, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.fillStyle = p.hairColor;
        ctx.fillRect(x + 10, y - 4, 30, 16);

        ctx.fillStyle = p.skinColor;
        ctx.fillRect(x + 14, y + 10, 22, 20);

        ctx.fillStyle = p.eyeColor;
        var eyeX = f === 1 ? x + 26 : x + 16;
        ctx.fillRect(eyeX, y + 18, 4, 4);

        ctx.fillStyle = p.color;
        ctx.fillRect(x + 10, y + 30, 30, 35);

        ctx.fillStyle = p.beltColor;
        ctx.fillRect(x + 8, y + 65, 34, 6);

        ctx.fillStyle = "#0F172A";
        if (p.isJumping) {
            ctx.fillRect(x + 6, y + 71, 16, 25);
            ctx.fillRect(x + 26, y + 71, 18, 20);
        } else {
            ctx.fillRect(x + 8, y + 71, 15, 35);
            ctx.fillRect(x + 27, y + 71, 15, 35);
        }

        ctx.fillStyle = p.skinColor;
        if (p.attacking) {
            var punchX = f === 1 ? x + 35 : x - 25;
            ctx.fillRect(punchX, y + 35, 35, 12);
            ctx.fillStyle = p.color;
            ctx.fillRect(punchX + (f === 1 ? 25 : 0), y + 33, 10, 16);
        } else {
            ctx.fillRect(f === 1 ? x + 30 : x + 2, y + 35, 14, 20);
        }
    }

    function drawSelectScreen() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#38BDF8";
        ctx.font = "bold 24px sans-serif";
        ctx.fillText("TEKKEN SELECT YOUR FIGHTER", 280, 40);

        CHARACTERS.forEach(function(c, i) {
            var row = Math.floor(i / 5);
            var col = i % 5;
            var x = 30 + col * 180;
            var y = 65 + row * 210;

            ctx.fillStyle = "#1E1B4B";
            ctx.fillRect(x, y, 160, 195);

            drawFacePortrait(c, x + 10, y + 10, 140, 95);

            ctx.fillStyle = "#FFFFFF";
            ctx.font = "bold 13px sans-serif";
            ctx.fillText(c.name, x + 8, y + 122);

            ctx.font = "11px sans-serif";
            ctx.fillStyle = "#94A3B8";
            ctx.fillText("HP: " + c.hp + " | ATK: " + c.atk, x + 10, y + 144);
            ctx.fillText("SPEED: " + c.speed, x + 10, y + 162);
            ctx.fillText("ULTIMATE: " + c.ult, x + 10, y + 180);

            if (p1Sel === i) {
                ctx.strokeStyle = "#EC4899";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 2, y - 2, 164, 199);
                ctx.fillStyle = "#EC4899";
                ctx.font = "bold 14px sans-serif";
                ctx.fillText(p1Ready ? "1P READY!" : "1P", x + 8, y - 6);
            }
            if (p2Sel === i) {
                ctx.strokeStyle = "#3B82F6";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 4, y - 4, 168, 203);
                ctx.fillStyle = "#3B82F6";
                ctx.font = "bold 14px sans-serif";
                ctx.fillText(p2Ready ? "2P READY!" : "2P", x + 90, y - 6);
            }
        });
    }

    function loop() {
        if (gameState === "SELECT") {
            drawSelectScreen();
        } else if (gameState === "PLAY") {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            updatePlayer(p1, p2, 'a', 'KeyA', 'd', 'KeyD', 'w', 'KeyW', 'f', 'KeyF', 'g', 'KeyG');
            updatePlayer(p2, p1, 'ArrowLeft', 'ArrowLeft', 'ArrowRight', 'ArrowRight', 'ArrowUp', 'ArrowUp', 'k', 'KeyK', 'l', 'KeyL');

            ctx.fillStyle = "#1E293B";
            ctx.fillRect(0, 430, canvas.width, 90);
            ctx.strokeStyle = "#38BDF8";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 430);
            ctx.lineTo(canvas.width, 430);
            ctx.stroke();

            drawPixelFighter(p1);
            drawPixelFighter(p2);

            if (p1.attackBox) {
                ctx.fillStyle = "rgba(236, 72, 153, 0.4)";
                ctx.fillRect(p1.attackBox.x, p1.attackBox.y, p1.attackBox.w, p1.attackBox.h);
            }
            if (p2.attackBox) {
                ctx.fillStyle = "rgba(59, 130, 246, 0.4)";
                ctx.fillRect(p2.attackBox.x, p2.attackBox.y, p2.attackBox.w, p2.attackBox.h);
            }

            ctx.fillStyle = "#1E1B2E"; ctx.fillRect(30, 20, 350, 24);
            ctx.fillStyle = "#EC4899"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 350, 24);
            ctx.fillStyle = "#FACC15"; ctx.fillRect(30, 48, (p1.ultGauge / 100) * 350, 6);

            ctx.fillStyle = "#1E1B2E"; ctx.fillRect(580, 20, 350, 24);
            ctx.fillStyle = "#3B82F6"; ctx.fillRect(580, 20, (p2.hp / p2.maxHp) * 350, 24);
            ctx.fillStyle = "#FACC15"; ctx.fillRect(580, 48, (p2.ultGauge / 100) * 350, 6);

            ctx.fillStyle = "#FFFFFF"; ctx.font = "bold 15px sans-serif";
            ctx.fillText("1P: " + p1.name, 30, 15);
            ctx.fillText("2P: " + p2.name, 580, 15);

            if (p1.hp <= 0 || p2.hp <= 0) {
                gameState = "END";
                var winner = p1.hp > 0 ? p1 : p2;
                if (winner.isGod) {
                    speakText(getRandomItem(GOD_PRAISES_WIN), 0.1, 0.7);
                }
            }
        } else if (gameState === "END") {
            ctx.fillStyle = "#FACC15";
            ctx.font = "bold 44px sans-serif";
            var winTxt = p1.hp > 0 ? "1P K.O. VICTORY!" : "2P K.O. VICTORY!";
            ctx.fillText(winTxt, 310, 230);

            ctx.fillStyle = "#38BDF8";
            ctx.font = "bold 20px sans-serif";
            ctx.fillText("Press 'R' Key to Play Again!", 340, 290);
        }

        requestAnimationFrame(loop);
    }

    loop();
});
</script>
</body>
</html>
"""

components.html(GAME_ENGINE, height=640)
