import pygame
import math
import sys

pygame.init()

# ----- 기본 설정 -----
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense - Front Target Merge Ver")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ----- 색상 -----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (80, 220, 80)
BLUE = (60, 140, 255)
CYAN = (60, 255, 255)
YELLOW = (255, 220, 60)
GREY = (150, 150, 150)
PATH_COLOR = (100, 80, 60)

# ----- 게임 변수 -----
money = 100
lives = 10
wave = 1
spawn_timer = 0
wave_timer = 0
enemies_to_spawn = 10
dragging_tower = None
drag_offset = (0, 0)

# ----- S자형 경로 -----
path_points = [
    (0, 100), (200, 100),
    (200, 300), (400, 300),
    (400, 150), (600, 150),
    (600, 400), (800, 400),
    (900, 400)
]

def draw_path():
    pygame.draw.lines(screen, PATH_COLOR, False, path_points, 25)

# ----- 클래스 정의 -----
class Enemy:
    def __init__(self, wave_level):
        self.path_index = 0
        self.pos = pygame.Vector2(path_points[0])
        self.speed = 1.5 + wave_level * 0.15
        self.hp = 100 + wave_level * 25
        self.max_hp = self.hp
        self.alive = True

    def update(self):
        if not self.alive:
            return
        if self.path_index < len(path_points) - 1:
            target = pygame.Vector2(path_points[self.path_index + 1])
            direction = target - self.pos
            distance = direction.length()
            if distance != 0:
                direction = direction.normalize()
                move = min(self.speed, distance)
                self.pos += direction * move
            if distance < self.speed:
                self.path_index += 1
        else:
            global lives
            lives -= 1
            self.alive = False

    def progress(self):
        """현재 경로 진행 비율 계산"""
        if self.path_index >= len(path_points) - 1:
            return float(self.path_index)
        current = pygame.Vector2(path_points[self.path_index])
        next_ = pygame.Vector2(path_points[self.path_index + 1])
        segment_len = (next_ - current).length()
        if segment_len == 0:
            return float(self.path_index)
        return self.path_index + (self.pos - current).length() / segment_len

    def draw(self):
        if self.alive:
            pygame.draw.circle(screen, RED, (int(self.pos.x), int(self.pos.y)), 15)
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, BLACK, (self.pos.x - 20, self.pos.y - 25, 40, 5))
            pygame.draw.rect(screen, GREEN, (self.pos.x - 20, self.pos.y - 25, 40 * ratio, 5))

class Bullet:
    def __init__(self, x, y, target, damage):
        self.pos = pygame.Vector2(x, y)
        self.target = target
        self.speed = 7
        self.damage = damage
        self.alive = True

    def update(self):
        if not self.alive or not self.target.alive:
            self.alive = False
            return
        direction = self.target.pos - self.pos
        distance = direction.length()
        if distance < self.speed or distance == 0:
            self.target.hp -= self.damage
            if self.target.hp <= 0:
                self.target.alive = False
                global money
                money += 15
            self.alive = False
        else:
            direction = direction.normalize()
            self.pos += direction * self.speed

    def draw(self):
        if self.alive:
            pygame.draw.circle(screen, YELLOW, (int(self.pos.x), int(self.pos.y)), 5)

class Tower:
    def __init__(self, x, y, power=25, cooldown=40, range_=130, level=1):
        self.x = x
        self.y = y
        self.power = power
        self.range = range_
        self.cooldown = cooldown
        self.timer = 0
        self.level = level

    def update(self, enemies, bullets):
        if self.timer > 0:
            self.timer -= 1
            return

        target = None
        max_progress = -1
        for e in enemies:
            if not e.alive:
                continue
            dist = math.hypot(e.pos.x - self.x, e.pos.y - self.y)
            if dist < self.range:
                prog = e.progress()
                if prog > max_progress:
                    max_progress = prog
                    target = e

        if target:
            bullets.append(Bullet(self.x, self.y, target, self.power))
            self.timer = self.cooldown

    def draw(self):
        color = BLUE if self.level == 1 else CYAN
        pygame.draw.circle(screen, color, (self.x, self.y), 18)
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.range, 1)
        if self.level > 1:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), 5)

    def merge(self, other):
        """타워 합성"""
        self.power *= 3
        self.range = int(self.range * 1.3)
        self.cooldown = max(10, int(self.cooldown * 0.7))
        self.level += 1

# ----- 게임 데이터 -----
enemies = []
towers = []
bullets = []

# ----- 메인 루프 -----
running = True
while running:
    dt = clock.tick(60)
    screen.fill((60, 180, 80))

    # ----- 이벤트 -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if event.button == 1:
                for t in towers:
                    if math.hypot(mx - t.x, my - t.y) < 20:
                        dragging_tower = t
                        drag_offset = (t.x - mx, t.y - my)
                        break
                else:
                    if money >= 50:
                        towers.append(Tower(mx, my))
                        money -= 50

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and dragging_tower:
                mx, my = pygame.mouse.get_pos()
                merge_target = None
                for t in towers:
                    if t is not dragging_tower and math.hypot(mx - t.x, my - t.y) < 25:
                        merge_target = t
                        break
                if merge_target:
                    merge_target.merge(dragging_tower)
                    towers.remove(dragging_tower)
                    for i in range(15):
                        pygame.draw.circle(screen, YELLOW, (merge_target.x, merge_target.y), 10 + i, 1)
                dragging_tower = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_tower:
                mx, my = pygame.mouse.get_pos()
                dragging_tower.x = mx + drag_offset[0]
                dragging_tower.y = my + drag_offset[1]

    # ----- 웨이브 관리 -----
    wave_timer += 1
    if wave_timer > 120:
        wave_timer = 0
        wave += 1
        enemies_to_spawn += 3

    spawn_timer += 1
    if spawn_timer > 60 and enemies_to_spawn > 0:
        enemies.append(Enemy(wave))
        enemies_to_spawn -= 1
        spawn_timer = 0

    # ----- 업데이트 -----
    for e in enemies:
        e.update()
    for t in towers:
        t.update(enemies, bullets)
    for b in bullets:
        b.update()

    enemies = [e for e in enemies if e.alive]
    bullets = [b for b in bullets if b.alive]

    # ----- 그리기 -----
    draw_path()
    for e in enemies:
        e.draw()
    for t in towers:
        t.draw()
    for b in bullets:
        b.draw()

    # ----- HUD -----
    pygame.draw.rect(screen, (40, 40, 40), (0, 0, WIDTH, 40))
    hud_text = font.render(f"💰 Money: {money}   ❤️ Lives: {lives}   🌊 Wave: {wave}", True, WHITE)
    screen.blit(hud_text, (15, 10))

    pygame.display.flip()

    if lives <= 0:
        screen.fill(BLACK)
        msg = font.render("Game Over", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        break