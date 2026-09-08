import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TEKKEN 3D THREE.JS EDITION", page_icon="🥊", layout="wide"
)

st.title("🥊 Three.js 기반 3D 철권 대전 게임")

GAME_ENGINE_3D = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    * { box-sizing: border-box; }
    body { background-color: #030308; color: white; text-align: center; font-family: 'Press Start 2P', cursive, sans-serif; margin: 0; padding: 10px; overflow: hidden; }
    #canvas-container { position: relative; width: 960px; height: 540px; margin: 0 auto; border: 4px solid #f43f5e; border-radius: 12px; box-shadow: 0 0 25px #f43f5e; }
    #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    .hp-bar-bg { position: absolute; top: 20px; width: 380px; height: 24px; background: #1e293b; border: 2px solid #fff; }
    .hp-bar-fill { height: 100%; transition: width 0.1s linear; }
    #p1-hp-bg { left: 30px; }
    #p1-hp { background: #ef4444; width: 100%; }
    #p2-hp-bg { right: 30px; }
    #p2-hp { background: #3b82f6; width: 100%; float: right; }
    .p-name { position: absolute; top: 48px; font-size: 12px; }
    #p1-name { left: 30px; color: #ef4444; }
    #p2-name { right: 30px; color: #3b82f6; }
    #vs-text { position: absolute; top: 18px; left: 50%; transform: translateX(-50%); font-size: 22px; color: #facc15; }
    #announcer { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 36px; color: #facc15; text-shadow: 3px 3px #000; }
    .controls-guide { font-family: sans-serif; font-size: 13px; color: #cbd5e1; background: #111827; padding: 10px 20px; border-radius: 8px; border: 1px solid #374151; margin-top: 10px; display: inline-block; }
</style>
<!-- Three.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="canvas-container">
        <div id="ui-layer">
            <div id="p1-hp-bg" class="hp-bar-bg"><div id="p1-hp" class="hp-bar-fill"></div></div>
            <div id="p1-name" class="p-name">1P KAZUYA</div>
            <div id="vs-text">VS</div>
            <div id="p2-hp-bg" class="hp-bar-bg"><div id="p2-hp" class="hp-bar-fill"></div></div>
            <div id="p2-name" class="p-name">2P JIN</div>
            <div id="announcer">READY...</div>
        </div>
    </div>
    <div class="controls-guide">
        <b>[1P]</b> 이동: A, D | 점프: W | 가드: S | 펀치: F | 킥: G<br>
        <b>[2P]</b> 이동: ←, → | 점프: ↑ | 가드: ↓ | 펀치: K | 킥: L
    </div>

<script>
function init3DGame() {
    var container = document.getElementById('canvas-container');
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a16);
    scene.fog = new THREE.FogExp2(0x0a0a16, 0.015);

    var camera = new THREE.PerspectiveCamera(45, 960 / 540, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(960, 540);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // 조명 설정
    var ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    var dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 15);
    dirLight.castShadow = true;
    scene.add(dirLight);

    var pointLight = new THREE.PointLight(0xf43f5e, 1, 30);
    pointLight.position.set(0, 5, 0);
    scene.add(pointLight);

    // 3D 스테이지 바닥
    var floorGeo = new THREE.PlaneGeometry(60, 60);
    var floorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.2 });
    var floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    var grid = new THREE.GridHelper(60, 30, 0xf43f5e, 0x334155);
    grid.position.y = 0.01;
    scene.add(grid);

    // 3D 관절 캐릭터 생성 함수
    function createFighter(color) {
        var group = new THREE.Group();

        // 몸통
        var torsoGeo = new THREE.BoxGeometry(0.8, 1.2, 0.5);
        var mat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.3 });
        var torso = new THREE.Mesh(torsoGeo, mat);
        torso.position.y = 1.6;
        torso.castShadow = true;
        group.add(torso);

        // 머리
        var headGeo = new THREE.SphereGeometry(0.35, 16, 16);
        var headMat = new THREE.MeshStandardMaterial({ color: 0xfdba74 });
        var head = new THREE.Mesh(headGeo, headMat);
        head.position.y = 0.95;
        head.castShadow = true;
        torso.add(head);

        // 오른팔 (펀치 관절)
        var armGeo = new THREE.BoxGeometry(0.25, 0.8, 0.25);
        var rArm = new THREE.Mesh(armGeo, mat);
        rArm.position.set(0.55, 0.2, 0);
        rArm.castShadow = true;
        torso.add(rArm);

        // 오른다리 (킥 관절)
        var legGeo = new THREE.BoxGeometry(0.3, 0.9, 0.3);
        var rLeg = new THREE.Mesh(legGeo, mat);
        rLeg.position.set(0.25, -0.9, 0);
        rLeg.castShadow = true;
        torso.add(rLeg);

        return {
            group: group,
            torso: torso,
            rArm: rArm,
            rLeg: rLeg,
            x: 0, y: 0,
            hp: 100,
            vx: 0, vy: 0,
            facing: 1,
            isGrounded: true,
            isAttacking: false,
            hitStun: 0
        };
    }

    var p1 = createFighter(0xef4444);
    var p2 = createFighter(0x3b82f6);

    p1.x = -4; p2.x = 4;
    p1.facing = 1; p2.facing = -1;

    scene.add(p1.group);
    scene.add(p2.group);

    var keys = {};
    window.addEventListener('keydown', function(e) { keys[e.key.toLowerCase()] = true; });
    window.addEventListener('keyup', function(e) { keys[e.key.toLowerCase()] = false; });

    var cameraShake = 0;
    var gameState = "PLAY";

    setTimeout(function() {
        document.getElementById('announcer').innerText = "FIGHT!";
        setTimeout(function() { document.getElementById('announcer').innerText = ""; }, 1000);
    }, 1000);

    function attack(attacker, defender, type) {
        if (attacker.isAttacking || attacker.hitStun > 0) return;

        attacker.isAttacking = true;
        var dmg = type === 'punch' ? 12 : 18;
        var range = type === 'punch' ? 2.2 : 2.8;

        if (type === 'punch') {
            attacker.rArm.rotation.x = -Math.PI / 2;
            attacker.rArm.position.z = 0.5 * attacker.facing;
        } else {
            attacker.rLeg.rotation.x = -Math.PI / 2;
            attacker.rLeg.position.z = 0.6 * attacker.facing;
        }

        // 히트 판정
        var dist = Math.abs(attacker.x - defender.x);
        if (dist < range) {
            defender.hp = Math.max(0, defender.hp - dmg);
            defender.hitStun = 10;
            defender.x += attacker.facing * 0.6;
            cameraShake = 0.3;

            // UI 갱신
            document.getElementById('p1-hp').style.width = p1.hp + '%';
            document.getElementById('p2-hp').style.width = p2.hp + '%';

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
        }, 200);
    }

    function update() {
        if (gameState === "PLAY") {
            // 1P 조작
            if (p1.hitStun === 0) {
                if (keys['a']) { p1.x -= 0.12; p1.facing = -1; }
                if (keys['d']) { p1.x += 0.12; p1.facing = 1; }
                if (keys['w'] && p1.isGrounded) { p1.vy = 0.22; p1.isGrounded = false; }
                if (keys['f']) attack(p1, p2, 'punch');
                if (keys['g']) attack(p1, p2, 'kick');
            } else { p1.hitStun--; }

            // 2P 조작
            if (p2.hitStun === 0) {
                if (keys['arrowleft']) { p2.x -= 0.12; p2.facing = -1; }
                if (keys['arrowright']) { p2.x += 0.12; p2.facing = 1; }
                if (keys['arrowup'] && p2.isGrounded) { p2.vy = 0.22; p2.isGrounded = false; }
                if (keys['k']) attack(p2, p1, 'punch');
                if (keys['l']) attack(p2, p1, 'kick');
            } else { p2.hitStun--; }

            // 중력 및 이동 업데이트
            [p1, p2].forEach(function(p) {
                p.vy -= 0.012;
                p.y += p.vy;
                if (p.y <= 0) { p.y = 0; p.vy = 0; p.isGrounded = true; }
                p.group.position.set(p.x, p.y, 0);
                p.group.rotation.y = p.facing === 1 ? Math.PI / 2 : -Math.PI / 2;
            });

            // 3D 동적 카메라 연출 (캐릭터간 거리 기반 줌인/줌아웃)
            var midX = (p1.x + p2.x) / 2;
            var dist = Math.abs(p1.x - p2.x);
            var targetCamZ = Math.max(8, Math.min(16, dist * 1.2 + 3));

            camera.position.x += (midX - camera.position.x) * 0.08;
            camera.position.z += (targetCamZ - camera.position.z) * 0.08;
            camera.position.y = 3.5;

            // 카메라 셰이크
            if (cameraShake > 0) {
                camera.position.x += (Math.random() - 0.5) * cameraShake;
                camera.position.y += (Math.random() - 0.5) * cameraShake;
                cameraShake *= 0.85;
            }

            camera.lookAt(midX, 1.5, 0);
        }

        renderer.render(scene, camera);
        requestAnimationFrame(update);
    }

    update();
}

window.onload = init3DGame;
</script>
</body>
</html>
"""

components.html(GAME_ENGINE_3D, height=680)
