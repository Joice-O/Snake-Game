import pygame  # biblioteca para desenvolvimento de jogos
from pygame.locals import *
import random

WINDOW_SIZE = (600, 400)
PIXEL_SIZE = 10

# função da colisão com o próprio corpo
def collision(pos1, pos2):
    return pos1 == pos2

# função de colisão com o fim da tela
def off_limits(pos):
    if 0 <= pos[0] < WINDOW_SIZE[0] and 0 <= pos[1] < WINDOW_SIZE[1]:
        return False
    else:
        return True

# função para gerar uma cor aleatória
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# atualiza a posição da maçã,
def random_on_grid():
    while True:
        x = random.randint(0, WINDOW_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE
        y = random.randint(0, WINDOW_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE
        # Garante que a maçã não apareça na área da pontuação
        if not (0 <= x < 100 and 0 <= y < 30):
            return x, y

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Inicialização da cobrinha
snake_pos = [(250, 50), (260, 50), (270, 50)]  # Cobrinha 3 pixels
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((0, 206, 209))
snake_direction = K_LEFT

# Inicialização da maçã
apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_pos = random_on_grid()
apple_color = random_color()  # Definindo a cor aleatória da maçã
apple_surface.fill(apple_color)

# Inicialização da pontuação
score = 0
font = pygame.font.SysFont('Comic Sans MS', 20)

# função para reiniciar o jogo
def restart_game():
    global snake_pos, apple_pos, snake_direction, score, apple_color
    snake_pos = [(250, 50), (260, 50), (270, 50)]
    snake_direction = K_LEFT
    apple_pos = random_on_grid()
    apple_color = random_color()  # Gerar nova cor para a maçã
    apple_surface.fill(apple_color)
    score = 0

while True:
    pygame.time.Clock().tick(13)  # tempo/velocidade de movimento da cobrinha
    screen.fill((50, 50, 50))
    
    for event in pygame.event.get():
        if event.type == QUIT:  # Evento para fechar a janela
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:  # direção da cobrinha
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    # Exibindo a maçã
    screen.blit(apple_surface, apple_pos)

    # Verificando colisão com a maçã
    if collision(apple_pos, snake_pos[0]):
        snake_pos.append(snake_pos[-1])  # Adiciona um novo segmento à cobra
        apple_pos = random_on_grid()  # Coloca a maçã em uma nova posição
        apple_color = random_color()  # Gera uma nova cor para a maçã
        apple_surface.fill(apple_color)
        score += 1  # Aumenta a pontuação

    # Atualizando a cobrinha
    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    # Atualizando a posição do corpo da cobrinha
    for i in range(len(snake_pos) - 1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            restart_game()  # Reinicia o jogo se a cobrinha colidir com ela mesma
            break
        snake_pos[i] = snake_pos[i - 1]

    # Impedindo a cobrinha de sair da tela
    head_x, head_y = snake_pos[0]
    if snake_direction == K_UP:
        if head_y > 0:
            snake_pos[0] = (head_x, head_y - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        if head_y < WINDOW_SIZE[1] - PIXEL_SIZE:
            snake_pos[0] = (head_x, head_y + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        if head_x > 0:
            snake_pos[0] = (head_x - PIXEL_SIZE, head_y)
    elif snake_direction == K_RIGHT:
        if head_x < WINDOW_SIZE[0] - PIXEL_SIZE:
            snake_pos[0] = (head_x + PIXEL_SIZE, head_y)

    # Exibindo a pontuação na tela
    score_text = font.render(f'Pontuação: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
