import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(
    page_title="2P 격투 게임 - 최강자 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (최강 히든: 배준서)")

# 2. 게임 HTML/JS 실행
GAME_CODE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { background-color: #111; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; }
    canvas { background: #222; border: 4px solid #555; display: block; margin: 10px auto; }
    .info { font-size: 14px; color: #ccc; margin-bottom: 5px; }
</style>
</head>
<body>
    <div class="info">
        <b>[1P 조작]</b> 이동: A, D, W(점프) | 평타: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, →, ↑(점프) | 평타: K | 궁극기: L
    </div>
    <canvas id="gameCanvas" width="900" height="450"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const CHARACTERS = [
    { name: "Bae Jun-seo (HIDDEN)", color: "#8A2BE2", hp: 200, speed: 8, atk: 25, ult: 80 },
    { name: "Kazuya", color: "#B22222", hp: 100, speed: 5, atk: 10, ult: 30 },
    { name: "Jin", color: "#228B22", hp: 90, speed: 6, atk: 8, ult: 25 },
    { name: "Paul", color: "#DAA520", hp: 120, speed: 4, atk: 15, ult: 40 },
    { name: "Law", color: "#9932CC", hp: 85, speed: 7, atk: 7, ult: 22 }
];

let gameState = "SELECT";
let p1Sel = 0, p2Sel = 1;
let p1Ready = false, p2Ready = false;
let keys = {};
let p1 = {}, p2 = {};

window.addEventListener("keydown", function(e) {
    keys[e.key] = true;
    keys[e.key.toLowerCase()] = true;

    if (gameState === "SELECT") {
        if (!p1Ready) {
            if (e.key === 'a' || e.key === 'A') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'd' || e.key === 'D') p1Sel = (p1Sel + 1) % CHARACTERS.length;
            if (e.key === 'f' || e.key === 'F') p1Ready = true;
        }
        if (!p2Ready) {
            if (e.key === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
            if (e.key === 'k' || e.key === 'K') p2Ready = true;
        }
        if (p1Ready && p2Ready) startGame();
    }
});

window.addEventListener("keyup", function(e) {
    keys[e.key] = false;
    keys[e.key.toLowerCase()] = false;
});

function startGame() {
    const c1 = CHARACTERS[p1Sel];
    const c2 = CHARACTERS[p2Sel];

    p1 = {
        x: 150, y: 300, w: 45, h: 90, color: c1.color, name: c1.name,
        hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
        vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
    };

    p2 = {
        x: 700, y: 300, w: 45, h: 90, color: c2.color, name: c2.name,
        hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
        vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
    };

    gameState = "PLAY";
}

function updatePlayer(p, enemy, leftKey, rightKey, jumpKey, atkKey, ultKey) {
    if (keys[leftKey]) p.x -= p.speed;
    if (keys[rightKey]) p.x += p.speed;

    if (keys[jumpKey] && !p.isJumping) {
        p.vy = -14;
        p.isJumping = true;
    }

    p.vy += 0.8;
    p.y += p.vy;

    if (p.y >= 300) {
        p.y = 300;
        p.isJumping = false;
    }

    p.x = Math.max(0, Math.min(canvas.width - p.w, p.x));

    if (keys[atkKey] && !p.attacking) {
        doAttack(p, enemy, p.atk, 60, false);
    }
    if (keys[ultKey] && !p.attacking && p.ultGauge >= 100) {
        doAttack(p, enemy, p.ultAtk, 120, true);
        p.ultGauge = 0;
    }
}

function doAttack(p, enemy, damage, range, isUlt) {
    p.attacking = true;
    const dir = p.x < enemy.x ? 1 : -1;
    const box = {
        x: dir === 1 ? p.x + p.w : p.x - range,
        y: p.y,
        w: range,
        h: p.h
    };
    p.attackBox = box;

    if (box.x < enemy.x + enemy.w && box.x + box.w > enemy.x &&
        box.y < enemy.y + enemy.h && box.y + box.h > enemy.y) {
        enemy.hp = Math.max(0, enemy.hp - damage);
        if (!isUlt) p.ultGauge = Math.min(100, p.ultGauge + 35);
    }

    setTimeout(function() {
        p.attacking = false;
        p.attackBox = null;
    }, 150);
}

function drawSelectScreen() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FFF";
    ctx.font = "20px sans-serif";
    ctx.fillText("Select Character (1P: A/D/F | 2P: Left/Right/K)", 220, 40);

    CHARACTERS.forEach(function(c, i) {
        const x = 50 + i * 165;
        const y = 100;

        ctx.fillStyle = c.color;
        ctx.fillRect(x, y, 140, 200);

        ctx.fillStyle = "#FFF";
        ctx.font = "13px sans-serif";
        ctx.fillText(c.name, x + 5, y + 25);
        ctx.fillText("HP: " + c.hp, x + 10, y + 70);
        ctx.fillText("ATK: " + c.atk, x + 10, y + 100);
        ctx.fillText("SPD: " + c.speed, x + 10, y + 130);

        if (p1Sel === i) {
            ctx.strokeStyle = "red";
            ctx.lineWidth = 4;
            ctx.strokeRect(x - 2, y - 2, 144, 204);
            ctx.fillStyle = "red";
            ctx.fillText("1P", x + 10, y - 10);
        }
        if (p2Sel === i) {
            ctx.strokeStyle = "cyan";
            ctx.lineWidth = 4;
            ctx.strokeRect(x - 4, y - 4, 148, 208);
            ctx.fillStyle = "cyan";
            ctx.fillText("2P", x + 100, y - 10);
        }
    });
}

function loop() {
    if (gameState === "SELECT") {
        drawSelectScreen();
    } else if (gameState === "PLAY") {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        updatePlayer(p1, p2, 'a', 'd', 'w', 'f', 'g');
        updatePlayer(p2, p1, 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'k', 'l');

        ctx.strokeStyle = "#555";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(0, 390);
        ctx.lineTo(canvas.width, 390);
        ctx.stroke();

        ctx.fillStyle = p1.color;
        ctx.fillRect(p1.x, p1.y, p1.w, p1.h);
        ctx.fillStyle = p2.color;
        ctx.fillRect(p2.x, p2.y, p2.w, p2.h);

        if (p1.attackBox) {
            ctx.fillStyle = "rgba(255,0,0,0.5)";
            ctx.fillRect(p1.attackBox.x, p1.attackBox.y, p1.attackBox.w, p1.attackBox.h);
        }
        if (p2.attackBox) {
            ctx.fillStyle = "rgba(0,255,255,0.5)";
            ctx.fillRect(p2.attackBox.x, p2.attackBox.y, p2.attackBox.w, p2.attackBox.h);
        }

        ctx.fillStyle = "#444"; ctx.fillRect(30, 20, 300, 20);
        ctx.fillStyle = "red"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 300, 20);
        ctx.fillStyle = "yellow"; ctx.fillRect(30, 45, (p1.ultGauge / 100) * 300, 8);

        ctx.fillStyle = "#444"; ctx.fillRect(570, 20, 300, 20);
        ctx.fillStyle = "cyan"; ctx.fillRect(570, 20, (p2.hp / p
