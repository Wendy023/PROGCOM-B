import pygame, sys, random, time

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
pygame.init()
ANCHO, ALTO = 600, 750
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cajero Automático GP3")

# COLORES
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (220, 220, 220)
GRIS_OSCURO = (160, 160, 160)
AZUL = (70, 130, 250)
VERDE = (60, 200, 100)
ROJO = (240, 80, 80)
DORADO = (250, 220, 90)

# FUENTES
F_TIT = pygame.font.SysFont("arial", 42, True)
F_TXT = pygame.font.SysFont("arial", 24)
F_BTN = pygame.font.SysFont("arial", 28, True)


# ==============================
# CLASES BASE
# ==============================
class Boton:
    def __init__(self, rect, texto, color):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=6)
        texto = F_BTN.render(self.texto, True, BLANCO)
        surf.blit(texto, texto.get_rect(center=self.rect.center))

    def click(self, pos):
        return self.rect.collidepoint(pos)


# ==============================
# CLASE CAJERO (LÓGICA)
# ==============================
class Cajero:
    def __init__(self):
        self.billetes = {100000: 5, 50000: 8, 20000: 10, 10000: 10, 5000: 10}

    def total_disponible(self):
        return sum(v * k for k, v in self.billetes.items())

    def retirar(self, monto):
        if monto > self.total_disponible() or monto <= 0:
            return None

        original = self.billetes.copy()
        entregados = {}
        for valor in sorted(self.billetes.keys(), reverse=True):
            while monto >= valor and self.billetes[valor] > 0:
                monto -= valor
                self.billetes[valor] -= 1
                entregados[valor] = entregados.get(valor, 0) + 1

        if monto != 0: 
            self.billetes = original
            return None

        return entregados

    def fuera_servicio(self):
        return self.total_disponible() <= 0


