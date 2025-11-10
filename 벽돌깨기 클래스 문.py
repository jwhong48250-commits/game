import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌 깨기 - 클래스 버전")

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 60


class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 30, 100, 10)
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 10, HEIGHT - 50, 20, 20)
        self.speed_x = 4
        self.speed_y = -4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 벽 충돌
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def check_collision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed_y *= -1

    def check_collision_with_bricks(self, bricks):
        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                self.speed_y *= -1
                bricks.remove(brick)

    def draw(self, screen):
        pygame.draw.ellipse(screen, RED, self.rect)


class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.create_bricks()
        self.running = True

    def create_bricks(self):
        brick_rows = 5
        brick_cols = 7
        brick_width = WIDTH // brick_cols
        brick_height = 20
        for row in range(brick_rows):
            for col in range(brick_cols):
                brick = Brick(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2)
                self.bricks.append(brick)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.paddle.move()
        self.ball.move()
        self.ball.check_collision_with_paddle(self.paddle)
        self.ball.check_collision_with_bricks(self.bricks)
        if self.ball.rect.bottom >= HEIGHT:
            print("게임 오버")
            self.running = False

    def draw(self):
        screen.fill(BLACK)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)
        pygame.display.flip()


# 게임 시작
game = Game()
game.run()

pygame.quit()
sys.exit()