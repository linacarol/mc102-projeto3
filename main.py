from labirintos import labirinto
import pygame
import sys

pygame.init()

LARGURA = 1200
ALTURA = 860
FPS = 30

tela = pygame.display.set_mode([LARGURA, ALTURA])
timer = pygame.time.Clock()
fonte = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 32)
nivel = 0
lab = labirinto[nivel]
cor = 'white'
cor_fundo = 'black'
jogador_imgs = []
for i in range(1, 5) :
    jogador_imgs.append(pygame.transform.scale(pygame.image.load(f'imgs/jogador/{i}.png'), (28, 28)))
vida_img = pygame.transform.scale(pygame.image.load('imgs/outros/vida.png'), (30, 30))

if nivel == 0 :
    posx_inicial = 30
    posy_inicial = 395
    tempo_inicial = 1300

jog_x = posx_inicial
jog_y = posy_inicial
direcao = 'direita'
direcao_comando = 'direita'
cont = 0
velocidade_jog = 2
vidas = 3


def desenha_labirinto(lab) :
    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    for i in range(len(lab)) :
        for j in range(len(lab[i])) :
            if lab[i][j] != 0 :
                pygame.draw.rect(tela, cor, (j*larg, i*alt, larg, alt))
                pygame.draw.line(tela, cor_fundo, (j * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_fundo, (j * larg, i * alt), ((j + 1) * larg, i * alt), 2)
                pygame.draw.line(tela, cor_fundo, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_fundo, ((j + 1) * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 1) * alt), 2)
                if j > 0 :
                    if lab[i][j-1] != 0 :          
                        pygame.draw.line(tela, cor_fundo, (j * larg, (i + 0.5) * alt), (j * larg, (i + 1) * alt), 2)

    if tempo > tempo_inicial/2 :
        pygame.draw.rect(tela, 'green', ((60, 800), (0.6*tempo, 30)))
    elif tempo > tempo_inicial/4 :
        pygame.draw.rect(tela, 'yellow', ((60, 800), (0.6*tempo, 30)))
    else :
        pygame.draw.rect(tela, 'red', ((60, 800), (0.6*tempo, 30)))

    if vidas > 0 :
        tela.blit(vida_img, (1020, 800))
    if vidas > 1 :
        tela.blit(vida_img, (1070, 800))
    if vidas > 2 :
        tela.blit(vida_img, (1120, 800))

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
    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    num = 14

    if centrox // 40 < 29 :
        if lab[(centroy-(num+8))//alt + 1][(centrox+num)//larg] == 0 and lab[(centroy-(num+8))//alt + 1][(centrox-num)//larg] == 0 :
            espacos[3] = True
        if lab[(centroy+(num+4))//alt - 1][(centrox+num)//larg] == 0 and lab[(centroy+(num+4))//alt - 1][(centrox-num)//larg] == 0 :
            espacos[2] = True
        if lab[(centroy-(num+2))//alt][(centrox-(num))//larg + 1] == 0 and lab[(centroy+(num-2))//alt][(centrox-(num))//larg + 1] == 0 :
            espacos[0] = True
        if lab[(centroy-(num+2))//alt][(centrox+(num-2))//larg - 1] == 0 and lab[(centroy+(num-2))//alt][(centrox+(num-2))//larg - 1] == 0 :
            espacos[1] = True
    else :
        espacos[0] = True
        espacos[1] = True

    return espacos

def move_jogador(jog_x, jog_y) :
    global direcao
    global direcao_comando
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_RIGHT] and pode_andar[0]:
        direcao = 'direita'
        direcao_comando = 'direita'
        jog_x += velocidade_jog
    elif tecla[pygame.K_LEFT] and pode_andar[1] :
        direcao = 'esquerda'
        direcao_comando = 'esquerda'
        jog_x -= velocidade_jog
    elif tecla[pygame.K_UP] and pode_andar[2] :
        direcao = 'cima'
        direcao_comando = 'cima'
        jog_y -= velocidade_jog
    elif tecla[pygame.K_DOWN] and pode_andar[3] :
        direcao = 'baixo'
        direcao_comando = 'baixo'
        jog_y += velocidade_jog
    return jog_x, jog_y

def menu_inicial():
    while True:
        tela.fill(cor_fundo)
        novo_jogo_txt = fonte.render('Novo Jogo', True, cor)
        informacoes_txt = fonte.render('Informações', True, cor)
        sair_txt = fonte.render('Sair', True, cor)
        carregar_txt = fonte.render('Carregar Jogo', True, cor)

        novo_jogo_rect = novo_jogo_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 100))
        informacoes_rect = informacoes_txt.get_rect(center=(LARGURA/2, ALTURA / 2))
        sair_rect = sair_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
        carregar_rect = carregar_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 50))

        tela.blit(novo_jogo_txt, novo_jogo_rect)
        tela.blit(informacoes_txt, informacoes_rect)
        tela.blit(sair_txt, sair_rect)
        tela.blit(carregar_txt, carregar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if novo_jogo_rect.collidepoint(event.pos):
                    return
                if informacoes_rect.collidepoint(event.pos):
                    informacoes()
                if sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
     
def informacoes():
    while True:
        tela.fill(cor_fundo)

        informacoes_txt = fonte.render('Texto exemplo de informações sobre o jogo', True, cor)
        voltar_txt = fonte.render('Voltar', True, cor)

        informacoes_rect = informacoes_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 50))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 50))

        tela.blit(informacoes_txt, informacoes_rect)
        tela.blit(voltar_txt, voltar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_rect.collidepoint(event.pos):
                    return
        pygame.display.flip()

def salvar_jogo():
    return

def pause():
    while True:
        tela.fill(cor_fundo)
        sair_txt = fonte.render('Sair', True, cor)
        voltar_txt = fonte.render('Voltar', True, cor)
        salvar_txt = fonte.render('Salvar', True, cor)

        sair_rect = sair_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 50))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2))
        salvar_rect = salvar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 50))

        tela.blit(sair_txt, sair_rect)
        tela.blit(voltar_txt, voltar_rect)
        tela.blit(salvar_txt, salvar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if voltar_rect.collidepoint(event.pos):
                    return
                if salvar_rect.collidepoint(event.pos):
                    salvar_jogo()
                    return
        pygame.display.flip()

def fim_jogo() :
    while True :
        global tempo
        global nivel
        global jog_x
        global jog_y
        global direcao
        global direcao_comando
        global vidas

        tela.fill(cor_fundo)
        fim_txt = fonte.render('Fim de jogo', True, cor)
        novo_jogo_txt = fonte.render('Jogar novamente', True, cor)
        sair_txt = fonte.render('Sair', True, cor)

        fim_rect = fim_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 80))
        novo_jogo_rect = novo_jogo_txt.get_rect(center = (LARGURA/2, ALTURA/2))
        sair_rect = sair_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 50))

        tela.blit(fim_txt, fim_rect)
        tela.blit(novo_jogo_txt, novo_jogo_rect)
        tela.blit(sair_txt, sair_rect)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                if sair_rect.collidepoint(event.pos) :
                    pygame.quit()
                    sys.exit()
                if novo_jogo_rect.collidepoint(event.pos) :
                    vidas = 3
                    tempo = tempo_inicial
                    nivel = 0
                    jog_x = 30
                    jog_y = 395
                    direcao = 'direita'
                    direcao_comando = 'direita'
                    return

        pygame.display.flip()

rodando = True
menu_inicial()
tempo = tempo_inicial
while rodando :
    timer.tick(FPS)
    if cont < 19 :
        cont += 1
    else :
        cont = 0
    tempo -= 1
    tela.fill(cor_fundo)
    desenha_labirinto(lab)
    desenha_jogador()
    centro_x = jog_x + 15
    centro_y = jog_y + 15
    pode_andar = verifica_posicao(centro_x, centro_y)
    jog_x, jog_y = move_jogador(jog_x, jog_y)

    if tempo <= 0 or vidas < 0:
        fim_jogo()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            rodando = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_p:
                pause()

        if direcao_comando == 'direita' and pode_andar[0] :
            direcao = 'direita'
        if direcao_comando == 'esquerda' and pode_andar[1] :
            direcao = 'esquerda'
        if direcao_comando == 'cima' and pode_andar[2] :
            direcao = 'cima'
        if direcao_comando == 'baixo' and pode_andar[3] :
            direcao = 'baixo'
        
        if jog_x > 1200 :
            jog_x = -30
        elif jog_x < -30 :
            jog_x = 1200

    pygame.display.flip()
pygame.quit()