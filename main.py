from labirintos import labirinto
import pygame
import sys
import json
import os
import time

pygame.init()

LARGURA = 1200
ALTURA = 860
FPS = 30

tela = pygame.display.set_mode([LARGURA, ALTURA])
timer = pygame.time.Clock()

fonte = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 32)
fonte_titulo = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 38)
fonte_instrucoes = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 22)
fonte_pontos = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 18)

jogador_img = pygame.transform.scale(pygame.image.load('imgs/jogador/jogador.png'), (35, 35))
colega_img = pygame.transform.scale(pygame.image.load('imgs/colegas/colega.png'), (35, 35))
ifgw_img = pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (30, 30))
imecc_img = pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (30, 30))
santiago_img = pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (30, 30))
vida_img = pygame.transform.scale(pygame.image.load('imgs/outros/vida.png'), (30, 30))
relogio_img = pygame.transform.scale(pygame.image.load('imgs/outros/relogio.png'), (30, 30))

nivel = 0
cor = 'white'
cor_fundo = 'black'

if nivel == 0 :
    posx_inicial = 30
    posy_inicial = 395
    tempo_inicial = 6500
    ganha_pontos = 5
    professor_img = ifgw_img
    profx_inicial = LARGURA//2 + 160
    profy_inicial = ALTURA//2 - 64
    prof_direcao = 'direita'
    prof_morto = False

jog_x = posx_inicial
jog_y = posy_inicial
direcao = 'direita'
direcao_comando = 'direita'
velocidade_jog = 2
vidas = 3
pegou_relogio = False
pontuacao = 0
ultimo_salvamento = time.time()
intervalo_salvamento = 5
prof_x = profx_inicial
prof_y = profy_inicial
prof_img = professor_img
velocidade_prof = 2
pode_mover = True

