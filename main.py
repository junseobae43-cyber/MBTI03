import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2P 철권 스타일 격투 - GOD 배준서", page_icon="🥊", layout="wide"
)

st.title("🥊 2P 격투 게임 (오류 수정 및 최적화 완료)")

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
    <div class="notice">⚡ GOD 배준서 스펙 초월 패치 (HP 2000 / ATK 150) ⚡</div>
    <div class="info">
        <b>[1P]</b> 이동: A, D | 점프: W | 가드: <b>S</b> | 공격: F | 궁극기: G | 잡기: <b>T</b><br>
        <b>[2P]</b> 이동: ←, → | 점프: ↑ | 가드: <b>↓</b> | 공격: K | 궁극기: L | 잡기: <b>P</b><br>
        <span style="color: #60a5fa;"><b>[게임 종료 후]</b> <b>R</b> 키를 누르면 재시작!</span>
    </div>
    
    <iframe id="yt-player" src="https://www.youtube.com/embed/YXxdETZ9npU?enablejsapi=1&autoplay=0&loop=1&playlist=YXxdETZ9npU" allow="autoplay"></iframe>

    <canvas id="gameCanvas" width="960" height="520" tabindex="0"></canvas>

<script>
(function() {
    var canvas = document.getElementById("gameCanvas");
    if (!canvas) return;
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
            osc.
