import pygame, sys, random, os

# ===============================
# CONFIGURACIÓN INICIAL
# ===============================
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 600, 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TIC-TAC-TOE — Humano vs Máquina")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (70, 130, 250)
ROJO = (240, 80, 80)
VERDE = (60, 200, 100)
AMARILLO = (250, 200, 60)

# Fuentes
F_TIT = pygame.font.SysFont("arial", 48, True)
F_TXT = pygame.font.SysFont("arial", 36)
F_BTN = pygame.font.SysFont("arial", 28, True)
F_SMALL = pygame.font.SysFont("arial", 22)

# ===============================
# SONIDOS
# ===============================
def cargar_sonido(nombre):
    try:
        return pygame.mixer.Sound(nombre)
    except:
        print(f"No se encontró el sonido: {nombre}")
        return None

SND_CLIC = cargar_sonido("clic.wav")
SND_IA = cargar_sonido("ia.wav")
SND_GANAR = cargar_sonido("victoria.wav")

def reproducir(sonido):
    if sonido:
        sonido.play()

# ===============================
# CLASES
# ===============================
class Button:
    def __init__(self, rect, text, color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=8)
        txt = F_BTN.render(self.text, True, BLANCO)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def click(self, pos):
        return self.rect.collidepoint(pos)


class TicTacToe:
    def __init__(self):
        self.tablero = [""] * 9
        self.humano = "X"
        self.maquina = "O"
        self.turno_humano = True
        self.juego_terminado = False
        self.ganador = None
        self.error_rate = 0.2
        self.dificultad = "Medio"

    def set_dificultad(self, nombre):
        self.dificultad = nombre
        if nombre == "Fácil":
            self.error_rate = 0.40
        elif nombre == "Medio":
            self.error_rate = 0.20
        else:
            self.error_rate = 0.0

    def reiniciar(self):
        self.tablero = [""] * 9
        self.turno_humano = True
        self.juego_terminado = False
        self.ganador = None

    def dibujar(self):
        VENTANA.fill(BLANCO)
        titulo = F_TIT.render("TIC-TAC-TOE", True, NEGRO)
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

        dif_txt = F_SMALL.render(f"Dificultad: {self.dificultad} ({int(self.error_rate*100)}% error IA)", True, NEGRO)
        VENTANA.blit(dif_txt, (20, 80))

        tablero_x, tablero_y = 150, 200
        tam_celda = 100

        # Líneas del tablero
        for i in range(1, 3):
            pygame.draw.line(VENTANA, NEGRO, (tablero_x + i * tam_celda, tablero_y),
                             (tablero_x + i * tam_celda, tablero_y + 3 * tam_celda), 5)
            pygame.draw.line(VENTANA, NEGRO, (tablero_x, tablero_y + i * tam_celda),
                             (tablero_x + 3 * tam_celda, tablero_y + i * tam_celda), 5)

        # Fichas X y O
        for i, celda in enumerate(self.tablero):
            fila, col = divmod(i, 3)
            x = tablero_x + col * tam_celda + tam_celda // 2
            y = tablero_y + fila * tam_celda + tam_celda // 2
            if celda != "":
                color = AZUL if celda == "X" else ROJO
                pieza = F_TIT.render(celda, True, color)
                VENTANA.blit(pieza, pieza.get_rect(center=(x, y)))

        # Estado
        if self.juego_terminado:
            if self.ganador == "Empate":
                msg = "¡Empate!"
            elif self.ganador == self.humano:
                msg = "¡Ganaste! 🎉"
            else:
                msg = "Perdiste"
            texto = F_TXT.render(msg, True, NEGRO)
            VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 540))
        else:
            turno_txt = f"Turno: {'Humano' if self.turno_humano else 'Máquina'}"
            VENTANA.blit(F_TXT.render(turno_txt, True, NEGRO), (ANCHO // 2 - 100, 540))

    def clic(self, pos):
        if self.juego_terminado or not self.turno_humano:
            return
        x, y = pos
        tablero_x, tablero_y = 150, 200
        tam_celda = 100

        if tablero_x <= x <= tablero_x + 3 * tam_celda and tablero_y <= y <= tablero_y + 3 * tam_celda:
            col = (x - tablero_x) // tam_celda
            fila = (y - tablero_y) // tam_celda
            idx = int(fila * 3 + col)

            if self.tablero[idx] == "":
                self.tablero[idx] = self.humano
                reproducir(SND_CLIC)
                self.turno_humano = False
                self.verificar_estado()

    def verificar_estado(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combos:
            if self.tablero[a] and self.tablero[a] == self.tablero[b] == self.tablero[c]:
                self.juego_terminado = True
                self.ganador = self.tablero[a]
                if self.ganador == self.humano:
                    reproducir(SND_GANAR)
                return
        if "" not in self.tablero:
            self.juego_terminado = True
            self.ganador = "Empate"

    def movimiento_maquina(self):
        if self.juego_terminado:
            return
        evaluaciones = []
        for i in range(9):
            if self.tablero[i] == "":
                self.tablero[i] = self.maquina
                puntaje = self.minimax(False)
                self.tablero[i] = ""
                evaluaciones.append((puntaje, i))
        if not evaluaciones:
            return

        evaluaciones.sort(reverse=True)
        mejor_puntaje, mejor_mov = evaluaciones[0]

        if random.random() < self.error_rate and len(evaluaciones) > 1:
            _, mov = random.choice(evaluaciones[1:])
        else:
            mov = mejor_mov

        self.tablero[mov] = self.maquina
        reproducir(SND_IA)
        self.turno_humano = True
        self.verificar_estado()

    def minimax(self, es_max):
        self.verificar_estado()
        if self.juego_terminado:
            if self.ganador == self.maquina:
                r = 1
            elif self.ganador == self.humano:
                r = -1
            else:
                r = 0
            self.juego_terminado = False
            self.ganador = None
            return r

        if es_max:
            mejor = -999
            for i in range(9):
                if self.tablero[i] == "":
                    self.tablero[i] = self.maquina
                    valor = self.minimax(False)
                    self.tablero[i] = ""
                    mejor = max(mejor, valor)
            return mejor
        else:
            peor = 999
            for i in range(9):
                if self.tablero[i] == "":
                    self.tablero[i] = self.humano
                    valor = self.minimax(True)
                    self.tablero[i] = ""
                    peor = min(peor, valor)
            return peor


# ===============================
# FUNCIÓN PRINCIPAL
# ===============================
def main():
    juego = TicTacToe()

    btn_x = Button((120, 600, 120, 44), "Soy X", AZUL)
    btn_o = Button((260, 600, 120, 44), "Soy O", ROJO)
    btn_reset = Button((400, 600, 120, 44), "Reiniciar", VERDE)
    btn_easy = Button((70, 110, 120, 36), "Fácil", AMARILLO)
    btn_medium = Button((210, 110, 120, 36), "Medio", AZUL)
    btn_hard = Button((350, 110, 120, 36), "Difícil", ROJO)

    juego.set_dificultad("Medio")

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_x.click(e.pos):
                    juego.humano, juego.maquina = "X", "O"
                    juego.turno_humano = True
                    juego.reiniciar()
                elif btn_o.click(e.pos):
                    juego.humano, juego.maquina = "O", "X"
                    juego.turno_humano = False
                    juego.reiniciar()
                elif btn_reset.click(e.pos):
                    juego.reiniciar()
                elif btn_easy.click(e.pos):
                    juego.set_dificultad("Fácil")
                elif btn_medium.click(e.pos):
                    juego.set_dificultad("Medio")
                elif btn_hard.click(e.pos):
                    juego.set_dificultad("Difícil")
                else:
                    juego.clic(e.pos)

        if not juego.turno_humano and not juego.juego_terminado:
            pygame.time.wait(300)
            juego.movimiento_maquina()

        juego.dibujar()
        btn_x.draw(VENTANA)
        btn_o.draw(VENTANA)
        btn_reset.draw(VENTANA)
        btn_easy.draw(VENTANA)
        btn_medium.draw(VENTANA)
        btn_hard.draw(VENTANA)
        pygame.display.flip()


if __name__ == "__main__":
    main()
