# Carolina Momoli da Costa - 252062
# Victor Amaral de Sousa - 281878

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
python_logo_img = pygame.transform.scale(pygame.image.load('imgs/outros/python_logo.png'), (30, 30))

musica_fundo = pygame.mixer.music.load('sons/musica_fundo.mp3')
som_perdeu_vida = pygame.mixer.Sound('sons/som_perdeu_vida.ogg')
som_perdeu = pygame.mixer.Sound('sons/som_perdeu.ogg')
som_pegou_relogio = pygame.mixer.Sound('sons/som_pegou_relogio.ogg')
som_pegou_python = pygame.mixer.Sound('sons/som_pegou_python.ogg')
som_resposta_correta = pygame.mixer.Sound('sons/som_resposta_correta.ogg')
som_click = pygame.mixer.Sound('sons/som_click.wav')
som_mostrar_nivel = pygame.mixer.Sound('sons/som_mostrar_nivel.ogg')

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

nivel = 0
cor_fundo = pygame.Color(10, 32, 47)
cor_titulo = pygame.Color(211, 40, 54)
cor_texto = pygame.Color(212, 226, 204)
cor_opcao = pygame.Color(132, 174, 164)
cor = 'white'

if nivel == 0 :
    posx_inicial = 30
    posy_inicial = 365
    tempo_inicial = 5000
    ganha_pontos = 5
    professor_img = ifgw_img
    profx_inicial = LARGURA//2 + 160
    profy_inicial = ALTURA//2 - 50
    prof_direcao = 'direita'
    prof_morto = False
    pegou_python = [False]*15
    quantos_pegou = 0
    colega_salvo = False

jog_x = posx_inicial
jog_y = posy_inicial
direcao = 'direita'
direcao_comando = 'direita'
velocidade_jog = 3
vidas = 3
pegou_relogio = False
pontuacao = 0
ultimo_salvamento = time.time()
intervalo_salvamento = 5
prof_x = profx_inicial
prof_y = profy_inicial
prof_img = professor_img
pode_mover = True
n_python_logos = 15
python_logos = [0]*15