class Professor :
    def __init__(self, coord_x, coord_y, alvo, velocidade, img, direc, morte) :
        self.pos_x = coord_x
        self.pos_y = coord_y
        self.centro_x = self.pos_x + 15
        self.centro_y = self.pos_y + 15
        self.alvo = alvo
        self.velocidade = velocidade
        self.img = img
        self.direcao = direc
        self.morte = morte
        self.movimentos = self.verif_colisoes()
        self.rect = self.desenha()

    def desenha(self) :
        if not self.morte :
            tela.blit(self.img, (self.pos_x, self.pos_y))
        prof_rect = pygame.rect.Rect((self.centro_x - 15, self.centro_y - 15), (35, 35))
        return prof_rect
    
    def verif_colisoes(self) :
        alt = (ALTURA - 70) // 21
        larg = LARGURA // 40
        num = 14
        self.movimentos = [False, False, False, False]

        if self.centro_x // 40 < 29 :
            if lab[(self.centro_y-(num+6))//alt + 1][(self.centro_x-14)//larg] == 0 and lab[(self.centro_y-(num+6))//alt + 1][(self.centro_x+14)//larg] == 0 :
                self.movimentos[3] = True
            if lab[(self.centro_y+(num+14))//alt - 1][(self.centro_x+14)//larg] == 0 and lab[(self.centro_y+(num+14))//alt - 1][(self.centro_x-4)//larg] == 0 :
                self.movimentos[2] = True
            if lab[(self.centro_y-(num-10))//alt][(self.centro_x-(num))//larg + 1] == 0 and lab[(self.centro_y+(num+4))//alt][(self.centro_x-(num))//larg + 1] == 0 :
                self.movimentos[0] = True
            if lab[(self.centro_y-(num-20))//alt][(self.centro_x+(num))//larg - 1] == 0 and lab[(self.centro_y+(num-20))//alt][(self.centro_x+(num+6))//larg - 1] == 0 :
                self.movimentos[1] = True
        else :
            self.movimentos[0] = True
            self.movimentos[1] = True

        return self.movimentos
    
    def anda(self) :
        if pode_mover :
            if self.direcao == 'direita' :
                if self.alvo[0] > self.pos_x and self.movimentos[0] :
                    self.pos_x += self.velocidade
                elif not self.movimentos[0] :
                    if self.alvo[1] > self.pos_y and self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                        self._direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                    elif self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                elif self.movimentos[0] :
                    if self.alvo[1] > self.pos_y and self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    else :
                        self.pos_x += self.velocidade

            elif self.direcao == 'esquerda' :
                if self.alvo[1] > self.pos_y and self.movimentos[3] :
                    self.direcao = 'baixo'
                    self.pos_y += self.velocidade
                elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                    self.pos_x -= self.velocidade
                elif not self.movimentos[1] :
                    if self.alvo[1] > self.pos_y and self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.alvo[0] > self.pos_x and self.movimentos[0] :
                        self._direcao = 'direita'
                        self.pos_x += self.velocidade
                    elif self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                elif self.movimentos[1] :
                    if self.alvo[1] > self.pos_y and self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    else :
                        self.pos_x -= self.velocidade

            elif self.direcao == 'cima' :
                if self.alvo[0] < self.pos_x and self.movimentos[1] :
                    self.direcao = 'esquerda'
                    self.pos_x -= self.velocidade
                elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                    self.pos_y -= self.velocidade
                elif not self.movimentos[2] :
                    if self.alvo[0] > self.pos_x and self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                    elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x += self.velocidade
                    elif self.alvo[1] > self.pos_y and self.movimentos[3] :
                        self._direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.movimentos[3] :
                        self.direcao = 'baixo'
                        self.pos_y += self.velocidade
                    elif self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                    elif self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                elif self.movimentos[2] :
                    if self.alvo[0] > self.pos_x and self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                    elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_y -= self.velocidade
                    else :
                        self.pos_y -= self.velocidade

            elif self.direcao == 'baixo' :
                if self.alvo[1] > self.pos_y and self.movimentos[3] :
                    self.pos_y += self.velocidade
                elif not self.movimentos[3] :
                    if self.alvo[0] > self.pos_x and self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                    elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                    elif self.alvo[1] < self.pos_y and self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.movimentos[2] :
                        self.direcao = 'cima'
                        self.pos_y -= self.velocidade
                    elif self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                    elif self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                elif self.movimentos[3] :
                    if self.alvo[0] > self.pos_x and self.movimentos[0] :
                        self.direcao = 'direita'
                        self.pos_x += self.velocidade
                    elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                        self.direcao = 'esquerda'
                        self.pos_x -= self.velocidade
                    else :
                        self.pos_y += self.velocidade
        
        if self.pos_x < 35 :
            self.pos_x = LARGURA
        elif self.pos_x > LARGURA :
            self.pos_x = -35

        return self.pos_x, self.pos_y, self.direcao

def desenha_labirinto(lab) :
    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    for i in range(len(lab)) :
        for j in range(len(lab[i])) :
            if lab[i][j] == 1 :
                pygame.draw.rect(tela, cor, (j*larg, i*alt, larg, alt))
                pygame.draw.line(tela, cor_fundo, (j * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_fundo, (j * larg, i * alt), ((j + 1) * larg, i * alt), 2)
                pygame.draw.line(tela, cor_fundo, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_fundo, ((j + 1) * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 1) * alt), 2)
                if j > 0 :
                    if lab[i][j-1] != 0 :          
                        pygame.draw.line(tela, cor_fundo, (j * larg, (i + 0.5) * alt), (j * larg, (i + 1) * alt), 2)
            elif lab[i][j] == 2 and not pegou_relogio :
                tela.blit(relogio_img, (j*larg, i*alt))
    
    pygame.draw.rect(tela, 'white', ((60, 800), (0.12*tempo_inicial, 30)))
    if tempo > tempo_inicial/2 :
        pygame.draw.rect(tela, 'green', ((60, 800), (0.12*tempo, 30)))
    elif tempo > tempo_inicial/4 :
        pygame.draw.rect(tela, 'yellow', ((60, 800), (0.12*tempo, 30)))
    else :
        pygame.draw.rect(tela, 'red', ((60, 800), (0.12*tempo, 30)))

    if vidas > 0 :
        tela.blit(vida_img, (1050, 800))
    if vidas > 1 :
        tela.blit(vida_img, (1090, 800))
    if vidas > 2 :
        tela.blit(vida_img, (1130, 800))
    
    pontos_txt = fonte_pontos.render(f'{pontuacao}', True, 'white')
    pontos_rect = pontos_txt.get_rect(topright=(1024, 808))
    tela.blit(pontos_txt, pontos_rect)

def desenha_jogador() :
    if direcao == 'direita' :
        tela.blit(pygame.transform.flip(jogador_img, True, False), (jog_x, jog_y))
    elif direcao == 'esquerda' :
        tela.blit(jogador_img, (jog_x, jog_y))
    elif direcao == 'cima' :
        tela.blit(pygame.transform.flip(jogador_img, True, False), (jog_x, jog_y))
    elif direcao == 'baixo' :
        tela.blit(jogador_img, (jog_x, jog_y))

def verifica_posicao(centrox, centroy) :
    espacos = [False, False, False, False]
    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    num = 14

    if centrox // 40 < 29 :
        if lab[(centroy-(num+2))//alt + 1][(centrox+14)//larg] != 1 and lab[(centroy-(num+2))//alt + 1][(centrox-4)//larg] != 1 :
            espacos[3] = True
        if lab[(centroy+(num+14))//alt - 1][(centrox+14)//larg] != 1 and lab[(centroy+(num+14))//alt - 1][(centrox-4)//larg] != 1 :
            espacos[2] = True
        if lab[(centroy-(num-10))//alt][(centrox-(num))//larg + 1] != 1 and lab[(centroy+(num+4))//alt][(centrox-(num))//larg + 1] != 1 :
            espacos[0] = True
        if lab[(centroy-(num-10))//alt][(centrox+(num+6))//larg - 1] != 1 and lab[(centroy+(num+4))//alt][(centrox+(num+6))//larg - 1] != 1 :
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
        titulo_txt = fonte_titulo.render('Os Labirintos da Unicamp', True, 'white')
        novo_jogo_txt = fonte.render('Novo Jogo', True, cor)
        informacoes_txt = fonte.render('Informações', True, cor)
        sair_txt = fonte.render('Sair', True, cor)
        carregar_txt = fonte.render('Carregar Jogo', True, cor)
        ranking_txt = fonte.render('Ranking', True, cor)

        titulo_rect = titulo_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 200))
        novo_jogo_rect = novo_jogo_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 60))
        carregar_rect = carregar_txt.get_rect(center=(LARGURA/2, ALTURA/2))
        informacoes_rect = informacoes_txt.get_rect(center=(LARGURA/2, ALTURA / 2 + 60))
        ranking_rect = ranking_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 120))
        sair_rect = sair_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 180))

        tela.blit(titulo_txt, titulo_rect)
        tela.blit(novo_jogo_txt, novo_jogo_rect)
        tela.blit(carregar_txt, carregar_rect)
        tela.blit(informacoes_txt, informacoes_rect)
        tela.blit(ranking_txt, ranking_rect)
        tela.blit(sair_txt, sair_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if novo_jogo_rect.collidepoint(event.pos):
                    return 'novo_jogo'
                if carregar_rect.collidepoint(event.pos):
                    return 'carregar_jogo'
                if informacoes_rect.collidepoint(event.pos):
                    informacoes()
                if sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if ranking_rect.collidepoint(event.pos):
                    mostrar_ranking()
        
        pygame.display.flip()
     
def informacoes():
    while True:
        tela.fill(cor_fundo)

        jogador_txt_linha1 = fonte_instrucoes.render('Este é você!', True, cor)
        jogador_txt_linha2 = fonte_instrucoes.render('Utilize as setas do teclado para andar', True, cor)
        professor_txt_linha1 = fonte_instrucoes.render('Cuidado com os professores!', True, cor)
        professor_txt_linha2 = fonte_instrucoes.render('Derrote-os respondendo às perguntas', True, cor)
        colega_txt_linha1 = fonte_instrucoes.render('Este é seu colega!', True, cor)
        colega_txt_linha2 = fonte_instrucoes.render('Liberte-o com os seus conhecimentos', True, cor)
        relogio_txt = fonte_instrucoes.render('Colete relógios para ganhar tempo', True, cor)
        coracao_txt = fonte_instrucoes.render('Não perca todas as suas vidas', True, cor)
        pausar_txt = fonte_instrucoes.render('Pressione p para pausar o jogo', True, cor)
        voltar_txt = fonte.render('Voltar', True, cor)

        jogador_rect_linha1 = jogador_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 - 50))
        jogador_rect_linha2 = jogador_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 - 10))
        professor_rect_linha1 = professor_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 100))
        professor_rect_linha2 = professor_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 140))
        colega_rect_linha1 = colega_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 220))
        colega_rect_linha2 = colega_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 260))
        relogio_rect = relogio_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 350))
        coracao_rect = coracao_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 440))
        pausar_rect = pausar_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 530))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, 6*ALTURA/7 + 50))

        tela.blit(pygame.transform.scale(pygame.image.load('imgs/jogador/jogador.png'), (70, 70)), (LARGURA/8 - 20, ALTURA / 6 - 60))
        tela.blit(jogador_txt_linha1, jogador_rect_linha1)
        tela.blit(jogador_txt_linha2, jogador_rect_linha2)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (70, 70)), (LARGURA/8 - 110, ALTURA / 6 + 90))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (70, 70)), (LARGURA/8 - 10, ALTURA / 6 + 90))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (70, 70)), (LARGURA/8 - 60, ALTURA / 6 + 90))
        tela.blit(professor_txt_linha1, professor_rect_linha1)
        tela.blit(professor_txt_linha2, professor_rect_linha2)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/colegas/colega.png'), (70, 70)), (LARGURA/8 - 20, ALTURA /6 + 210))
        tela.blit(colega_txt_linha1, colega_rect_linha1)
        tela.blit(colega_txt_linha2, colega_rect_linha2)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/outros/relogio.png'), (70, 70)), (LARGURA/8 - 20, ALTURA/6 + 320))
        tela.blit(relogio_txt, relogio_rect)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/outros/vida.png'), (70, 70)), (LARGURA/8 - 20, ALTURA/6 + 410))
        tela.blit(coracao_txt, coracao_rect)
        tela.blit(pausar_txt, pausar_rect)
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
    dados = {
        'jog_x': jog_x,
        'jog_y': jog_y,
        'tempo': tempo,
        'vidas': vidas,
        'pegou_relogio': pegou_relogio,
        'nome_jogador': nome_jogador,
        'nivel': nivel,
        'pontuacao': pontuacao
    }
    nome_arquivo = f'save_{nome_jogador}.json'
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo)

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
        global tempo, nivel, jog_x, jog_y, direcao, direcao_comando, vidas, pegou_relogio

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
                    pegou_relogio = False
                    return

        pygame.display.flip()

