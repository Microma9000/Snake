import pygame
import random

# 1. Инициализация Pygame
pygame.init()

# 2. Константы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 600
HEIGHT = 480
SNAKE_SIZE = 20
SNAKE_SPEED = 10

# 3. Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# 4. Начальные значения
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Случайное положение еды
food_pos = [random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE,
            random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE]
food_spawn = True

direction = 'RIGHT'
change_to = direction

# 5. Игровой цикл
clock = pygame.time.Clock()
game_over = False

while not game_over:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Изменение направления
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Движение змейки
    if direction == 'UP':
        snake_pos[1] -= SNAKE_SIZE
    if direction == 'DOWN':
        snake_pos[1] += SNAKE_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= SNAKE_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += SNAKE_SIZE

    # Поедание еды
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        food_spawn = False
    else:
        snake_body.pop()

    # Создание новой еды
    if not food_spawn:
        food_pos = [random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE,
                    random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE]
        food_spawn = True

    # Отрисовка
    screen.fill(BLACK)
    for pos in snake_body:  # Отрисовываем все тело змейки
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, WHITE, (food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

    # Проверка на столкновение
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over = True
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over = True

    # Обновление экрана
    pygame.display.flip()  # Используем flip вместо update
    clock.tick(SNAKE_SPEED)

# 6. Выход из Pygame
pygame.quit()
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(len(snake_body) - 3), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (WIDTH/10, 15)
    else:
        score_rect.midtop = (WIDTH/2, HEIGHT/1.25)
    screen.blit(score_surface, score_rect)

def game_over_screen():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WIDTH/2, HEIGHT/4)
    screen.blit(game_over_surface, game_over_rect)
    show_score(0, WHITE, 'times', 20)  # Вызываем show_score с choice=0
    pygame.display.flip()
    pygame.time.wait(3000) # Пауза в 3 секунды
    pygame.quit()