import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌 깨기")

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# 패들
paddle = pygame.Rect(WIDTH//2 - 50, HEIGHT - 30, 100, 10)
paddle_speed = 5

# 공
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT - 50, 20, 20)
ball_speed_x = 4
ball_speed_y = -4

# 벽돌
bricks = []
brick_rows = 5
brick_cols = 7
brick_width = WIDTH // brick_cols
brick_height = 20

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2)
        bricks.append(brick)

# 게임 루프
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # 공 이동
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 벽 충돌
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        print("게임 오버")
        running = False

    # 패들 충돌
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # 벽돌 충돌
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_speed_y *= -1
            bricks.remove(brick)

    # 화면 그리기
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)

    pygame.display.flip()

pygame.quit()
sys.exit()