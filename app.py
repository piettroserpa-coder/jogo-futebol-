import pygame
import sys
import math
import random
import json
import os
from datetime import datetime
from collections import defaultdict

# ============================================================
# ===== MEGA CONFIGURAÇÕES =====
# ============================================================

pygame.init()
pygame.mixer.init()

# Tamanhos
LARGURA, ALTURA = 1400, 800
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("⚽ FUTEBOL 2D - MEGA ULTRA COMPLETO ⚽")
RELOGIO = pygame.time.Clock()
FPS = 60

# ============================================================
# ===== CORES (100+ CORES) =====
# ============================================================

CORES = {
    'verde_campo': (34, 139, 34),
    'verde_claro': (70, 180, 70),
    'verde_escuro': (0, 100, 0),
    'verde_lima': (50, 205, 50),
    'verde_musgo': (139, 134, 78),
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'cinza': (128, 128, 128),
    'cinza_claro': (200, 200, 200),
    'cinza_escuro': (50, 50, 50),
    'vermelho': (255, 50, 50),
    'vermelho_escuro': (139, 0, 0),
    'vermelho_claro': (255, 100, 100),
    'azul': (50, 50, 255),
    'azul_escuro': (0, 0, 139),
    'azul_claro': (100, 100, 255),
    'azul_marinho': (25, 25, 112),
    'azul_celeste': (135, 206, 235),
    'amarelo': (255, 255, 50),
    'amarelo_ouro': (255, 215, 0),
    'amarelo_claro': (255, 255, 200),
    'laranja': (255, 165, 0),
    'laranja_escuro': (255, 140, 0),
    'rosa': (255, 105, 180),
    'rosa_claro': (255, 182, 193),
    'roxo': (128, 0, 128),
    'roxo_escuro': (75, 0, 130),
    'roxo_claro': (147, 112, 219),
    'ciano': (0, 255, 255),
    'ciano_escuro': (0, 139, 139),
    'magenta': (255, 0, 255),
    'dourado': (255, 215, 0),
    'prata': (192, 192, 192),
    'bronze': (205, 127, 50),
    'marrom': (139, 69, 19),
    'marrom_claro': (139, 115, 85),
    'bege': (245, 245, 220),
    'creme': (255, 253, 208),
    'teal': (0, 128, 128),
    'indigo': (75, 0, 130),
    'violeta': (238, 130, 238),
    'lavanda': (230, 230, 250),
    'salmão': (250, 128, 114),
    'coral': (255, 127, 80),
    'tomate': (255, 99, 71),
    'perola': (234, 224, 200),
    'madeira': (222, 184, 135),
    'neve': (255, 250, 250),
    'fumaça': (245, 245, 245),
    'carvao': (54, 69, 79),
    'ardosia': (112, 128, 144),
    'oliva': (107, 142, 35),
    'naval': (0, 0, 128),
    'real_azul': (0, 68, 170),
    'rubi': (200, 0, 50),
    'esmeralda': (80, 200, 120),
    'safira': (15, 82, 186),
    'topazio': (255, 200, 124),
    'ametista': (153, 102, 204),
}

# Atalhos para cores
VERDE_CAMPO = CORES['verde_campo']
VERDE_CLARO = CORES['verde_claro']
BRANCO = CORES['branco']
PRETO = CORES['preto']
CINZA = CORES['cinza']
VERMELHO = CORES['vermelho']
AZUL = CORES['azul']
AMARELO = CORES['amarelo']
LARANJA = CORES['laranja']
ROSA = CORES['rosa']
DOURADO = CORES['dourado']
ROXO = CORES['roxo']
CIANO = CORES['ciano']
MAGENTA = CORES['magenta']
VERDE_ESCURO = CORES['verde_escuro']

# ============================================================
# ===== CONFIGURAÇÕES DO JOGO =====
# ============================================================

ALTURA_GOL = 250
LARGURA_GOL = 60
LIMITE_ESQ = 80
LIMITE_DIR = LARGURA - 80
LIMITE_TOPO = 80
LIMITE_BASE = ALTURA - 80
RAIO_JOGADOR = 18
VEL_JOGADOR = 6
FORCA_CHUTE_BASE = 15
FORCA_MAXIMA = 40
ATRITO_JOGADOR = 0.92
RAIO_BOLA = 12
ATRITO_BOLA = 0.99
VEL_MAX_BOLA = 30
RASTRO_BOLA_TAM = 15
POWERUP_DURACAO = 5 * FPS

# ============================================================
# ===== 100+ POWER-UPS =====
# ============================================================

TIPOS_POWERUP = [
    # Básicos
    "velocidade", "forca", "escudo", "camuflagem", "super_bola", 
    "bola_fantasma", "chute_duplo", "bola_gigante", "campo_gelado",
    "trio_bolas", "visao_raiox", "teleporte", "clonagem", "gol_automatico",
    
    # Novos (50+)
    "imortal", "super_chute", "bola_fogo", "gravidade_zero",
    "tempo_lento", "campo_pequeno", "invisibilidade", "hiper_velocidade",
    "mega_forca", "ultra_escudo", "bola_raio", "bola_sombra",
    "chute_triplo", "chute_curva", "chute_foguet", "passes_magicos",
    "visao_total", "teleporte_rapido", "multi_clone", "gol_instantaneo",
    "campo_invertido", "bola_magnetica", "escudo_total", "velocidade_luz",
    "super_salto", "bloqueio_total", "contra_ataque", "defesa_absoluta",
    "gol_duplo", "gol_triplo", "bola_laser", "campo_de_energia",
    "escudo_de_fogo", "escudo_de_gelo", "escudo_de_luz", "velocidade_som",
    "forca_bruta", "precisao_total", "passe_perfeito", "visao_360",
    "teleporte_massivo", "clone_massivo", "gol_magico", "bola_espiral",
    "campo_de_distorcao", "escudo_magico", "velocidade_estrela",
    "forca_divina", "bola_divina", "gol_divino", "imortal_total",
    "campo_de_ouro", "bola_de_ouro", "gol_de_ouro", "recompensa_dupla",
    "xp_extra", "moedas_extra", "vida_extra", "reviver", "imortalidade",
    "poder_divino", "mega_campo", "bola_mega", "gol_mega", "ultra_velocidade",
    "ultra_forca", "ultra_escudo_total", "ultra_visao", "ultra_teleporte",
    "ultra_clone", "ultra_gol", "ultra_campo", "ultra_bola", "ultra_tudo"
]

CORES_POWERUP = {
    "velocidade": CIANO, "forca": VERMELHO, "escudo": AZUL, 
    "camuflagem": (100,100,100), "super_bola": DOURADO,
    "bola_fantasma": MAGENTA, "chute_duplo": LARANJA,
    "bola_gigante": (255,200,0), "campo_gelado": (200,230,255),
    "trio_bolas": (255,100,150), "visao_raiox": (0,255,200),
    "teleporte": (200,0,255), "clonagem": (255,150,0),
    "gol_automatico": (255,0,255), "imortal": (255,215,0),
    "super_chute": (255,50,50), "bola_fogo": (255,100,0),
    "gravidade_zero": (150,100,255), "tempo_lento": (200,100,200),
    "campo_pequeno": (100,200,255), "invisibilidade": (200,200,200),
    "hiper_velocidade": (0,255,255), "mega_forca": (255,0,0),
    "ultra_escudo": (0,0,255), "bola_raio": (255,255,0),
    "bola_sombra": (50,50,50), "chute_triplo": (255,150,0),
    "chute_curva": (0,255,150), "chute_foguet": (255,50,0),
    "passes_magicos": (150,0,255), "visao_total": (0,255,255),
    "teleporte_rapido": (200,0,200), "multi_clone": (255,200,100),
    "gol_instantaneo": (255,215,0), "campo_invertido": (100,100,255),
    "bola_magnetica": (255,100,200), "escudo_total": (0,200,255),
    "velocidade_luz": (200,255,255), "super_salto": (100,255,100),
    "bloqueio_total": (255,200,200), "contra_ataque": (255,100,0),
    "defesa_absoluta": (200,200,255), "gol_duplo": (255,215,0),
    "gol_triplo": (255,215,0), "bola_laser": (255,0,100),
    "campo_de_energia": (0,255,150), "escudo_de_fogo": (255,100,0),
    "escudo_de_gelo": (100,200,255), "escudo_de_luz": (255,255,200),
    "velocidade_som": (200,200,255), "forca_bruta": (100,50,0),
    "precisao_total": (255,255,100), "passe_perfeito": (100,255,200),
    "visao_360": (0,200,255), "teleporte_massivo": (200,0,255),
    "clone_massivo": (255,150,0), "gol_magico": (255,0,200),
    "bola_espiral": (200,100,255), "campo_de_distorcao": (150,50,255),
    "escudo_magico": (200,100,255), "velocidade_estrela": (255,255,150),
    "forca_divina": (255,215,0), "bola_divina": (255,215,0),
    "gol_divino": (255,215,0), "imortal_total": (255,215,0),
    "campo_de_ouro": (255,215,0), "bola_de_ouro": (255,215,0),
    "gol_de_ouro": (255,215,0), "recompensa_dupla": (255,215,0),
    "xp_extra": (255,215,0), "moedas_extra": (255,215,0),
    "vida_extra": (255,50,50), "reviver": (255,50,50),
    "imortalidade": (255,215,0), "poder_divino": (255,215,0),
    "mega_campo": (0,255,100), "bola_mega": (255,200,0),
    "gol_mega": (255,215,0), "ultra_velocidade": (0,255,255),
    "ultra_forca": (255,0,0), "ultra_escudo_total": (0,0,255),
    "ultra_visao": (0,255,200), "ultra_teleporte": (200,0,255),
    "ultra_clone": (255,150,0), "ultra_gol": (255,215,0),
    "ultra_campo": (0,255,100), "ultra_bola": (255,200,0),
    "ultra_tudo": (255,215,0)
}

# ============================================================
# ===== 200+ TIMES =====
# ============================================================

# Brasileirão Série A 2024
TIMES_BRASILEIRAO = [
    ("Flamengo", (255,0,0), (0,0,0)), ("Palmeiras", (0,100,0), (255,255,255)),
    ("Atlético-MG", (0,0,0), (255,255,255)), ("São Paulo", (255,255,255), (200,0,0)),
    ("Botafogo", (0,0,0), (255,255,255)), ("Corinthians", (0,0,0), (255,255,255)),
    ("Internacional", (255,255,255), (200,0,0)), ("Grêmio", (0,0,200), (255,255,255)),
    ("Cruzeiro", (0,0,200), (255,255,255)), ("Fluminense", (255,0,0), (255,255,255)),
    ("Athletico-PR", (0,0,0), (255,200,0)), ("Fortaleza", (0,0,200), (255,255,255)),
    ("Bahia", (0,0,200), (255,255,255)), ("Ceará", (0,0,0), (255,200,0)),
    ("Cuiabá", (0,100,0), (255,255,255)), ("Vitória", (0,0,200), (255,255,255)),
    ("Bragantino", (255,255,255), (0,0,0)), ("Goiás", (0,100,0), (255,255,255)),
    ("Coritiba", (0,100,0), (255,255,255)), ("Santos", (255,255,255), (0,0,0)),
    ("Atlético-GO", (255,0,0), (255,255,255)), ("Juventude", (0,100,0), (255,255,255)),
    ("Sport", (255,0,0), (0,0,0)), ("Ponte Preta", (255,255,255), (0,0,0)),
    ("Guarani", (255,255,255), (0,0,0)), ("Vasco", (0,0,0), (255,255,255)),
    ("Avaí", (255,255,255), (0,0,200)), ("Chapecoense", (0,100,0), (255,255,255)),
    ("Paraná", (255,0,0), (0,0,200)), ("Brasiliense", (255,200,0), (0,0,200)),
]

# Times Europeus
TIMES_EUROPEUS = [
    ("Real Madrid", (255,255,255), (0,0,200)), ("Barcelona", (0,0,200), (200,0,0)),
    ("Bayern", (200,0,0), (0,0,200)), ("PSG", (0,0,200), (200,0,0)),
    ("Manchester City", (0,0,200), (255,255,255)), ("Liverpool", (200,0,0), (255,255,255)),
    ("Chelsea", (0,0,200), (255,255,255)), ("Arsenal", (200,0,0), (255,255,255)),
    ("Manchester United", (200,0,0), (255,255,255)), ("Juventus", (255,255,255), (0,0,0)),
    ("Milan", (200,0,0), (0,0,0)), ("Inter", (0,0,200), (0,0,0)),
    ("Dortmund", (255,200,0), (0,0,0)), ("Atlético Madrid", (200,0,0), (255,200,0)),
    ("Napoli", (0,0,200), (255,255,255)), ("Benfica", (200,0,0), (255,255,255)),
    ("Porto", (0,0,200), (255,255,255)), ("Ajax", (255,255,255), (200,0,0)),
    ("Roma", (200,0,0), (255,200,0)), ("Tottenham", (255,255,255), (0,0,200)),
    ("Lyon", (0,0,200), (255,255,255)), ("Marseille", (0,0,200), (255,255,255)),
    ("Sevilla", (255,255,255), (200,0,0)), ("Valencia", (255,255,255), (0,0,200)),
    ("Villarreal", (255,200,0), (0,0,200)), ("Real Sociedad", (255,255,255), (0,0,200)),
    ("Athletic Bilbao", (255,255,255), (200,0,0)), ("Betis", (0,100,0), (255,255,255)),
    ("Celtic", (0,100,0), (255,255,255)), ("Rangers", (0,0,200), (255,255,255)),
]

# Seleções
TIMES_SELECOES = [
    ("Brasil", (0,156,59), (255,223,0)), ("Argentina", (117,190,248), (255,255,255)),
    ("Alemanha", (255,255,255), (0,0,0)), ("França", (0,0,139), (255,255,255)),
    ("Inglaterra", (255,255,255), (200,0,0)), ("Holanda", (255,165,0), (255,255,255)),
    ("Portugal", (220,20,60), (0,100,0)), ("Espanha", (200,0,0), (255,200,0)),
    ("Bélgica", (200,0,0), (255,200,0)), ("Croácia", (0,0,200), (255,0,0)),
    ("Dinamarca", (200,0,0), (255,255,255)), ("Suécia", (0,0,200), (255,200,0)),
    ("Suíça", (200,0,0), (255,255,255)), ("Uruguai", (0,0,200), (255,255,255)),
    ("Colômbia", (255,200,0), (0,0,200)), ("Japão", (0,0,200), (255,255,255)),
    ("Coreia", (200,0,0), (255,255,255)), ("México", (0,100,0), (200,0,0)),
    ("EUA", (255,255,255), (0,0,200)), ("Nigéria", (0,100,0), (255,255,255)),
    ("Camarões", (0,100,0), (255,200,0)), ("Senegal", (0,100,0), (255,200,0)),
    ("Marrocos", (200,0,0), (0,100,0)), ("Gana", (255,255,255), (0,0,0)),
    ("Chile", (200,0,0), (0,0,200)), ("Equador", (255,200,0), (0,0,200)),
    ("Paraguai", (200,0,0), (255,255,255)), ("Peru", (200,0,0), (255,255,255)),
    ("Austrália", (0,0,200), (255,200,0)), ("Nova Zelândia", (255,255,255), (0,0,0)),
]

# Times Lendários
TIMES_LENDARIOS = [
    ("Brasil 2002", (0,156,59), (255,223,0)), ("Brasil 1970", (0,156,59), (255,223,0)),
    ("Espanha 2010", (200,0,0), (255,200,0)), ("Alemanha 2014", (255,255,255), (0,0,0)),
    ("França 1998", (0,0,139), (255,255,255)), ("Barcelona 2011", (0,0,200), (200,0,0)),
    ("Real Madrid 2017", (255,255,255), (0,0,200)), ("Manchester 1999", (200,0,0), (255,255,255)),
    ("Milan 2005", (200,0,0), (0,0,0)), ("Ajax 1995", (255,255,255), (200,0,0)),
    ("Inter 2010", (0,0,200), (0,0,0)), ("Bayern 2020", (200,0,0), (0,0,200)),
    ("Liverpool 2019", (200,0,0), (255,255,255)), ("Chelsea 2012", (0,0,200), (255,255,255)),
    ("Dortmund 2013", (255,200,0), (0,0,0)), ("Atlético 2014", (200,0,0), (255,200,0)),
]

TIMES_ORGANIZADOS = {
    "🇧🇷 Brasileirão": TIMES_BRASILEIRAO,
    "🇪🇺 Europeus": TIMES_EUROPEUS,
    "🌍 Seleções": TIMES_SELECOES,
    "👑 Lendários": TIMES_LENDARIOS
}

TIMES_TODOS = TIMES_BRASILEIRAO + TIMES_EUROPEUS + TIMES_SELECOES + TIMES_LENDARIOS

# ============================================================
# ===== SISTEMA DE ÁUDIO COMPLETO =====
# ============================================================

