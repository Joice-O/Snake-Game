import pygame  # biblioteca para desenvolvimento de jogos
from pygame.locals import *
import random

WINDOW_SIZE = (500, 400) #tamanho da janela
PIXEL_SIZE = 10 #tamanho do pixel
BORDER_SIZE = 10  #tamanho da borda

# Função da colisão com o próprio corpo
def collision(pos1, pos2):
    return pos1 == pos2

# Função da colisão com a borda
def hit_border(pos):
    x, y = pos
    if x < BORDER_SIZE or x >= WINDOW_SIZE[0] - BORDER_SIZE or y < BORDER_SIZE or y >= WINDOW_SIZE[1] - BORDER_SIZE:
        return True
    return False

# Função para gerar uma cor aleatória
def random_color():
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if sum(color) > 100:  # Evitar cores escuras
            return color

# Função para gerar posição aletatória para maça sem deixar ser na borda
def random_on_grid():
    while True:
        x = random.randint(BORDER_SIZE // PIXEL_SIZE, (WINDOW_SIZE[0] - BORDER_SIZE) // PIXEL_SIZE - 1) * PIXEL_SIZE
        y = random.randint(BORDER_SIZE // PIXEL_SIZE, (WINDOW_SIZE[1] - BORDER_SIZE) // PIXEL_SIZE - 1) * PIXEL_SIZE
        return x, y

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Inicialização da cobrinha com tamanho 3
snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((0, 206, 209))
snake_direction = K_LEFT
next_direction = K_LEFT  

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

# Função para exibir a tela de Game Over
def game_over():
    font_large = pygame.font.SysFont('Comic Sans MS', 30)
    game_over_text = font_large.render('GAME OVER', True, (255, 0, 0))
    score_text = font.render(f'Pontuação Final: {score}', True, (255, 255, 255))
    restart_text = font.render('Pressione R para reiniciar ou Q para sair', True, (255, 255, 255))
    
    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (150, 100))
    screen.blit(score_text, (175, 150))
    screen.blit(restart_text, (100, 200))
    pygame.display.update()

# Função para tratar eventos após a colisão
def handle_game_over():
    global snake_pos, apple_pos, snake_direction, next_direction, score, apple_color
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_r:  # Reiniciar o jogo
                    restart_game()
                    return True  
                elif event.key == K_q:  # Sair do jogo
                    pygame.quit()
                    quit()

# Função de pausa
def pause_game():
    font_large = pygame.font.SysFont('Comic Sans MS', 30)
    pause_text = font_large.render('JOGO PAUSADO', True, (255, 255, 0))
    resume_text = font.render('Pressione P para continuar', True, (255, 255, 255))
    quit_text = font.render('Pressione Q para sair', True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(pause_text, (120, 100))
    screen.blit(resume_text, (150, 150))
    screen.blit(quit_text, (170, 200))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_p:  # Continuar o jogo
                    return
                elif event.key == K_q:  # Sair do jogo
                    pygame.quit()
                    quit()

while True:
    pygame.time.Clock().tick(13)
    screen.fill((0, 0, 0))

    # Desenho das bordas
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, WINDOW_SIZE[0], BORDER_SIZE))  # Topo
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, BORDER_SIZE, WINDOW_SIZE[1]))  # Esquerda
    pygame.draw.rect(screen, (50, 50, 50), (0, WINDOW_SIZE[1] - BORDER_SIZE, WINDOW_SIZE[0], BORDER_SIZE))  # Base
    pygame.draw.rect(screen, (50, 50, 50), (WINDOW_SIZE[0] - BORDER_SIZE, 0, BORDER_SIZE, WINDOW_SIZE[1]))  # Direita

    # Verifica os eventos do teclado/os botões
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
            elif event.key == K_p:  # Pausar o jogo
                pause_game()  # Chama a função de pausa

    # Atualiza a direção
    snake_direction = next_direction

    # Exibe a maçã
    pygame.draw.circle(screen, apple_color, (apple_pos[0] + PIXEL_SIZE // 2, apple_pos[1] + PIXEL_SIZE // 2), PIXEL_SIZE // 2)

    # Verifica a colisão com a maçã
    if collision(apple_pos, snake_pos[0]):
        snake_pos.append(snake_pos[-1])  # Adiciona mais um pixel ao corpo da cobra
        apple_pos = random_on_grid()
        apple_color = random_color()
        apple_surface.fill(apple_color)
        score += 1

    # Atualiza a posição do corpo da cobrinha
    for i in range(len(snake_pos) - 1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            game_over()  # Exibe tela de Game Over
            if handle_game_over():  # Aguarda a decisão do jogador
                break  # Sai do loop atual e reinicia o jogo
        snake_pos[i] = snake_pos[i - 1]

    # Movimenta a cabeça da cobrinha
    head_x, head_y = snake_pos[0]
    if snake_direction == K_UP:
        snake_pos[0] = (head_x, head_y - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (head_x, head_y + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (head_x - PIXEL_SIZE, head_y)
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (head_x + PIXEL_SIZE, head_y)

    # Verifica colisão com a borda
    if hit_border(snake_pos[0]):
        game_over()  # Exibe tela de Game Over
        if handle_game_over():  # Aguarda a decisão do jogador
            continue  # Reinicia o loop principal do jogo após a decisão
        else:
            break  # Sai do loop principal se o jogador escolher sair

    # Exibe a cobrinha
    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    # Exibe a pontuação dentro da borda
    score_text = font.render(f'Pontuação: {score}', True, (255, 255, 255))  
    screen.blit(score_text, (15, 10))

    pygame.display.update()