class Professor :
    """
    Classe que guarda as informações sobre os professores

    Parâmetros:
    coord_x: coordenada x do professor
    coord_y: coordenada y do professor
    alvo: coordenadas do aluno
    velocidade: com quantos pixels o professor se movimenta
    img: imagem do professor
    direc: direção do movimento do professor
    morte: variável que informa se o professor está ou não no jogo
    """
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
        """
        Desenha a imagem do professor na tela caso ele não tenha morrido
        """
        if not self.morte :
            tela.blit(self.img, (self.pos_x, self.pos_y))
        prof_rect = pygame.rect.Rect((self.centro_x - 15, self.centro_y - 15), (35, 35))
        return prof_rect
    
    def verif_colisoes(self) :
        """
        Método que verifica para quais lados o professor pode andar
        """
        alt = (ALTURA - 70) // 21
        larg = LARGURA // 40
        num = 14
        self.movimentos = [False, False, False, False]

        if self.centro_x // 40 < 29 :
            if lab[(self.centro_y-(num+6))//alt + 1][(self.centro_x-14)//larg] != 1 and lab[(self.centro_y-(num+6))//alt + 1][(self.centro_x+14)//larg] != 1 :
                self.movimentos[3] = True
            if lab[(self.centro_y+(num+14))//alt - 1][(self.centro_x+14)//larg] != 1 and lab[(self.centro_y+(num+14))//alt - 1][(self.centro_x-4)//larg] != 1 :
                self.movimentos[2] = True
            if lab[(self.centro_y-(num-10))//alt][(self.centro_x-(num))//larg + 1] != 1 and lab[(self.centro_y+(num+4))//alt][(self.centro_x-(num))//larg + 1] != 1 :
                self.movimentos[0] = True
            if lab[(self.centro_y-(num-20))//alt][(self.centro_x+(num))//larg - 1] != 1 and lab[(self.centro_y+(num-20))//alt][(self.centro_x+(num+6))//larg - 1] != 1 :
                self.movimentos[1] = True
        else :
            self.movimentos[0] = True
            self.movimentos[1] = True

        return self.movimentos
    
    def anda(self) :
        """
        Método que faz a movimentação do professor de acordo com as coordenadas do alvo
        """
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
                if self.alvo[0] < self.pos_x and self.movimentos[1] :
                    self.pos_x -= self.velocidade
                elif self.alvo[1] > self.pos_y and self.movimentos[3] :
                    self.direcao = 'baixo'
                    self.pos_y += self.velocidade
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
                if self.alvo[1] < self.pos_y and self.movimentos[2] :
                    self.pos_y -= self.velocidade
                elif self.alvo[0] < self.pos_x and self.movimentos[1] :
                    self.direcao = 'esquerda'
                    self.pos_x -= self.velocidade
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
        
        if self.pos_x < -30 :
            self.pos_x = LARGURA
        elif self.pos_x > LARGURA :
            self.pos_x = -30

        return self.pos_x, self.pos_y, self.direcao

def desenha_labirinto(lab) :
    """
    Função que desenha a tela do labirinto a partir de uma matriz,
    que será passada por meio do parâmetro lab
    """
    global python_logos, colega_x, colega_y, cor_linhas_lab, cor_parede, cor_fundo_lab

    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    cont_python = 0

    if nivel == 0 :
        cor_linhas_lab = pygame.Color(14,154,167)
        cor_parede = pygame.Color(150,206,180)
        cor_fundo_lab = 'lightskyblue1'
    elif nivel == 1 :
        cor_linhas_lab = pygame.Color(20, 30, 70)
        cor_parede = 'tomato'
        cor_fundo_lab = 'oldlace'
    elif nivel == 2 :
        cor_linhas_lab = pygame.Color(14,54,124)
        cor_parede = pygame.Color(251,162,87)
        cor_fundo_lab = 'floralwhite'

    tela.fill(cor_fundo_lab)

    for i in range(len(lab)) :
        for j in range(len(lab[i])) :
            if lab[i][j] == 1 :
                pygame.draw.rect(tela, cor_parede, (j*larg, i*alt, larg, alt))
                pygame.draw.line(tela, cor_linhas_lab, (j * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_linhas_lab, (j * larg, i * alt), ((j + 1) * larg, i * alt), 2)
                pygame.draw.line(tela, cor_linhas_lab, (j * larg, (i + 1) * alt), ((j + 1) * larg, (i + 1) * alt), 2)
                pygame.draw.line(tela, cor_linhas_lab, ((j + 0.5) * larg, i * alt), ((j + 0.5) * larg, (i + 0.5) * alt), 2)
                pygame.draw.line(tela, cor_linhas_lab, ((j + 1) * larg, (i + 0.5) * alt), ((j + 1) * larg, (i + 1) * alt), 2)
                pygame.draw.line(tela, cor_linhas_lab, (j * larg, (i + 0.5) * alt), (j * larg, (i + 1) * alt), 2)
                if j > 0 :
                    if lab[i][j-1] != 1 :
                        pygame.draw.line(tela, cor_linhas_lab, (j * larg, i * alt), (j * larg, (i + 1) * alt), 2)
                if j < len(lab[i]) - 1 :
                    if lab[i][j+1] != 1 :
                        pygame.draw.line(tela, cor_linhas_lab, ((j + 1) * larg, i * alt), ((j + 1) * larg, (i + 1) * alt), 2)
                if j == 0 :
                    pygame.draw.line(tela, cor_linhas_lab, (j * larg, i * alt), (j * larg, (i + 1) * alt), 2)
            elif lab[i][j] == 2 and not pegou_relogio :
                tela.blit(relogio_img, (j*larg, i*alt))
            elif lab[i][j] == 3 :
                if not pegou_python[cont_python] :
                    python_logos[cont_python] = (j * larg, i * alt)
                    tela.blit(python_logo_img, python_logos[cont_python])
                cont_python += 1
            elif lab[i][j] == 4 and not colega_salvo :
                colega_x = j*larg
                colega_y = i*alt
                tela.blit(colega_img, (j*larg, i*alt))

    pygame.draw.rect(tela, cor_linhas_lab, (0, ALTURA-82, LARGURA, 82))

    pygame.draw.rect(tela, 'white', ((60, 800), (0.165*tempo_inicial, 30)))
    if tempo > tempo_inicial/2 :
        pygame.draw.rect(tela, 'green', ((60, 800), (0.165*tempo, 30)))
    elif tempo > tempo_inicial/4 :
        pygame.draw.rect(tela, 'yellow', ((60, 800), (0.165*tempo, 30)))
    else :
        pygame.draw.rect(tela, 'red', ((60, 800), (0.165*tempo, 30)))

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
    """
    Função que desenha o jogador de acordo com a direção na qual ele se movimenta
    """
    if direcao == 'direita' :
        tela.blit(pygame.transform.flip(jogador_img, True, False), (jog_x, jog_y))
    elif direcao == 'esquerda' :
        tela.blit(jogador_img, (jog_x, jog_y))
    elif direcao == 'cima' :
        tela.blit(pygame.transform.flip(jogador_img, True, False), (jog_x, jog_y))
    elif direcao == 'baixo' :
        tela.blit(jogador_img, (jog_x, jog_y))

def verifica_posicao(centrox, centroy) :
    """
    Função que verifica para quais lados o jogador pode se movimentar,
    utilizando, como parâmetros, as coordenadas (x, y) do centro do jogador
    """
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
    """
    Função que faz a movimentação do jogador por meio das teclas do teclado
    Parâmetros: coordenadas (x, y) do jogador
    """
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
    """
    Função que desenha a tela inicial do jogo
    """
    while True:
        tela.fill(cor_fundo)

        tela.blit(pygame.transform.scale(pygame.image.load('imgs/jogador/jogador.png'), (900, 900)), (LARGURA/2 + 30, ALTURA/2 - 105))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (300, 300)), (128, ALTURA/2 - 150))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (300, 300)), (-70, ALTURA/2 - 150))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (310, 310)), (20, ALTURA/2))

        titulo_txt = fonte_titulo.render('Os Labirintos da Unicamp', True, cor_titulo)
        novo_jogo_txt = fonte.render('Novo Jogo', True, cor_opcao)
        informacoes_txt = fonte.render('Informações', True, cor_opcao)
        sair_txt = fonte.render('Sair', True, cor_opcao)
        carregar_txt = fonte.render('Carregar Jogo', True, cor_opcao)
        ranking_txt = fonte.render('Ranking', True, cor_opcao)

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
                    som_click.play()
                    inserir_nome()
                    dificuldades()
                    mostrar_nivel(nivel)
                    return
                if carregar_rect.collidepoint(event.pos):
                    som_click.play()
                    carregar_jogo()
                    dificuldades()
                    mostrar_nivel(nivel)
                    return
                if informacoes_rect.collidepoint(event.pos):
                    som_click.play()
                    informacoes()
                if sair_rect.collidepoint(event.pos):
                    som_click.play()
                    pygame.quit()
                    sys.exit()
                if ranking_rect.collidepoint(event.pos):
                    som_click.play()
                    mostrar_ranking()
        
        pygame.display.flip()
     