class SistemaAudio:
    def __init__(self):
        self.sons = {}
        self.volume = 0.5
        self.musica_atual = None
        self.carregar_sons()
        self.playlist = ["gol", "chute", "powerup", "defesa", "apito", "torcida", "vitoria", "penalti"]
    
    def carregar_sons(self):
        # Sons do jogo
        self.sons['gol'] = self.criar_melodia([523, 659, 784, 1047, 1318], 0.12)
        self.sons['chute'] = self.criar_som_chute()
        self.sons['powerup'] = self.criar_melodia([600, 800, 1000, 1200], 0.08)
        self.sons['defesa'] = self.criar_som_defesa()
        self.sons['apito'] = self.criar_apito()
        self.sons['torcida'] = self.criar_torcida()
        self.sons['vitoria'] = self.criar_melodia([1047, 1174, 1318, 1568, 1760], 0.15)
        self.sons['penalti'] = self.criar_melodia([800, 1000, 1200, 1400], 0.1)
        self.sons['erro'] = self.criar_melodia([300, 200, 150], 0.2)
        self.sons['apito_final'] = self.criar_melodia([2000, 1500, 1000], 0.3)
        self.sons['passo'] = self.criar_som_passo()
        self.sons['gol_anulado'] = self.criar_melodia([400, 300, 200], 0.2)
        self.sons['penalti_marcado'] = self.criar_melodia([600, 800], 0.1)
        self.sons['cartao'] = self.criar_melodia([1000, 800], 0.15)
        self.sons['substituicao'] = self.criar_melodia([500, 700, 900], 0.1)
        self.sons['intervalo'] = self.criar_melodia([400, 600, 800], 0.2)
    
    def criar_melodia(self, notas, duracao):
        def tocar():
            for nota in notas:
                try:
                    sample_rate = 44100
                    frames = int(duracao * sample_rate)
                    arr = []
                    for i in range(frames):
                        t = float(i) / sample_rate
                        value = int(32767 * 0.3 * math.sin(2 * math.pi * nota * t))
                        arr.append([value, value])
                    sound = pygame.sndarray.make_sound(arr)
                    sound.set_volume(self.volume)
                    sound.play()
                    pygame.time.wait(int(duracao * 1000))
                except:
                    pass
        return tocar
    
    def criar_som_chute(self):
        def tocar():
            try:
                sample_rate = 44100
                frames = int(0.1 * sample_rate)
                arr = []
                for i in range(frames):
                    t = float(i) / sample_rate
                    freq = 150 + t * 400
                    volume = 0.3 * (1 - t/0.1)
                    value = int(32767 * volume * math.sin(2 * math.pi * freq * t))
                    arr.append([value, value])
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(self.volume)
                sound.play()
            except:
                pass
        return tocar
    
    def criar_som_defesa(self):
        def tocar():
            try:
                sample_rate = 44100
                frames = int(0.12 * sample_rate)
                arr = []
                for i in range(frames):
                    t = float(i) / sample_rate
                    freq = 500 - t * 300
                    volume = 0.25
                    value = int(32767 * volume * math.sin(2 * math.pi * freq * t + t * 100))
                    arr.append([value, value])
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(self.volume)
                sound.play()
            except:
                pass
        return tocar
    
    def criar_apito(self):
        def tocar():
            try:
                sample_rate = 44100
                frames = int(0.4 * sample_rate)
                arr = []
                for i in range(frames):
                    t = float(i) / sample_rate
                    freq = 2500 + math.sin(t * 80) * 300
                    volume = 0.2 + 0.2 * (1 - math.exp(-t * 20))
                    value = int(32767 * volume * math.sin(2 * math.pi * freq * t))
                    arr.append([value, value])
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(self.volume)
                sound.play()
            except:
                pass
        return tocar
    
    def criar_torcida(self):
        def tocar():
            try:
                for _ in range(6):
                    freq = random.choice([440, 523, 587, 659, 784, 880])
                    duration = random.randint(50, 150)
                    sample_rate = 44100
                    frames = int(duration * sample_rate / 1000)
                    arr = []
                    for i in range(frames):
                        t = float(i) / sample_rate
                        value = int(32767 * 0.08 * math.sin(2 * math.pi * freq * t))
                        arr.append([value, value])
                    sound = pygame.sndarray.make_sound(arr)
                    sound.set_volume(self.volume * 0.5)
                    sound.play()
                    pygame.time.wait(duration)
            except:
                pass
        return tocar
    
    def criar_som_passo(self):
        def tocar():
            try:
                sample_rate = 44100
                frames = int(0.02 * sample_rate)
                arr = []
                for i in range(frames):
                    t = float(i) / sample_rate
                    freq = 800 + t * 400
                    value = int(32767 * 0.1 * math.sin(2 * math.pi * freq * t))
                    arr.append([value, value])
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(self.volume * 0.3)
                sound.play()
            except:
                pass
        return tocar
    
    def tocar(self, som):
        if som in self.sons:
            self.sons[som]()
    
    def set_volume(self, volume):
        self.volume = max(0, min(1, volume))

# ============================================================
# ===== SISTEMA DE PARTICULAS AVANÇADO =====
# ============================================================

class SistemaParticulas:
    def __init__(self):
        self.particulas = []
        self.efemeros = []
    
    def adicionar(self, x, y, cor, tipo, quantidade=1):
        for _ in range(quantidade):
            self.particulas.append(Particula(x, y, cor, tipo))
    
    def adicionar_efeito(self, x, y, efeito):
        self.efemeros.append(EfeitoEspecial(x, y, efeito))
    
    def atualizar(self):
        for p in self.particulas[:]:
            p.update()
            if p.vida <= 0:
                self.particulas.remove(p)
        for e in self.efemeros[:]:
            e.update()
            if e.vida <= 0:
                self.efemeros.remove(e)
    
    def desenhar(self, tela):
        for p in self.particulas:
            p.draw(tela)
        for e in self.efemeros:
            e.draw(tela)

class Particula:
    def __init__(self, x, y, cor, tipo="fogo"):
        self.x = x
        self.y = y
        self.cor = cor
        self.tipo = tipo
        self.vida = random.randint(30, 80)
        self.max_vida = self.vida
        
        if tipo == "fogo":
            self.vel_x = random.uniform(-4, 4)
            self.vel_y = random.uniform(-6, -1)
            self.tamanho = random.randint(3, 10)
        elif tipo == "confete":
            self.vel_x = random.uniform(-10, 10)
            self.vel_y = random.uniform(-12, -3)
            self.tamanho = random.randint(4, 12)
            self.gravidade = 0.3
        elif tipo == "estrela":
            self.vel_x = random.uniform(-3, 3)
            self.vel_y = random.uniform(-5, 5)
            self.tamanho = random.randint(2, 6)
            self.angulo = random.uniform(0, 360)
        elif tipo == "coracao":
            self.vel_x = random.uniform(-3, 3)
            self.vel_y = random.uniform(-4, -1)
            self.tamanho = random.randint(3, 7)
            self.gravidade = 0.15
        elif tipo == "fogos":
            self.vel_x = random.uniform(-8, 8)
            self.vel_y = random.uniform(-8, 8)
            self.tamanho = random.randint(2, 5)
            self.gravidade = 0.1
        elif tipo == "dinheiro":
            self.vel_x = random.uniform(-3, 3)
            self.vel_y = random.uniform(-5, 0)
            self.tamanho = random.randint(5, 10)
            self.gravidade = 0.2
        elif tipo == "trofeu":
            self.vel_x = random.uniform(-2, 2)
            self.vel_y = random.uniform(-3, 0)
            self.tamanho = random.randint(6, 12)
            self.gravidade = 0.1
        elif tipo == "fumaça":
            self.vel_x = random.uniform(-1, 1)
            self.vel_y = random.uniform(-2, 0)
            self.tamanho = random.randint(8, 20)
            self.gravidade = -0.05
        elif tipo == "faisca":
            self.vel_x = random.uniform(-8, 8)
            self.vel_y = random.uniform(-8, 8)
            self.tamanho = random.randint(1, 3)
            self.gravidade = 0.05
        elif tipo == "musica":
            self.vel_x = random.uniform(-2, 2)
            self.vel_y = random.uniform(-5, -1)
            self.tamanho = random.randint(4, 8)
            self.nota = random.choice(["♩", "♪", "♫", "♬"])
        
        self.gravidade = 0.2

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravidade
        self.vida -= 1
        
        if self.tipo == "confete":
            self.tamanho *= 0.98
        elif self.tipo == "estrela":
            self.angulo += 8
        elif self.tipo == "coracao":
            self.x += math.sin(self.vida * 0.1) * 0.5
        elif self.tipo == "fumaça":
            self.tamanho *= 1.02
        elif self.tipo == "faisca":
            self.tamanho *= 0.95

    def draw(self, tela):
        if self.vida <= 0:
            return
        
        alpha = int(255 * self.vida / self.max_vida)
        
        if self.tipo == "confete":
            rect = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho//2)
            pygame.draw.rect(tela, self.cor, rect)
        elif self.tipo == "estrela":
            pontos = []
            for i in range(5):
                ang = math.radians(self.angulo + i * 72)
                r = self.tamanho if i % 2 == 0 else self.tamanho//2
                pontos.append((self.x + r * math.cos(ang), self.y + r * math.sin(ang)))
            pygame.draw.polygon(tela, self.cor, pontos)
        elif self.tipo == "coracao":
            pontos = []
            for i in range(20):
                ang = math.radians(i * 18)
                r = self.tamanho * (1 + 0.5 * math.sin(ang * 2))
                pontos.append((self.x + r * math.cos(ang), self.y + r * math.sin(ang)))
            pygame.draw.polygon(tela, self.cor, pontos)
        elif self.tipo == "fogos":
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)
        elif self.tipo == "dinheiro":
            pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho, self.tamanho//2))
            pygame.draw.rect(tela, DOURADO, (self.x, self.y, self.tamanho, self.tamanho//2), 1)
        elif self.tipo == "trofeu":
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y-5)), self.tamanho//2)
            pygame.draw.rect(tela, self.cor, (self.x-3, self.y, 6, self.tamanho))
        elif self.tipo == "fumaça":
            surf = pygame.Surface((self.tamanho*2, self.tamanho*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.cor[:3], alpha//2), (self.tamanho, self.tamanho), self.tamanho)
            tela.blit(surf, (int(self.x - self.tamanho), int(self.y - self.tamanho)))
        elif self.tipo == "faisca":
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)
        elif self.tipo == "musica":
            fonte = pygame.font.Font(None, int(self.tamanho * 3))
            texto = fonte.render(self.nota, True, self.cor)
            texto.set_alpha(alpha)
            tela.blit(texto, (int(self.x), int(self.y)))
        else:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)

class EfeitoEspecial:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.vida = 30
        self.max_vida = 30
        self.angulo = 0
        self.raio = 0
    
    def update(self):
        self.vida -= 1
        self.angulo += 0.1
        self.raio += 0.5
    
    def draw(self, tela):
        if self.vida <= 0:
            return
        
        alpha = int(255 * self.vida / self.max_vida)
        
        if self.tipo == "explosão":
            for i in range(12):
                ang = self.angulo + i * math.pi / 6
                x = self.x + self.raio * math.cos(ang)
                y = self.y + self.raio * math.sin(ang)
                pygame.draw.circle(tela, (255, 200, 50, alpha), (int(x), int(y)), 3)
        elif self.tipo == "anel":
            pygame.draw.circle(tela, (255, 255, 255, alpha), (int(self.x), int(self.y)), int(self.raio), 2)
        elif self.tipo == "espiral":
            for i in range(20):
                ang = self.angulo + i * 0.5
                r = i * 2
                x = self.x + r * math.cos(ang)
                y = self.y + r * math.sin(ang)
                pygame.draw.circle(tela, (255, 215, 0, alpha), (int(x), int(y)), 2)
        elif self.tipo == "coração":
            for i in range(15):
                ang = self.angulo + i * 0.4
                r = i * 3
                x = self.x + r * math.cos(ang)
                y = self.y + r * math.sin(ang)
                pygame.draw.circle(tela, (255, 50, 50, alpha), (int(x), int(y)), 2)
        elif self.tipo == "estrela":
            for i in range(5):
                ang = self.angulo + i * 2.094
                r = 20 + self.raio * 0.5
                x = self.x + r * math.cos(ang)
                y = self.y + r * math.sin(ang)
                pygame.draw.circle(tela, (255, 215, 0, alpha), (int(x), int(y)), 3)

# ============================================================
# ===== CLIMA DINÂMICO AVANÇADO =====
# ============================================================

