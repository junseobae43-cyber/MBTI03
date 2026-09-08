import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ARCADE TEKKEN - HUMAN EDITION", page_icon="🥊", layout="wide"
)

st.title("🕹️ 오락실 스타일 2P 철권 (인간형 캐릭터 에디션)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    * { box-sizing: border-box; }
    body { background-color: #050508; color: white; text-align: center; font-family: 'Press Start 2P', cursive, sans-serif; margin: 0; padding: 10px; user-select: none; overflow: hidden; }
    .arcade-frame {
        border: 4px solid #ef4444;
        border-radius: 12px;
        box-shadow: 0 0 20px #ef4444, inset 0 0 15px rgba(239, 68, 68, 0.5);
        display: inline-block;
        padding: 8px;
        background: #000;
    }
    canvas { background: #090912; display: block; margin: 0 auto; outline: none; cursor: pointer; }
    .controls-guide { font-family: sans-serif; font-size: 13px; color: #cbd5e1; background: #111827; padding: 8px 16px; border-radius: 8px; border: 1px solid #374151; margin-top: 8px; display: inline-block; }
</style>
</head>
<body>
    <div class="arcade-frame">
        <canvas id="gameCanvas" width="960" height="520" tabindex="0"></canvas>
    </div>
    <br>
    <div class="controls-guide">
        <b>[1P]</b> 이동: A, D | 점프: W | 가드: <b>S</b> | 공격(주먹/킥): F | 궁극기: G | 잡기: T<br>
        <b>[2P]</b> 이동: ←, → | 점프: ↑ | 가드: <b>↓</b> | 공격(주먹/킥): K | 궁극기: L | 잡기: P
    </div>

<script>
function runGame() {
    var canvas = document.getElementById("gameCanvas");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");

    var audioCtx = null;
    var particles = [];
    var hitEffects = [];
    var announcerText = { text: "READY...", opacity: 1, scale: 1.5, life: 100 };

    function initAudio() {
        try {
            if (!audioCtx) {
                var AudioContextClass = window.AudioContext || window.webkitAudioContext;
                if (AudioContextClass) audioCtx = new AudioContextClass();
            }
            if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
        } catch(e) {}
    }

    function playSound(type) {
        try {
            initAudio();
            if (!audioCtx) return;
            var osc = audioCtx.createOscillator();
            var gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            var now = audioCtx.currentTime;

            if (type === 'hit') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.exponentialRampToValueAtTime(50, now + 0.12);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.start(now); osc.stop(now + 0.12);
            } else if (type === 'heavy') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(160, now);
                osc.frequency.exponentialRampToValueAtTime(20, now + 0.3);
                gain.gain.setValueAtTime(0.6, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.start(now); osc.stop(now + 0.3);
            } else if (type === 'block') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(450, now);
                osc.frequency.exponentialRampToValueAtTime(180, now + 0.08);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
                osc.start(now); osc.stop(now + 0.08);
            }
        } catch(e) {}
    }

    function speak(text) {
        try {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = 'en-US';
                msg.rate = 1.0;
                msg.pitch = 0.6;
                window.speechSynthesis.speak(msg);
            }
        } catch(e) {}
    }

    var CHARACTERS = [
        { name: "KAZUYA", color: "#DC2626", skin: "#fca5a5", hair: "#111827", hp: 200, speed: 8, atk: 22, ult: 85 },
        { name: "JIN", color: "#16A34A", skin: "#fed7aa", hair: "#1f2937", hp: 195, speed: 9, atk: 21, ult: 80 },
        { name: "PAUL", color: "#CA8A04", skin: "#fde047", hair: "#fef08a", hp: 230, speed: 6, atk: 28, ult: 95 },
        { name: "LAW", color: "#DB2777", skin: "#fcd34d", hair: "#000000", hp: 180, speed: 10, atk: 20, ult: 75 },
        { name: "KING", color: "#0891B2", skin: "#fdba74", hair: "#d97706", hp: 220, speed: 7, atk: 25, ult: 90 },
        { name: "NINA", color: "#E11D48", skin: "#fecdd3", hair: "#fef08a", hp: 185, speed: 9, atk: 21, ult: 78 },
        { name: "HWOARANG", color: "#EA580C", skin: "#fed7aa", hair: "#dc2626", hp: 180, speed: 11, atk: 19, ult: 72 },
        { name: "YOSHIMITSU", color: "#0D9488", skin: "#94a3b8", hair: "#475569", hp: 210, speed: 8, atk: 23, ult: 88 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var p1 = {}, p2 = {};
    var animFrame = 0;

    canvas.focus();
    window.addEventListener("click", function() { if (canvas) canvas.focus(); initAudio(); });

    window.addEventListener("keydown", function(e) {
        initAudio();
        if (!e) return;
        var k = e.key ? e.key.toLowerCase() : "";
        var c = e.code ? e.code : "";

        if (!keys[k] && !keys[c]) {
            if (gameState === "PLAY") {
                if (k === 'w' || c === 'KeyW') handleJump(p1);
                if (k === 'arrowup' || c === 'ArrowUp') handleJump(p2);

                if (k === 'f' || c === 'KeyF') handleAttack(p1, p2, 'normal');
                if (k === 'g' || c === 'KeyG') handleAttack(p1, p2, 'ult');
                if (k === 't' || c === 'KeyT') handleAttack(p1, p2, 'grab');

                if (k === 'k' || c === 'KeyK') handleAttack(p2, p1, 'normal');
                if (k === 'l' || c === 'KeyL') handleAttack(p2, p1, 'ult');
                if (k === 'p' || c === 'KeyP') handleAttack(p2, p1, 'grab');
            }
        }

        keys[k] = true; keys[c] = true;

        if (gameState === "SELECT") {
            if (!p1Ready) {
                if (k === 'a' || c === 'KeyA') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (k === 'd' || c === 'KeyD') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (k === 'f' || c === 'KeyF') p1Ready = true;
            }
            if (!p2Ready) {
                if (k === 'arrowleft' || c === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (k === 'arrowright' || c === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
                if (k === 'k' || c === 'KeyK') p2Ready = true;
            }
            if (p1Ready && p2Ready) startGame();
        } else if (gameState === "END") {
            if (k === 'r' || c === 'KeyR') resetToSelect();
        }
    });

    window.addEventListener("keyup", function(e) {
        if (!e) return;
        var k = e.key ? e.key.toLowerCase() : "";
        var c = e.code ? e.code : "";
        keys[k] = false; keys[c] = false;
    });

    function handleJump(p) {
        if (p.jumpCount < 2) {
            p.vy = -15;
            p.jumpCount++;
        }
    }

    function resetToSelect() {
        p1Ready = false; p2Ready = false;
        gameState = "SELECT";
        particles = []; hitEffects = [];
    }

    function startGame() {
        var c1 = CHARACTERS[p1Sel];
        var c2 = CHARACTERS[p2Sel];

        p1 = {
            x: 180, y: 300, w: 50, h: 120, color: c1.color, skin: c1.skin, hair: c1.hair, name: c1.name,
            hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            facing: 1, vy: 0, jumpCount: 0, ultGauge: 0, comboCount: 0,
            attacking: false, attackType: 'punch', attackCooldown: false, isGuarding: false, hitStun: 0, isMoving: false
        };

        p2 = {
            x: 720, y: 300, w: 50, h: 120, color: c2.color, skin: c2.skin, hair: c2.hair, name: c2.name,
            hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
            facing: -1, vy: 0, jumpCount: 0, ultGauge: 0, comboCount: 0,
            attacking: false, attackType: 'punch', attackCooldown: false, isGuarding: false, hitStun: 0, isMoving: false
        };

        gameState = "PLAY";
        announcerText = { text: "FIGHT!", opacity: 1, scale: 2.5, life: 60 };
        speak("FIGHT");
    }

    function handleAttack(p, enemy, type) {
        if (p.isGuarding || p.attacking || p.attackCooldown || p.hitStun > 0) return;

        p.attacking = true;
        p.attackCooldown = true;
        p.comboCount = (p.comboCount % 3) + 1;
        p.attackType = type === 'ult' ? 'ult' : (type === 'grab' ? 'grab' : (p.comboCount === 3 ? 'kick' : 'punch'));

        var range = type === 'ult' ? 180 : (type === 'grab' ? 70 : 110);
        var baseDmg = type === 'ult' ? p.ultAtk : (type === 'grab' ? Math.floor(p.atk * 1.3) : p.atk + (p.comboCount * 5));

        var hitBox = { x: p.facing === 1 ? p.x : p.x - range, y: p.y + 10, w: p.w + range, h: 80 };

        if (hitBox.x < enemy.x + enemy.w && hitBox.x + hitBox.w > enemy.x &&
            hitBox.y < enemy.y + enemy.h && hitBox.y + hitBox.h > enemy.y) {
            
            var targetX = enemy.x + enemy.w / 2;
            var targetY = enemy.y + 30;

            if (enemy.isGuarding && type !== 'grab') {
                enemy.hp -= Math.max(1, Math.floor(baseDmg * 0.15));
                playSound('block');
                addSparks(targetX, targetY, "#38BDF8", 8);
                hitEffects.push({ x: targetX, y: targetY, text: "GUARD", color: "#38BDF8", life: 30, scale: 1 });
            } else {
                enemy.hp = Math.max(0, enemy.hp - baseDmg);
                enemy.hitStun = 14;
                enemy.x += p.facing * (type === 'ult' ? 45 : 20);

                if (type === 'ult') {
                    playSound('heavy');
                    addSparks(targetX, targetY, "#EF4444", 25);
                    hitEffects.push({ x: targetX, y: targetY - 20, text: "K.O. HIT!", color: "#EF4444", life: 45, scale: 2 });
                } else {
                    playSound('hit');
                    addSparks(targetX, targetY, "#FACC15", 15);
                    var msg = p.comboCount === 3 ? "HIGH KICK!" : (type === 'grab' ? "THROW!" : "PUNCH!");
                    hitEffects.push({ x: targetX, y: targetY - 10, text: msg, color: "#FACC15", life: 35, scale: 1.3 });
                }

                if (type !== 'ult') p.ultGauge = Math.min(100, p.ultGauge + 18);
            }
        }

        setTimeout(function() { p.attacking = false; }, 200);
        setTimeout(function() { p.attackCooldown = false; }, 320);
    }

    function addSparks(x, y, color, count) {
        for (var i = 0; i < count; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 16,
                vy: (Math.random() - 0.5) * 16,
                size: Math.random() * 6 + 3,
                color: color, life: 1.0
            });
        }
    }

    function updatePlayer(p, enemy, lKey, rKey, gKey) {
        p.isGuarding = !!(keys[gKey]);
        p.isMoving = false;

        if (p.hitStun > 0) p.hitStun--;

        if (!p.isGuarding && p.hitStun === 0) {
            if (keys[lKey]) { p.x -= p.speed; p.facing = -1; p.isMoving = true; }
            if (keys[rKey]) { p.x += p.speed; p.facing = 1; p.isMoving = true; }
        }

        p.vy += 0.9;
        p.y += p.vy;

        if (p.y >= 300) {
            p.y = 300; p.vy = 0; p.jumpCount = 0;
        }

        p.x = Math.max(30, Math.min(canvas.width - p.w - 30, p.x));
    }

    function drawStage() {
        ctx.fillStyle = "#0c0a1d";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = "#1e1b4b";
        ctx.lineWidth = 2;
        for (var i = 0; i < canvas.width; i += 60) {
            ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 380); ctx.stroke();
        }

        var grad = ctx.createLinearGradient(0, 380, 0, 520);
        grad.addColorStop(0, "#1e293b");
        grad.addColorStop(1, "#0f172a");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 380, canvas.width, 140);

        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(0, 380); ctx.lineTo(canvas.width, 380); ctx.stroke();
    }

    // 인간형 파이터 그리기
    function drawHumanFighter(p) {
        var x = p.x + p.w / 2;
        var y = p.y;
        var dir = p.facing;

        // 바닥 그림자
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.beginPath();
        ctx.ellipse(x, 420, 30, 10, 0, 0, Math.PI * 2);
        ctx.fill();

        if (p.hitStun > 0) x += (Math.random() - 0.5) * 8;

        var legSwing = p.isMoving ? Math.sin(animFrame * 0.2) * 15 : 0;

        ctx.lineWidth = 8;
        ctx.lineCap = "round";

        // 다리 (바지/도복)
        ctx.strokeStyle = p.color;
        // 뒷다리
        ctx.beginPath();
        ctx.moveTo(x, y + 60);
        ctx.lineTo(x - (10 * dir) - legSwing, y + 90);
        ctx.lineTo(x - (15 * dir) - legSwing, y + 120);
        ctx.stroke();

        // 앞다리 (발차기 모션)
        ctx.beginPath();
        ctx.moveTo(x, y + 60);
        if (p.attacking && p.attackType === 'kick') {
            ctx.lineTo(x + (40 * dir), y + 40);
            ctx.lineTo(x + (70 * dir), y + 30);
        } else {
            ctx.lineTo(x + (10 * dir) + legSwing, y + 90);
            ctx.lineTo(x + (15 * dir) + legSwing, y + 120);
        }
        ctx.stroke();

        // 몸통
        ctx.strokeStyle = p.color;
        ctx.beginPath();
        ctx.moveTo(x, y + 25);
        ctx.lineTo(x, y + 65);
        ctx.stroke();

        // 머리 (피부 및 헤어)
        ctx.fillStyle = p.skin;
        ctx.beginPath();
        ctx.arc(x, y + 15, 14, 0, Math.PI * 2);
        ctx.fill();

        // 머리카락
        ctx.fillStyle = p.hair;
        ctx.beginPath();
        ctx.arc(x, y + 10, 15, Math.PI, Math.PI * 2);
        ctx.fill();

        // 눈
        ctx.fillStyle = "#000";
        ctx.beginPath();
        ctx.arc(x + (6 * dir), y + 15, 2, 0, Math.PI * 2);
        ctx.fill();

        // 팔 (상체 동작 및 펀치)
        ctx.strokeStyle = p.skin;

        // 뒷팔
        ctx.beginPath();
        ctx.moveTo(x, y + 30);
        ctx.lineTo(x - (15 * dir), y + 45);
        ctx.stroke();

        // 앞팔 (공격/가드 모션)
        ctx.beginPath();
        ctx.moveTo(x, y + 30);
        if (p.isGuarding) {
            ctx.lineTo(x + (10 * dir), y + 20);
            ctx.lineTo(x + (15 * dir), y + 10);
        } else if (p.attacking && p.attackType === 'punch') {
            ctx.lineTo(x + (30 * dir), y + 30);
            ctx.lineTo(x + (65 * dir), y + 30); // 펀치 쭉 뻗기
        } else if (p.attacking && p.attackType === 'ult') {
            ctx.lineTo(x + (40 * dir), y + 10);
            ctx.lineTo(x + (80 * dir), y + 10);
        } else {
            ctx.lineTo(x + (15 * dir), y + 45);
            ctx.lineTo(x + (25 * dir), y + 55);
        }
        ctx.stroke();

        // 가드 이펙트
        if (p.isGuarding) {
            ctx.strokeStyle = "#38BDF8";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(x, y + 40, 45, 0, Math.PI * 2);
            ctx.stroke();
        }
    }

    function drawUI() {
        ctx.fillStyle = "#1e293b"; ctx.fillRect(40, 25, 360, 26);
        ctx.fillStyle = "#ef4444"; ctx.fillRect(40, 25, Math.max(0, (p1.hp / p1.maxHp) * 360), 26);
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.strokeRect(40, 25, 360, 26);

        ctx.fillStyle = "#1e293b"; ctx.fillRect(560, 25, 360, 26);
        ctx.fillStyle = "#3b82f6"; ctx.fillRect(560, 25, Math.max(0, (p2.hp / p2.maxHp) * 360), 26);
        ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.strokeRect(560, 25, 360, 26);

        ctx.fillStyle = "#fff"; ctx.font = "14px 'Press Start 2P', sans-serif";
        ctx.fillText(p1.name, 40, 18);
        ctx.fillText(p2.name, 560, 18);

        ctx.fillStyle = "#facc15";
        ctx.fillRect(40, 56, (p1.ultGauge / 100) * 360, 8);
        ctx.fillRect(560, 56, (p2.ultGauge / 100) * 360, 8);

        ctx.fillStyle = "#f59e0b"; ctx.font = "bold 24px 'Press Start 2P'";
        ctx.fillText("VS", 455, 48);

        if (announcerText.life > 0) {
            announcerText.life--;
            ctx.save();
            ctx.translate(canvas.width / 2, canvas.height / 2 - 40);
            ctx.scale(announcerText.scale, announcerText.scale);
            ctx.fillStyle = "#facc15";
            ctx.textAlign = "center";
            ctx.font = "bold 32px 'Press Start 2P'";
            ctx.fillText(announcerText.text, 0, 0);
            ctx.restore();
        }
    }

    function renderEffects() {
        for (var i = particles.length - 1; i >= 0; i--) {
            var pt = particles[i];
            pt.x += pt.vx; pt.y += pt.vy; pt.life -= 0.04;
            if (pt.life <= 0) { particles.splice(i, 1); continue; }
            ctx.fillStyle = pt.color;
            ctx.fillRect(pt.x, pt.y, pt.size, pt.size);
        }

        for (var j = hitEffects.length - 1; j >= 0; j--) {
            var fx = hitEffects[j];
            fx.y -= 1; fx.life--;
            if (fx.life <= 0) { hitEffects.splice(j, 1); continue; }
            ctx.fillStyle = fx.color;
            ctx.font = "bold 16px 'Press Start 2P'";
            ctx.fillText(fx.text, fx.x - 20, fx.y);
        }
    }

    function drawSelectScreen() {
        ctx.fillStyle = "#05050a"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ef4444"; ctx.font = "20px 'Press Start 2P'";
        ctx.fillText("SELECT YOUR FIGHTER", 260, 50);

        CHARACTERS.forEach(function(c, i) {
            var x = 60 + (i % 4) * 210;
            var y = 100 + Math.floor(i / 4) * 190;

            ctx.fillStyle = "#1e1b4b"; ctx.fillRect(x, y, 180, 160);
            
            // 인간 미니 스티크맨 서있기 연출
            ctx.fillStyle = c.skin;
            ctx.beginPath(); ctx.arc(x + 90, y + 40, 12, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = c.color; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(x + 90, y + 52); ctx.lineTo(x + 90, y + 85); ctx.stroke();

            ctx.fillStyle = "#fff"; ctx.font = "12px 'Press Start 2P'";
            ctx.fillText(c.name, x + 30, y + 130);

            if (p1Sel === i) {
                ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 4;
                ctx.strokeRect(x - 4, y - 4, 188, 168);
            }
            if (p2Sel === i) {
                ctx.strokeStyle = "#3b82f6"; ctx.lineWidth = 4;
                ctx.strokeRect(x - 8, y - 8, 196, 176);
            }
        });
    }

    function loop() {
        animFrame++;

        if (gameState === "SELECT") {
            drawSelectScreen();
        } else if (gameState === "PLAY") {
            updatePlayer(p1, p2, 'a', 'd', 's');
            updatePlayer(p2, p1, 'arrowleft', 'arrowright', 'arrowdown');

            drawStage();
            drawHumanFighter(p1);
            drawHumanFighter(p2);
            renderEffects();
            drawUI();

            if (p1.hp <= 0 || p2.hp <= 0) {
                gameState = "END";
                var winner = p1.hp > 0 ? "1P WINNER!" : "2P WINNER!";
                announcerText = { text: winner, opacity: 1, scale: 2, life: 200 };
                speak("KO! " + winner);
            }
        } else if (gameState === "END") {
            drawStage();
            drawHumanFighter(p1);
            drawHumanFighter(p2);
            drawUI();
            ctx.fillStyle = "#facc15"; ctx.font = "16px 'Press Start 2P'";
            ctx.fillText("PRESS 'R' TO RESTART", 330, 300);
        }

        requestAnimationFrame(loop);
    }

    loop();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", runGame);
} else {
    runGame();
}
</script>
</body>
</html>
"""

components.html(GAME_ENGINE, height=680)