def informacoes():
    """
    Função que desenha a tela que contém as informações do jogo
    """
    while True:
        tela.fill(cor_fundo)

        jogador_txt_linha1 = fonte_instrucoes.render('Este é você!', True, cor_texto)
        jogador_txt_linha2 = fonte_instrucoes.render('Utilize as setas do teclado para andar', True, cor_texto)
        professor_txt_linha1 = fonte_instrucoes.render('Cuidado com os professores!', True, cor_texto)
        professor_txt_linha2 = fonte_instrucoes.render('Derrote-os respondendo às perguntas', True, cor_texto)
        colega_txt_linha1 = fonte_instrucoes.render('Este é seu colega!', True, cor_texto)
        colega_txt_linha2 = fonte_instrucoes.render('Liberte-o com os seus conhecimentos', True, cor_texto)
        relogio_txt = fonte_instrucoes.render('Colete relógios para ganhar tempo', True, cor_texto)
        coracao_txt = fonte_instrucoes.render('Não perca todas as suas vidas', True, cor_texto)
        minipythons_txt = fonte_instrucoes.render('Colete mini Pythons para ganhar pontos', True, cor_texto)
        voltar_txt = fonte.render('Voltar', True, cor_opcao)

        jogador_rect_linha1 = jogador_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 - 50))
        jogador_rect_linha2 = jogador_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 - 10))
        professor_rect_linha1 = professor_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 100))
        professor_rect_linha2 = professor_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 140))
        colega_rect_linha1 = colega_txt_linha1.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 220))
        colega_rect_linha2 = colega_txt_linha2.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 260))
        relogio_rect = relogio_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 350))
        coracao_rect = coracao_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 440))
        minipythons_rect = minipythons_txt.get_rect(topleft=(LARGURA/8 + 80, ALTURA/6 + 530))
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
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/outros/python_logo.png'), (70, 70)), (LARGURA/8 - 20, ALTURA/6 + 500))
        tela.blit(minipythons_txt, minipythons_rect)
        tela.blit(voltar_txt, voltar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_rect.collidepoint(event.pos):
                    som_click.play()
                    return
        pygame.display.flip()

def salvar_jogo():
    """
    Função utilizada para salvar o jogo
    """
    dados = {
        'jog_x': jog_x,
        'jog_y': jog_y,
        'tempo': tempo,
        'vidas': vidas,
        'pegou_relogio': pegou_relogio,
        'nome_jogador': nome_jogador,
        'nivel': nivel,
        'pontuacao': pontuacao,
        'prof_x': prof_x,
        'prof_y': prof_y,
        'prof_morto': prof_morto,
        'colega_salvo': colega_salvo,
        'python_logos': python_logos,
        'pegou_python': pegou_python,
        'quantos_pegou': quantos_pegou,
        'pode_mover': pode_mover,
        'ganha_pontos': ganha_pontos
    }
    nome_arquivo = f'save_{nome_jogador}.json'
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo)