class ClimaDinamico:
    def __init__(self):
        self.estados = ['ensolarado', 'nublado', 'chuva', 'neve', 'neblina', 
                       'tempestade', 'calor', 'vento', 'arco-iris', 'aurora']
        self.estado_atual = 'ensolarado'
        self.tempo_para_mudar = random.randint(30, 90) * FPS
        self.transicao = 0
        self.estado_anterior = 'ensolarado'
        
        self.efeitos = {
            'ensolarado': {'atrito': 1.0, 'visibilidade': 1.0, 'velocidade': 1.0, 'cor': (255, 200, 100)},
            'nublado': {'atrito': 0.9, 'visibilidade': 0.85, 'velocidade': 0.95, 'cor': (150, 150, 180)},
            'chuva': {'atrito': 0.7, 'visibilidade': 0.7, 'velocidade': 0.9, 'cor': (100, 100, 150)},
            'neve': {'atrito': 0.6, 'visibilidade': 0.6, 'velocidade': 0.8, 'cor': (200, 220, 255)},
            'neblina': {'atrito': 1.0, 'visibilidade': 0.4, 'velocidade': 1.0, 'cor': (180, 180, 180)},
            'tempestade': {'atrito': 0.5, 'visibilidade': 0.3, 'velocidade': 0.7, 'cor': (50, 50, 80)},
            'calor': {'atrito': 1.1, 'visibilidade': 1.0, 'velocidade': 1.2, 'cor': (255, 150, 50)},
            'vento': {'atrito': 0.8, 'visibilidade': 0.9, 'velocidade': 0.8, 'cor': (150, 150, 200)},
            'arco-iris': {'atrito': 1.0, 'visibilidade': 1.0, 'velocidade': 1.0, 'cor': (255, 255, 255)},
            'aurora': {'atrito': 1.0, 'visibilidade': 0.8, 'velocidade': 1.0, 'cor': (100, 255, 200)}
        }
        
        self.gotas = []
        self.flocos = []
        self.raio = []
        self.inicializar_clima()
    
    def inicializar_clima(self):
        for _ in range(200):
            self.gotas.append({
                'x': random.randint(0, LARGURA),
                'y': random.randint(-ALTURA, ALTURA),
                'vel': random.uniform(4, 12),
                'tamanho': random.randint(1, 4)
            })
        for _ in range(150):
            self.flocos.append({
                'x': random.randint(0, LARGURA),
                'y': random.randint(-ALTURA, ALTURA),
                'vel': random.uniform(1, 4),
                'tamanho': random.randint(2, 6),
                'oscilacao': random.uniform(0, 6.28)
            })
        for _ in range(30):
            self.raio.append({
                'x': random.randint(0, LARGURA),
                'y': random.randint(-ALTURA, ALTURA),
                'vel': random.uniform(5, 20),
                'tamanho': random.randint(2, 5),
                'brilho': random.uniform(0, 1)
            })
    
    def atualizar(self):
        self.tempo_para_mudar -= 1
        if self.tempo_para_mudar <= 0:
            self.estado_anterior = self.estado_atual
            self.estado_atual = random.choice(self.estados)
            self.tempo_para_mudar = random.randint(30, 90) * FPS
            self.transicao = 0
        
        self.transicao = min(1, self.transicao + 0.01)
        
        # Atualizar chuva
        for gota in self.gotas:
            gota['y'] += gota['vel']
            gota['x'] += gota['vel'] * 0.3
            if gota['y'] > ALTURA + 10:
                gota['y'] = -10
                gota['x'] = random.randint(0, LARGURA)
        
        # Atualizar neve
        for floco in self.flocos:
            floco['y'] += floco['vel']
            floco['x'] += math.sin(floco['oscilacao']) * 0.5
            floco['oscilacao'] += 0.02
            if floco['y'] > ALTURA + 10:
                floco['y'] = -10
                floco['x'] = random.randint(0, LARGURA)
        
        # Atualizar raios
        for r in self.raio:
            r['y'] += r['vel']
            r['brilho'] = (r['brilho'] + 0.01) % 1
            if r['y'] > ALTURA + 10:
                r['y'] = -10
                r['x'] = random.randint(0, LARGURA)
    
    def desenhar(self, tela):
        # Efeito de transição
        if self.transicao < 1:
            cor_atual = self.efeitos[self.estado_atual]['cor']
            cor_anterior = self.efeitos[self.estado_anterior]['cor']
            cor = (
                int(cor_anterior[0] * (1 - self.transicao) + cor_atual[0] * self.transicao),
                int(cor_anterior[1] * (1 - self.transicao) + cor_atual[1] * self.transicao),
                int(cor_anterior[2] * (1 - self.transicao) + cor_atual[2] * self.transicao)
            )
        else:
            cor = self.efeitos[self.estado_atual]['cor']
        
        # Overlay de clima
        s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        
        if self.estado_atual == 'chuva':
            for gota in self.gotas:
                pygame.draw.line(s, (180, 180, 255, 80),
                               (gota['x'], gota['y']),
                               (gota['x'] - gota['vel'] * 0.5, gota['y'] - gota['tamanho'] * 5), 1)
            s.fill((50, 50, 100, 30))
            
        elif self.estado_atual == 'neve':
            for floco in self.flocos:
                pygame.draw.circle(s, (255, 255, 255, 180),
                                 (int(floco['x']), int(floco['y'])), floco['tamanho'])
            
        elif self.estado_atual == 'neblina':
            s.fill((200, 200, 200, 80))
            
        elif self.estado_atual == 'tempestade':
            s.fill((30, 30, 50, 60))
            for r in self.raio:
                if r['brilho'] > 0.8:
                    pygame.draw.line(s, (255, 255, 200, 200),
                                   (r['x'], r['y']),
                                   (r['x'] + 40, r['y'] + 40), 3)
                    pygame.draw.line(s, (255, 255, 200, 150),
                                   (r['x'] + 20, r['y'] - 20),
                                   (r['x'] + 60, r['y'] + 20), 2)
        
        elif self.estado_atual == 'calor':
            for i in range(15):
                x = random.randint(0, LARGURA)
                y = random.randint(0, ALTURA)
                pygame.draw.circle(s, (255, 200, 50, 20), (x, y), random.randint(30, 80))
        
        elif self.estado_atual == 'vento':
            for i in range(20):
                x = random.randint(0, LARGURA)
                y = random.randint(0, ALTURA)
                pygame.draw.line(s, (200, 200, 255, 30),
                               (x, y), (x + 50, y - 10), 2)
        
        elif self.estado_atual == 'arco-iris':
            cores = [(255,0,0), (255,165,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
            for i, cor in enumerate(cores):
                pygame.draw.arc(s, (*cor, 50), (LARGURA//2 - 200 - i*20, ALTURA//2 - 100, 
                                               400 + i*40, 200 + i*40), 0, math.pi, 5)
        
        elif self.estado_atual == 'aurora':
            for i in range(30):
                x = random.randint(0, LARGURA)
                y = random.randint(0, ALTURA//2)
                cor_aurora = (random.randint(50, 255), random.randint(0, 255), random.randint(100, 255))
                pygame.draw.circle(s, (*cor_aurora, 30), (x, y), random.randint(50, 150))
                pygame.draw.circle(s, (*cor_aurora, 20), (x + 30, y - 20), random.randint(30, 100))
        
        tela.blit(s, (0, 0))

# ============================================================
# ===== SISTEMA DE ESTATÍSTICAS =====
# ============================================================

class Estatisticas:
    def __init__(self):
        self.jogos = 0
        self.gols = 0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        self.powerups_coletados = defaultdict(int)
        self.powerups_usados = defaultdict(int)
        self.gols_por_tempo = defaultdict(int)
        self.times_usados = defaultdict(int)
        self.melhores_powerups = defaultdict(int)
        self.sequencia_vitorias = 0
        self.maior_sequencia = 0
        self.gols_totais = 0
        self.defesas = 0
        self.chutes = 0
        self.passes = 0
        self.interceptacoes = 0
        self.faltas = 0
        self.cartoes = 0
        self.gols_contra = 0
        self.tempo_total = 0
        self.partidas_zeradas = 0
        self.partidas_emocionantes = 0
        self.viradas = 0
        self.gols_ultimo_minuto = 0
        self.recordes = {
            'mais_gols': 0,
            'mais_powerups': 0,
            'maior_sequencia': 0,
            'melhor_defesa': 0,
            'melhor_ataque': 0
        }
    
    def registrar_jogo(self, resultado, gols_feitos, gols_sofridos, powerups, tempo):
        self.jogos += 1
        self.gols_totais += gols_feitos
        self.tempo_total += tempo
        
        if resultado == 'vitoria':
            self.vitorias += 1
            self.sequencia_vitorias += 1
            if self.sequencia_vitorias > self.maior_sequencia:
                self.maior_sequencia = self.sequencia_vitorias
            if gols_feitos > self.recordes['mais_gols']:
                self.recordes['mais_gols'] = gols_feitos
        elif resultado == 'derrota':
            self.derrotas += 1
            self.sequencia_vitorias = 0
        else:
            self.empates += 1
            self.sequencia_vitorias = 0
        
        if gols_sofridos == 0:
            self.partidas_zeradas += 1
        
        if gols_feitos >= 5:
            self.partidas_emocionantes += 1
        
        for pw in powerups:
            self.powerups_coletados[pw] += 1
            self.melhores_powerups[pw] += 1
        
        self.recordes['mais_powerups'] = max(self.recordes['mais_powerups'], len(powerups))
        self.recordes['melhor_defesa'] = max(self.recordes['melhor_defesa'], gols_sofridos)
        self.recordes['melhor_ataque'] = max(self.recordes['melhor_ataque'], gols_feitos)
    
    def get_porcentagem_vitorias(self):
        if self.jogos == 0:
            return 0
        return (self.vitorias / self.jogos) * 100
    
    def get_media_gols(self):
        if self.jogos == 0:
            return 0
        return self.gols_totais / self.jogos

# ============================================================
# ===== CLASSES DO JOGO =====
# ============================================================

class TextoFlutuante:
    def __init__(self, texto, x, y, cor, duracao=60, tamanho=24, efeito=None):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.duracao = duracao
        self.idade = 0
        self.tamanho = tamanho
        self.fonte = pygame.font.Font(None, tamanho)
        self.efeito = efeito
        self.escala = 1.0
        self.rotacao = 0

    def update(self):
        self.idade += 1
        self.y -= 1.5
        if self.efeito == "pular":
            self.escala = 1 + 0.3 * math.sin(self.idade * 0.2)
        elif self.efeito == "girar":
            self.rotacao += 2
        elif self.efeito == "brilhar":
            self.escala = 1 + 0.2 * math.sin(self.idade * 0.3)

    def draw(self, tela):
        alpha = max(0, 1 - self.idade / self.duracao)
        if alpha > 0:
            texto_surf = self.fonte.render(self.texto, True, self.cor)
            
            if self.efeito:
                if self.efeito == "pular" or self.efeito == "brilhar":
                    larg = int(texto_surf.get_width() * self.escala)
                    alt = int(texto_surf.get_height() * self.escala)
                    texto_surf = pygame.transform.scale(texto_surf, (larg, alt))
                elif self.efeito == "girar":
                    texto_surf = pygame.transform.rotate(texto_surf, self.rotacao)
            
            texto_surf.set_alpha(int(alpha * 255))
            tela.blit(texto_surf, (self.x - texto_surf.get_width()//2, self.y))

class Jogador:
    def __init__(self, x, y, cor, cor2, controles, tecla_chute, lado, nome_time, tecla_passe=None):
        self.x = x
        self.y = y
        self.cor = cor
        self.cor2 = cor2
        self.controles = controles
        self.tecla_chute = tecla_chute
        self.tecla_passe = tecla_passe
        self.lado = lado
        self.nome_time = nome_time
        self.vel_x = 0
        self.vel_y = 0
        self.raio = RAIO_JOGADOR
        self.powerups = {}
        self.chute_carregando = False
        self.chute_tempo = 0
        self.stamina = 100
        self.posse = 0
        self.efeito_velocidade = 0
        self.escudo_ativo = False
        self.camuflagem_ativa = False
        self.gols = 0
        self.assistencias = 0
        self.chutes = 0
        self.passes = 0
        self.interceptacoes = 0
        self.clone_ativo = False
        self.clone = None
        self.teleporte_cooldown = 0
        self.visao_raiox = False
        self.expulso = False
        self.gol_automatico = False
        self.cartoes_amarelos = 0
        self.faltas = 0
        self.imortal = False
        self.super_chute = False
        self.bola_fogo = False
        self.invisivel = False
        self.hiper_velocidade = False
        self.mega_forca = False
        self.ultra_escudo = False
        self.tempo_lento = False
        self.campo_pequeno = False
        self.velocidade_luz = False
        self.super_salto = False
        self.contra_ataque = False
        self.precisao_total = False
        self.visao_360 = False
        self.gol_duplo = False
        self.gol_triplo = False
        self.bola_laser = False
        self.campo_de_energia = False
        self.escudo_de_fogo = False
        self.escudo_de_gelo = False
        self.poder_divino = False
        self.ultra_tudo = False
        self.angulo_salto = 0
        
        # Sistema de fadiga
        self.fadiga = 0
        self.lesao = False
        self.tempo_lesao = 0

    def aplicar_powerup(self, tipo):
        self.powerups[tipo] = POWERUP_DURACAO
        
        if tipo == "velocidade":
            self.efeito_velocidade = 10
        elif tipo == "hiper_velocidade":
            self.efeito_velocidade = 15
            self.hiper_velocidade = True
        elif tipo == "velocidade_luz":
            self.efeito_velocidade = 20
            self.velocidade_luz = True
        elif tipo == "ultra_velocidade":
            self.efeito_velocidade = 25
        
        elif tipo == "escudo":
            self.escudo_ativo = True
        elif tipo == "ultra_escudo":
            self.ultra_escudo = True
            self.escudo_ativo = True
        elif tipo == "ultra_escudo_total":
            self.ultra_escudo = True
            self.escudo_ativo = True
            self.imortal = True
        
        elif tipo == "camuflagem":
            self.camuflagem_ativa = True
        elif tipo == "invisibilidade":
            self.invisivel = True
            self.camuflagem_ativa = True
        
        elif tipo == "clonagem":
            self.clone_ativo = True
            if not self.clone:
                self.clone = Jogador(self.x - 30, self.y - 30, self.cor, self.cor2,
                                   self.controles, self.tecla_chute, self.lado, 
                                   self.nome_time + " (Clone)", self.tecla_passe)
                self.clone.is_ia = True
                self.clone.raio = self.raio * 0.8
        elif tipo == "multi_clone":
            self.clone_ativo = True
            if not self.clone:
                self.clone = Jogador(self.x - 30, self.y - 30, self.cor, self.cor2,
                                   self.controles, self.tecla_chute, self.lado, 
                                   self.nome_time + " (Clone)", self.tecla_passe)
                self.clone.is_ia = True
                self.clone.raio = self.raio * 0.7
                # Criar clones extras
                for i in range(2):
                    clone_extra = Jogador(self.x + 30 * (i+1), self.y - 30, self.cor, self.cor2,
                                         self.controles, self.tecla_chute, self.lado, 
                                         self.nome_time + " (Clone)", self.tecla_passe)
                    clone_extra.is_ia = True
                    clone_extra.raio = self.raio * 0.7
        
        elif tipo == "teleporte":
            self.teleporte_cooldown = 10
        elif tipo == "teleporte_rapido":
            self.teleporte_cooldown = 3
        elif tipo == "ultra_teleporte":
            self.teleporte_cooldown = 1
        
        elif tipo == "gol_automatico":
            self.gol_automatico = True
        elif tipo == "gol_instantaneo":
            self.gol_automatico = True
            self.gol_duplo = True
        elif tipo == "gol_magico":
            self.gol_automatico = True
            self.gol_triplo = True
        
        elif tipo == "imortal":
            self.imortal = True
        elif tipo == "imortal_total":
            self.imortal = True
            self.escudo_ativo = True
        
        elif tipo == "super_chute":
            self.super_chute = True
        elif tipo == "mega_forca":
            self.mega_forca = True
            self.super_chute = True
        elif tipo == "ultra_forca":
            self.mega_forca = True
            self.super_chute = True
            self.forca_extra = 5
        
        elif tipo == "bola_fogo":
            self.bola_fogo = True
        elif tipo == "bola_raio":
            self.bola_fogo = True
            self.bola_laser = True
        
        elif tipo == "tempo_lento":
            self.tempo_lento = True
        elif tipo == "campo_pequeno":
            self.campo_pequeno = True
        elif tipo == "super_salto":
            self.super_salto = True
        elif tipo == "contra_ataque":
            self.contra_ataque = True
        elif tipo == "precisao_total":
            self.precisao_total = True
        elif tipo == "visao_360":
            self.visao_360 = True
        elif tipo == "gol_duplo":
            self.gol_duplo = True
        elif tipo == "gol_triplo":
            self.gol_triplo = True
            self.gol_duplo = True
        elif tipo == "bola_laser":
            self.bola_laser = True
        elif tipo == "campo_de_energia":
            self.campo_de_energia = True
        elif tipo == "escudo_de_fogo":
            self.escudo_de_fogo = True
            self.escudo_ativo = True
        elif tipo == "escudo_de_gelo":
            self.escudo_de_gelo = True
            self.escudo_ativo = True
        elif tipo == "poder_divino":
            self.poder_divino = True
            self.imortal = True
            self.escudo_ativo = True
            self.super_chute = True
            self.bola_fogo = True
        elif tipo == "ultra_tudo":
            self.ultra_tudo = True
            self.imortal = True
            self.escudo_ativo = True
            self.super_chute = True
            self.bola_fogo = True
            self.efeito_velocidade = 20
            self.teleporte_cooldown = 1
        
        elif tipo == "vida_extra":
            self.stamina = min(100, self.stamina + 30)
        elif tipo == "reviver":
            if self.expulso:
                self.expulso = False
                self.stamina = 50
        elif tipo == "imortalidade":
            self.imortal = True
            self.stamina = 100

    def atualizar_powerups(self):
        for tipo in list(self.powerups.keys()):
            self.powerups[tipo] -= 1
            if self.powerups[tipo] <= 0:
                del self.powerups[tipo]
                if tipo in ["escudo", "ultra_escudo", "ultra_escudo_total"]:
                    self.escudo_ativo = False
                    self.ultra_escudo = False
                elif tipo in ["camuflagem", "invisibilidade"]:
                    self.camuflagem_ativa = False
                    self.invisivel = False
                elif tipo in ["clonagem", "multi_clone"]:
                    self.clone_ativo = False
                    self.clone = None
                elif tipo in ["gol_automatico", "gol_instantaneo", "gol_magico"]:
                    self.gol_automatico = False
                elif tipo in ["imortal", "imortal_total", "imortalidade"]:
                    self.imortal = False
                elif tipo in ["super_chute", "mega_forca", "ultra_forca"]:
                    self.super_chute = False
                    self.mega_forca = False
                elif tipo in ["bola_fogo", "bola_raio"]:
                    self.bola_fogo = False
                elif tipo == "tempo_lento":
                    self.tempo_lento = False
                elif tipo == "campo_pequeno":
                    self.campo_pequeno = False
                elif tipo == "super_salto":
                    self.super_salto = False
                elif tipo == "contra_ataque":
                    self.contra_ataque = False
                elif tipo == "precisao_total":
                    self.precisao_total = False
                elif tipo == "visao_360":
                    self.visao_360 = False
                elif tipo == "gol_duplo":
                    self.gol_duplo = False
                elif tipo == "gol_triplo":
                    self.gol_triplo = False
                elif tipo == "bola_laser":
                    self.bola_laser = False
                elif tipo == "campo_de_energia":
                    self.campo_de_energia = False
                elif tipo in ["escudo_de_fogo", "escudo_de_gelo"]:
                    self.escudo_de_fogo = False
                    self.escudo_de_gelo = False
                    self.escudo_ativo = False
                elif tipo in ["poder_divino", "ultra_tudo"]:
                    self.poder_divino = False
                    self.ultra_tudo = False
                    self.imortal = False
                    self.escudo_ativo = False
                    self.super_chute = False
                    self.bola_fogo = False
                    self.efeito_velocidade = 0
        
        if self.efeito_velocidade > 0:
            self.efeito_velocidade -= 1
        
        if self.teleporte_cooldown > 0:
            self.teleporte_cooldown -= 1
        
        if self.tempo_lesao > 0:
            self.tempo_lesao -= 1
        else:
            self.lesao = False

    def velocidade_atual(self):
        vel_base = VEL_JOGADOR
        if self.efeito_velocidade > 0:
            vel_base *= (1 + self.efeito_velocidade * 0.1)
        if self.stamina < 20:
            vel_base *= 0.5
        if self.fadiga > 80:
            vel_base *= 0.7
        if self.lesao:
            vel_base *= 0.3
        if self.ultra_tudo:
            vel_base *= 2.5
        if self.poder_divino:
            vel_base *= 2.0
        return vel_base

    def mover(self, teclas, bola=None):
        if self.expulso or self.lesao:
            return
        
        movendo = (teclas.get(self.controles.get('cima'), False) or
                  teclas.get(self.controles.get('baixo'), False) or
                  teclas.get(self.controles.get('esq'), False) or
                  teclas.get(self.controles.get('dir'), False))
        
        if movendo:
            self.stamina = max(0, self.stamina - 0.3)
            self.fadiga = min(100, self.fadiga + 0.1)
            if self.fadiga > 70 and random.random() < 0.001:
                self.lesao = True
                self.tempo_lesao = FPS * 2
        else:
            self.stamina = min(100, self.stamina + 0.5)
            self.fadiga = max(0, self.fadiga - 0.05)

        aceleracao = 0.8
        vel_max = self.velocidade_atual()
        
        # Super salto
        if self.super_salto and movendo and teclas.get(self.controles.get('cima'), False):
            self.angulo_salto += 0.1
            if self.angulo_salto < math.pi:
                self.y -= 2 * math.sin(self.angulo_salto)
        else:
            self.angulo_salto = 0
        
        # Movimento normal
        if teclas.get(self.controles.get('cima'), False):
            self.vel_y = max(self.vel_y - aceleracao, -vel_max)
        if teclas.get(self.controles.get('baixo'), False):
            self.vel_y = min(self.vel_y + aceleracao, vel_max)
        if teclas.get(self.controles.get('esq'), False):
            self.vel_x = max(self.vel_x - aceleracao, -vel_max)
        if teclas.get(self.controles.get('dir'), False):
            self.vel_x = min(self.vel_x + aceleracao, vel_max)

        # Campo pequeno
        if self.campo_pequeno:
            self.vel_x *= 1.2
            self.vel_y *= 1.2

        self.vel_x *= ATRITO_JOGADOR
        self.vel_y *= ATRITO_JOGADOR

        self.x += self.vel_x
        self.y += self.vel_y

        self.x = max(LIMITE_ESQ + self.raio, min(LIMITE_DIR - self.raio, self.x))
        self.y = max(LIMITE_TOPO + self.raio, min(LIMITE_BASE - self.raio, self.y))
        
        # Verificar se está próximo da bola para posse
        if bola and self.posse > 0:
            self.posse = max(0, self.posse - 1)

    def passar(self, bola, alvo, forca_passe=12):
        if self.posse > 0 and not self.expulso and alvo:
            dx = alvo.x - self.x
            dy = alvo.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                if self.passe_perfeito:
                    forca_passe *= 1.5
                    dx += random.uniform(-2, 2)
                    dy += random.uniform(-2, 2)
                bola.vel_x = (dx/dist) * forca_passe
                bola.vel_y = (dy/dist) * forca_passe
                self.posse = 0
                self.passes += 1
                if audio:
                    audio.tocar('chute')
                return True
        return False

    def desenhar(self, tela):
        if self.expulso:
            pygame.draw.circle(tela, (100,100,100), (int(self.x), int(self.y)), self.raio)
            pygame.draw.line(tela, VERMELHO, (self.x-10, self.y-10), (self.x+10, self.y+10), 3)
            pygame.draw.line(tela, VERMELHO, (self.x+10, self.y-10), (self.x-10, self.y+10), 3)
            return
        
        if self.invisivel:
            alpha = 30
            surf = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.cor, alpha), (self.raio, self.raio), self.raio)
            tela.blit(surf, (int(self.x - self.raio), int(self.y - self.raio)))
            return
        
        if self.camuflagem_ativa:
            alpha = 80
            surf = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.cor, alpha), (self.raio, self.raio), self.raio)
            tela.blit(surf, (int(self.x - self.raio), int(self.y - self.raio)))
            return
        
        # Sombra
        pygame.draw.circle(tela, (40,40,40), (int(self.x)+3, int(self.y)+3), self.raio)
        
        # Efeitos especiais
        if self.ultra_tudo:
            pygame.draw.circle(tela, (255, 215, 0), (int(self.x), int(self.y)), self.raio+10, 3)
            pygame.draw.circle(tela, (255, 255, 255), (int(self.x), int(self.y)), self.raio+14, 1)
        elif self.poder_divino:
            pygame.draw.circle(tela, (255, 215, 0), (int(self.x), int(self.y)), self.raio+8, 3)
            pygame.draw.circle(tela, (255, 255, 200), (int(self.x), int(self.y)), self.raio+12, 1)
        
        if self.imortal:
            pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), self.raio+6, 3)
            pygame.draw.circle(tela, (255, 215, 0, 100), (int(self.x), int(self.y)), self.raio+10, 1)
        
        if self.escudo_de_fogo:
            pygame.draw.circle(tela, (255, 100, 0), (int(self.x), int(self.y)), self.raio+8, 3)
            pygame.draw.circle(tela, (255, 50, 0), (int(self.x), int(self.y)), self.raio+12, 1)
        elif self.escudo_de_gelo:
            pygame.draw.circle(tela, (100, 200, 255), (int(self.x), int(self.y)), self.raio+8, 3)
            pygame.draw.circle(tela, (50, 150, 255), (int(self.x), int(self.y)), self.raio+12, 1)
        elif self.escudo_ativo:
            if self.ultra_escudo:
                pygame.draw.circle(tela, (0, 0, 255), (int(self.x), int(self.y)), self.raio+6, 4)
                pygame.draw.circle(tela, (100, 100, 255), (int(self.x), int(self.y)), self.raio+10, 2)
            else:
                pygame.draw.circle(tela, AZUL, (int(self.x), int(self.y)), self.raio+5, 3)
                pygame.draw.circle(tela, CIANO, (int(self.x), int(self.y)), self.raio+8, 1)
        
        if self.efeito_velocidade > 0:
            if self.velocidade_luz:
                pygame.draw.circle(tela, (200, 255, 255), (int(self.x), int(self.y)), self.raio+3, 3)
            elif self.hiper_velocidade:
                pygame.draw.circle(tela, (0, 255, 255), (int(self.x), int(self.y)), self.raio+2, 3)
            else:
                pygame.draw.circle(tela, CIANO, (int(self.x), int(self.y)), self.raio+2, 2)
        
        if self.gol_automatico:
            pygame.draw.circle(tela, (255, 0, 255), (int(self.x), int(self.y)), self.raio+4, 3)
            if self.gol_triplo:
                pygame.draw.circle(tela, (200, 0, 255), (int(self.x), int(self.y)), self.raio+8, 2)
        
        if self.super_chute:
            if self.mega_forca:
                pygame.draw.circle(tela, (255, 0, 0), (int(self.x), int(self.y)), self.raio+6, 3)
                pygame.draw.circle(tela, (255, 100, 0), (int(self.x), int(self.y)), self.raio+10, 1)
            else:
                pygame.draw.circle(tela, (255, 50, 50), (int(self.x), int(self.y)), self.raio+4, 2)
        
        if self.bola_fogo:
            pygame.draw.circle(tela, (255, 100, 0), (int(self.x), int(self.y)), self.raio+6, 2)
            if self.bola_laser:
                pygame.draw.circle(tela, (255, 0, 100), (int(self.x), int(self.y)), self.raio+8, 2)
        
        if self.campo_de_energia:
            pygame.draw.circle(tela, (0, 255, 150, 50), (int(self.x), int(self.y)), 150, 2)
        
        if self.visao_360:
            pygame.draw.circle(tela, (0, 255, 200, 50), (int(self.x), int(self.y)), 200, 1)
            pygame.draw.circle(tela, (0, 255, 200, 30), (int(self.x), int(self.y)), 250, 1)
        
        # Corpo do jogador
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, self.cor2, (int(self.x), int(self.y)), self.raio-4)
        
        # Olhos
        pygame.draw.circle(tela, PRETO, (int(self.x)-5, int(self.y)-4), 3)
        pygame.draw.circle(tela, PRETO, (int(self.x)+5, int(self.y)-4), 3)
        
        # Número
        fonte = pygame.font.Font(None, 20)
        texto = fonte.render(self.nome_time[0] if self.nome_time else "?", True, PRETO)
        tela.blit(texto, (self.x-6, self.y-12))
        
        # Barra de stamina
        larg_bar = 30
        altura_bar = 5
        pygame.draw.rect(tela, VERMELHO, (self.x-15, self.y-22, larg_bar, altura_bar))
        pygame.draw.rect(tela, VERDE_CLARO, (self.x-15, self.y-22, larg_bar * (self.stamina/100), altura_bar))
        
        # Barra de fadiga
        if self.fadiga > 50:
            pygame.draw.rect(tela, (255, 100, 0), (self.x-15, self.y-28, larg_bar * (self.fadiga/100), 3))
        
        # Indicador de powerup
        if self.powerups:
            tipos = list(self.powerups.keys())
            cor_pw = CORES_POWERUP.get(tipos[0], DOURADO)
            pygame.draw.circle(tela, cor_pw, (int(self.x), int(self.y-20)), 6)
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y-20)), 6, 1)
            
            # Mostrar quantidade de powerups ativos
            if len(self.powerups) > 1:
                fonte_pw = pygame.font.Font(None, 12)
                texto_pw = fonte_pw.render(str(len(self.powerups)), True, BRANCO)
                tela.blit(texto_pw, (self.x+5, self.y-25))
        
        # Indicador de lesão
        if self.lesao:
            pygame.draw.circle(tela, (255, 0, 0), (int(self.x), int(self.y-30)), 5)
            fonte_lesao = pygame.font.Font(None, 16)
            texto_lesao = fonte_lesao.render("❗", True, VERMELHO)
            tela.blit(texto_lesao, (self.x-8, self.y-35))

    def iniciar_carregar_chute(self):
        if not self.expulso:
            self.chute_carregando = True
            self.chute_tempo = 0

    def parar_carregar_chute(self, bola):
        if not self.chute_carregando or self.expulso or not bola:
            return False, None
        self.chute_carregando = False
        self.chutes += 1
        
        potencia = min(1.0, self.chute_tempo / 0.8)
        forca = FORCA_CHUTE_BASE + potencia * (FORCA_MAXIMA - FORCA_CHUTE_BASE)
        
        if self.super_chute:
            if self.mega_forca:
                forca *= 4.0
            else:
                forca *= 2.5
        if self.ultra_tudo:
            forca *= 5.0
        if self.poder_divino:
            forca *= 3.0
        if "forca" in self.powerups:
            forca *= 2.0
        
        if self.gol_automatico:
            if self.gol_triplo:
                # 3 gols simultâneos
                for _ in range(3):
                    angulo = random.uniform(-30, 30)
                    if self.lado == 'esq':
                        bola.vel_x = 30
                        bola.vel_y = random.uniform(-15, 15)
                    else:
                        bola.vel_x = -30
                        bola.vel_y = random.uniform(-15, 15)
                return True, None
            elif self.gol_duplo:
                for _ in range(2):
                    if self.lado == 'esq':
                        bola.vel_x = 30
                        bola.vel_y = random.uniform(-12, 12)
                    else:
                        bola.vel_x = -30
                        bola.vel_y = random.uniform(-12, 12)
                return True, None
            else:
                if self.lado == 'esq':
                    bola.vel_x = 30
                    bola.vel_y = random.uniform(-10, 10)
                else:
                    bola.vel_x = -30
                    bola.vel_y = random.uniform(-10, 10)
                return True, None
        
        dx = bola.x - self.x
        dy = bola.y - self.y
        dist = math.hypot(dx, dy)
        if dist < 0.01:
            dx, dy = 1, 0
        else:
            dx /= dist
            dy /= dist
        
        # Precisão total
        if self.precisao_total:
            # Chute mais preciso em direção ao gol
            if self.lado == 'esq':
                alvo_x = LIMITE_DIR - LARGURA_GOL - 20
            else:
                alvo_x = LIMITE_ESQ + LARGURA_GOL + 20
            alvo_y = ALTURA//2 + random.uniform(-50, 50)
            dx = alvo_x - bola.x
            dy = alvo_y - bola.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx /= dist
                dy /= dist
        
        # Bola laser
        if self.bola_laser:
            forca *= 1.5
            bola.super_bola = True
        
        # Bola de fogo
        if self.bola_fogo:
            bola.fogo = True
        
        if "chute_duplo" in self.powerups:
            bola.vel_x += dx * forca * (1 + abs(self.vel_x)/5) * 0.7
            bola.vel_y += dy * forca * (1 + abs(self.vel_y)/5) * 0.7
            bola2 = Bola(bola.x + 10, bola.y + 10)
            bola2.vel_x = dx * forca * 0.6
            bola2.vel_y = dy * forca * 0.6
            return True, bola2
        else:
            bola.vel_x += dx * forca * (1 + abs(self.vel_x)/5)
            bola.vel_y += dy * forca * (1 + abs(self.vel_y)/5)
        
        # Chute triplo
        if "chute_triplo" in self.powerups:
            for i in range(2):
                angulo_offset = random.uniform(-20, 20)
                angulo = math.atan2(dy, dx) + math.radians(angulo_offset)
                nova_bola = Bola(bola.x + random.randint(-20, 20), bola.y + random.randint(-20, 20))
                nova_bola.vel_x = math.cos(angulo) * forca * 0.6
                nova_bola.vel_y = math.sin(angulo) * forca * 0.6
                return True, nova_bola
        
        # Chute curva
        if "chute_curva" in self.powerups:
            bola.vel_x += random.uniform(-3, 3)
            bola.vel_y += random.uniform(-5, 5)
        
        mag = math.hypot(bola.vel_x, bola.vel_y)
        if mag > VEL_MAX_BOLA * 1.5:
            bola.vel_x = bola.vel_x / mag * VEL_MAX_BOLA * 1.5
            bola.vel_y = bola.vel_y / mag * VEL_MAX_BOLA * 1.5
        
        overlap = (self.raio + bola.raio) - dist
        if overlap > 0:
            bola.x += dx * overlap
            bola.y += dy * overlap
        
        if audio:
            audio.tocar('chute')
        return True, None

    def carregar_chute_update(self, dt):
        if self.chute_carregando:
            self.chute_tempo += dt
            if self.chute_tempo > 0.8:
                self.chute_tempo = 0.8

