import pygame as pg
import os
import random

tela_largura = 500
tela_altura = 800

img_cano = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'pipe.png')))
img_chao = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'base.png')))
img_fundo = pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bg.png')))
img_passaros = [
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird1.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird2.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('imgs', 'bird3.png')))
]

pg.font.init()
fonte_pontos = pg.font.SysFont('arial', 50)


class Passaro:
    # carregar imagens do pássaro:
    imgs = img_passaros

    # animações da rotação:
    rotacao_max = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento:
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # restigir o deslocamento:
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do passaro:
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_max:
                self.angulo = self.rotacao_max
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar:
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_imagem < self.tempo_animacao * 2:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao * 3:
            self.imagem = self.imgs[2]
        elif self.contagem_imagem < self.tempo_animacao * 4:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem >= ( (self.tempo_animacao * 4) + 1):
            self.imagem = self.imgs[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo eu não vou bater assa:
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_imagem = self.tempo_animacao * 2

        # desenhar a imagem:
        imagem_rotacionada = pg.transform.rotate(self.imagem, self.angulo)
        posi_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posi_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        pg.mask.from_surface(self.imagem)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pg.transform.flip(img_cano, False, True)
        self.cano_base = img_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pg.mask.from_surface(self.cano_topo)
        base_mask = pg.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        base_topo = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or base_topo:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = img_chao.get_height()
    imagem = img_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x2 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(img_fundo, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f'Pontuação: {pontos}', 1, (255, 255, 255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pg.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pg.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pg.time.Clock()

    while True:
        relogio.tick(45)
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                quit()
                break

        desenhar_tela(tela, passaros, canos, chao, pontos)