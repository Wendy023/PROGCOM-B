import pygame
import sys
import random
import time
import os

pygame.init()
pygame.mixer.init()

# =======================
# CONFIGURACIÓN GENERAL
# =======================
ANCHO, ALTO = 1024, 720
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("STOP! — Humano vs Máquina")
RELOJ = pygame.time.Clock()

# COLORES
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (220, 220, 220)
GRIS_OSCURO = (180, 180, 180)
AZUL = (70, 130, 250)
VERDE = (60, 200, 100)
ROJO = (240, 80, 80)
AMARILLO = (250, 200, 60)

# FUENTES
F_TIT = pygame.font.SysFont("arial", 40, True)
F_SUB = pygame.font.SysFont("arial", 26, True)
F_TXT = pygame.font.SysFont("arial", 22)
F_MONO = pygame.font.SysFont("consolas", 20)

# SONIDOS
try:
    SONIDO_INICIO = pygame.mixer.Sound("inicio.wav")
    SONIDO_STOP = pygame.mixer.Sound("stop.wav")
    SONIDO_GANAR = pygame.mixer.Sound("ganar.wav")
    SONIDO_PERDER = pygame.mixer.Sound("perder.wav")
except:
    SONIDO_INICIO = SONIDO_STOP = SONIDO_GANAR = SONIDO_PERDER = None

# =======================
# DATOS DE JUEGO
# =======================
CATEGORIAS = [
    ("nombre", "Nombre"),
    ("apellido", "Apellido"),
    ("ciudad", "Ciudad"),
    ("color", "Color"),
    ("fruta", "Fruta"),
    ("animal", "Animal"),
    ("cosa", "Cosa")
]

PALABRAS = {
    "nombre": ["ana", "andres", "alicia", "beatriz", "bernardo", "camila", "carlos", "david", "elena", "fernanda", "gabriel", "gustavo", "isabel", "ivan", "jose", "juan", "karla", "laura", "luis", "manuel", "maria", "natalia", "oscar", "paula", "pedro", "ricardo", "roberto", "sandra", "sofia", "tomas", "valentina", "victor", "ximena", "yolanda", "zulema"],
    "apellido": ["gomez", "rodriguez", "perez", "martinez", "lopez", "hernandez", "garcia", "diaz", "sanchez", "ramirez", "moreno", "torres", "jimenez", "vargas", "castro", "ortiz", "reyes", "flores", "carrillo", "guerra"],
    "ciudad": ["bogota", "bucaramanga", "medellin", "cali", "cartagena", "manizales", "pereira", "ibague", "neiva", "armenia", "tunja", "sincelejo", "monteria", "popayan", "villavicencio", "barranquilla", "cucuta", "pasto", "valledupar", "leticia"],
    "color": ["rojo", "azul", "verde", "amarillo", "naranja", "morado", "negro", "blanco", "gris", "rosado", "violeta", "celeste", "turquesa", "dorado", "plateado", "beige"],
    "fruta": ["fresa", "mango", "manzana", "pera", "uva", "papaya", "sandia", "melon", "durazno", "naranja", "limon", "cereza", "kiwi", "guayaba", "maracuya", "banano", "coco"],
    "animal": ["gato", "perro", "elefante", "leon", "tigre", "conejo", "jirafa", "pato", "caballo", "raton", "zorro", "lobo", "oso", "mono", "tortuga", "serpiente", "pez", "delfin", "pollo", "vaca"],
    "cosa": ["mesa", "silla", "vaso", "cuchara", "libro", "lapiz", "reloj", "radio", "computador", "celular", "ventilador", "zapato", "camisa", "bolsa", "espejo", "plato", "botella", "caja", "maleta"]
}

DIFICULTADES = {
    "Fácil": {"espera": (1.0, 2.5), "precision": 0.6, "tiempo": 30},
    "Normal": {"espera": (0.7, 1.2), "precision": 0.85, "tiempo": 25},
    "Are you crazy?!": {"espera": (0.3, 0.8), "precision": 0.98, "tiempo": 15},
}

# =======================
# FUNCIONES DE JUEGO
# =======================
def palabra_ia(letra, categoria, cfg):
    lista = PALABRAS[categoria]
    posibles = [p for p in lista if p.startswith(letra)]
    if posibles and random.random() < cfg["precision"]:
        return random.choice(posibles)
    elif posibles:
        return random.choice(lista)
    else:
        base = random.choice(lista)
        return letra + base[1:]

