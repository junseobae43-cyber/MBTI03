import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 격투 게임 - 최강자 배준서 참전", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (최강 히든: 배준서)")

# HTML/JS 코드 (문자열 이스케이프 및 구문 에러 완벽 해결)
game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
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
(function() {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // 캐릭터 데이터
    const CHARACTERS = [
        { name: "Bae Jun-seo (HIDDEN)", color: "#8A2BE2", hp: 200, speed: 8, atk: 25, ult: 80 },
        { name: "Kazuya", color: "#B22222", hp: 100, speed: 5, atk: 10, ult: 30 },
        { name: "Jin", color: "#228B22", hp: 90, speed: 6, atk: 8, ult: 25 },
        { name: "Paul", color: "#DAA520", hp: 120, speed: 4, atk: 15, ult: 40 },
        { name: "Law", color: "#9932CC", hp: 85, speed: 7, atk: 7, ult: 22 }
    ];

    let gameState = "SELECT"; // SELECT, PLAY, END
    let p1Sel = 0, p2Sel = 1;
    let p1Ready = false, p2Ready = false;
    let keys = {};
    let p1, p2;

    window.addEventListener("keydown", function(e) {
        keys[e.key] = true;
        keys[e.key.toLowerCase()] = true;

        if (gameState === "SELECT") {
            // 1P 선택 (A/D로 변경, F로 확정)
            if (!p1Ready) {
                if (e.key === 'a' || e.key === 'A') p1Sel = (p1Sel - 1 + CHARACTERS.length) % CHARACTERS.length;
                if (e.key === 'd' || e.key === 'D') p1Sel = (p1Sel + 1) % CHARACTERS.length;
                if (e.key === 'f' || e.key === 'F') p1Ready = true;
            }
            // 2P 선택 (화살표로 변경, K로 확정)
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
            hp: c2.hp, maxHp: c2.hp, speed: c2.speed, atk
