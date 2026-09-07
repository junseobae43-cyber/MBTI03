import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 철권 스타일 격투 v3.0 - GOD 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 v3.0 (이펙트 & 공중전 대규모 업데이트)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    * { box-sizing: border-box; }
    body { background-color: #08080c; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 8px; user-select: none; overflow: hidden; }
    canvas { background: #0b0914; border: 3px solid #3b82f6; display: block; margin: 0 auto; outline: none; box-shadow: 0 0 30px rgba(59,130,246,0.6); cursor: pointer; }
    .notice { color: #c084fc; font-weight: bold; margin-bottom: 6px; font-size: 14px; text-shadow: 0 0 10px #a855f7; }
    .info { font-size: 12px; color: #cbd5e1; background: #1e1b2e; padding: 6px 12px; display: inline-block; border-radius: 6px; border: 1px solid #475569; margin-bottom: 6px; }
</style>
</head>
<body>
    <div class="notice">⚡ GOD 배준서 (HP 2000 / ATK 150) & 16종 캐릭터 Ultimate Battle ⚡</div>
    <div class="info">
        <b>[1P]</b> 이동: A, D | 점프(2단): W | 가드: <b>S</b> | 공격: F | 궁극기: G | 잡기: <b>T</b><br>
        <b>[2P]</b> 이동: ←, → | 점프(2단): ↑ | 가드: <b>↓</b> | 공격: K | 궁극기: L | 잡기: <b>P</b><br>
        <span style="color: #60a5fa;"><b>[게임 종료]</b> <b>R</b> 키로 재시작 | <b>[특수]</b> 공중에서 점프 키 추가 입력 시 2단 점프!</span>
    </div>

    <canvas id="gameCanvas" width="960" height="520" tabindex="0"></canvas>

<script>
function runGame() {
    var canvas = document.getElementById("gameCanvas");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");

    var audioCtx = null;
    var particles = [];
    var damageTexts = [];

    var GOD_PRAISE_EXACT = "전지전능하신 천지신 세계의 왕 배준서님이 강림하셨다";
    var GOD_PRAISES_ATTACK = ["신벌이다!", "어디 감히!", "무릎 꿇어라!", "배준서 님의 일격!"];
    var GOD_PRAISES_ULT = ["전지전능한 창세의 권능!", "우주 파괴의 신벌을 받아라!", "배준서 님 앞에 모든 만물은 소멸한다!"];
    var GOD_PRAISES_WIN = ["전지전능하신 세계의 왕 배준서 님의 당연한 승리다!", "승자는 오직 절대존엄 배준서 님뿐이다!"];

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

    function playSound(type, pitchMultiplier) {
        try {
            initAudio();
            if (!audioCtx) return;

            var osc = audioCtx.createOscillator();
            var gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            var now = audioCtx.currentTime;
            var pitch = pitchMultiplier || 1.0;

            if (type === 'hit') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180 * pitch, now);
                osc.frequency.exponentialRampToValueAtTime(30 * pitch, now + 0.12);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
                osc.start(now);
                osc.stop(now + 0.12);
            } else if (type === 'godHit') {
                osc.type = 'square';
                osc.frequency.setValueAtTime(240, now);
                osc.frequency.exponentialRampToValueAtTime(20, now + 0.35);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
                osc.start(now);
                osc.stop(now + 0.35);
            } else if (type === 'ult') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(100 * pitch, now);
                osc.frequency.linearRampToValueAtTime(700 * pitch, now + 0.45);
                gain.gain.setValueAtTime(0.45, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.45);
                osc.start(now);
                osc.stop(now + 0.45);
            } else if (type === 'block') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.exponentialRampToValueAtTime(120, now + 0.1);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
                osc.start(now);
                osc.stop(now + 0.1);
            }
        } catch(e) {}
    }

    function addHitParticle(x, y, color) {
        for (var i = 0; i < 12; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 12,
                vy: (Math.random() - 0.5) * 12,
                size: Math.random() * 5 + 3,
                color: color || '#FACC15',
                life: 1.0
            });
        }
    }

    function addDamageText(x, y, text, color) {
        damageTexts.push({
            x: x, y: y,
            text: text,
            color: color || '#FF4500',
            vy: -2,
            life: 1.0
        });
    }

    var CHARACTERS = [
        { name: "⚡배준서 (GOD)⚡", color: "#A855F7", beltColor: "#FFD700", hairColor: "#E2E8F0", skinColor: "#FFF0E5", eyeColor: "#EF4444", hp: 2000, speed: 18, atk: 150, ult: 999, isGod: true },
        { name: "카즈야", color: "#DC2626", beltColor: "#000000", hairColor: "#1E293B", skinColor: "#F3D2C1", eyeColor: "#FF0000", hp: 200, speed: 7, atk: 22, ult: 80 },
        { name: "진 카자마", color: "#16A34A", beltColor: "#000000", hairColor: "#0F172A", skinColor: "#FFE5D9", eyeColor: "#38BDF8", hp: 195, speed: 8, atk: 21, ult: 75 },
        { name: "폴 피닉스", color: "#CA8A04", beltColor: "#000000", hairColor: "#FACC15", skinColor: "#FDE047", eyeColor: "#1E293B", hp: 230, speed: 6, atk: 27, ult: 90 },
        { name: "마샬 로우", color: "#DB2777", beltColor: "#000000", hairColor: "#18181B", skinColor: "#EAB308", eyeColor: "#000000", hp: 180, speed: 9, atk: 19, ult: 70 },
        { name: "킹", color: "#0891B2", beltColor: "#FFFFFF", hairColor: "#D97706", skinColor: "#B45309", eyeColor: "#000000", hp: 220, speed: 7, atk: 24, ult: 85 },
        { name: "니나 윌리엄스", color: "#E11D48", beltColor: "#FFFFFF", hairColor: "#FEF08A", skinColor: "#FFF0F5", eyeColor: "#2563EB", hp: 185, speed: 9, atk: 20, ult: 72 },
        { name: "화랑", color: "#EA580C", beltColor: "#000000", hairColor: "#F97316", skinColor: "#FFE4E6", eyeColor: "#1E293B", hp: 180, speed: 10, atk: 18, ult: 68 },
        { name: "요시미츠", color: "#0D9488", beltColor: "#FFD700", hairColor: "#64748B", skinColor: "#0284C7", eyeColor: "#FACC15", hp: 210, speed: 7, atk: 22, ult: 82 },
        { name: "브라이언 퓨리", color: "#475569", beltColor: "#000000", hairColor: "#94A3B8", skinColor: "#E2E8F0", eyeColor: "#DC2626", hp: 225, speed: 6, atk: 25, ult: 88 },
        { name: "스티브 Fox", color: "#3B82F6", beltColor: "#EF4444", hairColor: "#FDE047", skinColor: "#FFE4E6", eyeColor: "#1E3A8A", hp: 175, speed: 11, atk: 23, ult: 70 },
        { name: "릴리", color: "#EC4899", beltColor: "#FFFFFF", hairColor: "#FEF08A", skinColor: "#FFF0F5", eyeColor: "#06B6D4", hp: 185, speed: 9, atk: 20, ult: 74 },
        { name: "드라구노프", color: "#334155", beltColor: "#000000", hairColor: "#0F172A", skinColor: "#CBD5E1", eyeColor: "#475569", hp: 215, speed: 7, atk: 24, ult: 84 },
        { name: "아스카", color: "#84CC16", beltColor: "#15803D", hairColor: "#78350F", skinColor: "#FFE5D9", eyeColor: "#15803D", hp: 205, speed: 8, atk: 19, ult: 78 },
        { name: "클라우디오", color: "#6366F1", beltColor: "#4338CA", hairColor: "#1E1B4B", skinColor: "#F8FAFC", eyeColor: "#818CF8", hp: 190, speed: 8, atk: 21, ult: 95 },
        { name: "샤오유", color: "#F59E0B", beltColor: "#B45309", hairColor: "#18181B", skinColor: "#FDE047", eyeColor: "#78350F", hp: 170, speed: 11, atk: 18, ult: 65 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var lastJumpKeys = {};
    var p1 = {}, p2 = {};

    canvas.focus();

    window.addEventListener("click", function() { 
        if (canvas) canvas.focus();
        initAudio();
    });

    window.addEventListener("keydown", function(e) {
        initAudio();
        if (!e) return;
        var k = e.key ? e.key.toLowerCase() : "";
        var c = e.code ? e.code : "";

        if (!keys[k]) {
            if (gameState === "PLAY") {
                if (k === 'w' || c === 'KeyW') handleJump(p1);
                if (k === 'arrowup' || c === 'ArrowUp') handleJump(p2);
            }
        }

        keys[k] = true;
        keys[c] = true;

        if (gameState === "SELECT") {
            if (!p1Ready) {
                if (k === 'a' || c === 'KeyA') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (k === 'd' || c === 'KeyD') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (k === 'f' || c === 'KeyF') {
                    p1Ready = true;
                    if (CHARACTERS[p1Sel].isGod) speakText(GOD_PRAISE_EXACT, 0.1, 0.75);
                }
            }
            if (!p2Ready) {
                if (k === 'arrowleft' || c === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (k === 'arrowright' || c === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
                if (k === 'k' || c === 'KeyK') {
                    p2Ready = true;
                    if (CHARACTERS[p2Sel].isGod) speakText(GOD_PRAISE_EXACT, 0.1, 0.75);
                }
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
        keys[k] = false;
        keys[c] = false;
    });

    function handleJump(p) {
        if (p.jumpCount < 2) {
            p.vy = -14;
            p.jumpCount++;
            p.isJumping = true;
        }
    }

    function resetToSelect() {
        p1Ready = false;
        p2Ready = false;
        gameState = "SELECT";
        particles = [];
        damageTexts = [];
    }

    function startGame() {
        var c1 = CHARACTERS[p1Sel];
        var c2 = CHARACTERS[p2Sel];

        p1 = {
            x: 150, y: 310, w: 50, h: 110, color: c1.color, beltColor: c1.beltColor,
            hairColor: c1.hairColor, skinColor: c1.skinColor, eyeColor: c1.eyeColor,
            name: c1.name, hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            isGod: c1.isGod, facing: 1, vy: 0, jumpCount: 0, isJumping: false, ultGauge: 0, attacking: false, isGuarding: false, attackBox: null
        };

        p2 = {
            x: 760, y: 310, w: 50, h: 110, color: c2.color, beltColor: c2.beltColor,
            hairColor: c2.hairColor, skinColor: c2.skinColor, eyeColor: c2.eyeColor,
            name: c2.name, hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
            isGod: c2.isGod, facing: -1, vy: 0, jumpCount: 0, isJumping: false, ultGauge: 0, attacking: false, isGuarding: false, attackBox: null
        };

        gameState = "PLAY";
    }

    function updatePlayer(p, enemy, lKey, rKey, gKey, aKey, uKey, tKey) {
        p.isGuarding = !!(keys[gKey]);

        if (!p.isGuarding) {
            if (keys[lKey]) { p.x -= p.speed; p.facing = -1; }
            if (keys[rKey]) { p.x += p.speed; p.facing = 1; }
        }

        p.vy += 0.85;
        p.y += p.vy;

        if (p.y >= 310) {
            p.y = 310;
            p.vy = 0;
            p.jumpCount = 0;
            p.isJumping = false;
        }

        p.x = Math.max(20, Math.min(canvas.width - p.w - 20, p.x));

        if (!p.isGuarding && !p.attacking) {
            if (keys[aKey]) {
                doAttack(p, enemy, p.atk, 85, false, false);
            } else if (keys[uKey] && p.ultGauge >= 100) {
                doAttack(p, enemy, p.ultAtk, 160, true, false);
                p.ultGauge = 0;
            } else if (keys[tKey]) {
                doAttack(p, enemy, Math.floor(p.atk * 1.25), 65, false, true);
            }
        }
    }

    function doAttack(p, enemy, damage, range, isUlt, isGrab) {
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
            
            var finalDamage = damage;
            var hitX = enemy.x + enemy.w / 2;
            var hitY = enemy.y + enemy.h / 2;

            if (enemy.isGuarding && !isGrab) {
                finalDamage = Math.max(1, Math.floor(damage * 0.1));
                playSound('block', 1.0);
                addHitParticle(hitX, hitY, "#38BDF8");
                addDamageText(hitX, hitY - 20, "GUARD!", "#38BDF8");
            } else {
                if (p.isGod) {
                    if (isUlt) {
                        playSound('ult', 0.5);
                        speakText(getRandomItem(GOD_PRAISES_ULT), 0.1, 0.8);
                        addHitParticle(hitX, hitY, "#A855F7");
                    } else {
                        playSound('godHit', 1.0);
                        speakText(getRandomItem(GOD_PRAISES_ATTACK), 0.1, 1.0);
                        addHitParticle(hitX, hitY, "#C084FC");
                    }
                } else {
                    if (isUlt) {
                        playSound('ult', 1.0);
                        addHitParticle(hitX, hitY, "#EF4444");
                    } else {
                        playSound('hit', 1.0);
                        addHitParticle(hitX, hitY, "#FACC15");
                    }
                }
                addDamageText(hitX, hitY - 20, "-" + finalDamage, isUlt ? "#EF4444" : "#FACC15");
            }

            enemy.hp = Math.max(0, enemy.hp - finalDamage);
            if (!isUlt) p.ultGauge = Math.min(100, p.ultGauge + 50);
        }

        setTimeout(function() {
            p.attacking = false;
            p.attackBox = null;
        }, 150);
    }

    function updateAndDrawParticles() {
        for (var i = particles.length - 1; i >= 0; i--) {
            var pt = particles[i];
            pt.x += pt.vx;
            pt.y += pt.vy;
            pt.life -= 0.05;

            if (pt.life <= 0) {
                particles.splice(i, 1);
                continue;
            }

            ctx.fillStyle = pt.color;
            ctx.globalAlpha = pt.life;
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1.0;

        for (var j = damageTexts.length - 1; j >= 0; j--) {
            var dt = damageTexts[j];
            dt.y += dt.vy;
            dt.life -= 0.03;

            if (dt.life <= 0) {
                damageTexts.splice(j, 1);
                continue;
            }

            ctx.fillStyle = dt.color;
            ctx.globalAlpha = dt.life;
            ctx.font = "bold 18px sans-serif";
            ctx.fillText(dt.text, dt.x - 15, dt.y);
        }
        ctx.globalAlpha = 1.0;
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
        ctx.arc(x + width/2, y + height/2 + 3, 16, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = c.hairColor;
        if (c.isGod) {
            ctx.beginPath();
            ctx.moveTo(x + width/2 - 20, y + height/2 - 5);
            ctx.lineTo(x + width/2 - 6, y + height/2 - 25);
            ctx.lineTo(x + width/2, y + height/2 - 15);
            ctx.lineTo(x + width/2 + 10, y + height/2 - 27);
            ctx.lineTo(x + width/2 + 20, y + height/2 - 5);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = c.eyeColor;
            ctx.fillRect(x + width/2 - 10, y + height/2 + 2, 4, 3);
            ctx.fillRect(x + width/2 + 5, y + height/2 + 2, 4, 3);
        } else {
            ctx.beginPath();
            ctx.arc(x + width/2, y + height/2 - 5, 18, Math.PI, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = c.eyeColor;
            ctx.fillRect(x + width/2 - 8, y + height/2, 3, 3);
            ctx.fillRect(x + width/2 + 5, y + height/2, 3, 3);
        }
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

        if (p.isGuarding) {
            ctx.fillStyle = "rgba(56, 189, 248, 0.5)";
            ctx.beginPath();
            ctx.arc(x + 25, y + 55, 45, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#38BDF8";
            ctx.lineWidth = 3;
            ctx.stroke();
        }
    }

    function drawSelectScreen() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "#38BDF8";
        ctx.font = "bold 22px sans-serif";
        ctx.fillText("TEKKEN SELECT YOUR FIGHTER (16 CHARACTERS)", 220, 28);

        CHARACTERS.forEach(function(c, i) {
            var row = Math.floor(i / 8);
            var col = i % 8;
            var x = 15 + col * 115;
            var y = 40 + row * 230;

            ctx.fillStyle = "#1E1B4B";
            ctx.fillRect(x, y, 105, 215);

            drawFacePortrait(c, x + 8, y + 8, 89, 75);

            ctx.fillStyle = "#FFFFFF";
            ctx.font = "bold 11px sans-serif";
            ctx.fillText(c.name, x + 4, y + 100);

            ctx.font = "10px sans-serif";
            ctx.fillStyle = "#94A3B8";
            ctx.fillText("HP: " + c.hp, x + 6, y + 120);
            ctx.fillText("ATK: " + c.atk, x + 6, y + 138);
            ctx.fillText("SPD: " + c.speed, x + 6, y + 156);
            ctx.fillText("ULT: " + c.ult, x + 6, y + 174);

            if (p1Sel === i) {
                ctx.strokeStyle = "#EC4899";
                ctx.lineWidth = 3;
                ctx.strokeRect(x - 2, y - 2, 109, 219);
                ctx.fillStyle = "#EC4899";
                ctx.font = "bold 12px sans-serif";
                ctx.fillText(p1Ready ? "1P OK" : "1P", x + 4, y - 5);
            }
            if (p2Sel === i) {
                ctx.strokeStyle = "#3B82F6";
                ctx.lineWidth = 3;
                ctx.strokeRect(x - 4, y - 4, 113, 223);
                ctx.fillStyle = "#3B82F6";
                ctx.font = "bold 12px sans-serif";
                ctx.fillText(p2Ready ? "2P OK" : "2P", x + 60, y - 5);
            }
        });
    }

    function loop() {
        if (gameState === "SELECT") {
            drawSelectScreen();
        } else if (gameState === "PLAY") {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            updatePlayer(p1, p2, 'a', 'd', 's', 'f', 'g', 't');
            updatePlayer(p2, p1, 'arrowleft', 'arrowright', 'arrowdown', 'k', 'l', 'p');

            ctx.fillStyle = "#1E293B";
            ctx.fillRect(0, 420, canvas.width, 100);
            ctx.strokeStyle = "#38BDF8";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 420);
            ctx.lineTo(canvas.width, 420);
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

            updateAndDrawParticles();

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
            ctx.fillText(winTxt, 310, 220);

            ctx.fillStyle = "#38BDF8";
            ctx.font = "bold 20px sans-serif";
            ctx.fillText("Press 'R' Key to Play Again!", 340, 280);
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