def puntuar(h, m, cat):
    lista_valida = PALABRAS[cat]
    ph = pm = 0
    if h and h in lista_valida:
        ph += 10
    elif h:
        ph += 5
    if m and m in lista_valida:
        pm += 10
    return ph, pm

def valida(h, letra):
    return h.strip().lower().startswith(letra)

# =======================
# CLASES
# =======================
class InputBox:
    def __init__(self, rect, placeholder):
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False

    def handle(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(e.pos)
        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20 and e.unicode.isalpha():
                self.text += e.unicode

    def draw(self, surf):
        pygame.draw.rect(surf, BLANCO, self.rect, border_radius=6)
        pygame.draw.rect(surf, AZUL if self.active else GRIS_OSCURO, self.rect, 2)
        txt = self.text if self.text else self.placeholder
        col = NEGRO if self.text else (130, 130, 130)
        surf.blit(F_TXT.render(txt, True, col), (self.rect.x+8, self.rect.y+6))

    def clear(self):
        self.text = ""

class Button:
    def __init__(self, rect, label, color):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=8)
        txt = F_SUB.render(self.label, True, BLANCO)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, pos):
        return self.rect.collidepoint(pos)

# =======================
# FUNCIÓN PRINCIPAL
# =======================
def main():
    dificultad = "Normal"
    cfg = DIFICULTADES[dificultad]
    letra = "-"
    tiempo = 0
    jugando = False
    puntos_h = 0
    puntos_m = 0
    resultados = []

    # UI
    cajas = []
    inicio_y = 240
    espaciado = 52
    alto_caja = 34

    for idx, (_, label) in enumerate(CATEGORIAS):
        y = inicio_y + idx * espaciado
        cajas.append(InputBox((270, y, 380, alto_caja), label + "..."))


    btn_ronda = Button((60, 120, 180, 50), "Nueva ronda", VERDE)
    btn_stop = Button((260, 120, 120, 50), "STOP!", ROJO)
    btn_enviar = Button((400, 120, 180, 50), "Enviar", AZUL)
    btn_facil = Button((700, 120, 120, 40), "Fácil", AMARILLO)
    btn_normal = Button((830, 120, 120, 40), "Normal", AZUL)
    btn_crazy = Button((700, 170, 250, 40), "Are you crazy?!", ROJO)

    def comenzar():
        nonlocal letra, jugando, tiempo, resultados
        letra = random.choice("abcdefghijklmnñopqrstuvwxyz")
        tiempo = cfg["tiempo"]
        jugando = True
        resultados = []
        for c in cajas: c.clear()
        if SONIDO_INICIO: SONIDO_INICIO.play()

    def finalizar():
        nonlocal jugando, puntos_h, puntos_m, resultados
        jugando = False
        resultados.clear()
        resp_ia = {k: palabra_ia(letra, k, cfg) for k, _ in CATEGORIAS}
        for i, (k, label) in enumerate(CATEGORIAS):
            h = cajas[i].text.lower().strip()
            m = resp_ia[k].lower().strip()
            if not valida(h, letra):
                h = ""
            if not valida(m, letra):
                m = ""
            ph, pm = puntuar(h, m, k)
            puntos_h += ph
            puntos_m += pm
            resultados.append((label, h, m, ph, pm))
        if SONIDO_STOP: SONIDO_STOP.play()

        MAX_PUNTOS = 150
        ganador = None
        if puntos_h >= MAX_PUNTOS and puntos_m >= MAX_PUNTOS:
            ganador = "Empate"
        elif puntos_h >= MAX_PUNTOS:
            ganador = "Humano"
        elif puntos_m >= MAX_PUNTOS:
            ganador = "Máquina"

        if ganador:
            if ganador == "Humano":
                if SONIDO_GANAR: SONIDO_GANAR.play()
                mensaje = "¡El Humano gana la partida!"
            elif ganador == "Máquina":
                if SONIDO_PERDER: SONIDO_PERDER.play()
                mensaje = "La Máquina ha ganado..."
            else:
                mensaje = "¡Es un empate!"
            fin = True
            while fin:
                VENTANA.fill(BLANCO)
                VENTANA.blit(F_TIT.render(mensaje, True, NEGRO), (200, 300))
                VENTANA.blit(F_SUB.render("Presiona [ESPACIO] para reiniciar.", True, NEGRO), (250, 380))
                pygame.display.flip()
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                        puntos_h = puntos_m = 0
                        fin = False
                        break

    while True:
        dt = RELOJ.tick(60)/1000
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_ronda.click(e.pos): comenzar()
                if btn_enviar.click(e.pos) and jugando: finalizar()
                if btn_stop.click(e.pos) and jugando: finalizar()
                if not jugando:
                    if btn_facil.click(e.pos): dificultad="Fácil"; cfg=DIFICULTADES[dificultad]
                    if btn_normal.click(e.pos): dificultad="Normal"; cfg=DIFICULTADES[dificultad]
                    if btn_crazy.click(e.pos): dificultad="Are you crazy?!"; cfg=DIFICULTADES[dificultad]
            for c in cajas: c.handle(e)

        if jugando:
            tiempo -= dt
            if tiempo <= 0: finalizar()

        # =======================
        # DIBUJO EN PANTALLA
        # =======================
        VENTANA.fill(BLANCO)
        bloque_altura = len(CATEGORIAS) * espaciado + 100
        pygame.draw.rect(VENTANA, GRIS_OSCURO, (60, inicio_y - 40, 180, bloque_altura + 40), border_radius=10)
        VENTANA.blit(F_TIT.render("STOP! — Humano vs Máquina", True, NEGRO), (30, 20))
        VENTANA.blit(F_SUB.render(f"Dificultad: {dificultad}", True, NEGRO), (750, 20))
        VENTANA.blit(F_TXT.render(f"Puntos 👤 {puntos_h}    {puntos_m}", True, NEGRO), (750, 50))

        btn_ronda.draw(VENTANA)
        btn_stop.draw(VENTANA)
        btn_enviar.draw(VENTANA)
        btn_facil.draw(VENTANA)
        btn_normal.draw(VENTANA)
        btn_crazy.draw(VENTANA)

        pygame.draw.rect(VENTANA, GRIS_OSCURO, (60, 200, 180, 420), border_radius=10)
        VENTANA.blit(F_SUB.render("Letra:", True, NEGRO), (90, 210))
        VENTANA.blit(F_TIT.render(letra.upper(), True, ROJO), (115, 250))

        for i, (k, label) in enumerate(CATEGORIAS):
            VENTANA.blit(F_SUB.render(label + ":", True, NEGRO), (80, 320 + i * 60))
            cajas[i].draw(VENTANA)

        pygame.draw.rect(VENTANA, GRIS, (60, 640, 900, 60), border_radius=10)
        msg = "Escribe tus respuestas y pulsa ENVIAR o STOP!" if jugando else "Pulsa NUEVA RONDA para iniciar."
        VENTANA.blit(F_SUB.render(msg, True, NEGRO), (80, 655))

        if jugando:
            frac = tiempo / cfg["tiempo"]
            pygame.draw.rect(VENTANA, GRIS_OSCURO, (650, 60, 300, 18), border_radius=5)
            pygame.draw.rect(VENTANA, (255-int(frac*255), int(frac*200), 60), (650, 60, int(300*frac), 18), border_radius=5)
            VENTANA.blit(F_TXT.render(f"Tiempo: {int(tiempo)} s", True, NEGRO), (650, 85))

        if resultados:
            VENTANA.blit(F_SUB.render("Resultados:", True, NEGRO), (700, 180))
            VENTANA.blit(F_MONO.render(f"{'Categoría':<12}{'Humano':<15}{'Máquina':<15}{'+H/+M'}", True, NEGRO), (600, 210))
            pygame.draw.line(VENTANA, GRIS_OSCURO, (600, 230), (940, 230))
            for i, (label, h, m, ph, pm) in enumerate(resultados):
                txt = F_MONO.render(f"{label:<12}{h[:10]:<15}{m[:10]:<15}{ph:>2}/{pm:<2}", True, NEGRO)
                VENTANA.blit(txt, (600, 240 + i * 25))

        pygame.display.flip()

# =======================
# EJECUCIÓN
# =======================
if __name__ == "__main__":
    main()