def mostrar_nivel(nivel):
    tela.fill(cor_fundo)
    nivel_txt = fonte.render(f'Nível {nivel+1}', True, cor)
    nivel_rect = nivel_txt.get_rect(center=(LARGURA/2, ALTURA/2))
    tela.blit(nivel_txt, nivel_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def mostrar_ranking():
    ranking = [
        {'posicao': '1º', 'pontos': '?????'},
        {'posicao': '2º', 'pontos': '?????'},
        {'posicao': '3º', 'pontos': '?????'},
        {'posicao': '4º', 'pontos': '?????'},
        {'posicao': '5º', 'pontos': '?????'}
    ]

    while True:
        tela.fill(cor_fundo)
        ranking_txt = fonte.render('Ranking', True, cor)
        voltar_txt = fonte.render('Voltar', True, cor)
        ranking_rect = ranking_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 350))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 360))
        
        tela.blit(ranking_txt, ranking_rect)
        tela.blit(voltar_txt, voltar_rect)

        for i, item in enumerate(ranking):
            posicao_txt = fonte.render(f'{item['posicao']} ........................ {item['pontos']}', True, cor)
            posicao_rect = posicao_txt.get_rect(center=(LARGURA/2, 200 + i * 60))
            tela.blit(posicao_txt, posicao_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_rect.collidepoint:
                    return
    
        pygame.display.flip()

def colisao_relogio() :
    global pegou_relogio
    global tempo

    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    num = 14

    if centro_x // 40 < 29 :
        if lab[(centro_y-(num+2))//alt + 1][(centro_x+14)//larg] == 2 and lab[(centro_y-(num+2))//alt + 1][(centro_x-4)//larg] == 2 and not pegou_relogio :
            pegou_relogio = True
            if tempo + 500 <= tempo_inicial :
                tempo += 500
            else :
                tempo = tempo_inicial
        if lab[(centro_y+(num+14))//alt - 1][(centro_x+14)//larg] == 2 and lab[(centro_y+(num+14))//alt - 1][(centro_x-4)//larg] == 2 and not pegou_relogio :
            pegou_relogio = True
            if tempo + 500 <= tempo_inicial :
                tempo += 500
            else :
                tempo = tempo_inicial
        if lab[(centro_y-(num-10))//alt][(centro_x-(num))//larg + 1] == 2 and lab[(centro_y+(num+4))//alt][(centro_x-(num))//larg + 1] == 2 and not pegou_relogio :
            pegou_relogio = True
            if tempo + 500 <= tempo_inicial :
                tempo += 500
            else :
                tempo = tempo_inicial
        if lab[(centro_y-(num-10))//alt][(centro_x+(num+6))//larg - 1] == 2 and lab[(centro_y+(num+4))//alt][(centro_x+(num+6))//larg - 1] == 2 and not pegou_relogio :
            pegou_relogio = True
            if tempo + 500 <= tempo_inicial :
                tempo += 500
            else :
                tempo = tempo_inicial

def carregar_jogo():
    salvos = [i for i in os.listdir() if i.startswith('save_') and i.endswith('.json')]
    if not salvos:
        return None
    escolher_jogo = None
    while escolher_jogo == None:
        tela.fill(cor_fundo)
        titulo_carregar_txt = fonte_titulo.render('Selecione um jogo salvo: ', True, cor)
        tela.blit(titulo_carregar_txt, (LARGURA/2 - titulo_carregar_txt.get_width()/2, 65))
        
        salvos_rects = []
        for i, salvo in enumerate(salvos):
            nome_salvo = salvo.split('_')[1].replace('.json', '')
            salvo_txt = fonte.render(f'Carregamento {i+1}: {nome_salvo}', True, cor)
            salvo_rect = salvo_txt.get_rect(center=(LARGURA/2, 200 + i * 50))
            tela.blit(salvo_txt, salvo_rect)
            salvos_rects.append((salvo_rect, salvo))

        voltar_txt = fonte.render('Voltar', True, cor)
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 360))
        tela.blit(voltar_txt, voltar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for salvo_rect, salvo in salvos_rects:
                    if salvo_rect.collidepoint(event.pos):
                        escolher_jogo = salvo
                        break
                    if voltar_rect.collidepoint:
                        menu_inicial()

        pygame.display.flip()
        timer.tick(FPS)

    if escolher_jogo:
        with open(escolher_jogo, 'r') as arquivo:
            dados_salvos = json.load(arquivo)
        global jog_x, jog_y, nivel, vidas, tempo, lab, pegou_relogio, nome_jogador
        jog_x = dados_salvos['jog_x']
        jog_y = dados_salvos['jog_y']
        nivel = dados_salvos['nivel']
        vidas = dados_salvos['vidas']
        tempo = dados_salvos['tempo']
        pegou_relogio = dados_salvos['pegou_relogio']
        nome_jogador = dados_salvos['nome_jogador']
        lab = labirinto[nivel]

def inserir_nome():
    global nome_jogador
    nome_jogador = ''
    input = True
    while input:
        tela.fill(cor_fundo)
        inserir_nome_txt = fonte.render('Digite seu nome:', True, cor)
        nome_txt = fonte.render(nome_jogador, True, cor)
        tela.blit(inserir_nome_txt, (LARGURA/2 - inserir_nome_txt.get_width()/2, ALTURA/2 - 100))
        tela.blit(nome_txt, (LARGURA/2 - nome_txt.get_width()/2, ALTURA/2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input = False
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    nome_jogador += event.unicode

def colisao_prof() :
    global pode_mover, prof_morto, pontuacao, vidas

    if not prof_morto and centro_x // 40 < 29 :
        if centro_x >= prof_x and centro_x <= prof_x + 30 and centro_y >= prof_y and centro_y <= prof_y + 30 :
            pode_mover = False
            if nivel == 0 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (800, 800)), (LARGURA/2, -28))
            elif nivel == 1 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (800, 800)), (LARGURA/2, -28))
            elif nivel == 2 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (800, 800)), (LARGURA/2, -28))
            pygame.draw.rect(tela, 'blue', (10, ALTURA//2, LARGURA-20, 300))
            if nivel == 0 :
                pergunta_txt = fonte_instrucoes.render('Qual foi um objeto de estudo da física após 1920?', True, cor)
                alt_a_txt = fonte.render('Mecânica', True, cor)
                alt_b_txt = fonte.render('Gravitação', True, cor)
                alt_c_txt = fonte.render('Relatividade', True, cor)
            elif nivel == 1 :
                pergunta_txt = fonte_instrucoes.render('Qual das opções é uma quádrica?', True, cor)
                alt_a_txt = fonte.render('Elipsóide', True, cor)
                alt_b_txt = fonte.render('Hipérbole', True, cor)
                alt_c_txt = fonte.render('Parábola', True, cor)
            elif nivel == 2 :
                pergunta_txt = fonte_instrucoes.render('Qual é a função do processador central?', True, cor)
                alt_a_txt = fonte.render('Receber informações', True, cor)
                alt_b_txt = fonte.render('Coordenar o funcionamento do computador', True, cor)
                alt_c_txt = fonte.render('Guardar dados', True, cor)

            pergunta_rect = pergunta_txt.get_rect(topleft=(28, ALTURA//2 + 18))
            alt_a_rect = alt_a_txt.get_rect(topleft=(28, ALTURA//2 + 100))
            alt_b_rect = alt_b_txt.get_rect(topleft=(28, ALTURA//2 + 170))
            alt_c_rect = alt_c_txt.get_rect(topleft=(28, ALTURA//2 + 240))

            tela.blit(pergunta_txt, pergunta_rect)
            tela.blit(alt_a_txt, alt_a_rect)
            tela.blit(alt_b_txt, alt_b_rect)
            tela.blit(alt_c_txt, alt_c_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if nivel == 0 :
                        if alt_c_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                        elif alt_a_rect.collidepoint(event.pos) or alt_b_rect.collidepoint(event.pos) :
                            vidas -= 1
                    elif nivel == 1 :
                        if alt_a_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                        elif alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                    elif nivel == 2 :
                        if alt_b_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                        elif alt_a_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                    if alt_a_rect.collidepoint(event.pos) or alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                        prof_morto = True
                        pode_mover = True

rodando = True
tempo = tempo_inicial
opcao = menu_inicial()
if opcao == 'novo_jogo':
    inserir_nome()
    mostrar_nivel(nivel)
elif opcao == 'carregar_jogo':
    carregar_jogo()
    mostrar_nivel(nivel)
while rodando :
    timer.tick(FPS)
    lab = labirinto[nivel]
    tempo -= 1
    tela.fill(cor_fundo)
    desenha_labirinto(lab)
    alvo = (jog_x, jog_y)
    professor = Professor(prof_x, prof_y, alvo, velocidade_prof, prof_img,
                        prof_direcao, prof_morto)
    if not prof_morto :
        prof_x, prof_y, prof_direcao = professor.anda()
    desenha_jogador()
    centro_x = jog_x + 15
    centro_y = jog_y + 15
    pode_andar = verifica_posicao(centro_x, centro_y)
    if pode_mover :
        jog_x, jog_y = move_jogador(jog_x, jog_y)
    colisao_relogio()
    colisao_prof()

    if tempo <= 0 or vidas < 0:
        fim_jogo()
    
    if prof_morto :
        nivel += 1
        if nivel == 1 :
            tempo_inicial = 6000
            ganha_pontos = 10
            posx_inicial = 30
            posy_inicial = 30
            professor_img = imecc_img
            prof_morto = False
        elif nivel == 2 :
            tempo_inicial = 5500
            ganha_pontos = 15
            posx_inicial = LARGURA//2
            posy_inicial = (ALTURA-50)//2
            professor_img = santiago_img
            prof_morto = False
        elif nivel == 3 :
            fim_jogo()
        tempo = tempo_inicial
        pegou_relogio = False
        jog_x = posx_inicial
        jog_y = posy_inicial
        direcao = 'direita'
        direcao_comando = 'direita'
        prof_x = profx_inicial
        prof_y = profy_inicial
        prof_direcao = 'direita'
        prof_img = professor_img
        prof_morto = False
        pode_mover = True

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
    
    if time.time() - ultimo_salvamento > intervalo_salvamento:
        salvar_jogo()
        ultimo_salvamento = time.time()

    pygame.display.flip()
pygame.quit()