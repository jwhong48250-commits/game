import pygame
import random
import sys

pygame.init()

# ----- 기본 설정 -----
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("차차차 간단 버전")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ----- 색상 -----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BLUE = (60, 140, 255)
GRAY = (100, 100, 100)

# ----- 게임 변수 -----
car_width = 50
car_height = 80
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 7

obstacles = []
obstacle_width = 50
obstacle_height = 80
obstacle_speed = 5
spawn_timer = 0

score = 0

# ----- 메인 루프 -----
running = True
while running:
    dt = clock.tick(60)
    screen.fill(GRAY)

    # ----- 이벤트 처리 -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    # 화면 안에서만 이동
    car_x = max(0, min(WIDTH - car_width, car_x))

    # ----- 장애물 생성 -----
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_timer = 0
        obs_x = random.randint(0, WIDTH - obstacle_width)
        obstacles.append([obs_x, -obstacle_height])

    # ----- 장애물 이동 -----
    for obs in obstacles:
        obs[1] += obstacle_speed

    # ----- 충돌 검사 -----
    for obs in obstacles:
        if (car_x < obs[0] + obstacle_width and
            car_x + car_width > obs[0] and
            car_y < obs[1] + obstacle_height and
            car_y + car_height > obs[1]):
            running = False

    # ----- 점수 계산 -----
    score += 1

    # ----- 그리기 -----
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))
    for obs in obstacles:
        pygame.draw.rect(screen, RED, (obs[0], obs[1], obstacle_width, obstacle_height))

    score_text = font.render(f"Score: {score//10}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# ----- 게임 종료 -----
screen.fill(BLACK)
msg = font.render("Game Over", True, RED)
screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()