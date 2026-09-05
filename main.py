import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 격투 게임 - GOD 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (사람 형태 캐릭터 & 신성 음성 개편)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    body { background-color: #111; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; user-select: none; }
    canvas { background: #1a1a24; border: 4px solid #555; display: block; margin: 10px auto; outline: none; }
    .notice { color: #ffeb3b; font-weight: bold; margin: 10px 0 5px 0; font-size: 16px; }
    .info { font-size: 13px; color: #ccc; background: #222; padding: 8px; display: inline-block; border-radius: 5px; }
</style>
</head>
<body>
    <div class="notice">⚠️ 게임 화면을 마우스로 '클릭'해야 소리와 키보드가 정상 작동합니다!</div>
    <div class="info">
        <b>[1P 조작]</b> 이동: A, D | 점프: W | 공격: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, → | 점프: ↑ | 공격: K | 궁극기: L
    </div>
    <canvas id="gameCanvas" width="950" height="480" tabindex="0"></canvas>

<script>
(function() {
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");

    // Web Audio API 사운드
    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();

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
            osc.frequency.setValueAtTime(150 * pitch, now);
            osc.frequency.exponentialRampToValueAtTime(30 * pitch, now + 0.1);
            gain.gain.setValueAtTime(0.3, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
            osc.start(now);
            osc.stop(now + 0.1);
        } else if (type === 'godHit') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.exponentialRampToValueAtTime(30, now + 0.3);
            gain.gain.setValueAtTime(0.7, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
            osc.start(now);
            osc.stop(now + 0.3);
        } else if (type === 'ult') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(80 * pitch, now);
            osc.frequency.linearRampToValueAtTime(500 * pitch, now + 0.35);
            gain.gain.setValueAtTime(0.5, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
            osc.start(now);
            osc.stop(now + 0.35);
        }
    }

    // 개편된 웅장한 신성 음성 (속도 0.6, 피치 0.2로 극저음 설정)
    function speakPraise(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'ko-KR';
            msg.pitch = 0.2; 
            msg.rate = 0.65;  
            window.speechSynthesis.speak(msg);
        }
    }

    var CHARACTERS = [
        { name: "⚡배준서 (GOD)⚡", color: "#A855F7", hp: 1000, speed: 15, atk: 100, ult: 500, soundPitch: 0.5, isGod: true },
        { name: "카즈야", color: "#EF4444", hp: 100, speed: 5, atk: 10, ult: 30, soundPitch: 0.8 },
        { name: "진", color: "#22C55E", hp: 90, speed: 6, atk: 8, ult: 25, soundPitch: 1.0 },
        { name: "폴", color: "#EAB308", hp: 120, speed: 4, atk: 15, ult: 40, soundPitch: 0.7 },
        { name: "로우", color: "#EC4899", hp: 85, speed: 7, atk: 7, ult: 22, soundPitch: 1.4 },
        { name: "킹", color: "#06B6D4", hp: 110, speed: 5, atk: 12, ult: 35, soundPitch: 0.6 },
        { name: "니나", color: "#F472B6", hp: 95, speed: 7, atk: 9, ult: 28, soundPitch: 1.5 },
        { name: "화랑", color: "#F97316", hp: 90, speed: 8, atk: 8, ult: 26, soundPitch: 1.2 },
        { name: "요시미츠", color: "#14B8A6", hp: 105, speed: 6, atk: 11, ult: 32, soundPitch: 1.1 },
        { name: "브라이언", color: "#64748B", hp: 115, speed: 4, atk: 14, ult: 38, soundPitch: 0.75 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var p1 = {}, p2 = {};

    window.addEventListener("click", function() { 
        canvas.focus();
        if (audioCtx.state === 'suspended') audioCtx.resume();
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
                        speakPraise("시공을 초월한 절대신, 배준서 님께서 강림하셨다.");
                    }
                }
            }
            if (!p2Ready) {
                if (e.key === 'ArrowLeft' || e.code === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'ArrowRight' || e.code === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
                if (e.key === 'k' || e.key === 'K' || e.code === 'KeyK') {
                    p2Ready = true;
                    if (CHARACTERS[p2Sel].isGod) {
                        speakPraise("모두 무릎을 꿇어라. 파멸의 절대존엄 배준서 님이다.");
                    }
                }
            }
            if (p1Ready && p2Ready) startGame();
        }
    });

    window.addEventListener("keyup", function(e) {
        keys[e.key] = false;
        keys[e.code] = false;
    });

    function startGame() {
        var c1 = CHARACTERS[p1Sel];
        var c2 = CHARACTERS[p2Sel];

        p1 = {
            x: 150, y: 310, w: 40, h: 100, color: c1.color, name: c1.name,
            hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            soundPitch: c1.soundPitch, isGod: c1.isGod, facing: 1,
            vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        p2 = {
            x: 750, y: 310, w: 40, h: 100, color: c2.color, name: c2.name,
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
            p.vy = -14;
            p.isJumping = true;
        }

        p.vy += 0.8;
        p.y += p.vy;

        if (p.y >= 310) {
            p.y = 310;
            p.isJumping = false;
        }

        p.x = Math.max(20, Math.min(canvas.width - p.w - 20, p.x));

        if ((keys[a1] || keys[a2]) && !p.attacking) {
            doAttack(p, enemy, p.atk, 70, false);
        }
        if ((keys[u1] || keys[u2]) && !p.attacking && p.ultGauge >= 100) {
            doAttack(p, enemy, p.ultAtk, 140, true);
            p.ultGauge = 0;
        }
    }

    function doAttack(p, enemy, damage, range, isUlt) {
        p.attacking = true;
        var box = {
            x: p.facing === 1 ? p.x + p.w : p.x - range,
            y: p.y,
            w: range,
            h: p.h
        };
        p.attackBox = box;

        if (box.x < enemy.x + enemy.w && box.x + box.w > enemy.x &&
            box.y < enemy.y + enemy.h && box.y + box.h > enemy.y) {
            enemy.hp = Math.max(0, enemy.hp - damage);
            if (!isUlt) p.ultGauge = Math.min(100, p.ultGauge + 50);

            if (isUlt) {
                playSound('ult', p.soundPitch);
            } else if (p.isGod) {
                playSound('godHit', 1.0);
            } else {
                playSound('hit', enemy.soundPitch);
            }
        }

        setTimeout(function() {
            p.attacking = false;
            p.attackBox = null;
        }, 150);
    }

    // 사람 형태 (머리, 몸통, 팔, 다리, 눈) 그리기 함수
    function drawHumanoid(p) {
        var cx = p.x + p.w / 2;
        var topY = p.y;

        ctx.strokeStyle = p.color;
        ctx.fillStyle = p.color;
        ctx.lineWidth = 5;
        ctx.lineCap = "round";

        // 배준서 후광 오라 효과
        if (p.isGod) {
            ctx.beginPath();
            ctx.arc(cx, topY + 12, 22, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(168, 85, 247, 0.3)";
            ctx.fill();
        }

        // 1. 머리
        ctx.beginPath();
        ctx.arc(cx, topY + 12, 12, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();

        // 눈
        ctx.fillStyle = "#FFF";
        var eyeX = cx + (p.facing * 4);
        ctx.fillRect(eyeX, topY + 9, 3, 3);

        // 2. 몸통
        ctx.beginPath();
        ctx.moveTo(cx, topY + 24);
        ctx.lineTo(cx, topY + 60);
        ctx.stroke();

        // 3. 다리
        ctx.beginPath();
        if (p.isJumping) {
            ctx.moveTo(cx, topY + 60);
            ctx.lineTo(cx - 12, topY + 80);
            ctx.moveTo(cx, topY + 60);
            ctx.lineTo(cx + 12, topY + 75);
        } else {
            ctx.moveTo(cx, topY + 60);
            ctx.lineTo(cx - 10, topY + 98);
            ctx.moveTo(cx, topY + 60);
            ctx.lineTo(cx + 10, topY + 98);
        }
        ctx.stroke();

        // 4. 팔
        ctx.beginPath();
        if (p.attacking) {
            // 공격 시 펀치 동작
            ctx.moveTo(cx, topY + 35);
            ctx.lineTo(cx + (p.facing * 35), topY + 35);
            ctx.moveTo(cx, topY + 35);
            ctx.lineTo(cx - (p.facing * 10), topY + 48);
        } else {
            // 기본 방어 자세
            ctx.moveTo(cx, topY + 35);
            ctx.lineTo(cx + (p.facing * 15), topY + 50);
            ctx.moveTo(cx, topY + 35);
            ctx.lineTo(cx - (p.facing * 12), topY + 52);
        }
        ctx.stroke();
    }

    function drawSelectScreen() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#FFF";
        ctx.font = "bold 20px sans-serif";
        ctx.fillText("캐릭터 선택 (1P: A/D/F선택 | 2P: 방향키/K선택)", 260, 40);

        CHARACTERS.forEach(function(c, i) {
            var row = Math.floor(i / 5);
            var col = i % 5;
            var x = 35 + col * 175;
            var y = 80 + row * 180;

            ctx.fillStyle = "#222230";
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
            ctx.fillText("이동속도: " + c.speed, x + 10, y + 110);
            ctx.fillText("궁극기: " + c.ult, x + 10, y + 135);

            if (p1Sel === i) {
                ctx.strokeStyle = "#FF3333";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 2, y - 2, 159, 164);
                ctx.fillStyle = "#FF3333";
                ctx.fillText(p1Ready ? "1P (확정)" : "1P", x + 10, y - 8);
            }
            if (p2Sel === i) {
                ctx.strokeStyle = "#00FFFF";
                ctx.lineWidth = 4;
                ctx.strokeRect(x - 4, y - 4, 163, 168);
                ctx.fillStyle = "#00FFFF";
                ctx.fillText(p2Ready ? "2P (확정)" : "2P", x + 100, y - 8);
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

            // 바닥
            ctx.strokeStyle = "#444";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(0, 410);
            ctx.lineTo(canvas.width, 410);
            ctx.stroke();

            // 캐릭터 사람 형태로 그리기
            drawHumanoid(p1);
            drawHumanoid(p2);

            // 공격 이펙트
            if (p1.attackBox) {
                ctx.fillStyle = "rgba(255, 51, 51, 0.4)";
                ctx.fillRect(p1.attackBox.x, p1.attackBox.y + 20, p1.attackBox.w, 30);
            }
            if (p2.attackBox) {
                ctx.fillStyle = "rgba(0, 255, 255, 0.4)";
                ctx.fillRect(p2.attackBox.x, p2.attackBox.y + 20, p2.attackBox.w, 30);
            }

            // 체력바 & 궁극기바 UI
            ctx.fillStyle = "#333"; ctx.fillRect(30, 20, 320, 20);
            ctx.fillStyle = "#FF3333"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 320, 20);
            ctx.fillStyle = "#A855F7"; ctx.fillRect(30, 43, (p1.ultGauge / 100) * 320, 6);

            ctx.fillStyle = "#333"; ctx.fillRect(600, 20, 320, 20);
            ctx.fillStyle = "#00FFFF"; ctx.fillRect(600, 20, (p2.hp / p2.maxHp) * 320, 20);
            ctx.fillStyle = "#A855F7"; ctx.fillRect(600, 43, (p2.ultGauge / 100) * 320, 6);

            ctx.fillStyle = "#FFF"; ctx.font = "bold 15px sans-serif";
            ctx.fillText("1P: " + p1.name, 30, 15);
            ctx.fillText("2P: " + p2.name, 600, 15);

            if (p1.hp <= 0 || p2.hp <= 0) gameState = "END";
        } else if (gameState === "END") {
            ctx.fillStyle = "#FFD700";
            ctx.font = "bold 40px sans-serif";
            var winTxt = p1.hp > 0 ? "1P 승리!" : "2P 승리!";
            ctx.fillText(winTxt, 410, 240);
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
