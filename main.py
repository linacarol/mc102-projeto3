from labirintos import labirinto
import pygame

pygame.init()

LARGURA = 1200
ALTURA = 860
FPS = 30

tela = pygame.display.set_mode([LARGURA, ALTURA])
timer = pygame.time.Clock()
fonte = pygame.font.Font('freesansbold.ttf')
nivel = 0
lab = labirinto[nivel]
cor = 'white'
jogador_imgs = []
for i in range(1, 5) :
    jogador_imgs.append(pygame.transform.scale(pygame.image.load(f'imgs/jogador/{i}.png'), (40, 40)))

jog_x = 600
jog_y = 424
direcao = 'direita'
cont = 0

def desenha_labirinto(lab) :
    larg = (LARGURA + 100) // 32
    alt = (ALTURA - 70) // 32
    for i in range(len(lab)) :
        for j in range(len(lab[i])) :
            if lab[i][j] == 1 :
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 1) * alt), 3)
            elif lab[i][j] == 2 :
                pygame.draw.line(tela, cor, (j * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 3)
            elif lab[i][j] == 3 :
                pygame.draw.line(tela, cor, (j * larg, (i + 0.5) * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 3)
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, (i + 0.5) * alt), ((j + 0.5) * larg, (i + 1) * alt), 3)
            elif lab[i][j] == 4 :
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 3)
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, (i + 0.5) * alt), ((j + 0.5) * larg, (i + 1) * alt), 3)
            elif lab[i][j] == 5 :
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 3)
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 3)
            elif lab[i][j] == 6 :
                pygame.draw.line(tela, cor, (j * larg, (i + 0.5) * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 3)
                pygame.draw.line(tela, cor, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 3)

def desenha_jogador() :
    if direcao == 'direita' :
        tela.blit(jogador_imgs[cont // 5], (jog_x, jog_y))
    elif direcao == 'esquerda' :
        tela.blit(pygame.transform.flip(jogador_imgs[cont // 5], True, False), (jog_x, jog_y))
    elif direcao == 'cima' :
        tela.blit(pygame.transform.rotate(jogador_imgs[cont // 5], 90), (jog_x, jog_y))
    elif direcao == 'baixo' :
        tela.blit(pygame.transform.rotate(jogador_imgs[cont // 5], 270), (jog_x, jog_y))

def verifica_posicao(centrox, centroy) :
    espacos = [False, False, False, False]

    return espacos

rodando = True
while rodando :
    timer.tick(FPS)
    if cont < 19 :
        cont += 1
    else :
        cont = 0
    tela.fill('black')
    desenha_labirinto(lab)
    desenha_jogador()
    centro_x = jog_x + 20
    centro_y = jog_y + 20
    pode_andar = verifica_posicao(centro_x, centro_y)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            rodando = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RIGHT :
                direcao = 'direita'
            elif event.key == pygame.K_LEFT :
                direcao = 'esquerda'
            elif event.key == pygame.K_UP :
                direcao = 'cima'
            elif event.key == pygame.K_DOWN :
                direcao = 'baixo'

    pygame.display.flip()
pygame.quit()