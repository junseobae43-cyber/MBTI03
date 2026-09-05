import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 레트로 격투 - GOD 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (NO BATIDAO Extended 원곡 재생)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    body { background-color: #0b0b10; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; user-select: none; }
    canvas { background: #13111c; border: 4px solid #3b82f6; display: block; margin: 10px auto; outline: none; box-shadow: 0 0 25px rgba(59,130,246,0.6); }
    .notice { color: #60a5fa; font-weight: bold; margin: 10px 0 5px 0; font-size: 16px; text-shadow: 0 0 8px #3b82f6; }
    .info { font-size: 13px; color: #ccc; background: #1e1b2e; padding: 8px; display: inline-block; border-radius: 5px; border: 1px solid #3b82f6; }
    #yt-player { position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
</style>
</head>
<body>
    <div class="notice">🔊 화면을 마우스로 클릭하면 유튜브 NO BATIDAO (Extended) 원곡 BGM이 재생됩니다!</div>
    <div class="info">
        <b>[1P 조작]</b> 이동: A, D | 점프: W | 공격: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, → | 점프: ↑ | 공격: K | 궁극기: L <br>
        <span style="color: #60a5fa;"><b>[게임 종료 후]</b> <b>R</b> 키를 누르면 재시작!</span>
    </div>
    
    <!-- 유튜브 원곡 NO BATIDAO (Extended) 플레이어 -->
    <iframe id="yt-player" src="https://www.youtube.com/embed/YXxdETZ9npU?enablejsapi=1&autoplay=0&loop=1&playlist=YXxdETZ9npU" allow="autoplay"></iframe>

    <canvas id="gameCanvas" width="950" height="480" tabindex="0"></canvas>

<script>
(function() {
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");

    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var ytPlayer = document.getElementById("yt-player");

    // 🔊 특정 요청 대사
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

    // Voice Synthesis System
    function speakText(text, pitch, rate) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'ko-KR';
            msg.pitch = pitch || 0.2;
            msg.rate = rate || 0.8;
            window.speechSynthesis.speak(msg);
        }
    }

    function playBGM() {
        if (ytPlayer && ytPlayer.contentWindow) {
            ytPlayer.contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
        }
    }

    function playSound(type, pitchMultiplier) {
        if (audioCtx.state === 'suspended') audioCtx.resume();
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
            gain.gain.setValueAtTime(0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
            osc.start(now);
            osc.stop(now + 0.12);
        } else if (type === 'godHit') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.exponentialRampToValueAtTime(15, now + 0.35);
            gain.gain.setValueAtTime(0.8, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
            osc.start(now);
            osc.stop(now + 0.35);
        } else if (type === 'ult') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(90 * pitch, now);
            osc.frequency.linearRampToValueAtTime(650 * pitch, now + 0.4);
            gain.gain.setValueAtTime(0.6, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
            osc.start(now);
            osc.stop(now + 0.4);
        }
    }

    var CHARACTERS = [
        { name: "⚡배준서 (GOD)⚡", color: "#A855F7", beltColor: "#FFD700", hp: 1000, speed: 15, atk: 100, ult: 500, soundPitch: 0.5, isGod: true },
        { name: "카즈야", color: "#DC2626", beltColor: "#000", hp: 100, speed: 5, atk: 10, ult: 30, soundPitch: 0.8 },
        { name: "진", color: "#16A34A", beltColor: "#000", hp: 90, speed: 6, atk: 8, ult: 25, soundPitch: 1.0 },
        { name: "폴", color: "#CA8A04", beltColor: "#000", hp: 120, speed: 4, atk: 15, ult: 40, soundPitch: 0.7 },
        { name: "로우", color: "#DB2777", beltColor: "#000", hp: 85, speed: 7, atk: 7, ult: 22, soundPitch: 1.4 },
        { name: "킹", color: "#0891B2", beltColor: "#FFF", hp: 110, speed: 5, atk: 12, ult: 35, soundPitch: 0.6 },
        { name: "니나", color: "#E11D48", beltColor: "#FFF", hp: 95, speed: 7, atk: 9, ult: 28, soundPitch: 1.5 },
        { name: "화랑", color: "#EA580C", beltColor: "#000", hp: 90, speed: 8, atk: 8, ult: 26, soundPitch: 1.2 },
        { name: "요시미츠", color: "#0D9488", beltColor: "#FFD700", hp: 105, speed: 6, atk: 11, ult: 32, soundPitch: 1.1 },
        { name: "브라이언", color: "#475569", beltColor: "#000", hp: 115, speed: 4, atk: 14, ult: 38, soundPitch: 0.75 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var p1 = {}, p2 = {};

    window.addEventListener("click", function() { 
        canvas.focus();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        playBGM();
    });

    window.addEventListener("keydown", function(e) {
        keys[e.key] = true;
        keys[e.code] = true;

        if (gameState === "SELECT") {
            if (!p1Ready) {
                if (e.key === 'a' || e.key === 'A' || e.code === 'KeyA') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'd' || e.key === 'D' || e.code === 'KeyD') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (e.key === 'f' || e.key === 'F' || e.code === 'KeyF') {
                    p1Ready = true;
                    if (CHARACTERS[p1Sel].isGod) {
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
        playBGM();
    }

    function startGame() {
        var c1 = CHARACTERS[p1Sel];
        var c2 = CHARACTERS[p2Sel];

        p1 = {
            x: 150, y: 290, w: 50, h: 110, color: c1.color, beltColor: c1.beltColor, name: c1.name,
            hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            soundPitch: c1.soundPitch, isGod: c1.isGod, facing: 1,
            vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        p2 = {
            x: 750, y: 290, w: 50, h: 110, color: c2.color, beltColor: c2.beltColor, name: c2.name,
            hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
            soundPitch: c2.soundPitch, isGod: c2.isGod, facing: -1,
            vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
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

        if (p.y >= 290) {
            p.y = 290;
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
                    playSound('ult', p.soundPitch);
                    speakText(getRandomItem(GOD_PRAISES_ULT), 0.1, 0.85);
                } else {
                    playSound('godHit', 1.0);
                    speakText(getRandomItem(GOD_PRAISES_ATTACK), 0.1, 1.1);
                }
            } else {
                if (isUlt) playSound('ult', p.soundPitch);
                else playSound('hit', enemy.soundPitch);
            }
        }

        setTimeout(function() {
            p.attacking = false;
            p.attackBox = null;
        }, 150);
    }

    function drawPixelFighter(p) {
        var x = p.x;
        var y = p.y;
        var f = p.facing;

        if (p.isGod) {
            ctx.fillStyle = "rgba(168, 85, 247, 0.35)";
            ctx.beginPath();
            ctx.arc(x + 25, y + 55, 65, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.fillStyle = p.isGod ? "#FFD700" : "#222";
        ctx.fillRect(x + 12, y, 26, 12); 
        ctx.fillStyle = "#FFDBAC";
        ctx.fillRect(x + 14, y + 10, 22, 20);

        ctx.fillStyle = p.color;
        ctx.fillRect(x + 12, y + 10, 26, 6);
        ctx.fillStyle = "#000";
        var eyeX = f === 1 ? x + 26 : x + 16;
        ctx.fillRect(eyeX, y + 18, 4, 4);

        ctx.fillStyle = p.color;
        ctx.fillRect(x + 10, y + 30, 30, 35);

        ctx.fillStyle = p.beltColor;
        ctx.fillRect(x + 8, y + 65, 34, 6);

        ctx.fillStyle = "#111";
        if (p.isJumping) {
            ctx.fillRect(x + 6, y + 71, 16, 25);
            ctx.fillRect(x + 26, y + 71, 18, 20);
        } else {
            ctx.fillRect(x + 8, y + 71, 15, 35);
            ctx.fillRect(x + 27, y + 71, 15, 35);
        }

        ctx.fillStyle = p.color;
        ctx.fillRect(x + 6, y + 102, 18, 8);
        ctx.fillRect(x + 26, y + 102, 18, 8);

        ctx.fillStyle = "#FFDBAC";
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
        ctx.fillStyle = "#60A5FA";
        ctx.font = "bold 22px sans-serif";
        ctx.fillText("SELECT YOUR FIGHTER", 340, 45);

        CHARACTERS.forEach(function(c, i) {
            var row = Math.floor(i / 5);
            var col = i % 5;
            var x = 35 + col * 175;
            var y = 80 + row * 180;

            ctx.fillStyle = "#1c1c2a";
            ctx.fillRect(x, y, 155, 160);

            ctx.fillStyle = c.color;
            ctx.fillRect(x, y, 155, 6);

            ctx.fillStyle = "#FFF";
            ctx.font = "bold 13px sans-serif";
            ctx.fillText(c.name, x + 8, y + 28);
            ctx.font = "12px sans-serif";
            ctx.fillStyle = "#AAA";
            ctx.fillText("체력: " + c.hp, x + 10, y + 60);
            ctx.fillText("공격력: " + c.atk, x + 10, y + 85);
            ctx.fillText("속도: " + c.speed, x + 10, y + 110);
            ctx.fillText("필살기: " + c.ult, x + 10, y + 135);

            if (p1Sel === i) {
                ctx.strokeStyle = "#FF3366";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 2, y - 2, 159, 164);
                ctx.fillStyle = "#FF3366";
                ctx.fillText(p1Ready ? "1P (READY)" : "1P", x + 10, y - 8);
            }
            if (p2Sel === i) {
                ctx.strokeStyle = "#3B82F6";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 4, y - 4, 163, 168);
                ctx.fillStyle = "#3B82F6";
                ctx.fillText(p2Ready ? "2P (READY)" : "2P", x + 85, y - 8);
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

            ctx.fillStyle = "#1e1b2e";
            ctx.fillRect(0, 400, canvas.width, 80);
            ctx.strokeStyle = "#3b82f6";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 400);
            ctx.lineTo(canvas.width, 400);
            ctx.stroke();

            drawPixelFighter(p1);
            drawPixelFighter(p2);

            if (p1.attackBox) {
                ctx.fillStyle = "rgba(255, 51, 102, 0.4)";
                ctx.fillRect(p1.attackBox.x, p1.attackBox.y, p1.attackBox.w, p1.attackBox.h);
            }
            if (p2.attackBox) {
                ctx.fillStyle = "rgba(59, 130, 246, 0.4)";
                ctx.fillRect(p2.attackBox.x, p2.attackBox.y, p2.attackBox.w, p2.attackBox.h);
            }

            ctx.fillStyle = "#222"; ctx.fillRect(30, 20, 320, 22);
            ctx.fillStyle = "#FF3366"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 320, 22);
            ctx.fillStyle = "#FFD700"; ctx.fillRect(30, 45, (p1.ultGauge / 100) * 320, 6);

            ctx.fillStyle = "#222"; ctx.fillRect(600, 20, 320, 22);
            ctx.fillStyle = "#3B82F6"; ctx.fillRect(600, 20, (p2.hp / p2.maxHp) * 320, 22);
            ctx.fillStyle = "#FFD700"; ctx.fillRect(600, 45, (p2.ultGauge / 100) * 320, 6);

            ctx.fillStyle = "#FFF"; ctx.font = "bold 15px sans-serif";
            ctx.fillText("1P: " + p1.name, 30, 15);
            ctx.fillText("2P: " + p2.name, 600, 15);

            if (p1.hp <= 0 || p2.hp <= 0) {
                gameState = "END";
                var winner = p1.hp > 0 ? p1 : p2;
                if (winner.isGod) {
                    speakText(getRandomItem(GOD_PRAISES_WIN), 0.1, 0.7);
                }
            }
        } else if (gameState === "END") {
            ctx.fillStyle = "#FFD700";
            ctx.font = "bold 42px sans-serif";
            var winTxt = p1.hp > 0 ? "1P K.O. 승리!" : "2P K.O. 승리!";
            ctx.fillText(winTxt, 350, 210);

            ctx.fillStyle = "#60A5FA";
            ctx.font = "bold 20px sans-serif";
            ctx.fillText("Press 'R' Key to Play Again!", 330, 270);
        }

        requestAnimationFrame(loop);
    }

    loop();
})();
</script>
</body>
</html>
"""

components.html(GAME_ENGINE, height=600)
