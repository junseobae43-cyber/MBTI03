import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 격투 게임 - 최강자 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (10인 캐릭터 & 최강 배준서 참전)")

GAME_ENGINE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    body { background-color: #111; color: white; text-align: center; font-family: sans-serif; margin: 0; padding: 0; user-select: none; }
    canvas { background: #222; border: 4px solid #555; display: block; margin: 10px auto; outline: none; }
    .notice { color: #ffeb3b; font-weight: bold; margin: 10px 0 5px 0; font-size: 16px; }
    .info { font-size: 13px; color: #ccc; background: #222; padding: 8px; display: inline-block; border-radius: 5px; }
</style>
</head>
<body>
    <div class="notice">⚠️ 아래 검은색 게임 화면을 '마우스로 한번 클릭'해야 키보드가 작동합니다!</div>
    <div class="info">
        <b>[1P 조작]</b> 이동: A, D | 점프: W | 공격: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ←, → | 점프: ↑ | 공격: K | 궁극기: L
    </div>
    <canvas id="gameCanvas" width="950" height="480" tabindex="0"></canvas>

<script>
(function() {
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");

    var CHARACTERS = [
        { name: "배준서 (히든)", color: "#8A2BE2", hp: 200, speed: 9, atk: 25, ult: 80 },
        { name: "카즈야", color: "#B22222", hp: 100, speed: 5, atk: 10, ult: 30 },
        { name: "진", color: "#228B22", hp: 90, speed: 6, atk: 8, ult: 25 },
        { name: "폴", color: "#DAA520", hp: 120, speed: 4, atk: 15, ult: 40 },
        { name: "로우", color: "#9932CC", hp: 85, speed: 7, atk: 7, ult: 22 },
        { name: "킹", color: "#008B8B", hp: 110, speed: 5, atk: 12, ult: 35 },
        { name: "니나", color: "#FF69B4", hp: 95, speed: 7, atk: 9, ult: 28 },
        { name: "화랑", color: "#FF4500", hp: 90, speed: 8, atk: 8, ult: 26 },
        { name: "요시미츠", color: "#20B2AA", hp: 105, speed: 6, atk: 11, ult: 32 },
        { name: "브라이언", color: "#708090", hp: 115, speed: 4, atk: 14, ult: 38 }
    ];

    var gameState = "SELECT";
    var p1Sel = 0, p2Sel = 1;
    var p1Ready = false, p2Ready = false;
    var keys = {};
    var p1 = {}, p2 = {};

    window.addEventListener("click", function() { canvas.focus(); });

    window.addEventListener("keydown", function(e) {
        keys[e.key] = true;
        keys[e.code] = true;

        if (gameState === "SELECT") {
            if (!p1Ready) {
                if (e.key === 'a' || e.key === 'A' || e.code === 'KeyA') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'd' || e.key === 'D' || e.code === 'KeyD') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (e.key === 'f' || e.key === 'F' || e.code === 'KeyF') p1Ready = true;
            }
            if (!p2Ready) {
                if (e.key === 'ArrowLeft' || e.code === 'ArrowLeft') p2Sel = (p2Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'ArrowRight' || e.code === 'ArrowRight') p2Sel = (p2Sel + 1) % CHARACTERS.length;
                if (e.key === 'k' || e.key === 'K' || e.code === 'KeyK') p2Ready = true;
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
            x: 150, y: 320, w: 45, h: 90, color: c1.color, name: c1.name,
            hp: c1.hp, maxHp: c1.hp, speed: c1.speed, atk: c1.atk, ultAtk: c1.ult,
            vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        p2 = {
            x: 750, y: 320, w: 45, h: 90, color: c2.color, name: c2.name,
            hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk: c2.atk, ultAtk: c2.ult,
            vy: 0, isJumping: false, ultGauge: 0, attacking: false, attackBox: null
        };

        gameState = "PLAY";
    }

    function updatePlayer(p, enemy, l1, l2, r1, r2, j1, j2, a1, a2, u1, u2) {
        if (keys[l1] || keys[l2]) p.x -= p.speed;
        if (keys[r1] || keys[r2]) p.x += p.speed;

        if ((keys[j1] || keys[j2]) && !p.isJumping) {
            p.vy = -14;
            p.isJumping = true;
        }

        p.vy += 0.8;
        p.y += p.vy;

        if (p.y >= 320) {
            p.y = 320;
            p.isJumping = false;
        }

        p.x = Math.max(0, Math.min(canvas.width - p.w, p.x));

        if ((keys[a1] || keys[a2]) && !p.attacking) {
            doAttack(p, enemy, p.atk, 65, false);
        }
        if ((keys[u1] || keys[u2]) && !p.attacking && p.ultGauge >= 100) {
            doAttack(p, enemy, p.ultAtk, 130, true);
            p.ultGauge = 0;
        }
    }

    function doAttack(p, enemy, damage, range, isUlt) {
        p.attacking = true;
        var dir = p.x < enemy.x ? 1 : -1;
        var box = {
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
        ctx.font = "bold 20px sans-serif";
        ctx.fillText("캐릭터 선택 (1P: A/D/F선택 | 2P: 방향키/K선택)", 260, 40);

        CHARACTERS.forEach(function(c, i) {
            var row = Math.floor(i / 5);
            var col = i % 5;
            var x = 35 + col * 175;
            var y = 80 + row * 180;

            ctx.fillStyle = c.color;
            ctx.fillRect(x, y, 155, 160);

            ctx.fillStyle = "#FFF";
            ctx.font = "bold 14px sans-serif";
            ctx.fillText(c.name, x + 8, y + 25);
            ctx.font = "12px sans-serif";
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

            ctx.strokeStyle = "#666";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(0, 410);
            ctx.lineTo(canvas.width, 410);
            ctx.stroke();

            ctx.fillStyle = p1.color;
            ctx.fillRect(p1.x, p1.y, p1.w, p1.h);
            ctx.fillStyle = p2.color;
            ctx.fillRect(p2.x, p2.y, p2.w, p2.h);

            if (p1.attackBox) {
                ctx.fillStyle = "rgba(255,51,51,0.5)";
                ctx.fillRect(p1.attackBox.x, p1.attackBox.y, p1.attackBox.w, p1.attackBox.h);
            }
            if (p2.attackBox) {
                ctx.fillStyle = "rgba(0,255,255,0.5)";
                ctx.fillRect(p2.attackBox.x, p2.attackBox.y, p2.attackBox.w, p2.attackBox.h);
            }

            ctx.fillStyle = "#444"; ctx.fillRect(30, 20, 320, 22);
            ctx.fillStyle = "#FF3333"; ctx.fillRect(30, 20, (p1.hp / p1.maxHp) * 320, 22);
            ctx.fillStyle = "#FFD700"; ctx.fillRect(30, 47, (p1.ultGauge / 100) * 320, 8);

            ctx.fillStyle = "#444"; ctx.fillRect(600, 20, 320, 22);
            ctx.fillStyle = "#00FFFF"; ctx.fillRect(600, 20, (p2.hp / p2.maxHp) * 320, 22);
            ctx.fillStyle = "#FFD700"; ctx.fillRect(600, 47, (p2.ultGauge / 100) * 320, 8);

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
