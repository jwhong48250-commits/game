import pygame
import random
import sys

pygame.init()

# ----- 기본 설정 -----
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("무법자 칼치기")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ----- 배경 이미지 -----
background = pygame.image.load("img/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bg_y = 0  # 배경 Y 위치

# ----- 플레이어 자동차 이미지 -----
car_image = pygame.image.load("img/내자동차.png")
car_width, car_height = 50, 80
car_image = pygame.transform.scale(car_image, (car_width, car_height))
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 7

# ----- 장애물 자동차 이미지 3종 -----
obstacle_images = [
    pygame.image.load("img/자동차1.png"),
    pygame.image.load("img/자동차2.png"),
    pygame.image.load("img/자동차3.png")
]
for i in range(3):
    obstacle_images[i] = pygame.transform.scale(obstacle_images[i], (50, 80))

# ----- 장애물 변수 -----
obstacles = []
obstacle_speed = 5
spawn_timer = 0

# ----- 색상 -----
WHITE = (255, 255, 255)

# ----- 점수 -----
score = 0

# ----- 메인 루프 -----
running = True
while running:
    dt = clock.tick(60)

    # ----- 배경 스크롤 -----
    bg_y += 2
    if bg_y >= HEIGHT:
        bg_y = 0
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - HEIGHT))

    # ----- 이벤트 처리 -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ----- 플레이어 이동 -----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed
    car_x = max(0, min(WIDTH - car_width, car_x))

    # ----- 장애물 생성 -----
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_timer = 0
        obs_x = random.randint(0, WIDTH - 50)
        obs_img = random.choice(obstacle_images)
        obstacles.append([obs_x, -80, obs_img])

    # ----- 장애물 이동 -----
    for obs in obstacles:
        obs[1] += obstacle_speed

    # ----- 충돌 검사 -----
    for obs in obstacles:
        if (car_x < obs[0] + 50 and
            car_x + car_width > obs[0] and
            car_y < obs[1] + 80 and
            car_y + car_height > obs[1]):
            running = False

    # ----- 그리기 -----
    screen.blit(car_image, (car_x, car_y))  # 플레이어 자동차
    for obs in obstacles:
        screen.blit(obs[2], (obs[0], obs[1]))  # 장애물 이미지

    # ----- 점수 -----
    score += 1
    score_text = font.render(f"Score: {score//10}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# ----- 게임 종료 -----
screen.fill((0, 0, 0))
msg = font.render("Game Over", True, (255, 0, 0))
screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
