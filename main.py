import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TEKKEN 8 CHARACTER SELECT EDITION", page_icon="🥊", layout="wide"
)

st.title("🥊 철권 8 스타일 캐릭터 선택 & 3D 대전")

GAME_ENGINE_SELECT_3D = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    * { box-sizing: border-box; }
    body { background-color: #030308; color: white; text-align: center; font-family: 'Press Start 2P', cursive, sans-serif; margin: 0; padding: 10px; overflow: hidden; user-select: none; }
    
    #app-container { position: relative; width: 960px; height: 540px; margin: 0 auto; border: 4px solid #ef4444; border-radius: 12px; box-shadow: 0 0 30px rgba(239, 68, 68, 0.4); background: radial-gradient(circle, #1a0826 0%, #05020a 100%); overflow: hidden; }

    /* --- 캐릭터 선택 UI --- */
    #select-screen { position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: 10; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
    .select-title { font-size: 20px; color: #facc15; text-shadow: 0 0 10px #facc15, 2px 2px #000; margin-top: 5px; }

    /* 철권8 스타일 사선 그리드 */
    .grid-container { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
    .grid-row { display: flex; gap: 6px; transform: skewX(-18deg); }
    
    .char-slot {
        width: 80px; height: 75px; background: #1e1b4b; border: 2px solid #334155;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        position: relative; transition: all 0.15s ease; cursor: pointer; overflow: hidden;
    }
    .char-slot .avatar { width: 32px; height: 32px; border-radius: 50%; border: 2px solid #fff; margin-bottom: 4px; transform: skewX(18deg); }
    .char-slot .char-name { font-size: 7px; color: #cbd5e1; transform: skewX(18deg); text-align: center; }

    /* 커서 및 선택 효과 */
    .char-slot.p1-hover { border: 3px solid #ef4444; box-shadow: 0 0 15px #ef4444; z-index: 2; }
    .char-slot.p2-hover { border: 3px solid #3b82f6; box-shadow: 0 0 15px #3b82f6; z-index: 2; }
    .char-slot.p1-hover.p2-hover { border: 3px solid #a855f7; box-shadow: 0 0 15px #a855f7; }
    .char-slot.selected { background: #3730a3; }

    .player-banner { position: absolute; bottom: 25px; width: 220px; padding: 12px; background: rgba(0,0,0,0.8); border-radius: 8px; font-size: 11px; text-align: center; }
    #p1-banner { left: 20px; border-left: 6px solid #ef4444; color: #fca5a5; }
    #p2-banner { right: 20px; border-right: 6px solid #3b82f6; color: #93c5fd; }
    .status-text { font-size: 10px; margin-top: 6px; color: #facc15; }

    /* --- 3D 게임 화면 --- */
    #game-canvas { display: none; width: 100%; height: 100%; }
    #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; display: none; }
    .hp-bar-bg { position: absolute; top: 20px; width: 380px; height: 24px; background: #1e293b; border: 2px solid #fff; }
    .hp-bar-fill { height: 100%; transition: width 0.1s linear; }
    #p1-hp-bg { left: 30px; } #p1-hp { background: #ef4444; width: 100%; }
    #p2-hp-bg { right: 30px; } #p2-hp { background: #3b82f6; width: 100%; float: right; }
    .p-name { position: absolute; top: 48px; font-size: 12px; }
    #p1-name-ui { left: 30px; color: #ef4444; }
    #p2-name-ui { right: 30px; color: #3b82f6; }
    #vs-text { position: absolute; top: 18px; left: 50%; transform: translateX(-50%); font-size: 22px; color: #facc15; }
    #announcer { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 36px; color: #facc15; text-shadow: 3px 3px #000; }

    .controls-guide { font-family: sans-serif; font-size: 13px; color: #cbd5e1; background: #111827; padding: 10px 20px; border-radius: 8px; border: 1px solid #374151; margin-top: 10px; display: inline-block; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="app-container">
        <!-- 캐릭터 선택 화면 -->
        <div id="select-screen">
            <div class="select-title">SELECT YOUR FIGHTER</div>
            
            <div class="grid-container" id="grid-container"></div>

            <div id="p1-banner">
                <div>1P PLAYER</div>
                <div id="p1-char-name" style="font-size: 14px; margin-top: 4px; color: #fff;">KAZUYA</div>
                <div id="p1-status" class="status-text">[F] SELECT</div>
            </div>

            <div id="p2-banner">
                <div>2P PLAYER</div>
                <div id="p2-char-name" style="font-size: 14px; margin-top: 4px; color: #fff;">JIN</div>
                <div id="p2-status" class="status-text">[K] SELECT</div>
            </div>
        </div>

        <!-- 3D 인게임 CANVAS & UI -->
        <canvas id="game-canvas"></canvas>
        <div id="ui-layer">
            <div id="p1-hp-bg" class="hp-bar-bg"><div id="p1-hp" class="hp-bar-fill"></div></div>
            <div id="p1-name-ui" class="p-name">KAZUYA</div>
            <div id="vs-text">VS</div>
            <div id="p2-hp-bg" class="hp-bar-bg"><div id="p2-hp" class="hp-bar-fill"></div></div>
            <div id="p2-name-ui" class="p-name">JIN</div>
            <div id="announcer">READY...</div>
        </div>
    </div>

    <div class="controls-guide">
        <b>[선택 화면]</b> 1P: A/D (이동), F (선택) | 2P: ←/→ (이동), K (선택)<br>
        <b>[인게임]</b> 1P: A/D(이동), W(점프), F(펀치), G(킥) | 2P: ←/→(이동), ↑(점프), K(펀치), L(킥)
    </div>

<script>
// 32명 로스터 데이터
var CHARACTERS = [
    { id: 0, name: "JIN", color: "#16a34a", skin: "#fed7aa" },
    { id: 1, name: "KAZUYA", color: "#dc2626", skin: "#fca5a5" },
    { id: 2, name: "JUN", color: "#38bdf8", skin: "#fef08a" },
    { id: 3, name: "PAUL", color: "#ca8a04", skin: "#fde047" },
    { id: 4, name: "LAW", color: "#db2777", skin: "#fcd34d" },
    { id: 5, name: "KING", color: "#0891b2", skin: "#fdba74" },
    { id: 6, name: "LARS", color: "#a855f7", skin: "#fed7aa" },
    { id: 7, name: "XIAOYU", color: "#f43f5e", skin: "#fecdd3" },
    { id: 8, name: "JACK-8", color: "#475569", skin: "#64748b" },
    { id: 9, name: "NINA", color: "#e11d48", skin: "#fecdd3" },
    { id: 10, name: "ASUKA", color: "#0284c7", skin: "#fed7aa" },
    { id: 11, name: "LEROY", color: "#f59e0b", skin: "#d97706" },
    { id: 12, name: "LILI", color: "#ec4899", skin: "#fef08a" },
    { id: 13, name: "HWOARANG", color: "#ea580c", skin: "#fed7aa" },
    { id: 14, name: "BRYAN", color: "#52525b", skin: "#e4e4e7" },
    { id: 15, name: "CLAUDIO", color: "#2563eb", skin: "#fed7aa" },
    { id: 16, name: "AZUCENA", color: "#10b981", skin: "#fcd34d" },
    { id: 17, name: "RAVEN", color: "#1e1b4b", skin: "#78350f" },
    { id: 18, name: "LEO", color: "#84cc16", skin: "#fef08a" },
    { id: 19, name: "YOSHIMITSU", color: "#0d9488", skin: "#94a3b8" },
    { id: 20, name: "STEVE", color: "#0284c7", skin: "#fed7aa" },
    { id: 21, name: "DRAGUNOV", color: "#334155", skin: "#cbd5e1" },
    { id: 22, name: "SHAHEEN", color: "#d97706", skin: "#fed7aa" },
    { id: 23, name: "KUMA", color: "#78350f", skin: "#451a03" },
    { id: 24, name: "PANDA", color: "#f8fafc", skin: "#0f172a" },
    { id: 25, name: "ZAFINA", color: "#7e22ce", skin: "#fecdd3" },
    { id: 26, name: "LEE", color: "#9333ea", skin: "#fef08a" },
    { id: 27, name: "ALISA", color: "#f472b6", skin: "#fecdd3" },
    { id: 28, name: "VICTOR", color: "#475569", skin: "#fed7aa" },
    { id: 29, name: "RENA", color: "#818cf8", skin: "#fecdd3" },
    { id: 30, name: "EDDY", color: "#15803d", skin: "#b45309" },
    { id: 31, name: "LYDIA", color: "#e2e8f0", skin: "#fed7aa" }
];

var p1Idx = 1, p2Idx = 0;
var p1Ready = false, p2Ready = false;

// 4행 8열 사선 그리드 세팅
function initSelectGrid() {
    var container = document.getElementById('grid-container');
    container.innerHTML = '';

    for (var r = 0; r < 4; r++) {
        var rowDiv = document.createElement('div');
        rowDiv.className = 'grid-row';

        for (var c = 0; c < 8; c++) {
            var idx = r * 8 + c;
            var charData = CHARACTERS[idx];

            var slot = document.createElement('div');
            slot.className = 'char-slot';
            slot.id = 'slot-' + idx;

            var avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.style.backgroundColor = charData.skin;

            var name = document.createElement('div');
            name.className = 'char-name';
            name.innerText = charData.name;

            slot.appendChild(avatar);
            slot.appendChild(name);
            rowDiv.appendChild(slot);
        }
        container.appendChild(rowDiv);
    }
    updateSelectUI();
}

function updateSelectUI() {
    document.querySelectorAll('.char-slot').forEach(function(s) {
        s.classList.remove('p1-hover', 'p2-hover');
    });

    var s1 = document.getElementById('slot-' + p1Idx);
    var s2 = document.getElementById('slot-' + p2Idx);

    if (s1) s1.classList.add('p1-hover');
    if (s2) s2.classList.add('p2-hover');

    document.getElementById('p1-char-name').innerText = CHARACTERS[p1Idx].name;
    document.getElementById('p2-char-name').innerText = CHARACTERS[p2Idx].name;

    document.getElementById('p1-status').innerText = p1Ready ? "READY!" : "[F] SELECT";
    document.getElementById('p1-status').style.color = p1Ready ? "#4ade80" : "#facc15";

    document.getElementById('p2-status').innerText = p2Ready ? "READY!" : "[K] SELECT";
    document.getElementById('p2-status').style.color = p2Ready ? "#4ade80" : "#facc15";

    if (p1Ready && p2Ready) {
        setTimeout(start3DMatch, 600);
    }
}

window.addEventListener('keydown', function(e) {
    var k = e.key.toLowerCase();

    // 1P 조작 (A, D, F)
    if (!p1Ready) {
        if (k === 'a') { p1Idx = (p1Idx - 1 + 32) % 32; updateSelectUI(); }
        if (k === 'd') { p1Idx = (p1Idx + 1) % 32; updateSelectUI(); }
        if (k === 'f') { p1Ready = true; updateSelectUI(); }
    }

    // 2P 조작 (Left, Right, K)
    if (!p2Ready) {
        if (k === 'arrowleft') { p2Idx = (p2Idx - 1 + 32) % 32; updateSelectUI(); }
        if (k === 'arrowright') { p2Idx = (p2Idx + 1) % 32; updateSelectUI(); }
        if (k === 'k') { p2Ready = true; updateSelectUI(); }
    }
});

// Three.js 3D 대전 진입
function start3DMatch() {
    document.getElementById('select-screen').style.display = 'none';
    document.getElementById('game-canvas').style.display = 'block';
    document.getElementById('ui-layer').style.display = 'block';

    document.getElementById('p1-name-ui').innerText = CHARACTERS[p1Idx].name;
    document.getElementById('p2-name-ui').innerText = CHARACTERS[p2Idx].name;

    init3DEngine();
}

function init3DEngine() {
    var canvas = document.getElementById('game-canvas');
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a16);

    var camera = new THREE.PerspectiveCamera(45, 960 / 540, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setSize(960, 540);

    var ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    var dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 15);
    scene.add(dirLight);

    // 바닥
    var floorGeo = new THREE.PlaneGeometry(60, 60);
    var floorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
    var floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    var grid = new THREE.GridHelper(60, 30, 0xef4444, 0x334155);
    grid.position.y = 0.01;
    scene.add(grid);

    function createFighter(charData) {
        var group = new THREE.Group();
        var mat = new THREE.MeshStandardMaterial({ color: charData.color });
        var torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.5), mat);
        torso.position.y = 1.6;
        group.add(torso);

        var head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({ color: charData.skin }));
        head.position.y = 0.95;
        torso.add(head);

        var rArm = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.8, 0.25), mat);
        rArm.position.set(0.55, 0.2, 0);
        torso.add(rArm);

        return {
            group: group, torso: torso, rArm: rArm,
            x: 0, y: 0, hp: 100, facing: 1, hitStun: 0
        };
    }

    var p1 = createFighter(CHARACTERS[p1Idx]);
    var p2 = createFighter(CHARACTERS[p2Idx]);
    p1.x = -4; p2.x = 4;
    p1.facing = 1; p2.facing = -1;

    scene.add(p1.group);
    scene.add(p2.group);

    var inGameKeys = {};
    window.addEventListener('keydown', function(e) { inGameKeys[e.key.toLowerCase()] = true; });
    window.addEventListener('keyup', function(e) { inGameKeys[e.key.toLowerCase()] = false; });

    setTimeout(function() {
        document.getElementById('announcer').innerText = "FIGHT!";
        setTimeout(function() { document.getElementById('announcer').innerText = ""; }, 1000);
    }, 1000);

    function gameLoop() {
        // 1P
        if (inGameKeys['a']) { p1.x -= 0.12; p1.facing = -1; }
        if (inGameKeys['d']) { p1.x += 0.12; p1.facing = 1; }
        
        // 2P
        if (inGameKeys['arrowleft']) { p2.x -= 0.12; p2.facing = -1; }
        if (inGameKeys['arrowright']) { p2.x += 0.12; p2.facing = 1; }

        [p1, p2].forEach(function(p) {
            p.group.position.set(p.x, p.y, 0);
            p.group.rotation.y = p.facing === 1 ? Math.PI / 2 : -Math.PI / 2;
        });

        var midX = (p1.x + p2.x) / 2;
        var dist = Math.abs(p1.x - p2.x);
        camera.position.x += (midX - camera.position.x) * 0.1;
        camera.position.z = Math.max(8, dist * 1.2 + 3);
        camera.position.y = 3.5;
        camera.lookAt(midX, 1.5, 0);

        renderer.render(scene, camera);
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
}

window.onload = initSelectGrid;
</script>
</body>
</html>
"""

components.html(GAME_ENGINE_SELECT_3D, height=680)
