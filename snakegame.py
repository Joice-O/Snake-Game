import pygame  # biblioteca para desenvolvimento de jogos
from pygame.locals import *
import random

WINDOW_SIZE = (500, 400)
PIXEL_SIZE = 10
BORDER_SIZE = 10  # Tamanho da borda

# Função da colisão com o próprio corpo
def collision(pos1, pos2):
    return pos1 == pos2

# Função para verificar colisão com a borda
def hit_border(pos):
    x, y = pos
    if x < BORDER_SIZE or x >= WINDOW_SIZE[0] - BORDER_SIZE or y < BORDER_SIZE or y >= WINDOW_SIZE[1] - BORDER_SIZE:
        return True
    return False

# Função para gerar uma cor aleatória
def random_color():
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if sum(color) > 100:  # Evita cores muito escuras (preto/cinza)
            return color

# Atualiza a posição da maçã garantindo que ela não apareça na borda
def random_on_grid():
    while True:
        x = random.randint(BORDER_SIZE // PIXEL_SIZE, (WINDOW_SIZE[0] - BORDER_SIZE) // PIXEL_SIZE - 1) * PIXEL_SIZE
        y = random.randint(BORDER_SIZE // PIXEL_SIZE, (WINDOW_SIZE[1] - BORDER_SIZE) // PIXEL_SIZE - 1) * PIXEL_SIZE
        return x, y

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Inicialização da cobrinha
snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((0, 206, 209))
snake_direction = K_LEFT
next_direction = K_LEFT  # Para evitar mudanças instantâneas erradas

# Inicialização da maçã
apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_pos = random_on_grid()
apple_color = random_color()
apple_surface.fill(apple_color)

# Inicialização da pontuação
score = 0
font = pygame.font.SysFont('Comic Sans MS', 15)

# Função para reiniciar o jogo
def restart_game():
    global snake_pos, apple_pos, snake_direction, next_direction, score, apple_color
    snake_pos = [(250, 50), (260, 50), (270, 50)]
    snake_direction = K_LEFT
    next_direction = K_LEFT
    apple_pos = random_on_grid()
    apple_color = random_color()
    apple_surface.fill(apple_color)
    score = 0

while True:
    pygame.time.Clock().tick(13)
    screen.fill((0, 0, 0))

    # Desenhando a borda
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, WINDOW_SIZE[0], BORDER_SIZE))  # Topo
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, BORDER_SIZE, WINDOW_SIZE[1]))  # Esquerda
    pygame.draw.rect(screen, (50, 50, 50), (0, WINDOW_SIZE[1] - BORDER_SIZE, WINDOW_SIZE[0], BORDER_SIZE))  # Base
    pygame.draw.rect(screen, (50, 50, 50), (WINDOW_SIZE[0] - BORDER_SIZE, 0, BORDER_SIZE, WINDOW_SIZE[1]))  # Direita

    # Eventos do teclado
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_UP and snake_direction != K_DOWN:
                next_direction = K_UP
            elif event.key == K_DOWN and snake_direction != K_UP:
                next_direction = K_DOWN
            elif event.key == K_LEFT and snake_direction != K_RIGHT:
                next_direction = K_LEFT
            elif event.key == K_RIGHT and snake_direction != K_LEFT:
                next_direction = K_RIGHT

    # Atualizando a direção
    snake_direction = next_direction

    # Exibindo a maçã
    pygame.draw.circle(screen, apple_color, (apple_pos[0] + PIXEL_SIZE // 2, apple_pos[1] + PIXEL_SIZE // 2), PIXEL_SIZE // 2)

    # Verificando colisão com a maçã
    if collision(apple_pos, snake_pos[0]):
        snake_pos.append(snake_pos[-1])  # Cresce ao comer a maçã
        apple_pos = random_on_grid()
        apple_color = random_color()
        apple_surface.fill(apple_color)
        score += 1

    # Atualizando a posição do corpo da cobrinha
    for i in range(len(snake_pos) - 1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            restart_game()
            break
        snake_pos[i] = snake_pos[i - 1]

    # Movendo a cabeça da cobrinha
    head_x, head_y = snake_pos[0]
    if snake_direction == K_UP:
        snake_pos[0] = (head_x, head_y - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (head_x, head_y + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (head_x - PIXEL_SIZE, head_y)
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (head_x + PIXEL_SIZE, head_y)

    # Verificando colisão com a borda
    if hit_border(snake_pos[0]):
        restart_game()

    # Exibindo a cobrinha
    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    # Exibindo a pontuação dentro da borda
    score_text = font.render(f'Pontuação: {score}', True, (255, 255, 255))  
    screen.blit(score_text, (15,10))  

    pygame.display.update()
