import sys
import pygame

# 초기화
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2P 격투 게임")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
GREEN = (50, 220, 50)
YELLOW = (240, 200, 50)
GRAY = (100, 100, 100)

# 캐릭터 정보 (6명)
CHARACTERS = [
    {
        "name": "Kazuya",
        "color": (180, 50, 50),
        "hp": 100,
        "speed": 6,
        "atk": 10,
        "ult": 30,
    },
    {
        "name": "Jin",
        "color": (50, 180, 50),
        "hp": 90,
        "speed": 8,
        "atk": 8,
        "ult": 25,
    },
    {
        "name": "Paul",
        "color": (220, 180, 50),
        "hp": 120,
        "speed": 5,
        "atk": 15,
        "ult": 40,
    },
    {
        "name": "Law",
        "color": (180, 50, 180),
        "hp": 85,
        "speed": 9,
        "atk": 7,
        "ult": 22,
    },
    {
        "name": "King",
        "color": (50, 180, 180),
        "hp": 110,
        "speed": 6,
        "atk": 12,
        "ult": 35,
    },
    {
        "name": "Nina",
        "color": (200, 100, 150),
        "hp": 95,
        "speed": 7,
        "atk": 9,
        "ult": 28,
    },
]

font_large = pygame.font.SysFont("malgungothic", 36)
font_small = pygame.font.SysFont("malgungothic", 20)


class Player:

    def __init__(self, x, y, stats, is_p1):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.name = stats["name"]
        self.color = stats["color"]
        self.max_hp = stats["hp"]
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.atk_damage = stats["atk"]
        self.ult_damage = stats["ult"]
        self.is_p1 = is_p1

        # 상태 변수
        self.vel_y = 0
        self.is_jumping = False
        self.attacking = False
        self.attack_type = None  # 'normal' or 'ult'
        self.attack_timer = 0
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.ult_gauge = 0  # 궁극기 게이지 (100 최대)

    def move(self, keys):
        dx = 0
        gravity = 1

        # 이동 키 설정
        if self.is_p1:
            if keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_d]:
                dx = self.speed
            if keys[pygame.K_w] and not self.is_jumping:
                self.vel_y = -15
                self.is_jumping = True
        else:
            if keys[pygame.K_LEFT]:
                dx = -self.speed
            if keys[pygame.K_RIGHT]:
                dx = self.speed
            if keys[pygame.K_UP] and not self.is_jumping:
                self.vel_y = -15
                self.is_jumping = True

        # 점프 및 중력 처리
        self.vel_y += gravity
        self.y += self.vel_y

        # 바닥 충돌
        if self.y >= HEIGHT - 150:
            self.y = HEIGHT - 150
            self.is_jumping = False

        # 화면 좌우 경계
        self.x = max(0, min(WIDTH - self.width, self.x + dx))

    def attack(self, target, atk_type):
        if self.attacking:
            return

        if atk_type == "ult" and self.ult_gauge < 100:
            return  # 게이지 부족시 궁극기 불가

        self.attacking = True
        self.attack_type = atk_type
        self.attack_