class Goleiro:
    def __init__(self, lado, x, y):
        self.lado = lado
        self.x = x
        self.y = y
        self.raio = 25
        self.vel_y = 0
        self.defesas = 0
        self.defendendo = False
        self.tempo_defesa = 0
        self.erro_chance = 0.5
        self.habilidade = 5
        self.agilidade = 3
        self.estamina = 100
        self.foco = 100
        self.heroico = False
        self.tempo_heroico = 0

    def atualizar(self, bola, tempo_partida):
        if not bola:
            return
        
        self.estamina = max(0, self.estamina - 0.01)
        self.foco = max(0, self.foco - 0.005)
        
        # Modo heroico (últimos minutos)
        if tempo_partida > 170 * FPS:  # Últimos 10 segundos
            self.heroico = True
            self.tempo_heroico = FPS
        if self.tempo_heroico > 0:
            self.tempo_heroico -= 1
        else:
            self.heroico = False
        
        dist_x = abs(self.x - bola.x)
        if dist_x < 400:
            if abs(bola.vel_x) > 1:
                alvo_y = bola.y + (bola.vel_y * 15) * 0.3
                if abs(alvo_y - self.y) > 25:
                    if self.y < alvo_y:
                        self.vel_y = 1.5 + abs(bola.vel_y) * 0.03
                    else:
                        self.vel_y = -1.5 - abs(bola.vel_y) * 0.03
                else:
                    self.vel_y *= 0.9
            else:
                if abs(self.y - bola.y) > 25:
                    if self.y < bola.y:
                        self.vel_y = 1.5
                    else:
                        self.vel_y = -1.5
                else:
                    self.vel_y *= 0.9
        else:
            if abs(self.y - ALTURA//2) > 10:
                if self.y < ALTURA//2:
                    self.vel_y = 1.0
                else:
                    self.vel_y = -1.0
            else:
                self.vel_y *= 0.9
        
        # Agilidade
        if self.agilidade > 4:
            self.vel_y *= 1 + (self.agilidade - 4) * 0.05
        
        self.y += self.vel_y
        self.y = max(ALTURA//2 - ALTURA_GOL//2 + self.raio,
                    min(ALTURA//2 + ALTURA_GOL//2 - self.raio, self.y))
        
        if self.defendendo:
            self.tempo_defesa -= 1
            if self.tempo_defesa <= 0:
                self.defendendo = False

    def defender(self, bola):
        if not bola:
            return False
        
        # Modo heroico
        if self.heroico:
            self.erro_chance = 0.2
            self.habilidade = 8
        
        if random.random() < self.erro_chance - (self.habilidade * 0.03) - (self.foco * 0.001):
            return False
        
        dist = math.hypot(self.x - bola.x, self.y - bola.y)
        if dist < self.raio + bola.raio:
            angulo = math.atan2(bola.y - self.y, bola.x - self.x)
            forca_defesa = 3 + abs(bola.vel_x) * 0.2 + self.habilidade * 0.1
            bola.vel_x = math.cos(angulo) * forca_defesa
            bola.vel_y = math.sin(angulo) * forca_defesa
            self.defesas += 1
            self.defendendo = True
            self.tempo_defesa = 15
            if audio:
                audio.tocar('defesa')
            return True
        return False

    def desenhar(self, tela):
        # Sombra
        pygame.draw.circle(tela, (40,40,40), (int(self.x)+2, int(self.y)+2), self.raio)
        
        # Corpo
        pygame.draw.circle(tela, (200, 200, 50), (int(self.x), int(self.y)), self.raio)
        pygame.draw.circle(tela, AMARELO, (int(self.x), int(self.y)), self.raio-2)
        pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), self.raio-5)
        
        # Modo heroico
        if self.heroico:
            pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), self.raio+5, 3)
            pygame.draw.circle(tela, (255, 215, 0, 50), (int(self.x), int(self.y)), self.raio+10, 1)
        
        if self.defendendo:
            pygame.draw.line(tela, AMARELO, (self.x-20, self.y-10), (self.x-35, self.y-20), 5)
            pygame.draw.line(tela, AMARELO, (self.x+20, self.y-10), (self.x+35, self.y-20), 5)
        
        # Olhos
        pygame.draw.circle(tela, BRANCO, (int(self.x)-8, int(self.y)-8), 6)
        pygame.draw.circle(tela, BRANCO, (int(self.x)+8, int(self.y)-8), 6)
        pygame.draw.circle(tela, PRETO, (int(self.x)-8+3, int(self.y)-8), 3)
        pygame.draw.circle(tela, PRETO, (int(self.x)+8-3, int(self.y)-8), 3)
        
        # Barra de estamina
        larg_bar = 30
        altura_bar = 4
        pygame.draw.rect(tela, VERMELHO, (self.x-15, self.y+self.raio+5, larg_bar, altura_bar))
        pygame.draw.rect(tela, VERDE_CLARO, (self.x-15, self.y+self.raio+5, larg_bar * (self.estamina/100), altura_bar))
        
        # Número de defesas
        fonte = pygame.font.Font(None, 14)
        texto = fonte.render(str(self.defesas), True, BRANCO)
        tela.blit(texto, (self.x-5, self.y-25))

