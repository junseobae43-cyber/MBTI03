import streamlit as st

st.set_page_config(
    page_title="2P 격투 게임 - 배준서 참전", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 스트리트 파이터 (최강자 배준서 참전)")

# HTML5 Canvas 기반 2인용 격투 게임 (Keydown 버그 및 폰트 에러 완벽 해결)
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { background-color: #111; color: white; text-align: center; font-family: sans-serif; margin: 0; }
    canvas { background: #222; border: 4px solid #555; margin-top: 10px; display: block; margin-left: auto; margin-right: auto; }
    #ui { font-size: 16px; margin: 10px; }
</style>
</head>
<body>
    <div id="ui">
        <b>[1P 조작]</b> 이동: A / D / W | 평타: F | 궁극기: G <br>
        <b>[2P 조작]</b> 이동: ← / → / ↑ | 평타: K | 궁극기: L
    </div>
    <canvas id="gameCanvas" width="900" height="450"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 캐릭터 명단
const CHARACTERS = [
    { name: "배준서 (HIDDEN)", color: "#8A2BE2", hp: 200, speed: 8, atk: 25, ult: 80 }, // ★ 최강 스펙
    { name: "카즈야", color: "#B22222", hp: 100, speed: 5, atk: 10, ult: 30 },
    { name: "진", color: "#228B22", hp: 90, speed: 6, atk: 8, ult: 25 },
    { name: "폴", color: "#DAA520", hp: 120, speed: 4, atk: 15, ult: 40 },
    { name: "로우", color: "#9932CC", hp: 85, speed: 7, atk: 7, ult: 22 }
];

let gameState = "SELECT"; // SELECT -> PLAY -> END
let p1Select = 0; // 기본 선택: 배준서
let p2Select = 1;
let p1Ready = false;
let p2Ready = false;

let keys = {};
let p1, p2;

window.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()] = true;
    keys[e.key] = true;
    
    // 캐릭터 선택 창 컨트롤
    if (gameState === "SELECT") {
        // 1P 선택 (A/D로 이동, F로 확정)
        if (!p1Ready) {
            if (e.key === 'a' || e.key === 'A') p1Select = (p1Select - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'd' || e.key === 'D') p1Select = (p1Select + 1) % CHARACTERS.length;
            if (e.key === 'f' || e.key === 'F') p1Ready = true;
        }
        // 2P 선택 (화살표로 이동, K로 확정)
        if (!p2Ready) {
            if (e.key === 'ArrowLeft') p2Select = (p2Select - 1 + CHARACTERS.length) % CHARACTERS.length;
            if (e.key === 'ArrowRight') p2Select = (p2Select + 1) % CHARACTERS.length;
            if (e.key === 'k' || e.key === 'K') p2Ready = true;
        }
        
        if (p1Ready && p2Ready) initGame();
    }
});

window.addEventListener("keyup", e => {