def pause():
    """
    Função utilizada para pausar o jogo
    """
    while True:
        tela.fill(cor_fundo)
        sair_txt = fonte.render('Sair', True, cor_opcao)
        voltar_txt = fonte.render('Voltar', True, cor_opcao)
        salvar_txt = fonte.render('Salvar', True, cor_opcao)

        sair_rect = sair_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 50))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2))
        salvar_rect = salvar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 50))

        tela.blit(sair_txt, sair_rect)
        tela.blit(voltar_txt, voltar_rect)
        tela.blit(salvar_txt, salvar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salvar_jogo()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sair_rect.collidepoint(event.pos):
                    som_click.play()
                    pygame.quit()
                    sys.exit()
                if voltar_rect.collidepoint(event.pos):
                    som_click.play()
                    return
                if salvar_rect.collidepoint(event.pos):
                    som_click.play()
                    salvar_jogo()
                    return
        pygame.display.flip()

def perdeu_jogo() :
    """
    Função que desenha a tela de derrota do jogo
    """
    while True :
        global tempo, nivel, lab, jog_x, jog_y, direcao, direcao_comando, vidas, pegou_relogio, pontuacao, ganha_pontos
        global prof_x, prof_y, prof_direcao, prof_img, prof_morto, pode_mover, quantos_pegou, python_logos, pegou_python, colega_salvo, velocidade_prof

        tela.fill(cor_fundo)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (400, 400)), (-140, ALTURA - 600))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (400, 400)), (-10, ALTURA - 420))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (400, 400)), (LARGURA - 380, ALTURA - 440))

        fim_txt = fonte_titulo.render('Fim de jogo', True, cor_titulo)
        exame_txt = fonte.render('Você ficou de exame!', True, cor_texto)
        estude_txt = fonte.render('Estude mais e tente novamente', True, cor_texto)
        pontuacao_txt = fonte.render(f'Pontuação: {pontuacao}', True, cor_texto)
        novo_jogo_txt = fonte.render('Jogar novamente', True, cor_opcao)
        sair_txt = fonte.render('Sair', True, cor_opcao)

        fim_rect = fim_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 200))
        exame_rect = exame_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 100))
        estude_rect = estude_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 40))
        pontuacao_rect = fim_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 70))
        novo_jogo_rect = novo_jogo_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 170))
        sair_rect = sair_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 240))

        tela.blit(fim_txt, fim_rect)
        tela.blit(exame_txt, exame_rect)
        tela.blit(estude_txt, estude_rect)
        tela.blit(pontuacao_txt, pontuacao_rect)
        tela.blit(novo_jogo_txt, novo_jogo_rect)
        tela.blit(sair_txt, sair_rect)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                if sair_rect.collidepoint(event.pos) :
                    som_click.play()
                    pygame.quit()
                    sys.exit()
                if novo_jogo_rect.collidepoint(event.pos) :
                    som_click.play()
                    inserir_nome()
                    dificuldades()
                    if dificuldade == 0 :
                        tempo_inicial = 5000
                        tempo = tempo_inicial
                        velocidade_prof = 2
                        ganha_pontos = 5
                    elif dificuldade == 1 :
                        tempo_inicial = 5000
                        tempo = tempo_inicial
                        velocidade_prof = 4
                        ganha_pontos = 10
                    elif dificuldade == 2 :
                        tempo_inicial = 4500
                        tempo = tempo_inicial
                        velocidade_prof = 4
                        ganha_pontos = 15
                    nivel = 0
                    lab = labirinto[nivel]
                    vidas = 3
                    jog_x = 30
                    jog_y = 365
                    direcao = 'direita'
                    direcao_comando = 'direita'
                    pegou_relogio = False
                    pontuacao = 0
                    prof_x = LARGURA//2 + 160
                    prof_y = ALTURA//2 - 50
                    prof_direcao = 'direita'
                    prof_img = ifgw_img
                    prof_morto = False
                    pode_mover = True
                    quantos_pegou = 0
                    python_logos = [0]*15
                    pegou_python = [False]*15
                    colega_salvo = False
                    mostrar_nivel(nivel)
                    return
        adicionar_entrada(nome_jogador, pontuacao)
        pygame.display.flip()