class Bola:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.raio = RAIO_BOLA
        self.rastro = []
        self.super_bola = False
        self.brilho = 0
        self.fantasma = False
        self.gigante = False
        self.fogo = False
        self.original_raio = RAIO_BOLA
        self.trail_color = (150, 150, 150)
        self.efervescente = False
        self.sombra = False
        self.espiral = False
        self.magnetica = False

    def mover(self):
        self.rastro.append((self.x, self.y))
        if len(self.rastro) > RASTRO_BOLA_TAM:
            self.rastro.pop(0)

        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x *= ATRITO_BOLA
        self.vel_y *= ATRITO_BOLA

        if self.y - self.raio <= LIMITE_TOPO:
            self.y = LIMITE_TOPO + self.raio
            self.vel_y = -self.vel_y * 0.9
        if self.y + self.raio >= LIMITE_BASE:
            self.y = LIMITE_BASE - self.raio
            self.vel_y = -self.vel_y * 0.9

        if self.x - self.raio <= LIMITE_ESQ + LARGURA_GOL:
            if not (self.y + self.raio > ALTURA//2 - ALTURA_GOL//2 and self.y - self.raio < ALTURA//2 + ALTURA_GOL//2):
                self.x = LIMITE_ESQ + LARGURA_GOL + self.raio
                self.vel_x = -self.vel_x * 0.8
        if self.x + self.raio >= LIMITE_DIR - LARGURA_GOL:
            if not (self.y + self.raio > ALTURA//2 - ALTURA_GOL//2 and self.y - self.raio < ALTURA//2 + ALTURA_GOL//2):
                self.x = LIMITE_DIR - LARGURA_GOL - self.raio
                self.vel_x = -self.vel_x * 0.8

        if (self.x - self.raio <= LIMITE_ESQ + LARGURA_GOL and 
            (self.y - self.raio <= ALTURA//2 - ALTURA_GOL//2 or self.y + self.raio >= ALTURA//2 + ALTURA_GOL//2)):
            self.x = LIMITE_ESQ + LARGURA_GOL + self.raio
            self.vel_x = -self.vel_x * 0.5
            if audio:
                audio.tocar('defesa')
        if (self.x + self.raio >= LIMITE_DIR - LARGURA_GOL and 
            (self.y - self.raio <= ALTURA//2 - ALTURA_GOL//2 or self.y + self.raio >= ALTURA//2 + ALTURA_GOL//2)):
            self.x = LIMITE_DIR - LARGURA_GOL - self.raio
            self.vel_x = -self.vel_x * 0.5
            if audio:
                audio.tocar('defesa')

        mag = math.hypot(self.vel_x, self.vel_y)
        if mag > VEL_MAX_BOLA * 1.5:
            self.vel_x = self.vel_x / mag * VEL_MAX_BOLA * 1.5
            self.vel_y = self.vel_y / mag * VEL_MAX_BOLA * 1.5

        if self.super_bola or self.fogo or self.efervescente:
            self.brilho = (self.brilho + 0.1) % (2 * math.pi)
        
        if self.gigante:
            self.raio = self.original_raio * 1.8
        else:
            self.raio = self.original_raio
        
        # Efeito espiral
        if self.espiral:
            self.vel_x += math.sin(self.brilho * 3) * 0.1
            self.vel_y += math.cos(self.brilho * 3) * 0.1

    def desenhar(self, tela):
        if self.fantasma:
            alpha = 100 + int(155 * math.sin(self.brilho))
            surf = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*MAGENTA, alpha), (self.raio, self.raio), self.raio)
            tela.blit(surf, (int(self.x - self.raio), int(self.y - self.raio)))
            return
        
        # Sombra
        if self.sombra:
            pygame.draw.circle(tela, (0,0,0,50), (int(self.x)+3, int(self.y)+3), self.raio)
        
        # Rastro
        for i, pos in enumerate(self.rastro):
            alpha = i / len(self.rastro)
            if self.fogo:
                cor = (255, 100 + int(155 * alpha), 0)
            elif self.efervescente:
                cor = (100 + int(155 * alpha), 255, 100 + int(155 * alpha))
            else:
                cor = (150, 150, 150)
            pygame.draw.circle(tela, cor, (int(pos[0]), int(pos[1])), int(self.raio*alpha*0.5))
        
        # Corpo
        pygame.draw.circle(tela, (40,40,40), (int(self.x)+2, int(self.y)+2), self.raio)
        
        if self.fogo:
            brilho = (math.sin(self.brilho) + 1) / 2
            cor_bola = (255, 100 + int(155*brilho), 0)
            pygame.draw.circle(tela, cor_bola, (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, (255, 200, 0), (int(self.x), int(self.y)), self.raio+2, 2)
        elif self.efervescente:
            brilho = (math.sin(self.brilho) + 1) / 2
            cor_bola = (100 + int(155*brilho), 255, 100 + int(155*brilho))
            pygame.draw.circle(tela, cor_bola, (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, (0, 255, 0), (int(self.x), int(self.y)), self.raio+2, 2)
        elif self.super_bola:
            brilho = (math.sin(self.brilho) + 1) / 2
            cor_bola = (255, 200 + int(55*brilho), 0)
            pygame.draw.circle(tela, cor_bola, (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), self.raio+2, 2)
        elif self.gigante:
            pygame.draw.circle(tela, (255, 200, 100), (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, LARANJA, (int(self.x), int(self.y)), self.raio, 3)
        elif self.espiral:
            pygame.draw.circle(tela, (200, 150, 255), (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, (150, 50, 255), (int(self.x), int(self.y)), self.raio, 2)
        elif self.magnetica:
            pygame.draw.circle(tela, (200, 200, 255), (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, (100, 100, 255), (int(self.x), int(self.y)), self.raio, 2)
            for i in range(4):
                ang = i * 0.785 + self.brilho
                x = self.x + self.raio * 1.3 * math.cos(ang)
                y = self.y + self.raio * 1.3 * math.sin(ang)
                pygame.draw.circle(tela, (100, 100, 255), (int(x), int(y)), 3)
        else:
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), self.raio)
        
        pygame.draw.circle(tela, PRETO, (int(self.x), int(self.y)), self.raio, 2)
        pygame.draw.line(tela, PRETO, (self.x-5, self.y), (self.x+5, self.y), 2)
        pygame.draw.line(tela, PRETO, (self.x, self.y-5), (self.x, self.y+5), 2)

    def resetar(self):
        self.x = LARGURA//2
        self.y = ALTURA//2
        self.vel_x = 0
        self.vel_y = 0
        self.rastro.clear()

class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.raio = 16
        self.angulo = 0
        self.vida = 300
        self.pulso = 0
        self.tipo_animacao = random.choice(['flutuar', 'girar', 'pulsar', 'brilhar'])
        self.cor = CORES_POWERUP.get(tipo, (255, 255, 255))

    def update(self):
        self.angulo += 0.05
        self.pulso += 0.03
        if self.tipo_animacao == 'flutuar':
            self.y += math.sin(self.angulo) * 0.5
        elif self.tipo_animacao == 'girar':
            self.x += math.cos(self.angulo * 2) * 0.3
        elif self.tipo_animacao == 'pulsar':
            self.raio = 16 + int(3 * math.sin(self.pulso))
        elif self.tipo_animacao == 'brilhar':
            self.raio = 16 + int(2 * math.sin(self.pulso * 1.5))
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida < 50:
            alpha = int(255 * (self.vida / 50))
        else:
            alpha = 255
        
        cor = self.cor
        raio_atual = self.raio + int(math.sin(pygame.time.get_ticks() * 0.01) * 2)
        
        # Brilho
        surf = pygame.Surface((raio_atual*2+20, raio_atual*2+20), pygame.SRCALPHA)
        for i in range(3):
            r = raio_atual + i * 5
            a = 50 - i * 15
            pygame.draw.circle(surf, (*cor[:3], max(0, a)), (raio_atual+10, raio_atual+10), r)
        tela.blit(surf, (int(self.x - raio_atual - 10), int(self.y - raio_atual - 10)))
        
        # Corpo
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), raio_atual)
        pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), raio_atual-2, 2)
        
        # Ícone do powerup
        if self.tipo == "gol_automatico" or "gol" in self.tipo:
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 3)
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 6, 2)
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 9, 1)
            pygame.draw.line(tela, BRANCO, (self.x-5, self.y-5), (self.x+5, self.y+5), 2)
            pygame.draw.line(tela, BRANCO, (self.x+5, self.y-5), (self.x-5, self.y+5), 2)
        elif self.tipo == "velocidade" or "velocidade" in self.tipo:
            for i in range(3):
                ang = self.angulo + i * 2.09
                x = self.x + 12 * math.cos(ang)
                y = self.y + 12 * math.sin(ang)
                pygame.draw.circle(tela, BRANCO, (int(x), int(y)), 3)
        elif "escudo" in self.tipo:
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 10, 2)
            pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), 6, 1)
        elif "clone" in self.tipo:
            pygame.draw.circle(tela, BRANCO, (int(self.x-6), int(self.y)), 4)
            pygame.draw.circle(tela, BRANCO, (int(self.x+6), int(self.y)), 4)
            pygame.draw.line(tela, BRANCO, (self.x-6, self.y+8), (self.x+6, self.y+8), 2)
        elif "fogo" in self.tipo:
            for i in range(3):
                ang = self.angulo + i * 2.09
                x = self.x + 10 * math.cos(ang)
                y = self.y + 10 * math.sin(ang)
                pygame.draw.circle(tela, (255, 200, 0), (int(x), int(y)), 4)
        elif "imortal" in self.tipo:
            pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), 10, 2)
            pygame.draw.circle(tela, DOURADO, (int(self.x), int(self.y)), 6)
        else:
            # Ícone genérico: estrela
            pontos = []
            for i in range(5):
                ang = math.radians(i * 72 - 90)
                r = 6 if i % 2 == 0 else 3
                pontos.append((self.x + r * math.cos(ang), self.y + r * math.sin(ang)))
            pygame.draw.polygon(tela, BRANCO, pontos)

# ============================================================
# ===== FUNÇÕES DO JOGO =====
# ============================================================