# ==============================
# CLASE INTERFAZ (GRÁFICA)
# ==============================
class Interfaz:
    def __init__(self):
        self.cajero = Cajero()
        self.monto = ""
        self.mensaje = ""
        self.resultado = {}

        self.boton_retirar = Boton((150, 640, 130, 50), "Retirar", VERDE)
        self.boton_limpiar = Boton((320, 640, 130, 50), "Limpiar", AZUL)
        self.crear_teclado()

    def crear_teclado(self):
        self.botones_num = []
        x0, y0 = 160, 350
        w, h = 80, 60
        num = 1
        for fila in range(3):
            for col in range(3):
                self.botones_num.append(Boton((x0 + col * 90, y0 + fila * 70, w, h), str(num), GRIS_OSCURO))
                num += 1
        self.botones_num.append(Boton((x0 + 90, y0 + 3 * 70, w, h), "0", GRIS_OSCURO))
        self.botones_num.append(Boton((x0 + 2 * 90, y0 + 3 * 70, w, h), "←", ROJO))

    def manejar_evento(self, pos):
        for b in self.botones_num:
            if b.click(pos):
                if b.texto == "←":
                    self.monto = self.monto[:-1]
                else:
                    self.monto += b.texto
                return

        # Retirar
        if self.boton_retirar.click(pos):
            if self.monto.isdigit():
                monto = int(self.monto)
                billetes = self.cajero.retirar(monto)
                if billetes:
                    self.resultado = billetes
                    self.animar_billetes(billetes)
                    self.monto = ""
                    self.mensaje = ""
                else:
                    self.mensaje = "Monto no disponible."
            else:
                self.mensaje = "Ingrese un número válido."

        # Limpiar
        if self.boton_limpiar.click(pos):
            self.monto = ""
            self.mensaje = ""
            self.resultado = {}

    def dibujar(self):
        VENTANA.fill(BLANCO)
        titulo = F_TIT.render("CAJERO AUTOMÁTICO", True, NEGRO)
        VENTANA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))

        # Cuadro monto
        pygame.draw.rect(VENTANA, GRIS, (ANCHO//2 - 130, 120, 260, 50), border_radius=5)
        pygame.draw.rect(VENTANA, NEGRO, (ANCHO//2 - 130, 120, 260, 50), 2, border_radius=5)
        texto_monto = F_TXT.render(self.monto if self.monto else "Digite monto...", True, NEGRO)
        VENTANA.blit(texto_monto, (ANCHO//2 - texto_monto.get_width()//2, 135))

        # Cuadro de resultados
        pygame.draw.rect(VENTANA, GRIS, (110, 190, 370, 120), border_radius=5)
        VENTANA.blit(F_TXT.render("Billetes entregados:", True, NEGRO), (130, 200))
        y = 230
        for valor, cant in self.resultado.items():
            VENTANA.blit(F_TXT.render(f"${valor:,} x {cant}", True, NEGRO), (150, y))
            y += 25

        # Teclado
        for b in self.botones_num:
            b.draw(VENTANA)

        # Botones principales
        self.boton_retirar.draw(VENTANA)
        self.boton_limpiar.draw(VENTANA)

        # Total
        total_txt = F_TXT.render(f"Total disponible: ${self.cajero.total_disponible():,}", True, NEGRO)
        VENTANA.blit(total_txt, (30, 710))

        # Mensaje o fuera de servicio
        if self.cajero.fuera_servicio():
            fs_txt = F_TXT.render("Fuera de servicio", True, ROJO)
            VENTANA.blit(fs_txt, (400, 710))
        elif self.mensaje:
            msg_txt = F_TXT.render(self.mensaje, True, ROJO)
            VENTANA.blit(msg_txt, (150, 310))

    # ==============================
    # ANIMACIÓN DE BILLETES
    # ==============================
    def animar_billetes(self, billetes):
        billete_sprites = []
        for valor, cantidad in billetes.items():
            for _ in range(cantidad):
                x = 230 + random.randint(-20, 20)
                y = 540
                billete_sprites.append({
                    "valor": valor,
                    "rect": pygame.Rect(x, y, 140, 50),
                    "vel": random.uniform(-2.5, -4.5)
                })

        tiempo_inicio = time.time()
        duracion = 3

        while time.time() - tiempo_inicio < duracion:
            pygame.event.pump()
            VENTANA.fill(BLANCO)
            self.dibujar_estatico()

            for b in billete_sprites:
                b["rect"].y += b["vel"]
                pygame.draw.rect(VENTANA, DORADO, b["rect"], border_radius=8)
                t = F_TXT.render(f"${b['valor']:,}", True, NEGRO)
                VENTANA.blit(t, t.get_rect(center=b["rect"].center))

            pygame.display.flip()
            pygame.time.wait(30)

    def dibujar_estatico(self):
        """Dibuja todo menos los billetes"""
        VENTANA.fill(BLANCO)
        titulo = F_TIT.render("CAJERO AUTOMÁTICO", True, NEGRO)
        VENTANA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))

        pygame.draw.rect(VENTANA, GRIS, (ANCHO//2 - 130, 120, 260, 50), border_radius=5)
        pygame.draw.rect(VENTANA, NEGRO, (ANCHO//2 - 130, 120, 260, 50), 2, border_radius=5)
        texto_monto = F_TXT.render(self.monto if self.monto else "Digite monto...", True, NEGRO)
        VENTANA.blit(texto_monto, (ANCHO//2 - texto_monto.get_width()//2, 135))

        for b in self.botones_num: b.draw(VENTANA)
        self.boton_retirar.draw(VENTANA)
        self.boton_limpiar.draw(VENTANA)
        total_txt = F_TXT.render(f"Total disponible: ${self.cajero.total_disponible():,}", True, NEGRO)
        VENTANA.blit(total_txt, (30, 710))


# ==============================
# LOOP PRINCIPAL
# ==============================
def main():
    interfaz = Interfaz()
    reloj = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                interfaz.manejar_evento(e.pos)

        interfaz.dibujar()
        pygame.display.flip()
        reloj.tick(60)


# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    main()
