<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>2P 격투 게임 - 최강 배준서 참전</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 { margin-bottom: 10px; }
        .controls {
            background: #222;
            display: inline-block;
            padding: 10px 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 14px;
        }
        canvas {
            background: #1e1e1e;
            border: 4px solid #444;
            border-radius: 4px;
            display: block;
            margin: 0 auto;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
    </style>
</head>
<body>

    <h1>🥊 2P 스트리트 파이터 (최강 히든: 배준서)</h1>
    <div class="controls">
        <b>[1P 조작]</b> 이동: A, D | 점프: W | 평타: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, → | 점프: ↑ | 평타: K | 궁극기: L
    </div>

    <canvas id="game" width="900" height="450"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// 캐릭터 정보 (첫 번째가 최강 히든 캐릭터 '배준서')
const CHARACTERS = [
    { name: "배준서 (HIDDEN)", color: "#9b59b6", hp: 200, speed: 9, atk: 25, ult: 80 },
    { name: "카즈야", color: "#e74c3c", hp: 100, speed: 5, atk: 10, ult: 30 },
    { name: "진", color: "#2ecc71", hp: 90, speed: 6, atk: 8, ult: 25 },
    { name: "폴", color: "#f1c40f", hp: 120, speed: 4, atk: 15, ult: 40 },
    { name: "로우", color: "#e67e22", hp: 85, speed: 7, atk: 7, ult: 22 }
];

let state = "SELECT"; // SELECT -> PLAY -> END
let p1Sel = 0, p2Sel = 1;
let p1Ready = false, p2Ready = false;
const keys = {};

let p1 = {}, p2 = {};

window.addEventListener("keydown", e => {
    keys[e.key] = true;
    keys[e.key.toLowerCase()] = true;

    if (state === "SELECT") {
        // 1P 선택 (A/D로 이동, F로 확정)
        if (!p1Ready) {
            if (e.key === 'a' || e.key === 'A') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'd' || e.key === 'D') p1Sel = (p1Sel + 1) % CHARACTERS.length;
            if (e.key === 'f' || e.key === 'F') p1Ready = true;
        }
        // 2P 선택 (화살표 좌우로 이동, K로 확정)
        if (!p2Ready) {
            if (e.key === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
            if (e.key === 'k' || e.key === 'K') p2Ready = true;
        }
        if (p1Ready && p2Ready) startGame();
    }
});

window.addEventListener("keyup", e => {
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

    state = "PLAY";
}

function updatePlayer(p, enemy, leftKey, rightKey, jumpKey, atkKey, ultKey) {
    if (keys[leftKey]) p.x -= p.speed;
    if (keys[rightKey]) p.x += p.speed;

    if (keys[jumpKey] && !p.isJumping) {
        p.vy = -14;
        p.isJumping = true;
    }

    p.vy += 0.8; // 중력
    p.y += p.vy;

    if (p.y >= 300) {
        p.y = 300;
        p.isJumping = false;
    }

    p.x = Math.max(0, Math.min(canvas.width - p.w, p.x));

    // 평타
    if (keys[atkKey] && !p.attacking) {
        attack(p, enemy, p.atk, 60, false);
    }
    // 궁극기
    if (keys[ultKey] && !p.attacking && p.ultGauge >= 100) {
        attack(p, enemy, p.ultAtk, 120, true);
        p.ultGauge = 0;
    }
}

function attack(p, enemy, damage, range, isUlt) {
    p.attacking = true;
    const dir = p.x < enemy.x ? 1 : -1;
    const box = {
        x: dir === 1 ? p.x + p.w : p.x - range,
        y: p.y,
        w: range,
        h: p.h
    };
    p.attackBox = box;

    // 히트 판정
    if (box.x < enemy.x + enemy.w && box.x + box.w > enemy.x &&
        box.y < enemy.y + enemy.h && box.y + box.h > enemy.y) {
        enemy.hp = Math.max(0, enemy.hp - damage);
        if (!isUlt) p.ultGauge = Math.min(100, p.ultGauge + 35);
    }

    setTimeout(() => {
        p.attacking = false;
        p.attackBox = null;
    }, 150);
}

function drawSelectScreen() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FFF";
    ctx.font = "bold 22px sans-serif";
    ctx.fillText("캐릭터 선택 (1P: A/D/F확정 | 2P: ←/→/K확정)", 220, 50);

    CHARACTERS.forEach((c, i) => {
        const x = 40 + i * 168;
        const y = 110;

        ctx.fillStyle = c.color;
        ctx.fillRect(x, y, 145, 210);

        ctx.fillStyle = "#FFF";
        ctx.font = "bold 14px sans-serif";
        ctx.fillText(c.name, x + 8, y + 30);
        ctx.font = "12px sans-serif";
        ctx.fillText("체력: " + c.hp, x + 10, y + 80);
        ctx.fillText("공격력: " + c.atk, x + 10, y + 110);
        ctx.fillText("속도: " + c.speed, x + 10, y + 140);
        ctx.fillText("궁극기: " + c.ult, x + 10, y + 170);

        if (p1Sel === i) {
            ctx.strokeStyle = "#e74c3c";
            ctx.lineWidth = 5;
            ctx.strokeRect(x - 3, y - 3, 151, 216);
            ctx.fillStyle = "#e74c3c";
            ctx.fillText("1P", x + 10, y - 10);
        }
        if (p2Sel === i) {
            ctx.strokeStyle = "#3498db";
            ctx.lineWidth = 5;
            ctx.strokeRect(x - 5, y - 5, 155, 220);
            ctx.fillStyle = "#3498db";
            ctx.fillText("2P", x + 110, y - 10);
        }
    });
}

function loop() {
    if (state === "SELECT") {
        drawSelectScreen();
    } else if (state === "PLAY") {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        updatePlayer(p1, p2, 'a', 'd', 'w', 'f', 'g');
        updatePlayer(p2, p1, 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'k', 'l');

        // 바닥선
        ctx.strokeStyle = "#666";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(0, 390);
        ctx.lineTo(canvas.width, 390);
        ctx.stroke();

        // 본체
        ctx.fillStyle = p1.color;
        ctx.fillRect(p1.x, p1.y, p1.w, p1.h);
        ctx.fillStyle = p2.color;
        ctx.fillRect(p2.x, p2.y, p2.w, p2.h);

        // 공격 범위 이펙트
        if (p1.attackBox) {
            ctx.fillStyle = "rgba(231, 76, 60, 0.5)";
            ctx.fillRect(p1.attackBox.x, p1.attackBox.y, p1.attackBox.w, p1.attackBox.h);
        }
        if (p2.attackBox) {
            ctx.fillStyle = "rgba(52, 152, 219, 0.5)";
            ctx.fillRect(p2.attackBox.x, p2.attackBox.y, p2.attackBox.w, p2.attackBox.h);
        }

        // UI 체력바 & 궁극기 게이지
        ctx.fillStyle = "#444"; ctx.fillRect(30, 20, 300, 20);
        ctx.fillStyle = "#e74c3c"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 300, 20);
        ctx.fillStyle = "#f1c40f"; ctx.fillRect(30, 45, (p1.ultGauge / 100) * 300, 8);

        ctx.fillStyle = "#444"; ctx.fillRect(570, 20, 300, 20);
        ctx.fillStyle = "#3498db"; ctx.fillRect(570, 20, (p2.hp / p2.maxHp) * 300, 20);
        ctx.fillStyle = "#f1c40f"; ctx.fillRect(570, 45, (p2.ultGauge / 100) * 300, 8);

        ctx.fillStyle = "#FFF"; ctx.font = "bold 14px sans-serif";
        ctx.fillText("1P: " + p1.name, 30, 15);
        ctx.fillText("2P: " + p2.name, 570, 15);

        if (p1.hp <= 0 || p2.hp <= 0) state = "END";
    } else if (state === "END") {
        ctx.fillStyle = "#f1c40f";
        ctx.font = "bold 40px sans-serif";
        const winTxt = p1.hp > 0 ? "1P 승리!" : "2P 승리!";
        ctx.fillText(winTxt, 380, 220);
    }

    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