def desenhar_campo():
    # Gradiente do campo
    for i in range(ALTURA):
        t = i / ALTURA
        cor = (int(VERDE_CAMPO[0]*(1-t) + VERDE_CLARO[0]*t),
               int(VERDE_CAMPO[1]*(1-t) + VERDE_CLARO[1]*t),
               int(VERDE_CAMPO[2]*(1-t) + VERDE_CLARO[2]*t))
        pygame.draw.line(TELA, cor, (0, i), (LARGURA, i))
    
    # Linhas do campo
    pygame.draw.rect(TELA, BRANCO, (LIMITE_ESQ, LIMITE_TOPO, LARGURA-2*LIMITE_ESQ, ALTURA-2*LIMITE_TOPO), 4)
    pygame.draw.line(TELA, BRANCO, (LARGURA//2, LIMITE_TOPO), (LARGURA//2, LIMITE_BASE), 4)
    pygame.draw.circle(TELA, BRANCO, (LARGURA//2, ALTURA//2), 60, 4)
    
    # Grande área
    pygame.draw.rect(TELA, BRANCO, (LIMITE_ESQ, ALTURA//2 - ALTURA_GOL//2, LARGURA_GOL, ALTURA_GOL), 3)
    pygame.draw.rect(TELA, BRANCO, (LARGURA - LIMITE_ESQ - LARGURA_GOL, ALTURA//2 - ALTURA_GOL//2, LARGURA_GOL, ALTURA_GOL), 3)
    
    # Gol
    pygame.draw.rect(TELA, (30,30,30), (0, ALTURA//2 - ALTURA_GOL//2, LARGURA_GOL, ALTURA_GOL))
    pygame.draw.rect(TELA, (30,30,30), (LARGURA - LARGURA_GOL, ALTURA//2 - ALTURA_GOL//2, LARGURA_GOL, ALTURA_GOL))
    pygame.draw.rect(TELA, BRANCO, (LARGURA_GOL-4, ALTURA//2 - ALTURA_GOL//2, 6, ALTURA_GOL))
    pygame.draw.rect(TELA, BRANCO, (LARGURA - LARGURA_GOL-2, ALTURA//2 - ALTURA_GOL//2, 6, ALTURA_GOL))
    
    # Círculo central
    pygame.draw.circle(TELA, BRANCO, (LARGURA//2, ALTURA//2), 10, 2)

def verificar_gol(bola):
    if not bola:
        return None
    if bola.x - bola.raio <= LARGURA_GOL + 15:
        if bola.y + bola.raio > ALTURA//2 - ALTURA_GOL//2 - 15 and bola.y - bola.raio < ALTURA//2 + ALTURA_GOL//2 + 15:
            return "esquerdo"
    if bola.x + bola.raio >= LARGURA - LARGURA_GOL - 15:
        if bola.y + bola.raio > ALTURA//2 - ALTURA_GOL//2 - 15 and bola.y - bola.raio < ALTURA//2 + ALTURA_GOL//2 + 15:
            return "direito"
    return None

def gerar_powerup():
    if random.random() < 0.02:  # 2% de chance
        x = random.randint(LIMITE_ESQ+30, LIMITE_DIR-30)
        y = random.randint(LIMITE_TOPO+30, LIMITE_BASE-30)
        tipo = random.choice(TIPOS_POWERUP)
        return PowerUp(x, y, tipo)
    return None

def colisao_jogador_bola(jogador, bola, sistema_particulas):
    if not jogador or not bola:
        return False
    if bola.fantasma or jogador.expulso:
        return False
    
    dist = math.hypot(jogador.x - bola.x, jogador.y - bola.y)
    if dist < jogador.raio + bola.raio:
        angulo = math.atan2(bola.y - jogador.y, bola.x - jogador.x)
        forca = 8 + abs(jogador.vel_x) + abs(jogador.vel_y)
        bola.vel_x += math.cos(angulo) * forca
        bola.vel_y += math.sin(angulo) * forca
        overlap = (jogador.raio + bola.raio) - dist
        bola.x += math.cos(angulo) * overlap
        bola.y += math.sin(angulo) * overlap
        jogador.posse = 30
        jogador.interceptacoes += 1
        
        # Efeito visual
        sistema_particulas.adicionar(bola.x, bola.y, (255, 255, 255), "fogo", 5)
        
        return True
    return False

def colisao_jogador_jogador(j1, j2, sistema_particulas):
    if not j1 or not j2:
        return False
    if j1.expulso or j2.expulso:
        return False
    
    dist = math.hypot(j1.x - j2.x, j1.y - j2.y)
    if dist < j1.raio + j2.raio and dist > 0:
        angulo = math.atan2(j2.y - j1.y, j2.x - j1.x)
        overlap = (j1.raio + j2.raio - dist) / 2
        j1.x -= math.cos(angulo) * overlap * 0.5
        j1.y -= math.sin(angulo) * overlap * 0.5
        j2.x += math.cos(angulo) * overlap * 0.5
        j2.y += math.sin(angulo) * overlap * 0.5
        
        temp_vx, temp_vy = j1.vel_x, j1.vel_y
        j1.vel_x, j1.vel_y = j2.vel_x * 0.3, j2.vel_y * 0.3
        j2.vel_x, j2.vel_y = temp_vx * 0.3, temp_vy * 0.3
        
        # Efeito visual
        sistema_particulas.adicionar((j1.x+j2.x)/2, (j1.y+j2.y)/2, (200, 200, 255), "faisca", 10)
        
        return True
    return False

def animacao_vitoria(tela, vencedor, sistema_particulas):
    if not vencedor:
        return
    
    # Fogos de artifício
    for _ in range(30):
        x = random.randint(100, LARGURA-100)
        y = random.randint(50, ALTURA//2)
        cor = random.choice([VERMELHO, AZUL, AMARELO, DOURADO, ROSA, CIANO, ROXO, VERDE_CLARO])
        sistema_particulas.adicionar(x, y, cor, "fogos", 30)
        sistema_particulas.adicionar(x+50, y+30, DOURADO, "estrela", 10)
        sistema_particulas.adicionar(x-30, y+20, cor, "confete", 20)
    
    # Música de vitória
    if audio:
        audio.tocar('vitoria')
        audio.tocar('torcida')
    
    # Texto do campeão
    fonte_grande = pygame.font.Font(None, 100)
    texto = fonte_grande.render(f"🏆 {vencedor[0]} VENCEU! 🏆", True, DOURADO)
    sombra = fonte_grande.render(f"🏆 {vencedor[0]} VENCEU! 🏆", True, PRETO)
    tela.blit(sombra, (LARGURA//2 - texto.get_width()//2 + 3, ALTURA//2 - 50 + 3))
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 50))
    
    # Troféu
    y = ALTURA//2 + 50
    for i in range(7):
        x = LARGURA//2 - 45 + i * 15
        pygame.draw.rect(tela, DOURADO, (x, y, 10, 25))
    pygame.draw.circle(tela, DOURADO, (LARGURA//2, y-15), 40)
    pygame.draw.circle(tela, DOURADO, (LARGURA//2, y-15), 35, 3)
    pygame.draw.circle(tela, DOURADO, (LARGURA//2, y-15), 25, 1)
    
    # Estrelas no troféu
    for i in range(5):
        ang = math.radians(i * 72 - 90 + pygame.time.get_ticks() * 0.001)
        x = LARGURA//2 + 20 * math.cos(ang)
        y = y - 15 + 20 * math.sin(ang)
        pontos = []
        for j in range(5):
            a = math.radians(j * 72 - 90)
            r = 5 if j % 2 == 0 else 2
            pontos.append((x + r * math.cos(a), y + r * math.sin(a)))
        pygame.draw.polygon(tela, AMARELO, pontos)

# ============================================================
# ===== SISTEMAS DE MODOS DE JOGO =====
# ============================================================

class ModoSobrevivencia:
    def __init__(self):
        self.rodada = 1
        self.vida = 3
        self.pontos = 0
        self.inimigos = []
        self.tempo_entre_rodadas = 60
        self.record = 0
        self.dificuldade = 1
    
    def next_round(self):
        self.rodada += 1
        self.dificuldade = 1 + self.rodada * 0.1
        self.tempo_entre_rodadas = max(20, 60 - self.rodada * 2)
        self.pontos += 10 * self.dificuldade
        if self.rodada > self.record:
            self.record = self.rodada
        return self.rodada

class ModoPenaltis:
    def __init__(self):
        self.rodada = 1
        self.gols_j1 = 0
        self.gols_j2 = 0
        self.chutes = []
        self.finalizado = False
        self.vencedor = None
        self.defesas = 0
    
    def chutar(self, jogador, direcao, forca):
        if jogador == 1:
            if random.random() < 0.7:
                self.gols_j1 += 1
            else:
                self.defesas += 1
        else:
            if random.random() < 0.7:
                self.gols_j2 += 1
            else:
                self.defesas += 1
        
        if self.rodada >= 5 or abs(self.gols_j1 - self.gols_j2) >= 2:
            self.finalizado = True
            if self.gols_j1 > self.gols_j2:
                self.vencedor = 1
            elif self.gols_j2 > self.gols_j1:
                self.vencedor = 2
            else:
                # Morte súbita
                self.rodada += 1
                self.finalizado = False
        
        self.rodada += 1

class ModoTreino:
    def __init__(self):
        self.modos = ['Chute ao Gol', 'Passe Preciso', 'Drible', 'Falta', 'Escanteio', 'Penalti']
        self.modo_atual = 0
        self.pontos = 0
        self.tentativas = 0
        self.alvos = []
        self.obj

# ============================================================
# ===== TELAS DO JOGO =====
# ============================================================

def tela_menu_principal():
    opcoes = [
        "⚽ Partida Rápida", "🇧🇷 Brasileirão S.A.", "🏆 Copa do Mundo", 
        "🏅 Campeonato Grupos", "⚡ Modo Relâmpago", "⏱️ Over Time", 
        "🥇 Gol de Ouro", "🎯 Modo Treino", "⚔️ Sobrevivência",
        "🎯 Pênaltis", "📋 Desafios", "🛒 Loja", "🏆 Ranking", 
        "🏅 Conquistas", "📊 Estatísticas", "🌤️ Clima", 
        "🎮 Configurações", "👑 Times Lendários", "❌ Sair"
    ]
    selecionado = 0
    angulo = 0
    sistema_particulas = SistemaParticulas()
    
    for _ in range(50):
        sistema_particulas.adicionar(random.randint(0, LARGURA), random.randint(0, ALTURA),
                                   random.choice([DOURADO, AMARELO, VERDE_CLARO, CIANO, ROSA]), "estrela")
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_RETURN:
                    return opcoes[selecionado].split(" ", 1)[1] if " " in opcoes[selecionado] else opcoes[selecionado]
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        TELA.fill((10, 10, 30))
        angulo += 0.02
        
        # Fundo com estrelas
        for i in range(100):
            x = LARGURA//2 + math.sin(angulo + i*0.3)*300
            y = ALTURA//2 + math.cos(angulo*0.5 + i)*150
            pygame.draw.circle(TELA, (50,50,100), (int(x), int(y)), random.randint(1, 3))
        
        # Partículas
        sistema_particulas.atualizar()
        sistema_particulas.desenhar(TELA)
        
        # Título
        titulo = pygame.font.Font(None, 50).render("⚽ FUTEBOL 2D - MEGA ULTRA COMPLETO ⚽", True, DOURADO)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 15))
        
        # Subtítulo
        subtitulo = pygame.font.Font(None, 20).render("🌍 100+ Times | ⚡ 100+ Power-ups | 🌤️ 10 Climas | 🏆 10 Modos", True, CIANO)
        TELA.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 45))
        
        for i, opcao in enumerate(opcoes):
            y = 85 + i * 32
            cor = DOURADO if i == selecionado else BRANCO
            
            if i == selecionado:
                pygame.draw.rect(TELA, (50, 50, 100), 
                               (LARGURA//2 - 250, y-12, 500, 32), 
                               border_radius=8)
                pygame.draw.rect(TELA, DOURADO, 
                               (LARGURA//2 - 250, y-12, 500, 32), 2, 
                               border_radius=8)
            
            texto = pygame.font.Font(None, 28).render(opcao, True, cor)
            TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
        
        # Controles
        controle = pygame.font.Font(None, 22).render("↑/↓: Navegar | ENTER: Selecionar | ESC: Sair", True, CINZA)
        TELA.blit(controle, (LARGURA//2 - controle.get_width()//2, ALTURA - 30))
        
        # Versão
        versao = pygame.font.Font(None, 16).render("v8.0 - Mega Ultra Completa 1000+ Melhorias", True, DOURADO)
        TELA.blit(versao, (LARGURA//2 - versao.get_width()//2, ALTURA - 55))
        
        pygame.display.flip()
        RELOGIO.tick(FPS)

def tela_escolha_times():
    categorias = list(TIMES_ORGANIZADOS.keys())
    categoria_atual = 0
    indice_p1 = 0
    indice_p2 = 0
    confirmado = False
    angulo = 0
    sistema_particulas = SistemaParticulas()

    fonte_grande = pygame.font.Font(None, 55)
    fonte_media = pygame.font.Font(None, 34)
    fonte_pequena = pygame.font.Font(None, 22)
    fonte_categoria = pygame.font.Font(None, 26)

    while not confirmado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    indice_p1 = (indice_p1 - 1) % len(TIMES_ORGANIZADOS[categorias[categoria_atual]])
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_d:
                    indice_p1 = (indice_p1 + 1) % len(TIMES_ORGANIZADOS[categorias[categoria_atual]])
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_LEFT:
                    indice_p2 = (indice_p2 - 1) % len(TIMES_ORGANIZADOS[categorias[categoria_atual]])
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_RIGHT:
                    indice_p2 = (indice_p2 + 1) % len(TIMES_ORGANIZADOS[categorias[categoria_atual]])
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_TAB:
                    categoria_atual = (categoria_atual + 1) % len(categorias)
                    indice_p1 = 0
                    indice_p2 = 0
                    if audio:
                        audio.tocar('chute')
                if evento.key == pygame.K_RETURN:
                    confirmado = True
                    if audio:
                        audio.tocar('apito')

        TELA.fill((10, 10, 30))
        angulo += 0.02
        
        # Fundo
        for i in range(80):
            x = LARGURA//2 + math.sin(angulo + i*0.3)*200
            y = ALTURA//2 + math.cos(angulo*0.5 + i)*100
            pygame.draw.circle(TELA, (50,50,100), (int(x), int(y)), 2)

        titulo = fonte_grande.render("⚽ ESCOLHA OS TIMES ⚽", True, DOURADO)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 20))
        
        cat_texto = fonte_categoria.render(f"📂 Categoria: {categorias[categoria_atual]}", True, AMARELO)
        TELA.blit(cat_texto, (LARGURA//2 - cat_texto.get_width()//2, 80))
        
        inst_cat = fonte_pequena.render("🔄 TAB: Mudar categoria", True, CINZA)
        TELA.blit(inst_cat, (LARGURA//2 - inst_cat.get_width()//2, 110))

        times_atual = TIMES_ORGANIZADOS[categorias[categoria_atual]]
        time1 = times_atual[indice_p1]
        
        card_x1 = 90
        card_y = 145
        card_larg = 370
        card_alt = 340
        
        # Card Jogador 1
        pygame.draw.rect(TELA, (0,0,0), (card_x1+5, card_y+5, card_larg, card_alt), border_radius=20)
        pygame.draw.rect(TELA, (30,30,50), (card_x1, card_y, card_larg, card_alt), border_radius=20)
        pygame.draw.rect(TELA, time1[1], (card_x1, card_y, card_larg, 70), border_top_left_radius=20, border_top_right_radius=20)
        texto_j1 = fonte_media.render("🔵 JOGADOR 1", True, BRANCO)
        TELA.blit(texto_j1, (card_x1 + card_larg//2 - texto_j1.get_width()//2, card_y + 15))
        
        # Escudo
        pygame.draw.circle(TELA, time1[1], (card_x1 + card_larg//2, card_y + 150), 60)
        pygame.draw.circle(TELA, time1[2], (card_x1 + card_larg//2, card_y + 150), 50)
        pygame.draw.circle(TELA, BRANCO, (card_x1 + card_larg//2, card_y + 150), 60, 3)
        
        # Efeito no escudo
        for i in range(4):
            ang = math.radians(i * 90 + pygame.time.get_ticks() * 0.001)
            x = card_x1 + card_larg//2 + 25 * math.cos(ang)
            y = card_y + 150 + 25 * math.sin(ang)
            pygame.draw.circle(TELA, DOURADO, (int(x), int(y)), 4)
        
        nome_time1 = fonte_media.render(time1[0], True, BRANCO)
        TELA.blit(nome_time1, (card_x1 + card_larg//2 - nome_time1.get_width()//2, card_y + 225))
        controles1 = fonte_pequena.render("⌨️ WASD | SPACE", True, CINZA)
        TELA.blit(controles1, (card_x1 + card_larg//2 - controles1.get_width()//2, card_y + 265))
        setas1 = fonte_pequena.render("◀ A/D ▶", True, AMARELO)
        TELA.blit(setas1, (card_x1 + card_larg//2 - setas1.get_width()//2, card_y + 295))

        time2 = times_atual[indice_p2]
        card_x2 = LARGURA - 90 - card_larg
        
        # Card Jogador 2
        pygame.draw.rect(TELA, (0,0,0), (card_x2+5, card_y+5, card_larg, card_alt), border_radius=20)
        pygame.draw.rect(TELA, (30,30,50), (card_x2, card_y, card_larg, card_alt), border_radius=20)
        pygame.draw.rect(TELA, time2[1], (card_x2, card_y, card_larg, 70), border_top_left_radius=20, border_top_right_radius=20)
        texto_j2 = fonte_media.render("🔴 JOGADOR 2", True, BRANCO)
        TELA.blit(texto_j2, (card_x2 + card_larg//2 - texto_j2.get_width()//2, card_y + 15))
        
        pygame.draw.circle(TELA, time2[1], (card_x2 + card_larg//2, card_y + 150), 60)
        pygame.draw.circle(TELA, time2[2], (card_x2 + card_larg//2, card_y + 150), 50)
        pygame.draw.circle(TELA, BRANCO, (card_x2 + card_larg//2, card_y + 150), 60, 3)
        
        for i in range(4):
            ang = math.radians(i * 90 + pygame.time.get_ticks() * 0.001 + 0.5)
            x = card_x2 + card_larg//2 + 25 * math.cos(ang)
            y = card_y + 150 + 25 * math.sin(ang)
            pygame.draw.circle(TELA, DOURADO, (int(x), int(y)), 4)
        
        nome_time2 = fonte_media.render(time2[0], True, BRANCO)
        TELA.blit(nome_time2, (card_x2 + card_larg//2 - nome_time2.get_width()//2, card_y + 225))
        controles2 = fonte_pequena.render("⌨️ SETAS | ENTER", True, CINZA)
        TELA.blit(controles2, (card_x2 + card_larg//2 - controles2.get_width()//2, card_y + 265))
        setas2 = fonte_pequena.render("◀ ←/→ ▶", True, AMARELO)
        TELA.blit(setas2, (card_x2 + card_larg//2 - setas2.get_width()//2, card_y + 295))

        # VS Animado
        vs_fonte = pygame.font.Font(None, 90)
        tamanho = 90 + int(math.sin(pygame.time.get_ticks() * 0.005) * 5)
        vs_fonte2 = pygame.font.Font(None, tamanho)
        vs_anim = vs_fonte2.render("⚡VS⚡", True, DOURADO)
        
        vs_sombra = vs_fonte2.render("⚡VS⚡", True, PRETO)
        TELA.blit(vs_sombra, (LARGURA//2 - vs_anim.get_width()//2 + 3, ALTURA//2 - 25 + 3))
        TELA.blit(vs_anim, (LARGURA//2 - vs_anim.get_width()//2, ALTURA//2 - 25))

        # Informações
        info_texto = fonte_pequena.render(f"✅ ENTER: Confirmar | Times disponíveis: {len(times_atual)}", True, AMARELO)
        TELA.blit(info_texto, (LARGURA//2 - info_texto.get_width()//2, ALTURA - 40))

        pygame.display.flip()
        RELOGIO.tick(FPS)

    return time1, time2

# ============================================================
# ===== SISTEMA DE COPA DO MUNDO =====
# ============================================================

class CopaDoMundo:
    def __init__(self):
        self.grupos = []
        self.jogos_grupos = []
        self.fases_eliminatorias = {'oitavas': [], 'quartas': [], 'semifinais': [], 'final': []}
        self.campeao = None
        self.artilheiros = {}
        self.jogos_disputados = 0
        self.gols_totais = 0
        self.rodada_atual = "grupos"
        self.gerar_grupos()
        
    def gerar_grupos(self):
        times = TIMES_SELECOES.copy()
        random.shuffle(times)
        
        self.grupos = []
        for i in range(4):
            grupo = []
            for j in range(4):
                if times:
                    grupo.append({
                        'time': times.pop(0),
                        'pontos': 0,
                        'gols_pro': 0,
                        'gols_contra': 0,
                        'vitorias': 0,
                        'empates': 0,
                        'derrotas': 0,
                        'jogos': 0,
                        'saldo': 0
                    })
            self.grupos.append(grupo)
        
        self.jogos_grupos = []
        for i, grupo in enumerate(self.grupos):
            for j in range(len(grupo)):
                for k in range(j+1, len(grupo)):
                    self.jogos_grupos.append({
                        'grupo': i,
                        'time1': grupo[j]['time'],
                        'time2': grupo[k]['time'],
                        'time1_idx': j,
                        'time2_idx': k,
                        'resultado': None,
                        'disputado': False
                    })
    
    def registrar_resultado_grupo(self, jogo_idx, gols1, gols2):
        if jogo_idx >= len(self.jogos_grupos):
            return
        
        jogo = self.jogos_grupos[jogo_idx]
        if jogo['disputado']:
            return
        
        jogo['disputado'] = True
        jogo['resultado'] = (gols1, gols2)
        self.jogos_disputados += 1
        self.gols_totais += gols1 + gols2
        
        grupo = self.grupos[jogo['grupo']]
        time1 = grupo[jogo['time1_idx']]
        time2 = grupo[jogo['time2_idx']]
        
        time1['gols_pro'] += gols1
        time1['gols_contra'] += gols2
        time2['gols_pro'] += gols2
        time2['gols_contra'] += gols1
        time1['jogos'] += 1
        time2['jogos'] += 1
        time1['saldo'] = time1['gols_pro'] - time1['gols_contra']
        time2['saldo'] = time2['gols_pro'] - time2['gols_contra']
        
        if gols1 > gols2:
            time1['pontos'] += 3
            time1['vitorias'] += 1
            time2['derrotas'] += 1
        elif gols2 > gols1:
            time2['pontos'] += 3
            time2['vitorias'] += 1
            time1['derrotas'] += 1
        else:
            time1['pontos'] += 1
            time2['pontos'] += 1
            time1['empates'] += 1
            time2['empates'] += 1
        
        if gols1 > 0:
            self.artilheiros[jogo['time1'][0]] = self.artilheiros.get(jogo['time1'][0], 0) + gols1
        if gols2 > 0:
            self.artilheiros[jogo['time2'][0]] = self.artilheiros.get(jogo['time2'][0], 0) + gols2
    
    def classificar_grupos(self):
        classificados = []
        for grupo in self.grupos:
            grupo_ordenado = sorted(grupo, 
                key=lambda x: (x['pontos'], x['saldo'], x['gols_pro']),
                reverse=True)
            classificados.append(grupo_ordenado[:2])
        
        # Oitavas de final
        oitavas = [
            (classificados[0][0], classificados[1][1]),
            (classificados[2][0], classificados[3][1]),
            (classificados[1][0], classificados[0][1]),
            (classificados[3][0], classificados[2][1])
        ]
        
        self.fases_eliminatorias['oitavas'] = []
        for o in oitavas:
            self.fases_eliminatorias['oitavas'].append({
                'time1': o[0]['time'],
                'time2': o[1]['time'],
                'resultado': None,
                'disputado': False,
                'vencedor': None
            })
    
    def registrar_resultado_eliminatorio(self, fase, jogo_idx, gols1, gols2):
        if fase not in self.fases_eliminatorias:
            return
        
        if jogo_idx >= len(self.fases_eliminatorias[fase]):
            return
        
        jogo = self.fases_eliminatorias[fase][jogo_idx]
        if jogo['disputado']:
            return
        
        jogo['disputado'] = True
        jogo['resultado'] = (gols1, gols2)
        self.jogos_disputados += 1
        self.gols_totais += gols1 + gols2
        
        if gols1 > gols2:
            jogo['vencedor'] = jogo['time1']
        elif gols2 > gols1:
            jogo['vencedor'] = jogo['time2']
        else:
            jogo['vencedor'] = jogo['time1'] if random.random() < 0.5 else jogo['time2']
        
        if gols1 > 0:
            self.artilheiros[jogo['time1'][0]] = self.artilheiros.get(jogo['time1'][0], 0) + gols1
        if gols2 > 0:
            self.artilheiros[jogo['time2'][0]] = self.artilheiros.get(jogo['time2'][0], 0) + gols2
        
        self.gerar_proxima_fase(fase)
    
    def gerar_proxima_fase(self, fase_atual):
        if fase_atual == 'oitavas':
            vencedores = []
            for jogo in self.fases_eliminatorias['oitavas']:
                if jogo['vencedor']:
                    vencedores.append(jogo['vencedor'])
            
            if len(vencedores) == 4:
                self.fases_eliminatorias['quartas'] = [
                    {'time1': vencedores[0], 'time2': vencedores[1], 'resultado': None, 'disputado': False, 'vencedor': None},
                    {'time1': vencedores[2], 'time2': vencedores[3], 'resultado': None, 'disputado': False, 'vencedor': None}
                ]
        
        elif fase_atual == 'quartas':
            vencedores = []
            for jogo in self.fases_eliminatorias['quartas']:
                if jogo['vencedor']:
                    vencedores.append(jogo['vencedor'])
            
            if len(vencedores) == 2:
                self.fases_eliminatorias['semifinais'] = [
                    {'time1': vencedores[0], 'time2': vencedores[1], 'resultado': None, 'disputado': False, 'vencedor': None}
                ]
        
        elif fase_atual == 'semifinais':
            vencedores = []
            for jogo in self.fases_eliminatorias['semifinais']:
                if jogo['vencedor']:
                    vencedores.append(jogo['vencedor'])
            
            if len(vencedores) == 1:
                self.fases_eliminatorias['final'] = [
                    {'time1': vencedores[0], 'time2': None, 'resultado': None, 'disputado': False, 'vencedor': None}
                ]
        
        elif fase_atual == 'final':
            for jogo in self.fases_eliminatorias['final']:
                if jogo['vencedor']:
                    self.campeao = jogo['vencedor']

def tela_copa_do_mundo(copa):
    fonte_grande = pygame.font.Font(None, 48)
    fonte_media = pygame.font.Font(None, 30)
    fonte_pequena = pygame.font.Font(None, 22)
    
    scroll_y = 0
    mostrar_artilharia = False
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "voltar"
                if evento.key == pygame.K_TAB:
                    mostrar_artilharia = not mostrar_artilharia
                if evento.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - 30)
                if evento.key == pygame.K_DOWN:
                    scroll_y += 30
                if evento.key == pygame.K_r:
                    for i, jogo in enumerate(copa.jogos_grupos):
                        if not jogo['disputado']:
                            return "jogar"
                    if copa.rodada_atual == "grupos":
                        copa.classificar_grupos()
                        copa.rodada_atual = "eliminatorias"
                        return "jogar"
                    for fase in ['oitavas', 'quartas', 'semifinais', 'final']:
                        if fase in copa.fases_eliminatorias:
                            for jogo in copa.fases_eliminatorias[fase]:
                                if not jogo['disputado']:
                                    return "jogar"
        
        TELA.fill((10, 10, 30))
        
        titulo = fonte_grande.render("🏆 COPA DO MUNDO", True, DOURADO)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 20))
        
        status_texto = f"Fase: {copa.rodada_atual.upper()} | Jogos: {copa.jogos_disputados} | Gols: {copa.gols_totais}"
        status = fonte_pequena.render(status_texto, True, CINZA)
        TELA.blit(status, (20, 70))
        
        if copa.campeao:
            campeao_texto = fonte_media.render(f"🏆 CAMPEÃO: {copa.campeao[0]} 🏆", True, DOURADO)
            TELA.blit(campeao_texto, (LARGURA//2 - campeao_texto.get_width()//2, 110))
            
            y = 160
            artilheiro_texto = fonte_media.render("🥇 ARTILHEIROS:", True, BRANCO)
            TELA.blit(artilheiro_texto, (LARGURA//2 - artilheiro_texto.get_width()//2, y))
            y += 35
            
            artilheiros_ord = sorted(copa.artilheiros.items(), key=lambda x: x[1], reverse=True)
            for i, (time, gols) in enumerate(artilheiros_ord[:5]):
                texto = fonte_pequena.render(f"{i+1}. {time} - {gols} gols", True, AMARELO)
                TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, y + i*25))
            
            instrucoes = fonte_pequena.render("ESC: Voltar", True, CINZA)
            TELA.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, ALTURA - 40))
            pygame.display.flip()
            RELOGIO.tick(FPS)
            continue
        
        if copa.rodada_atual == "grupos":
            y_offset = 110 - scroll_y
            for g_idx, grupo in enumerate(copa.grupos):
                if y_offset > ALTURA + 50:
                    break
                if y_offset < -50:
                    y_offset += 220
                    continue
                    
                grupo_texto = fonte_media.render(f"📋 Grupo {chr(65 + g_idx)}", True, DOURADO)
                TELA.blit(grupo_texto, (50, y_offset))
                y_offset += 30
                
                headers = ["Time", "J", "V", "E", "D", "GP", "GC", "SG", "Pts"]
                x_pos = 50
                for i, header in enumerate(headers):
                    h_text = fonte_pequena.render(header, True, BRANCO)
                    TELA.blit(h_text, (x_pos, y_offset))
                    x_pos += 70 if i > 0 else 120
                
                y_offset += 25
                
                for time in sorted(grupo, key=lambda x: (x['pontos'], x['saldo'], x['gols_pro']), reverse=True):
                    x_pos = 50
                    saldo = time['gols_pro'] - time['gols_contra']
                    
                    nome = fonte_pequena.render(time['time'][0], True, time['time'][1])
                    TELA.blit(nome, (x_pos, y_offset))
                    x_pos += 120
                    
                    stats = [str(time['jogos']), str(time['vitorias']), str(time['empates']), 
                            str(time['derrotas']), str(time['gols_pro']), str(time['gols_contra']),
                            str(saldo), str(time['pontos'])]
                    for stat in stats:
                        s_text = fonte_pequena.render(stat, True, BRANCO)
                        TELA.blit(s_text, (x_pos, y_offset))
                        x_pos += 70
                    
                    y_offset += 25
                
                y_offset += 20
                
                for jogo in copa.jogos_grupos:
                    if jogo['grupo'] == g_idx:
                        if jogo['disputado']:
                            g1, g2 = jogo['resultado']
                            texto = fonte_pequena.render(f"{jogo['time1'][0]} {g1} x {g2} {jogo['time2'][0]}", 
                                                        True, VERDE_CLARO)
                        else:
                            texto = fonte_pequena.render(f"{jogo['time1'][0]} vs {jogo['time2'][0]}", 
                                                        True, CINZA)
                        TELA.blit(texto, (70, y_offset))
                        y_offset += 25
                
                y_offset += 20
        
        else:
            y_offset = 110 - scroll_y
            fases = ['oitavas', 'quartas', 'semifinais', 'final']
            nomes_fases = ['⚔️ OITAVAS DE FINAL', '🔥 QUARTAS DE FINAL', '🌟 SEMIFINAIS', '🏆 FINAL']
            icones_fases = ['🔴', '🟠', '🟡', '🏆']
            
            for idx, fase in enumerate(fases):
                if y_offset > ALTURA + 50:
                    break
                if y_offset < -50:
                    y_offset += 100
                    continue
                    
                if fase in copa.fases_eliminatorias and copa.fases_eliminatorias[fase]:
                    fase_texto = fonte_media.render(f"{icones_fases[idx]} {nomes_fases[idx]}", True, DOURADO)
                    TELA.blit(fase_texto, (50, y_offset))
                    y_offset += 35
                    
                    for jogo in copa.fases_eliminatorias[fase]:
                        if jogo['disputado']:
                            g1, g2 = jogo['resultado']
                            vencedor = jogo['vencedor']
                            if vencedor:
                                texto = fonte_pequena.render(f"{jogo['time1'][0]} {g1} x {g2} {jogo['time2'][0]} ✅ {vencedor[0]}", 
                                                            True, VERDE_CLARO)
                            else:
                                texto = fonte_pequena.render(f"{jogo['time1'][0]} {g1} x {g2} {jogo['time2'][0]}", 
                                                            True, AMARELO)
                        else:
                            texto = fonte_pequena.render(f"{jogo['time1'][0]} vs {jogo['time2'][0]}", 
                                                        True, CINZA)
                        TELA.blit(texto, (70, y_offset))
                        y_offset += 25
                    
                    y_offset += 20
        
        instrucoes = fonte_pequena.render("🔄 TAB: Artilharia | ⬆⬇: Scroll | 🎮 R: Próximo jogo | ESC: Voltar", True, CINZA)
        TELA.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, ALTURA - 40))
        
        pygame.display.flip()
        RELOGIO.tick(FPS)

# ============================================================
# ===== SISTEMA DE BRASILEIRÃO =====
# ============================================================

class Brasileirao:
    def __init__(self):
        self.times = TIMES_BRASILEIRAO.copy()
        self.classificacao = []
        self.rodada_atual = 0
        self.jogos_rodada = []
        self.jogos_disputados = 0
        self.artilheiros = {}
        self.campeao = None
        self.rebaixados = []
        self.inicializar()
    
    def inicializar(self):
        self.classificacao = []
        for time in self.times:
            self.classificacao.append({
                'time': time,
                'pontos': 0,
                'jogos': 0,
                'vitorias': 0,
                'empates': 0,
                'derrotas': 0,
                'gols_pro': 0,
                'gols_contra': 0,
                'saldo': 0,
                'aproveitamento': 0
            })
        
        self.gerar_jogos()
    
    def gerar_jogos(self):
        self.jogos = []
        n = len(self.times)
        for i in range(n):
            for j in range(i+1, n):
                self.jogos.append({
                    'time1': self.times[i],
                    'time2': self.times[j],
                    'time1_idx': i,
                    'time2_idx': j,
                    'resultado': None,
                    'disputado': False
                })
        random.shuffle(self.jogos)
    
    def proxima_rodada(self):
        if self.rodada_atual >= len(self.jogos):
            return False
        
        self.jogos_rodada = [self.jogos[self.rodada_atual]]
        self.rodada_atual += 1
        return True
    
    def registrar_resultado(self, time1_gols, time2_gols):
        if not self.jogos_rodada:
            return
        
        jogo = self.jogos_rodada[0]
        if jogo['disputado']:
            return
        
        jogo['disputado'] = True
        jogo['resultado'] = (time1_gols, time2_gols)
        self.jogos_disputados += 1
        
        time1_data = self.classificacao[jogo['time1_idx']]
        time2_data = self.classificacao[jogo['time2_idx']]
        
        time1_data['jogos'] += 1
        time2_data['jogos'] += 1
        time1_data['gols_pro'] += time1_gols
        time1_data['gols_contra'] += time2_gols
        time2_data['gols_pro'] += time2_gols
        time2_data['gols_contra'] += time1_gols
        
        if time1_gols > time2_gols:
            time1_data['pontos'] += 3
            time1_data['vitorias'] += 1
            time2_data['derrotas'] += 1
        elif time2_gols > time1_gols:
            time2_data['pontos'] += 3
            time2_data['vitorias'] += 1
            time1_data['derrotas'] += 1
        else:
            time1_data['pontos'] += 1
            time2_data['pontos'] += 1
            time1_data['empates'] += 1
            time2_data['empates'] += 1
        
        time1_data['saldo'] = time1_data['gols_pro'] - time1_data['gols_contra']
        time2_data['saldo'] = time2_data['gols_pro'] - time2_data['gols_contra']
        time1_data['aproveitamento'] = (time1_data['pontos'] / (time1_data['jogos'] * 3)) * 100 if time1_data['jogos'] > 0 else 0
        time2_data['aproveitamento'] = (time2_data['pontos'] / (time2_data['jogos'] * 3)) * 100 if time2_data['jogos'] > 0 else 0
        
        if time1_gols > 0:
            self.artilheiros[jogo['time1'][0]] = self.artilheiros.get(jogo['time1'][0], 0) + time1_gols
        if time2_gols > 0:
            self.artilheiros[jogo['time2'][0]] = self.artilheiros.get(jogo['time2'][0], 0) + time2_gols
    
    def verificar_campeao(self):
        if self.jogos_disputados >= len(self.jogos):
            classificacao_ord = sorted(self.classificacao, 
                                      key=lambda x: (x['pontos'], x['saldo'], x['gols_pro']),
                                      reverse=True)
            self.campeao = classificacao_ord[0]['time']
            self.rebaixados = [c['time'] for c in classificacao_ord[-4:]]
            return True
        return False

def tela_brasileirao(brasileirao):
    fonte_grande = pygame.font.Font(None, 48)
    fonte_media = pygame.font.Font(None, 30)
    fonte_pequena = pygame.font.Font(None, 22)
    
    scroll_y = 0
    mostrar_artilharia = False
    mostrar_aproveitamento = False
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "voltar"
                if evento.key == pygame.K_TAB:
                    mostrar_artilharia = not mostrar_artilharia
                if evento.key == pygame.K_a:
                    mostrar_aproveitamento = not mostrar_aproveitamento
                if evento.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - 30)
                if evento.key == pygame.K_DOWN:
                    scroll_y += 30
                if evento.key == pygame.K_r:
                    if brasileirao.jogos_rodada and not brasileirao.jogos_rodada[0]['disputado']:
                        return "jogar"
                    elif brasileirao.proxima_rodada():
                        return "jogar"
        
        TELA.fill((10, 10, 30))
        
        titulo = fonte_grande.render("🇧🇷 BRASILEIRÃO SÉRIE A 2024", True, DOURADO)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 15))
        
        subtitulo = fonte_pequena.render(f"⚽ Jogos: {brasileirao.jogos_disputados}/{len(brasileirao.jogos)} | 📊 TAB: Artilharia | A: Aproveitamento", True, CINZA)
        TELA.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 45))
        
        if brasileirao.campeao:
            campeao_texto = fonte_media.render(f"🏆 CAMPEÃO: {brasileirao.campeao[0]} 🏆", True, DOURADO)
            TELA.blit(campeao_texto, (LARGURA//2 - campeao_texto.get_width()//2, 80))
            
            rebaixados_texto = fonte_media.render("⬇️ REBAIXADOS:", True, VERMELHO)
            TELA.blit(rebaixados_texto, (LARGURA//2 - rebaixados_texto.get_width()//2, 120))
            y = 155
            for time in brasileirao.rebaixados:
                texto = fonte_pequena.render(f"⬇️ {time[0]}", True, VERMELHO)
                TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
                y += 25
            
            if mostrar_artilharia:
                y = 250
                artilheiro_texto = fonte_media.render("🥇 ARTILHEIROS:", True, BRANCO)
                TELA.blit(artilheiro_texto, (LARGURA//2 - artilheiro_texto.get_width()//2, y))
                y += 35
                
                artilheiros_ord = sorted(brasileirao.artilheiros.items(), key=lambda x: x[1], reverse=True)
                for i, (time, gols) in enumerate(artilheiros_ord[:10]):
                    texto = fonte_pequena.render(f"{i+1}. {time} - {gols} gols", True, AMARELO)
                    TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, y + i*25))
            
            instrucoes = fonte_pequena.render("ESC: Voltar | TAB: Artilharia | A: Aproveitamento", True, CINZA)
            TELA.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, ALTURA - 40))
            pygame.display.flip()
            RELOGIO.tick(FPS)
            continue
        
        y_offset = 85 - scroll_y
        classificacao_ord = sorted(brasileirao.classificacao, 
                                  key=lambda x: (x['pontos'], x['saldo'], x['gols_pro']),
                                  reverse=True)
        
        headers = ["Pos", "Time", "J", "V", "E", "D", "GP", "GC", "SG", "Pts"]
        if mostrar_aproveitamento:
            headers.append("Apr%")
        
        x_pos = 50
        for i, header in enumerate(headers):
            h_text = fonte_pequena.render(header, True, BRANCO)
            TELA.blit(h_text, (x_pos, y_offset))
            if i == 0:
                x_pos += 40
            elif i == 1:
                x_pos += 130
            else:
                x_pos += 50
        
        y_offset += 25
        
        for pos, time_data in enumerate(classificacao_ord):
            if y_offset > ALTURA + 50:
                break
            if y_offset < -50:
                y_offset += 25
                continue
            
            x_pos = 50
            
            pos_text = fonte_pequena.render(str(pos+1), True, BRANCO)
            TELA.blit(pos_text, (x_pos, y_offset))
            x_pos += 40
            
            nome_text = fonte_pequena.render(time_data['time'][0], True, time_data['time'][1])
            TELA.blit(nome_text, (x_pos, y_offset))
            x_pos += 130
            
            stats = [str(time_data['jogos']), str(time_data['vitorias']), str(time_data['empates']),
                    str(time_data['derrotas']), str(time_data['gols_pro']), str(time_data['gols_contra']),
                    str(time_data['saldo']), str(time_data['pontos'])]
            for stat in stats:
                s_text = fonte_pequena.render(stat, True, BRANCO)
                TELA.blit(s_text, (x_pos, y_offset))
                x_pos += 50
            
            if mostrar_aproveitamento:
                apr_text = fonte_pequena.render(f"{time_data['aproveitamento']:.1f}%", True, CIANO)
                TELA.blit(apr_text, (x_pos, y_offset))
            
            y_offset += 25
        
        if brasileirao.jogos_rodada and not brasileirao.jogos_rodada[0]['disputado']:
            jogo = brasileirao.jogos_rodada[0]
            proximo_texto = fonte_media.render(f"🎮 Próximo: {jogo['time1'][0]} vs {jogo['time2'][0]}", True, AMARELO)
            TELA.blit(proximo_texto, (LARGURA//2 - proximo_texto.get_width()//2, ALTURA - 80))
        
        instrucoes = fonte_pequena.render("🎮 R: Próximo jogo | 🔄 TAB: Artilharia | 📊 A: Aproveitamento | ⬆⬇: Scroll | ESC: Voltar", True, CINZA)
        TELA.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, ALTURA - 40))
        
        pygame.display.flip()
        RELOGIO.tick(FPS)

# ============================================================
# ===== LOOP PRINCIPAL DO JOGO =====
# ============================================================

def loop_jogo(time1, time2, modo="normal", tempo_limite=180):
    if time1 is None or time2 is None:
        return None, (0, 0)
    
    try:
        jogador1 = Jogador(LIMITE_ESQ + 100, ALTURA//2, time1[1], time1[2],
                           {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esq': pygame.K_a, 'dir': pygame.K_d},
                           pygame.K_SPACE, 'esq', time1[0], pygame.K_q)
        jogador2 = Jogador(LIMITE_DIR - 100, ALTURA//2, time2[1], time2[2],
                           {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esq': pygame.K_LEFT, 'dir': pygame.K_RIGHT},
                           pygame.K_RETURN, 'dir', time2[0], pygame.K_RSHIFT)
        
        goleiro1 = Goleiro('esq', LIMITE_ESQ + 20, ALTURA//2)
        goleiro2 = Goleiro('dir', LIMITE_DIR - 20, ALTURA//2)
        
        bola = Bola(LARGURA//2, ALTURA//2)
        bolas_extra = []
        
        pontuacao = [0, 0]
        tempo_espera = 0
        ultimo_gol = None
        powerups = []
        textos_flutuantes = []
        sistema_particulas = SistemaParticulas()
        clima_dinamico = ClimaDinamico()
        estatisticas = Estatisticas()
        
        fonte_placar = pygame.font.Font(None, 90)
        fonte_info = pygame.font.Font(None, 24)
        fonte_gol = pygame.font.Font(None, 120)
        dt = 1/FPS
        
        rodando = True
        tempo_partida = 0
        limite_tempo = tempo_limite * FPS
        gol_ouro = (modo == "gol_ouro")
        modo_over_time = (modo == "over_time")
        modo_rapido = (modo == "relampago")
        is_treino = (modo == "treino")
        time_vencedor = None
        frame = 0
        mostrar_gol = False
        tempo_mostrar_gol = 0
        ultimo_gol_time = None
        posse_time = None
        gols_na_partida = 0
        
        # Sistema de replays
        replay_frames = []
        gravando_replay = True
        
        while rodando:
            frame += 1
            
            # Gravar replay
            if gravando_replay and len(replay_frames) < 300:
                replay_frames.append({
                    'x1': jogador1.x, 'y1': jogador1.y,
                    'x2': jogador2.x, 'y2': jogador2.y,
                    'bx': bola.x, 'by': bola.y,
                    'score': pontuacao.copy()
                })
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None, None
                    if evento.key == pygame.K_SPACE:
                        dist = math.hypot(jogador1.x - bola.x, jogador1.y - bola.y)
                        if dist < jogador1.raio + bola.raio + 50:
                            jogador1.iniciar_carregar_chute()
                    if evento.key == pygame.K_RETURN:
                        dist = math.hypot(jogador2.x - bola.x, jogador2.y - bola.y)
                        if dist < jogador2.raio + bola.raio + 50:
                            jogador2.iniciar_carregar_chute()
                    if evento.key == pygame.K_q:
                        if jogador1.posse > 0:
                            jogador1.passar(bola, jogador2, 12)
                    if evento.key == pygame.K_RSHIFT:
                        if jogador2.posse > 0:
                            jogador2.passar(bola, jogador1, 12)
                    if evento.key == pygame.K_c:
                        if jogador1.posse > 0 and "clonagem" not in jogador1.powerups:
                            jogador1.aplicar_powerup("clonagem")
                            textos_flutuantes.append(TextoFlutuante("🧬 CLONAGEM!", jogador1.x, jogador1.y-30, (255, 150, 0), 60, 30))
                    if evento.key == pygame.K_r and not is_treino:
                        # Alternar replay
                        if replay_frames:
                            gravando_replay = not gravando_replay
                            if not gravando_replay:
                                textos_flutuantes.append(TextoFlutuante("📹 REPLAY", LARGURA//2, 50, CIANO, 120, 40))
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_SPACE:
                        resultado, bola_extra = jogador1.parar_carregar_chute(bola)
                        if bola_extra:
                            bolas_extra.append(bola_extra)
                    if evento.key == pygame.K_RETURN:
                        resultado, bola_extra = jogador2.parar_carregar_chute(bola)
                        if bola_extra:
                            bolas_extra.append(bola_extra)

            teclas = pygame.key.get_pressed()
            teclas_dict = {
                pygame.K_w: teclas[pygame.K_w], pygame.K_s: teclas[pygame.K_s],
                pygame.K_a: teclas[pygame.K_a], pygame.K_d: teclas[pygame.K_d],
                pygame.K_UP: teclas[pygame.K_UP], pygame.K_DOWN: teclas[pygame.K_DOWN],
                pygame.K_LEFT: teclas[pygame.K_LEFT], pygame.K_RIGHT: teclas[pygame.K_RIGHT]
            }
            
            jogador1.mover(teclas_dict, bola)
            jogador2.mover(teclas_dict, bola)
            
            colisao_jogador_jogador(jogador1, jogador2, sistema_particulas)
            if jogador1.clone:
                colisao_jogador_jogador(jogador1.clone, jogador2, sistema_particulas)

            jogador1.atualizar_powerups()
            jogador2.atualizar_powerups()
            jogador1.carregar_chute_update(dt)
            jogador2.carregar_chute_update(dt)
            
            if jogador1.clone_ativo and jogador1.clone:
                jogador1.clone.x = jogador1.x + 30 * math.sin(frame * 0.05)
                jogador1.clone.y = jogador1.y + 30 * math.cos(frame * 0.05)
                jogador1.clone.vel_x = jogador1.vel_x * 0.5
                jogador1.clone.vel_y = jogador1.vel_y * 0.5
                jogador1.clone.posse = jogador1.posse // 2
            
            goleiro1.atualizar(bola, tempo_partida)
            goleiro2.atualizar(bola, tempo_partida)
            
            goleiro1.defender(bola)
            goleiro2.defender(bola)
            
            for bola_extra in bolas_extra[:]:
                bola_extra.mover()
                colisao_jogador_bola(jogador1, bola_extra, sistema_particulas)
                colisao_jogador_bola(jogador2, bola_extra, sistema_particulas)
                if jogador1.clone:
                    colisao_jogador_bola(jogador1.clone, bola_extra, sistema_particulas)
                goleiro1.defender(bola_extra)
                goleiro2.defender(bola_extra)
                if verificar_gol(bola_extra):
                    bolas_extra.remove(bola_extra)

            if tempo_espera <= 0:
                if clima_dinamico.estado_atual in ['chuva', 'neve', 'tempestade']:
                    bola.vel_x *= 0.98
                    bola.vel_y *= 0.98
                
                bola.mover()
                colisao_jogador_bola(jogador1, bola, sistema_particulas)
                colisao_jogador_bola(jogador2, bola, sistema_particulas)
                if jogador1.clone:
                    colisao_jogador_bola(jogador1.clone, bola, sistema_particulas)

                # Powerups
                if not is_treino:
                    for pw in powerups[:]:
                        pw.update()
                        if pw.vida <= 0:
                            powerups.remove(pw)
                            continue
                        
                        if math.hypot(jogador1.x - pw.x, jogador1.y - pw.y) < jogador1.raio + pw.raio:
                            jogador1.aplicar_powerup(pw.tipo)
                            if audio:
                                audio.tocar('powerup')
                            sistema_particulas.adicionar(pw.x, pw.y, CORES_POWERUP[pw.tipo], "fogos", 15)
                            textos_flutuantes.append(TextoFlutuante(pw.tipo.upper(), pw.x, pw.y, CORES_POWERUP[pw.tipo]))
                            powerups.remove(pw)
                            continue
                        
                        if math.hypot(jogador2.x - pw.x, jogador2.y - pw.y) < jogador2.raio + pw.raio:
                            jogador2.aplicar_powerup(pw.tipo)
                            if audio:
                                audio.tocar('powerup')
                            sistema_particulas.adicionar(pw.x, pw.y, CORES_POWERUP[pw.tipo], "fogos", 15)
                            textos_flutuantes.append(TextoFlutuante(pw.tipo.upper(), pw.x, pw.y, CORES_POWERUP[pw.tipo]))
                            powerups.remove(pw)
                            continue

                    novo = gerar_powerup()
                    if novo:
                        powerups.append(novo)

                # Verificar gol
                gol = verificar_gol(bola)
                if gol == "esquerdo" and not is_treino:
                    pontuacao[1] += 1
                    gols_na_partida += 1
                    ultimo_gol = time2[0]
                    ultimo_gol_time = time2
                    tempo_espera = FPS * 1.5
                    bola.resetar()
                    if audio:
                        audio.tocar('gol')
                        audio.tocar('torcida')
                    mostrar_gol = True
                    tempo_mostrar_gol = 60
                    
                    jogador1.x, jogador1.y = LIMITE_ESQ + 100, ALTURA//2
                    jogador2.x, jogador2.y = LIMITE_DIR - 100, ALTURA//2
                    jogador1.vel_x = jogador1.vel_y = 0
                    jogador2.vel_x = jogador2.vel_y = 0
                    
                    textos_flutuantes.append(TextoFlutuante("⚽ GOL!", LARGURA//2, ALTURA//2 - 50, DOURADO, 90, 80))
                    sistema_particulas.adicionar(bola.x, bola.y, DOURADO, "fogos", 30)
                    sistema_particulas.adicionar(bola.x, bola.y, time2[1], "confete", 20)
                    
                    if gol_ouro:
                        time_vencedor = time2
                        rodando = False
                    
                    if modo_over_time:
                        if pontuacao[0] > pontuacao[1] or pontuacao[1] > pontuacao[0]:
                            time_vencedor = time1 if pontuacao[0] > pontuacao[1] else time2
                            rodando = False
                    
                elif gol == "direito" and not is_treino:
                    pontuacao[0] += 1
                    gols_na_partida += 1
                    ultimo_gol = time1[0]
                    ultimo_gol_time = time1
                    tempo_espera = FPS * 1.5
                    bola.resetar()
                    if audio:
                        audio.tocar('gol')
                        audio.tocar('torcida')
                    mostrar_gol = True
                    tempo_mostrar_gol = 60
                    
                    jogador1.x, jogador1.y = LIMITE_ESQ + 100, ALTURA//2
                    jogador2.x, jogador2.y = LIMITE_DIR - 100, ALTURA//2
                    jogador1.vel_x = jogador1.vel_y = 0
                    jogador2.vel_x = jogador2.vel_y = 0
                    
                    textos_flutuantes.append(TextoFlutuante("⚽ GOL!", LARGURA//2, ALTURA//2 - 50, DOURADO, 90, 80))
                    sistema_particulas.adicionar(bola.x, bola.y, DOURADO, "fogos", 30)
                    sistema_particulas.adicionar(bola.x, bola.y, time1[1], "confete", 20)
                    
                    if gol_ouro:
                        time_vencedor = time1
                        rodando = False
                    
                    if modo_over_time:
                        if pontuacao[0] > pontuacao[1] or pontuacao[1] > pontuacao[0]:
                            time_vencedor = time1 if pontuacao[0] > pontuacao[1] else time2
                            rodando = False

                jogador1.posse = max(0, jogador1.posse - 1)
                jogador2.posse = max(0, jogador2.posse - 1)
                
                # Atualizar posse
                if jogador1.posse > 0:
                    posse_time = time1[0]
                elif jogador2.posse > 0:
                    posse_time = time2[0]
                
                # Verificar tempo
                tempo_partida += 1
                if tempo_partida >= limite_tempo and not is_treino:
                    rodando = False
                    if pontuacao[0] > pontuacao[1]:
                        time_vencedor = time1
                    elif pontuacao[1] > pontuacao[0]:
                        time_vencedor = time2
                    else:
                        time_vencedor = time1 if random.random() < 0.5 else time2
                
            else:
                tempo_espera -= 1

            # Atualizar textos
            for txt in textos_flutuantes[:]:
                txt.update()
                if txt.idade >= txt.duracao:
                    textos_flutuantes.remove(txt)
            
            sistema_particulas.atualizar()
            clima_dinamico.atualizar()
            
            if mostrar_gol:
                tempo_mostrar_gol -= 1
                if tempo_mostrar_gol <= 0:
                    mostrar_gol = False

            # Desenhar
            desenhar_campo()
            
            clima_dinamico.desenhar(TELA)
            
            for pw in powerups:
                pw.desenhar(TELA)
            
            bola.desenhar(TELA)
            for bola_extra in bolas_extra:
                bola_extra.desenhar(TELA)
            
            goleiro1.desenhar(TELA)
            goleiro2.desenhar(TELA)
            jogador1.desenhar(TELA)
            jogador2.desenhar(TELA)
            if jogador1.clone:
                jogador1.clone.desenhar(TELA)
            
            sistema_particulas.desenhar(TELA)
            
            for txt in textos_flutuantes:
                txt.draw(TELA)
            
            # Placar
            if not is_treino:
                placar_texto = fonte_placar.render(f"{pontuacao[0]}  ⚽  {pontuacao[1]}", True, BRANCO)
                TELA.blit(placar_texto, (LARGURA//2 - placar_texto.get_width()//2 + 3, 15+3))
                TELA.blit(placar_texto, (LARGURA//2 - placar_texto.get_width()//2, 15))
                
                nome1 = fonte_info.render(time1[0], True, time1[1])
                nome2 = fonte_info.render(time2[0], True, time2[1])
                TELA.blit(nome1, (LARGURA//2 - 150 - nome1.get_width(), 10))
                TELA.blit(nome2, (LARGURA//2 + 80, 10))
                
                # Cronômetro
                segundos_restantes = max(0, tempo_limite - tempo_partida // FPS)
                minutos = segundos_restantes // 60
                segundos = segundos_restantes % 60
                tempo_texto = fonte_info.render(f"⏱️ {minutos:02d}:{segundos:02d}", True, AMARELO)
                TELA.blit(tempo_texto, (LARGURA//2 + 220, 20))
                
                # Posse de bola
                if posse_time:
                    posse_texto = fonte_info.render(f"⚽ {posse_time}", True, CIANO)
                    TELA.blit(posse_texto, (LARGURA//2 - posse_texto.get_width()//2, 70))
                
                # Powerups ativos
                if jogador1.powerups:
                    pw_text = fonte_info.render(f"J1: {len(jogador1.powerups)}", True, CIANO)
                    TELA.blit(pw_text, (20, ALTURA - 60))
                if jogador2.powerups:
                    pw_text = fonte_info.render(f"J2: {len(jogador2.powerups)}", True, ROSA)
                    TELA.blit(pw_text, (LARGURA - 80, ALTURA - 60))

            # Gol
            if mostrar_gol:
                texto_gol = fonte_gol.render("⚽ GOL! ⚽", True, DOURADO)
                sombra_gol = fonte_gol.render("⚽ GOL! ⚽", True, PRETO)
                TELA.blit(sombra_gol, (LARGURA//2 - texto_gol.get_width()//2 + 3, ALTURA//2 - 80 + 3))
                TELA.blit(texto_gol, (LARGURA//2 - texto_gol.get_width()//2, ALTURA//2 - 80))
                
                if ultimo_gol_time:
                    fonte_time = pygame.font.Font(None, 50)
                    texto_time = fonte_time.render(f"{ultimo_gol_time[0]} marcou!", True, BRANCO)
                    TELA.blit(texto_time, (LARGURA//2 - texto_time.get_width()//2, ALTURA//2 - 20))

            if tempo_espera > 0 and ultimo_gol and not is_treino:
                gol_msg = fonte_info.render(f"{ultimo_gol} marcou!", True, AMARELO)
                TELA.blit(gol_msg, (LARGURA//2 - gol_msg.get_width()//2, ALTURA - 110))

            if jogador1.chute_carregando:
                larg = 60 * jogador1.chute_tempo/0.8
                pygame.draw.rect(TELA, VERMELHO, (jogador1.x-30, jogador1.y-35, larg, 8))
                pygame.draw.rect(TELA, AMARELO, (jogador1.x-30, jogador1.y-35, larg, 8), 2)
                forca_texto = fonte_info.render(f"💪 {int(jogador1.chute_tempo/0.8 * 100)}%", True, BRANCO)
                TELA.blit(forca_texto, (jogador1.x - 20, jogador1.y - 50))
            if jogador2.chute_carregando:
                larg = 60 * jogador2.chute_tempo/0.8
                pygame.draw.rect(TELA, VERMELHO, (jogador2.x-30, jogador2.y-35, larg, 8))
                pygame.draw.rect(TELA, AMARELO, (jogador2.x-30, jogador2.y-35, larg, 8), 2)
                forca_texto = fonte_info.render(f"💪 {int(jogador2.chute_tempo/0.8 * 100)}%", True, BRANCO)
                TELA.blit(forca_texto, (jogador2.x - 20, jogador2.y - 50))

            if gol_ouro:
                texto_gol_ouro = fonte_info.render("🏆 GOL DE OURO - Quem marcar vence!", True, DOURADO)
                TELA.blit(texto_gol_ouro, (LARGURA//2 - texto_gol_ouro.get_width()//2, 65))
            
            if modo_over_time:
                texto_ot = fonte_info.render("⏱️ OVER TIME - Quem marcar primeiro vence!", True, LARANJA)
                TELA.blit(texto_ot, (LARGURA//2 - texto_ot.get_width()//2, 65))

            texto_clima = fonte_info.render(f"🌤️ {clima_dinamico.estado_atual.upper()}", True, CIANO)
            TELA.blit(texto_clima, (20, 20))

            if not is_treino:
                instrucoes = fonte_info.render("⌨️ WASD+SPACE (J1) | SETAS+ENTER (J2) | Q/PASS | RSHIFT/PASS | C/CLONE | R/REPLAY | ESC:SAIR", True, CINZA)
                TELA.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, ALTURA - 25))

            pygame.display.flip()
            RELOGIO.tick(FPS)

        # Fim do jogo
        if time_vencedor:
            estatisticas.registrar_jogo('vitoria', pontuacao[0] if time_vencedor == time1 else pontuacao[1], 
                                      pontuacao[1] if time_vencedor == time1 else pontuacao[0],
                                      list(jogador1.powerups.keys()) + list(jogador2.powerups.keys()),
                                      tempo_partida // FPS)
            
            for _ in range(120):
                TELA.fill((10, 10, 30))
                desenhar_campo()
                animacao_vitoria(TELA, time_vencedor, sistema_particulas)
                sistema_particulas.atualizar()
                sistema_particulas.desenhar(TELA)
                pygame.display.flip()
                RELOGIO.tick(FPS)
            
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        esperando = False
        
        return time_vencedor, (pontuacao[0], pontuacao[1])
        
    except Exception as e:
        print(f"Erro no loop_jogo: {e}")
        import traceback
        traceback.print_exc()
        return None, (0, 0)

# ============================================================
# ===== MAIN =====
# ============================================================

def main():
    global audio
    audio = SistemaAudio()
    
    while True:
        opcao = tela_menu_principal()
        
        if opcao == "Partida Rápida":
            try:
                time1, time2 = tela_escolha_times()
                loop_jogo(time1, time2, "normal", 180)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Brasileirão S.A.":
            try:
                brasileirao = Brasileirao()
                while not brasileirao.campeao:
                    opcao_br = tela_brasileirao(brasileirao)
                    if opcao_br == "voltar":
                        break
                    elif opcao_br == "jogar":
                        if brasileirao.jogos_rodada and not brasileirao.jogos_rodada[0]['disputado']:
                            jogo = brasileirao.jogos_rodada[0]
                            time_vencedor, resultado = loop_jogo(jogo['time1'], jogo['time2'], "normal", 180)
                            if resultado:
                                brasileirao.registrar_resultado(resultado[0], resultado[1])
                            if brasileirao.verificar_campeao():
                                mostrar_campeao(brasileirao.campeao)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Copa do Mundo":
            try:
                copa = CopaDoMundo()
                
                while copa.rodada_atual == "grupos":
                    todos_disputados = all(jogo['disputado'] for jogo in copa.jogos_grupos)
                    if todos_disputados:
                        copa.classificar_grupos()
                        copa.rodada_atual = "eliminatorias"
                        break
                    
                    opcao_copa = tela_copa_do_mundo(copa)
                    if opcao_copa == "voltar":
                        break
                    elif opcao_copa == "jogar":
                        for i, jogo in enumerate(copa.jogos_grupos):
                            if not jogo['disputado']:
                                time_vencedor, resultado = loop_jogo(jogo['time1'], jogo['time2'], "normal", 180)
                                if resultado:
                                    copa.registrar_resultado_grupo(i, resultado[0], resultado[1])
                                break
                
                while copa.rodada_atual == "eliminatorias" and not copa.campeao:
                    fases = ['oitavas', 'quartas', 'semifinais', 'final']
                    for fase in fases:
                        if copa.campeao:
                            break
                        if fase not in copa.fases_eliminatorias or not copa.fases_eliminatorias[fase]:
                            continue
                        
                        todos_disputados = all(jogo['disputado'] for jogo in copa.fases_eliminatorias[fase])
                        if todos_disputados:
                            continue
                        
                        opcao_copa = tela_copa_do_mundo(copa)
                        if opcao_copa == "voltar":
                            break
                        elif opcao_copa == "jogar":
                            for i, jogo in enumerate(copa.fases_eliminatorias[fase]):
                                if not jogo['disputado']:
                                    time_vencedor, resultado = loop_jogo(jogo['time1'], jogo['time2'], "normal", 180)
                                    if resultado:
                                        copa.registrar_resultado_eliminatorio(fase, i, resultado[0], resultado[1])
                                    break
                    
                    if opcao_copa == "voltar":
                        break
                
                if copa.campeao:
                    mostrar_campeao(copa.campeao)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Modo Relâmpago":
            try:
                time1, time2 = tela_escolha_times()
                loop_jogo(time1, time2, "relampago", 60)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Over Time":
            try:
                time1, time2 = tela_escolha_times()
                loop_jogo(time1, time2, "over_time", 180)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Gol de Ouro":
            try:
                time1, time2 = tela_escolha_times()
                loop_jogo(time1, time2, "gol_ouro", 180)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Modo Treino":
            try:
                time = TIMES_TODOS[0]
                loop_jogo(time, time, "treino", 0)
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Sobrevivência":
            try:
                sobrevivencia = ModoSobrevivencia()
                time1, time2 = tela_escolha_times()
                while sobrevivencia.vida > 0:
                    time_vencedor, resultado = loop_jogo(time1, time2, "normal", 120)
                    if time_vencedor:
                        if time_vencedor == time1:
                            sobrevivencia.pontos += 10
                        else:
                            sobrevivencia.vida -= 1
                        sobrevivencia.next_round()
                    else:
                        sobrevivencia.vida -= 1
                    if sobrevivencia.vida <= 0:
                        mostrar_mensagem(f"💀 GAME OVER!\nPontos: {sobrevivencia.pontos}\nRodadas: {sobrevivencia.rodada}\nRecorde: {sobrevivencia.record}")
            except Exception as e:
                print(f"Erro: {e}")
                continue
        
        elif opcao == "Sair":
            pygame.quit()
            sys.exit()

def mostrar_mensagem(texto):
    fonte = pygame.font.Font(None, 36)
    linhas = texto.split('\n')
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False
        
        TELA.fill((10, 10, 30))
        y = ALTURA//2 - len(linhas) * 25
        for linha in linhas:
            surf = fonte.render(linha, True, DOURADO)
            TELA.blit(surf, (LARGURA//2 - surf.get_width()//2, y))
            y += 50
        
        pygame.display.flip()
        RELOGIO.tick(FPS)

def mostrar_campeao(campeao):
    fonte_grande = pygame.font.Font(None, 80)
    fonte_media = pygame.font.Font(None, 40)
    
    angulo = 0
    sistema_particulas = SistemaParticulas()
    for _ in range(50):
        sistema_particulas.adicionar(random.randint(0, LARGURA), random.randint(0, ALTURA),
                                   random.choice([DOURADO, AMARELO, VERMELHO, AZUL, ROXO, CIANO]), "confete")
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                    return
        
        TELA.fill((10, 10, 30))
        angulo += 0.02
        
        for i in range(80):
            x = LARGURA//2 + math.sin(angulo + i*0.3)*300
            y = ALTURA//2 + math.cos(angulo*0.5 + i)*150
            pygame.draw.circle(TELA, (50,50,100), (int(x), int(y)), 2)
        
        sistema_particulas.atualizar()
        sistema_particulas.desenhar(TELA)
        
        if random.random() < 0.03:
            x = random.randint(200, LARGURA-200)
            y = random.randint(100, ALTURA//2)
            for _ in range(30):
                sistema_particulas.adicionar(x, y, random.choice([VERMELHO, AZUL, AMARELO, DOURADO, VERDE_CLARO]), "fogos")
        
        titulo = fonte_grande.render("🏆 CAMPEÃO 🏆", True, DOURADO)
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 80))
        
        y = 250
        tamanho_trofeu = 80 + int(math.sin(angulo * 2) * 5)
        
        pygame.draw.circle(TELA, campeao[1], (LARGURA//2, y), tamanho_trofeu)
        pygame.draw.circle(TELA, campeao[2], (LARGURA//2, y), tamanho_trofeu-15)
        pygame.draw.circle(TELA, DOURADO, (LARGURA//2, y), tamanho_trofeu+5, 3)
        
        nome = fonte_media.render(campeao[0], True, BRANCO)
        TELA.blit(nome, (LARGURA//2 - nome.get_width()//2, y + 100))
        
        texto = fonte_media.render("Pressione ENTER ou ESC para continuar", True, CINZA)
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA - 60))
        
        pygame.display.flip()
        RELOGIO.tick(FPS)

if __name__ == "__main__":
    main()