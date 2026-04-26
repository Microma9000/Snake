import pygame
import random
import sys

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 1000
HEIGHT = 1000
SNAKE_SIZE = 20
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake-Edition from KKPlatFormme")

snake_body = [[160, 100], [140, 100], [120, 100], [100, 100]]
direction = 'RIGHT'
change_to = direction
score = 0

def generate_food_pos(snake_body):
    while True:
        x = random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE
        if [x, y] not in snake_body:
            return [x, y]

food_pos = generate_food_pos(snake_body)
clock = pygame.time.Clock()

def show_score():
    font = pygame.font.SysFont('consolas', 20)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont('times new roman', 70)
    text = font.render('YOU DIED! Game OVER!', True, RED)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(text, rect)
    show_score()
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# ====================== ГЛАВНЫЙ ЦИКЛ ======================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    # Новая голова
    head = snake_body[0][:]
    if direction == 'UP':
        head[1] -= SNAKE_SIZE
    elif direction == 'DOWN':
        head[1] += SNAKE_SIZE
    elif direction == 'LEFT':
        head[0] -= SNAKE_SIZE
    elif direction == 'RIGHT':
        head[0] += SNAKE_SIZE

    snake_body.insert(0, head)

    # === ПРОВЕРКА СЪЕДАНИЯ (самое важное место) ===
    ate = False
    if head == food_pos:
        score += 1
        food_pos = generate_food_pos(snake_body)
        ate = True
        print(f"Съедено! Новая еда: {food_pos}")   # отладка в консоль

    if not ate:
        snake_body.pop()

    # Столкновения
    if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT):
        running = False
    for segment in snake_body[1:]:
        if head == segment:
            running = False

    # Отрисовка
    screen.fill(BLACK)

    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.draw.rect(screen, WHITE, (food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

    # Отладочная сетка (можно потом убрать)
    # for x in range(0, WIDTH, SNAKE_SIZE):
    #     pygame.draw.line(screen, (40,40,40), (x, 0), (x, HEIGHT))
    # for y in range(0, HEIGHT, SNAKE_SIZE):
    #     pygame.draw.line(screen, (40,40,40), (0, y), (WIDTH, y))

    show_score()
    pygame.display.flip()
    clock.tick(FPS)

game_over_screen()