def ganhou_jogo() :
    """
    Função que desenha a tela de vitória do jogo
    """
    while True :
        global tempo, nivel, lab, jog_x, jog_y, direcao, direcao_comando, vidas, pegou_relogio, pontuacao, ganha_pontos
        global prof_x, prof_y, prof_direcao, prof_img, prof_morto, pode_mover, quantos_pegou, python_logos, pegou_python, colega_salvo, velocidade_prof

        tela.fill(cor_fundo)
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/jogador/jogador.png'), (600, 600)), (LARGURA/2 + 180, ALTURA - 400))
        tela.blit(pygame.transform.scale(pygame.image.load('imgs/colegas/colega.png'), (300, 300)), (60, 30))
        
        fim_txt = fonte_titulo.render('Parabéns!', True, cor_titulo)
        exame_txt = fonte.render('Você sobreviveu ao', True, cor_texto)
        estude_txt = fonte.render('primeiro semestre na Unicamp!', True, cor_texto)
        pontuacao_txt = fonte.render(f'Pontuação: {pontuacao}', True, cor_texto)
        novo_jogo_txt = fonte.render('Jogar novamente', True, cor_opcao)
        sair_txt = fonte.render('Sair', True, cor_opcao)

        fim_rect = fim_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 200))
        exame_rect = exame_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 100))
        estude_rect = estude_txt.get_rect(center = (LARGURA/2, ALTURA/2 - 40))
        pontuacao_rect = fim_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 70))
        novo_jogo_rect = novo_jogo_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 170))
        sair_rect = sair_txt.get_rect(center = (LARGURA/2, ALTURA/2 + 240))

        tela.blit(fim_txt, fim_rect)
        tela.blit(exame_txt, exame_rect)
        tela.blit(estude_txt, estude_rect)
        tela.blit(pontuacao_txt, pontuacao_rect)
        tela.blit(novo_jogo_txt, novo_jogo_rect)
        tela.blit(sair_txt, sair_rect)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                if sair_rect.collidepoint(event.pos) :
                    som_click.play()
                    pygame.quit()
                    sys.exit()
                if novo_jogo_rect.collidepoint(event.pos) :
                    som_click.play()
                    inserir_nome()
                    dificuldades()
                    if dificuldade == 0 :
                        tempo_inicial = 5000
                        tempo = tempo_inicial
                        velocidade_prof = 2
                        ganha_pontos = 5
                    elif dificuldade == 1 :
                        tempo_inicial = 5000
                        tempo = tempo_inicial
                        velocidade_prof = 4
                        ganha_pontos = 10
                    elif dificuldade == 2 :
                        tempo_inicial = 4500
                        tempo = tempo_inicial
                        velocidade_prof = 4
                        ganha_pontos = 15
                    nivel = 0
                    lab = labirinto[nivel]
                    vidas = 3
                    jog_x = 30
                    jog_y = 365
                    direcao = 'direita'
                    direcao_comando = 'direita'
                    pegou_relogio = False
                    pontuacao = 0
                    prof_x = LARGURA//2 + 160
                    prof_y = ALTURA//2 - 50
                    prof_direcao = 'direita'
                    prof_img = ifgw_img
                    prof_morto = False
                    pode_mover = True
                    quantos_pegou = 0
                    python_logos = [0]*15
                    pegou_python = [False]*15
                    colega_salvo = False
                    mostrar_nivel(nivel)
                    return
        adicionar_entrada(nome_jogador, pontuacao)
        pygame.display.flip()

def mostrar_nivel(nivel):
    """
    Função que desenha a tela de níveis no inicio de cada nível diferente
    """
    if nivel == 0 :
        local = 'IFGW'
    elif nivel == 1 :
        local = 'IMECC'
    elif nivel == 2 :
        local = 'IC'

    tela.fill(cor_fundo)
    nivel_txt = fonte.render(f'Nível {nivel+1}', True, cor_titulo)
    local_txt = fonte.render(f'{local}', True, cor_texto)
    nivel_rect = nivel_txt.get_rect(center=(LARGURA/2, ALTURA/2))
    local_rect = local_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
    tela.blit(nivel_txt, nivel_rect)
    tela.blit(local_txt, local_rect)

    som_mostrar_nivel.play()
    pygame.display.flip()
    pygame.time.delay(2000)

def mostrar_ranking():
    """
    Função utilizada para mostrar a tela de ranking do jogo
    """
    ranking = carregar_ranking()
    ranking_ordenado = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
 
    while True:
        tela.fill(cor_fundo)
        ranking_txt = fonte.render('Ranking', True, cor_titulo)
        voltar_txt = fonte.render('Voltar', True, cor_opcao)
        ranking_rect = ranking_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 350))
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 360))
        
        tela.blit(ranking_txt, ranking_rect)
        tela.blit(voltar_txt, voltar_rect)

        y_pos = 200
        for nome, pontos in ranking_ordenado:
            posicao_txt = fonte.render(f'{nome} - {pontos} pontos!', True, cor_texto)
            posicao_rect = posicao_txt.get_rect(center=(LARGURA/2, y_pos))
            tela.blit(posicao_txt, posicao_rect)
            y_pos += 60 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_rect.collidepoint:
                    som_click.play()
                    return
    
        pygame.display.flip()

