import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TEKKEN 8 BATTLE ENGINE", page_icon="🥊", layout="wide"
)

st.title("🥊 철권 8 스타일 3D 대전 격투 (Heat System & HUD)")

GAME_ENGINE_TEKKEN8 = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    * { box-sizing: border-box; }
    body { background-color: #030308; color: white; text-align: center; font-family: 'Press Start 2P', cursive, sans-serif; margin: 0; padding: 10px; overflow: hidden; user-select: none; }
    
    #app-container { 
        position: relative; 
        width: 960px; 
        height: 540px; 
        margin: 0 auto; 
        border: 3px solid #f43f5e; 
        border-radius: 8px; 
        box-shadow: 0 0 35px rgba(244, 63, 94, 0.5); 
        background: #000; 
        overflow: hidden; 
    }

    /* 3D Canvas */
    #game-canvas { width: 100%; height: 100%; display: block; }

    /* UI 레이어 */
    #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }

    /* 중앙 타이머 & 라운드 */
    #timer-container {
        position: absolute; top: 12px; left: 50%; transform: translateX(-50%);
        font-size: 32px; font-weight: bold; color: #fff; text-shadow: 0 0 10px #f43f5e, 2px 2px #000;
        z-index: 10;
    }
    .round-dots { font-size: 10px; color: #64748b; margin-bottom: 2px; letter-spacing: 4px; }
    .round-dots span.win { color: #facc15; text-shadow: 0 0 8px #facc15; }

    /* 상단 체력바 (기울어진 철권8 스타일) */
    .hp-container { position: absolute; top: 20px; width: 380px; }
    #p1-hp-container { left: 15px; }
    #p2-hp-container { right: 15px; }

    .hp-bar-outer {
        width: 100%; height: 26px; background: rgba(15, 23, 42, 0.85);
        border: 2px solid #cbd5e1; transform: skewX(-20deg); overflow: hidden;
        box-shadow: inset 0 0 10px #000;
    }
    .hp-bar-fill { height: 100%; transition: width 0.1s linear; }
    #p1-hp { background: linear-gradient(90deg, #ef4444 0%, #f97316 100%); width: 100%; }
    #p2-hp { background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%); width: 100%; float: right; }

    /* 히트 게이지 (Heat Gauge) */
    .heat-bar-outer {
        width: 90%; height: 6px; background: #1e293b;
        transform: skewX(-20deg); margin-top: 4px; border: 1px solid #475569;
    }
    #p1-heat-outer { float: left; } #p2-heat-outer { float: right; }
    .heat-bar-fill { height: 100%; background: #facc15; box-shadow: 0 0 8px #facc15; width: 100%; }

    /* 캐릭터 프로필 & 이름 */
    .char-profile { position: absolute; top: 56px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    #p1-name { left: 20px; color: #fca5a5; text-shadow: 0 0 6px #ef4444; }
    #p2-name { right: 20px; color: #93c5fd; text-shadow: 0 0 6px #3b82f6; }

    /* 철권 8 스페셜 스타일 스킬 패널 (좌/우 하단) */
    .special-panel {
        position: absolute; bottom: 20px; width: 180px;
        background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px; padding: 8px 10px; font-family: sans-serif; font-size: 10px; color: #cbd5e1;
        backdrop-filter: blur(4px); text-align: left;
    }
    #p1-special { left: 15px; border-left: 4px solid #ef4444; }
    #p2-special { right: 15px; border-right: 4px solid #3b82f6; text-align: right; }
    .skill-row { margin: 4px 0; display: flex; align-items: center; justify-content: space-between; }
    .key-badge { background: #334155; border: 1px solid #94a3b8; border-radius: 3px; padding: 1px 4px; font-size: 9px; color: #facc15; font-weight: bold; }

    /* 아나운서 텍스트 */
    #announcer { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 42px; color: #facc15; text-shadow: 0 0 20px #ef4444, 4px 4px #000; }

    .controls-guide { font-family: sans-serif; font-size: 13px; color: #cbd5e1; background: #111827; padding: 10px 20px; border-radius: 8px; border: 1px solid #374151; margin-top: 10px; display: inline-block; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="app-container">
        <canvas id="game-canvas"></canvas>

        <!-- UI 레이어 -->
        <div id="ui-layer">
            <!-- 중앙 타이머 & 라운드 -->
            <div id="timer-container">
                <div class="round-dots"><span class="win">●</span>●● &nbsp; ●●●</div>
                <span id="timer">60</span>
            </div>

            <!-- 1P HP & HEAT -->
            <div id="p1-hp-container" class="hp-container">
                <div class="hp-bar-outer"><div id="p1-hp" class="hp-bar-fill"></div></div>
                <div id="p1-heat-outer" class="heat-bar-outer"><div id="p1-heat" class="heat-bar-fill"></div></div>
            </div>
            <div id="p1-name" class="char-profile">JIN</div>

            <!-- 2P HP & HEAT -->
            <div id="p2-hp-container" class="hp-container">
                <div class="hp-bar-outer"><div id="p2-hp" class="hp-bar-fill"></div></div>
                <div id="p2-heat-outer" class="heat-bar-outer"><div id="p2-heat" class="heat-bar-fill"></div></div>
            </div>
            <div id="p2-name" class="char-profile">XIAOYU</div>

            <!-- 1P 스페셜 패널 -->
            <div id="p1-special" class="special-panel">
                <div class="skill-row"><span>Specialty Move</span> <span class="key-badge">F</span></div>
                <div class="skill-row"><span>Air Combos</span> <span class="key-badge">G</span></div>
                <div class="skill-row"><span>Power Crush</span> <span class="key-badge">T</span></div>
                <div class="skill-row"><span>Heat Smash</span> <span class="key-badge">R</span></div>
            </div>

            <!-- 2P 스페셜 패널 -->
            <div id="p2-special" class="special-panel">
                <div class="skill-row"><span class="key-badge">K</span> <span>Specialty Move</span></div>
                <div class="skill-row"><span class="key-badge">L</span> <span>Air Combos</span></div>
                <div class="skill-row"><span class="key-badge">P</span> <span>Power Crush</span></div>
                <div class="skill-row"><span class="key-badge">O</span> <span>Heat Smash</span></div>
            </div>

            <div id="announcer">READY...</div>
        </div>
    </div>

    <div class="controls-guide">
        <b>[1P]</b> 이동: A, D | 점프: W | 펀치: F | 킥: G | 잡기: T | <b>HEAT SMASH: R</b><br>
        <b>[2P]</b> 이동: ←, → | 점프: ↑ | 펀치: K | 킥: L | 잡기: P | <b>HEAT SMASH: O</b>
    </div>

<script>
function initTekken8Game() {
    var canvas = document.getElementById('game-canvas');
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x05050d);
    scene.fog = new THREE.FogExp2(0x05050d, 0.018);

    var camera = new THREE.PerspectiveCamera(45, 960 / 540, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
    renderer.setSize(960, 540);
    renderer.shadowMap.enabled = true;

    // 조명 (화려한 네온 격투장 느킴)
    var ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    var mainLight = new THREE.DirectionalLight(0xffffff, 0.9);
    mainLight.position.set(10, 25, 15);
    mainLight.castShadow = true;
    scene.add(mainLight);

    var redLight = new THREE.PointLight(0xef4444, 2, 25);
    redLight.position.set(-8, 4, 2);
    scene.add(redLight);

    var blueLight = new THREE.PointLight(0x3b82f6, 2, 25);
    blueLight.position.set(8, 4, 2);
    scene.add(blueLight);

    // 바닥 (철권 8 화려한 아레나 매쉬)
    var floorGeo = new THREE.PlaneGeometry(60, 60);
    var floorMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.2, metalness: 0.5 });
    var floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    var grid = new THREE.GridHelper(60, 30, 0xef4444, 0x1e293b);
    grid.position.y = 0.01;
    scene.add(grid);

    // 파티클 엔진 (스파크 / 폭발)
    var particles = [];
    function createHitSpark(x, y, z, colorHex, count) {
        for (var i = 0; i < count; i++) {
            var geo = new THREE.SphereGeometry(Math.random() * 0.12 + 0.04, 8, 8);
            var mat = new THREE.MeshBasicMaterial({ color: colorHex });
            var p = new THREE.Mesh(geo, mat);
            p.position.set(x, y, z);
            scene.add(p);

            particles.push({
                mesh: p,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.3) * 0.4,
                vz: (Math.random() - 0.5) * 0.4,
                life: 1.0
            });
        }
    }

    // 캐릭터 생성
    function createFighter(colorHex, isP1) {
        var group = new THREE.Group();
        var mat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.3, metalness: 0.3 });
        
        // 상체
        var torso = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.25, 0.5), mat);
        torso.position.y = 1.6;
        torso.castShadow = true;
        group.add(torso);

        // 머리
        var head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 16, 16), new THREE.MeshStandardMaterial({ color: 0xfdba74 }));
        head.position.y = 0.95;
        head.castShadow = true;
        torso.add(head);

        // 오른팔
        var rArm = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.85, 0.25), mat);
        rArm.position.set(0.55, 0.2, 0);
        rArm.castShadow = true;
        torso.add(rArm);

        // 오른다리
        var rLeg = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.95, 0.3), mat);
        rLeg.position.set(0.25, -0.9, 0);
        rLeg.castShadow = true;
        torso.add(rLeg);

        return {
            group: group, torso: torso, rArm: rArm, rLeg: rLeg,
            x: isP1 ? -3.5 : 3.5, y: 0, hp: 100, heat: 100, facing: isP1 ? 1 : -1,
            isGrounded: true, vy: 0, isAttacking: false, hitStun: 0
        };
    }

    var p1 = createFighter(0xdc2626, true);
    var p2 = createFighter(0x0284c7, false);

    scene.add(p1.group);
    scene.add(p2.group);

    var keys = {};
    window.addEventListener('keydown', function(e) { keys[e.key.toLowerCase()] = true; });
    window.addEventListener('keyup', function(e) { keys[e.key.toLowerCase()] = false; });

    var cameraShake = 0;
    var timerValue = 60;
    var gameState = "PLAY";

    // 타이머 인터벌
    setInterval(function() {
        if (gameState === "PLAY" && timerValue > 0) {
            timerValue--;
            document.getElementById('timer').innerText = timerValue;
        }
    }, 1000);

    setTimeout(function() {
        document.getElementById('announcer').innerText = "FIGHT!";
        setTimeout(function() { document.getElementById('announcer').innerText = ""; }, 1000);
    }, 1000);

    // 공격 처리 (철권 8 화려한 파티클 연출)
    function handleAttack(attacker, defender, type) {
        if (attacker.isAttacking || attacker.hitStun > 0) return;

        attacker.isAttacking = true;
        var dmg = type === 'heat' ? 30 : (type === 'kick' ? 16 : 10);
        var range = type === 'heat' ? 3.0 : 2.2;

        if (type === 'punch') {
            attacker.rArm.rotation.x = -Math.PI / 2;
            attacker.rArm.position.z = 0.5 * attacker.facing;
        } else if (type === 'kick') {
            attacker.rLeg.rotation.x = -Math.PI / 2;
            attacker.rLeg.position.z = 0.6 * attacker.facing;
        } else if (type === 'heat') {
            attacker.rArm.rotation.x = -Math.PI / 2;
            attacker.rArm.position.z = 0.8 * attacker.facing;
            attacker.heat = Math.max(0, attacker.heat - 50);
        }

        var dist = Math.abs(attacker.x - defender.x);
        if (dist < range) {
            defender.hp = Math.max(0, defender.hp - dmg);
            defender.hitStun = 12;
            defender.x += attacker.facing * (type === 'heat' ? 1.2 : 0.5);
            cameraShake = type === 'heat' ? 0.6 : 0.25;

            // 스크린샷과 같은 화려한 불꽃/스파크 생성
            var targetX = defender.x;
            var targetY = 1.6;
            var color = type === 'heat' ? 0xff3300 : 0xfacc15;
            createHitSpark(targetX, targetY, 0, color, type === 'heat' ? 40 : 20);

            // UI 업데이트
            document.getElementById('p1-hp').style.width = p1.hp + '%';
            document.getElementById('p2-hp').style.width = p2.hp + '%';
            document.getElementById('p1-heat').style.width = p1.heat + '%';
            document.getElementById('p2-heat').style.width = p2.heat + '%';

            if (defender.hp <= 0 && gameState === "PLAY") {
                gameState = "END";
                var winner = attacker === p1 ? "1P WINNER!" : "2P WINNER!";
                document.getElementById('announcer').innerText = winner;
            }
        }

        setTimeout(function() {
            attacker.rArm.rotation.set(0, 0, 0);
            attacker.rArm.position.set(0.55, 0.2, 0);
            attacker.rLeg.rotation.set(0, 0, 0);
            attacker.rLeg.position.set(0.25, -0.9, 0);
            attacker.isAttacking = false;
        }, 220);
    }

    function animate() {
        if (gameState === "PLAY") {
            // 1P 컨트롤
            if (p1.hitStun === 0) {
                if (keys['a']) { p1.x -= 0.12; p1.facing = -1; }
                if (keys['d']) { p1.x += 0.12; p1.facing = 1; }
                if (keys['w'] && p1.isGrounded) { p1.vy = 0.22; p1.isGrounded = false; }
                if (keys['f']) handleAttack(p1, p2, 'punch');
                if (keys['g']) handleAttack(p1, p2, 'kick');
                if (keys['r']) handleAttack(p1, p2, 'heat');
            } else { p1.hitStun--; }

            // 2P 컨트롤
            if (p2.hitStun === 0) {
                if (keys['arrowleft']) { p2.x -= 0.12; p2.facing = -1; }
                if (keys['arrowright']) { p2.x += 0.12; p2.facing = 1; }
                if (keys['arrowup'] && p2.isGrounded) { p2.vy = 0.22; p2.isGrounded = false; }
                if (keys['k']) handleAttack(p2, p1, 'punch');
                if (keys['l']) handleAttack(p2, p1, 'kick');
                if (keys['o']) handleAttack(p2, p1, 'heat');
            } else { p2.hitStun--; }

            // 중력 및 이동
            [p1, p2].forEach(function(p) {
                p.vy -= 0.012;
                p.y += p.vy;
                if (p.y <= 0) { p.y = 0; p.vy = 0; p.isGrounded = true; }
                p.group.position.set(p.x, p.y, 0);
                p.group.rotation.y = p.facing === 1 ? Math.PI / 2 : -Math.PI / 2;
            });

            // 파티클 업데이트
            for (var i = particles.length - 1; i >= 0; i--) {
                var pt = particles[i];
                pt.mesh.position.x += pt.vx;
                pt.mesh.position.y += pt.vy;
                pt.mesh.position.z += pt.vz;
                pt.life -= 0.04;
                pt.mesh.scale.setScalar(pt.life);
                if (pt.life <= 0) {
                    scene.remove(pt.mesh);
                    particles.splice(i, 1);
                }
            }

            // 철권 8 시네마틱 카메라 (줌인/줌아웃 & 셰이크)
            var midX = (p1.x + p2.x) / 2;
            var dist = Math.abs(p1.x - p2.x);
            var targetCamZ = Math.max(7, Math.min(15, dist * 1.1 + 3));

            camera.position.x += (midX - camera.position.x) * 0.1;
            camera.position.z += (targetCamZ - camera.position.z) * 0.1;
            camera.position.y = 3.2;

            if (cameraShake > 0) {
                camera.position.x += (Math.random() - 0.5) * cameraShake;
                camera.position.y += (Math.random() - 0.5) * cameraShake;
                cameraShake *= 0.85;
            }

            camera.lookAt(midX, 1.5, 0);
        }

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    animate();
}

window.onload = initTekken8Game;
</script>
</body>
</html>
"""

components.html(GAME_ENGINE_TEKKEN8, height=680)
