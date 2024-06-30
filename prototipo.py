import pygame
from board import boards
import math

pygame.init()

LARGURA = 900
ALTURA = 950
PI = math.pi
screen = pygame.display.set_mode([LARGURA, ALTURA])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
nivel = boards
color = 'blue'
jogador_img = pygame.transform.scale(pygame.image.load('img/pacman.png'), (45, 45))

jogador_x = 450
jogador_y = 663
direcao = 'direita'
contador = 0

def desenha_tabuleiro(nvl) :
    num1 = (ALTURA - 50) // 32
    num2 = LARGURA // 30

    for i in range(len(nivel)) :
        for j in range(len(nivel[i])) :
            if nivel[i][j] == 1 :
                # desenha um circulo
                # na tela, na cor branca, (centro x, centro y), raio
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if nivel[i][j] == 2 :
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if nivel[i][j] == 3 :
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), (i + 1) * num1), 3)
            if nivel[i][j] == 4 :
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 ((j + 1) * num2, i * num1 + (0.5 * num1)), 3)
            if nivel[i][j] == 5 :
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if nivel[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if nivel[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if nivel[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if nivel[i][j] == 9 :
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 ((j + 1) * num2, i * num1 + (0.5 * num1)), 2)

def desenha_jogador() :
    if direcao == 'direita' :
        screen.blit(jogador_img, (jogador_x, jogador_y))
    elif direcao == 'esquerda' :
        screen.blit(pygame.transform.flip(jogador_img, True, False), (jogador_x, jogador_y))
    elif direcao == 'cima' :
        screen.blit(pygame.transform.rotate(jogador_img, 90), (jogador_x, jogador_y))
    elif direcao == 'baixo' :
        screen.blit(pygame.transform.rotate(jogador_img, 270), (jogador_x, jogador_y))

run = True
while run :
    timer.tick(fps)
    screen.fill('black')
    desenha_tabuleiro(nivel)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    pygame.display.flip()

pygame.quit()