def colisao_relogio() :
    """
    Função utilizada para verificar se o jogador colidiu com o relógio
    Caso sim, o tempo do nível é aumentado
    """
    global pegou_relogio
    global tempo

    larg = LARGURA // 40
    alt = (ALTURA - 70) // 21
    num = 14

    if centro_x // 40 < 29 :
        if lab[(centro_y-(num+2))//alt + 1][(centro_x+14)//larg] == 2 and lab[(centro_y-(num+2))//alt + 1][(centro_x-4)//larg] == 2 and not pegou_relogio :
            pegou_relogio = True
            som_pegou_relogio.play()
            if tempo + 1000 <= tempo_inicial :
                tempo += 1000
            else :
                tempo = tempo_inicial
        if lab[(centro_y+(num+14))//alt - 1][(centro_x+14)//larg] == 2 and lab[(centro_y+(num+14))//alt - 1][(centro_x-4)//larg] == 2 and not pegou_relogio :
            pegou_relogio = True
            som_pegou_relogio.play()
            if tempo + 1000 <= tempo_inicial :
                tempo += 1000
            else :
                tempo = tempo_inicial
        if lab[(centro_y-(num-10))//alt][(centro_x-(num))//larg + 1] == 2 and lab[(centro_y+(num+4))//alt][(centro_x-(num))//larg + 1] == 2 and not pegou_relogio :
            pegou_relogio = True
            som_pegou_relogio.play()
            if tempo + 1000 <= tempo_inicial :
                tempo += 1000
            else :
                tempo = tempo_inicial
        if lab[(centro_y-(num-10))//alt][(centro_x+(num+6))//larg - 1] == 2 and lab[(centro_y+(num+4))//alt][(centro_x+(num+6))//larg - 1] == 2 and not pegou_relogio :
            pegou_relogio = True
            som_pegou_relogio.play()
            if tempo + 1000 <= tempo_inicial :
                tempo += 1000
            else :
                tempo = tempo_inicial

def carregar_jogo():
    """
    Função que desenha a tela que mostra os jogos salvos
    """
    salvos = [i for i in os.listdir() if i.startswith('save_') and i.endswith('.json')]
    if not salvos:
        return None
    escolher_jogo = None
    while escolher_jogo == None:
        tela.fill(cor_fundo)
        titulo_carregar_txt = fonte_titulo.render('Selecione um jogo salvo: ', True, cor_titulo)
        tela.blit(titulo_carregar_txt, (LARGURA/2 - titulo_carregar_txt.get_width()/2, 65))
        
        salvos_rects = []
        for i, salvo in enumerate(salvos):
            nome_salvo = salvo.split('_')[1].replace('.json', '')
            salvo_txt = fonte.render(f'Carregamento {i+1}: {nome_salvo}', True, cor_texto)
            salvo_rect = salvo_txt.get_rect(center=(LARGURA/2, 200 + i * 50))
            tela.blit(salvo_txt, salvo_rect)
            salvos_rects.append((salvo_rect, salvo))

        voltar_txt = fonte.render('Voltar', True, cor_opcao)
        voltar_rect = voltar_txt.get_rect(center=(LARGURA/2, ALTURA/2 + 360))
        tela.blit(voltar_txt, voltar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for salvo_rect, salvo in salvos_rects:
                    if salvo_rect.collidepoint(event.pos):
                        som_click.play()
                        escolher_jogo = salvo
                        break
                    if voltar_rect.collidepoint:
                        som_click.play()
                        menu_inicial()

        pygame.display.flip()
        timer.tick(FPS)

    if escolher_jogo:
        with open(escolher_jogo, 'r') as arquivo:
            dados_salvos = json.load(arquivo)
        global jog_x, jog_y, nivel, vidas, tempo, lab, pegou_relogio, nome_jogador, pontuacao, prof_x, prof_y, prof_img, prof_direcao, prof_morto
        global colega_salvo, python_logos, pegou_python, quantos_pegou, pode_mover, ganha_pontos

        jog_x = dados_salvos['jog_x']
        jog_y = dados_salvos['jog_y']
        nivel = dados_salvos['nivel']
        vidas = dados_salvos['vidas']
        tempo = dados_salvos['tempo']
        pegou_relogio = dados_salvos['pegou_relogio']
        nome_jogador = dados_salvos['nome_jogador']
        pontuacao = dados_salvos['pontuacao']
        prof_x = dados_salvos['prof_x']
        prof_y = dados_salvos['prof_y']
        prof_morto = dados_salvos['prof_morto']
        colega_salvo = dados_salvos['colega_salvo']
        python_logos = dados_salvos['python_logos']
        pegou_python = dados_salvos['pegou_python']
        quantos_pegou = dados_salvos['quantos_pegou']
        pode_mover = dados_salvos['pode_mover']
        ganha_pontos = dados_salvos['ganha_pontos']

        lab = labirinto[nivel]

def inserir_nome():
    """
    Função que desenha a tela de inserção de nome antes de cada jogo novo
    """
    global nome_jogador
    nome_jogador = ''
    input = True
    while input:
        tela.fill(cor_fundo)
        inserir_nome_txt = fonte.render('Digite seu nome:', True, cor_titulo)
        nome_txt = fonte.render(nome_jogador, True, cor_texto)
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
    """
    Função que verifica se o jogador colidiu com o professor
    Caso sim, as perguntas são desenhadas na tela
    """
    global pode_mover, prof_morto, pontuacao, vidas

    if not prof_morto and centro_x // 40 < 29 :
        if centro_x >= prof_x - 4 and centro_x <= prof_x + 34 and centro_y >= prof_y - 4 and centro_y <= prof_y + 34 :
            pode_mover = False
            if nivel == 0 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_ifgw.png'), (800, 800)), (LARGURA/2, -28))
            elif nivel == 1 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_imecc.png'), (800, 800)), (LARGURA/2, -28))
            elif nivel == 2 :
                tela.blit(pygame.transform.scale(pygame.image.load('imgs/professor/professor_santiago.png'), (800, 800)), (LARGURA/2, -28))
            pygame.draw.rect(tela, cor_linhas_lab, (10, ALTURA//2, LARGURA-20, 300))
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
                pergunta_txt = fonte_instrucoes.render('O que as bibliotecas em python fazem?', True, cor)
                alt_a_txt = fonte.render('Guardam livros', True, cor)
                alt_b_txt = fonte.render('Compartilham códigos já escritos', True, cor)
                alt_c_txt = fonte.render('Escrevem códigos novos', True, cor)

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
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1   
                        elif alt_a_rect.collidepoint(event.pos) or alt_b_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    elif nivel == 1 :
                        if alt_a_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1  
                        elif alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    elif nivel == 2 :
                        if alt_b_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1 
                        elif alt_a_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    if alt_a_rect.collidepoint(event.pos) or alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                        prof_morto = True
                        pode_mover = True
        else :
            pode_mover = True

def colisao_python():
    """
    Função que verifica se o jogador colidiu com os mini Pythons
    Se sim, o jogador pontua
    """
    global pontuacao, pegou_python, quantos_pegou

    jogador_rect = pygame.Rect(jog_x, jog_y, 35, 35)
    cont_python = 0
    for pos_python in python_logos:
        python_rect = pygame.Rect(pos_python[0], pos_python[1], 30, 30)
        if jogador_rect.colliderect(python_rect) and pegou_python[cont_python] == False :
            pegou_python[cont_python] = True
            som_pegou_python.play()
            pontuacao += ganha_pontos
            quantos_pegou += 1
        cont_python += 1

def colisao_colega() :
    """
    Função que verifica que o jogador colidiu com o colega
    Caso sim, as perguntas aparecem na tela
    """
    global pode_mover, colega_salvo, pontuacao, vidas

    if not colega_salvo and centro_x // 40 < 29 :
        if centro_x >= colega_x and centro_x <= colega_x + 30 and centro_y >= colega_y and centro_y <= colega_y + 30 :
            pode_mover = False
            tela.blit(pygame.transform.scale(pygame.image.load('imgs/colegas/colega.png'), (800, 800)), (LARGURA/2, -28))
            pygame.draw.rect(tela, cor_linhas_lab, (10, ALTURA//2, LARGURA-20, 300))
            if nivel == 0 :
                pergunta_txt = fonte_instrucoes.render('Qual interação tem a massa como carga?', True, cor)
                alt_a_txt = fonte.render('Fraca', True, cor)
                alt_b_txt = fonte.render('Gravitacional', True, cor)
                alt_c_txt = fonte.render('Eletromagnética', True, cor)
            elif nivel == 1 :
                pergunta_txt = fonte_instrucoes.render('O que significa F(x) ser primitiva de f(x)?', True, cor)
                alt_a_txt = fonte.render('A derivada de F(x) é f(x)', True, cor)
                alt_b_txt = fonte.render('F(x) foi descoberta primeiro', True, cor)
                alt_c_txt = fonte.render('A integral de F(x) é f(x)', True, cor)
            elif nivel == 2 :
                pergunta_txt = fonte_instrucoes.render('Qual operador é lido primeiro em Python?', True, cor)
                alt_a_txt = fonte.render('**', True, cor)
                alt_b_txt = fonte.render('/', True, cor)
                alt_c_txt = fonte.render('+', True, cor)

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
                        if alt_b_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1  
                        elif alt_a_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    elif nivel == 1 :
                        if alt_a_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1 
                        elif alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    elif nivel == 2 :
                        if alt_a_rect.collidepoint(event.pos) :
                            pontuacao += ganha_pontos
                            som_resposta_correta.play()   
                            if vidas < 3 :
                                vidas += 1                 
                        elif alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                            vidas -= 1
                            som_perdeu_vida.play()
                    if alt_a_rect.collidepoint(event.pos) or alt_b_rect.collidepoint(event.pos) or alt_c_rect.collidepoint(event.pos) :
                        colega_salvo = True
                        pode_mover = True

def dificuldades() :
    """
    Função que desenha a tela de escolha de dificuldades
    """
    global dificuldade

    while True:
        tela.fill(cor_fundo)
        selecione_txt = fonte_titulo.render('Selecione a dificuldade:', True, cor_titulo)
        facil_txt = fonte.render('Fácil', True, cor_opcao)
        medio_txt = fonte.render('Médio', True, cor_opcao)
        dificil_txt = fonte.render('Difícil', True, cor_opcao)

        selecione_rect = selecione_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 200))
        facil_rect = facil_txt.get_rect(center=(LARGURA/2, ALTURA/2 - 60))
        medio_rect = medio_txt.get_rect(center=(LARGURA/2, ALTURA/2))
        dificil_rect = dificil_txt.get_rect(center=(LARGURA/2, ALTURA / 2 + 60))

        tela.blit(selecione_txt, selecione_rect)
        tela.blit(facil_txt, facil_rect)
        tela.blit(medio_txt, medio_rect)
        tela.blit(dificil_txt, dificil_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if facil_rect.collidepoint(event.pos):
                    som_click.play()
                    dificuldade = 0
                    return
                if medio_rect.collidepoint(event.pos):
                    som_click.play()
                    dificuldade = 1
                    return
                if dificil_rect.collidepoint(event.pos):
                    som_click.play()
                    dificuldade = 2
                    return
        
        pygame.display.flip()

def carregar_ranking():
    """
    Função que abre o arquivo que guarda as pontuações no ranking
    """
    ranking = {}
    if os.path.exists('ranking.json'):
        with open('ranking.json', 'r') as arquivo:
            ranking = json.load(arquivo)
    return ranking

def adicionar_entrada(nome, pontuacao):
    """
    Função que adiciona entradas no ranking
    """
    ranking = carregar_ranking()
    if nome in ranking:
        if pontuacao > ranking[nome]:
            ranking[nome] = pontuacao
    else:
        ranking[nome] = pontuacao
    salvar_ranking(ranking)

def salvar_ranking(ranking):
    """
    Função que salva o arquivo do ranking
    """
    with open('ranking.json', 'w') as arquivo:
        json.dump(ranking, arquivo)

rodando = True
menu_inicial()

if dificuldade == 0 :
    tempo = tempo_inicial
    velocidade_prof = 2
    ganha_pontos = 5
elif dificuldade == 1 :
    tempo = tempo_inicial
    velocidade_prof = 4
    ganha_pontos = 10
elif dificuldade == 2 :
    tempo_inicial -= 1000
    tempo = tempo_inicial
    velocidade_prof = 4
    ganha_pontos = 15

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
    colisao_python()
    colisao_colega()

    if tempo <= 0 or vidas < 0:
        som_perdeu.play()
        perdeu_jogo()
    
    if prof_morto and quantos_pegou == 15 and colega_salvo :
        nivel += 1
        if nivel == 1 :
            posx_inicial = LARGURA//2 - 17
            posy_inicial = 31
            professor_img = imecc_img
            prof_morto = False
        elif nivel == 2 :
            tempo_inicial *= 0.9
            posx_inicial = LARGURA//2 - 17
            posy_inicial = 31
            professor_img = santiago_img
            prof_morto = False
        elif nivel == 3 :
            ganhou_jogo()
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
        quantos_pegou = 0
        python_logos = [0]*15
        pegou_python = [False]*15
        colega_salvo = False
        mostrar_nivel(nivel)

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