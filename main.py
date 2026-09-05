import sys
import pygame

# 초기화
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2P 격투 게임 - 최강자 배준서 참전!")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
GREEN = (50, 220, 50)
YELLOW = (240, 200, 50)
PURPLE = (150, 0, 255)
GRAY = (100, 100, 100)

# 캐릭터 정보 (7명 / 히든 캐릭터: 배준서)
CHARACTERS = [
    {
        "name": "Bae Jun-seo (HIDDEN)",
        "color": PURPLE,
        "hp": 200,
        "speed": 12,
        "atk": 25,
        "ult": 80,
    },  # ★ 최강 히든
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

# 폰트 에러 방지를 위해 파이썬 기본 폰트 사용
font_large = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)


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
        self.attack_type = None
        self.attack_timer = 0
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.ult_gauge = 0  # 궁극기 게이지 (100 최대)

    def move(self, keys):
        dx = 0
        gravity = 1

        # 이동 조작
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

        # 중력 적용
        self.vel_y += gravity
        self.y += self.vel_y

        # 바닥 경계
        if self.y >= HEIGHT - 150:
            self.y = HEIGHT - 150
            self.is_jumping = False

        # 좌우 경계
        self.x = max(0, min(WIDTH - self.width, self.x + dx))

    def attack(self, target, atk_type):
        if self.attacking:
            return

        if atk_type == "ult" and self.ult_gauge < 100:
            return

        self.attacking = True
        self.attack_type = atk_type
        self.attack_timer = 15

        # 공격 범위 설정
        direction = 1 if self.x < target.x else -1
        range_width = 90 if atk_type == "normal" else 150
        damage = self.atk_damage if atk_type == "normal" else self.ult_damage

        if direction == 1:
            self.hitbox = pygame.Rect(
                self.x + self.width, self.y, range_width, self.height
            )
        else:
            self.hitbox = pygame.Rect(
                self.x - range_width, self.y, range_width, self.height
            )

        # 히트 판정
        target_rect = pygame.Rect(
            target.x, target.y, target.width, target.height
        )
        if self.hitbox.colliderect(target_rect):
            target.hp = max(0, target.hp - damage)
            if atk_type == "normal":
                self.ult_gauge = min(100, self.ult_gauge + 35)

        if atk_type == "ult":
            self.ult_gauge = 0

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=5,
        )

        if self.attacking:
            color = RED if self.attack_type == "normal" else YELLOW
            pygame.draw.rect(surface, color, self.hitbox, 3)


def select_screen():
    p1_idx = 0  # 1P 기본값: 배준서
    p2_idx = 1
    selected = [False, False]

    while True:
        screen.fill(BLACK)
        title = font_large.render(
            "SELECT CHARACTER (1P: A/D/F | 2P: LEFT/RIGHT/K)", True, WHITE
        )
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        # 캐릭터 셀 그리드
        for i, char in enumerate(CHARACTERS):
            x = 50 + (i % 4) * 230
            y = 80 + (i // 4) * 160
            rect = pygame.Rect(x, y, 210, 140)

            pygame.draw.rect(screen, char["color"], rect, border_radius=10)

            # 테두리 표시
            if p1_idx == i:
                pygame.draw.rect(screen, RED, rect, 5, border_radius=10)
                p1_txt = font_small.render("1P", True, RED)
                screen.blit(p1_txt, (x + 10, y + 10))

            if p2_idx == i:
                pygame.draw.rect(screen, BLUE, rect, 5, border_radius=10)
                p2_txt = font_small.render("2P", True, BLUE)
                screen.blit(p2_txt, (x + 170, y + 10))

            name = font_small.render(char["name"], True, WHITE)
            info = font_small.render(
                f"HP:{char['hp']} ATK:{char['atk']}", True, WHITE
            )
            screen.blit(name, (x + 15, y + 45))
            screen.blit(info, (x + 15, y + 85))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # 1P (A/D로 선택, F로 확정)
                if not selected[0]:
                    if event.key == pygame.K_a:
                        p1_idx = (p1_idx - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_d:
                        p1_idx = (p1_idx + 1) % len(CHARACTERS)
                    elif event.key == pygame.K_f:
                        selected[0] = True

                # 2P (화살표 좌/우로 선택, K로 확정)
                if not selected[1]:
                    if event.key == pygame.K_LEFT:
                        p2_idx = (p2_idx - 1) % len(CHARACTERS)
                    elif event.key == pygame.K_RIGHT:
                        p2_idx = (p2_idx + 1) % len(CHARACTERS)
                    elif event.key == pygame.K_k:
                        selected[1] = True

        if selected[0] and selected[1]:
            return CHARACTERS[p1_idx], CHARACTERS[p2_idx]


def main():
    p1_stats, p2_stats = select_screen()

    p1 = Player(150, 350, p1_stats, is_p1=True)
    p2 = Player(800, 350, p2_stats, is_p1=False)

    running = True
    winner = None

    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))

        # 바닥
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not winner:
                # 1P 공격 (F: 평타, G: 궁극기)
                if event.key == pygame.K_f:
                    p1.attack(p2, "normal")
                elif event.key == pygame.K_g:
                    p1.attack(p2, "ult")

                # 2P 공격 (K: 평타, L: 궁극기)
                if event.key == pygame.K_k:
                    p2.attack(p1, "normal")
                elif event.key == pygame.K_l:
                    p2.attack(p1, "ult")

        if not winner:
            keys = pygame.key.get_pressed()
            p1.move(keys)
            p2.move(keys)

            p1.update()
            p2.update()

            if p1.hp <= 0:
                winner = "2P WIN!"
            elif p2.hp <= 0:
                winner = "1P WIN!"

        p1.draw(screen)
        p2.draw(screen)

        # 체력 및 궁극기 게이지 UI
        pygame.draw.rect(screen, GRAY, (50, 30, 300, 25))
        pygame.draw.rect(
            screen, RED, (50, 30, (p1.hp / p1.max_hp) * 300, 25)
        )
        p1_name = font_small.render(f"1P: {p1.name}", True, WHITE)
        screen.blit(p1_name, (50, 5))

        pygame.draw.rect(screen, GRAY, (50, 60, 300, 10))
        pygame.draw.rect(
            screen, YELLOW, (50, 60, (p1.ult_gauge / 100) * 300, 10)
        )

        pygame.draw.rect(screen, GRAY, (650, 30, 300, 25))
        pygame.draw.rect(
            screen, BLUE, (650, 30, (p2.
