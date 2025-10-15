import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def cargar_imagen(paths_posibles):
    
    last = None
    for p in paths_posibles:
        last = p
        if p and os.path.exists(p):
            try:
                return Image.open(p), p
            except Exception:
                pass
    return None, last


class VisorFloristeria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Floristería Rossbella — Visor de Partes")
        self.geometry("900x650")
        self.configure(bg="#fafafa")

     
        self.partes = [
            {
                "nombre": "Techo",
                "rutas": [
                    os.path.join("imagenes", "techo.png"),
                    "/mnt/data/cd3a17d7-cb27-4647-8718-ebed6bc6c737.png",
                ],
                "Descripción": "Este es el techo de la floristería; es de color rosado."
            },
            {
                "nombre": "Parte delantera",
                "rutas": [
                    os.path.join("imagenes", "delantera.png"),
                    "/mnt/data/43a60ca2-dd3e-43dd-86a3-62bf49789db0.png",
                ],
                "Descripción": (
                    "Fachada con un letrero rosado que dice 'Floristería', "
                    "una puerta morada, dos macetas marrones con flores amarillas "
                    "y una cámara en la parte superior derecha."
                )
            },
            {
                "nombre": "Lateral izquierdo",
                "rutas": [
                    os.path.join("imagenes", "lateral_izquierdo.png"),
                    "/mnt/data/47f2df2e-0d60-433a-95c6-20d0a8882cd8.png",
                ],
                "Descripción": (
                    "Lateral izquierdo con cuatro enredaderas, una en cada esquina; "
                    "una maceta naranja con un girasol grande artificial y una cámara en la parte superior derecha."
                )
            },
            {
                "nombre": "Parte trasera",
                "rutas": [
                    os.path.join("imagenes", "trasera.png"),
                    "/mnt/data/73a28230-bd1f-4df2-95c9-663a9c6530f3.png",
                ],
                "Descripción": (
                    "Parte trasera con dos enredaderas que caen desde la parte superior de cada esquina hasta el suelo."
                )
            },
            {
                "nombre": "Lateral derecho",
                "rutas": [
                    os.path.join("imagenes", "lateral_derecho.png"),
                    "/mnt/data/b221c669-f880-4fc0-ad1a-fa04590adcab.png",
                ],
                "Descripción": (
                    "Lateral derecho con una ventana central y dos pequeñas enredaderas en las esquinas superiores."
                )
            },
        ]

        
        self.idx_parte = 0
        self.imagen_original = None
        self.imagen_mostrada = None

        top = tk.Frame(self, bg="#fafafa")
        top.pack(fill="x", padx=12, pady=8)

        tk.Label(top, text="Selecciona la parte:", bg="#fafafa", fg="#333", font=("Arial", 11, "bold")).pack(side="left")

        self.combo = ttk.Combobox(
            top,
            state="readonly",
            values=[p["nombre"] for p in self.partes],
            width=28
        )
        self.combo.current(self.idx_parte)
        self.combo.pack(side="left", padx=8)

        ttk.Button(top, text="Mostrar", command=self.mostrar_seleccion).pack(side="left", padx=4)
        ttk.Button(top, text="⟵ Anterior", command=self.anterior).pack(side="left", padx=6)
        ttk.Button(top, text="Siguiente ⟶", command=self.siguiente).pack(side="left")

        center = tk.Frame(self, bg="#eaeaea", bd=1, relief="sunken")
        center.pack(fill="both", expand=True, padx=12, pady=(4, 6))

        self.canvas = tk.Canvas(center, bg="#ddd", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize_canvas)

        bottom = tk.Frame(self, bg="#fafafa")
        bottom.pack(fill="x", padx=12, pady=(0, 10))

        tk.Label(bottom, text="Descripción:", bg="#fafafa", fg="#333", font=("Arial", 11, "bold")).pack(anchor="w")
        self.txt = tk.Text(bottom, height=4, wrap="word", font=("Arial", 10), bg="#ffffff")
        self.txt.pack(fill="x")
        self.txt.configure(state="disabled")

        self._load_current_part()

  
    def mostrar_seleccion(self):
        nombre = self.combo.get()
        for i, p in enumerate(self.partes):
            if p["nombre"] == nombre:
                self.idx_parte = i
                break
        self._load_current_part()

    def anterior(self):
        self.idx_parte = (self.idx_parte - 1) % len(self.partes)
        self.combo.current(self.idx_parte)
        self._load_current_part()

    def siguiente(self):
        self.idx_parte = (self.idx_parte + 1) % len(self.partes)
        self.combo.current(self.idx_parte)
        self._load_current_part()


    def _load_current_part(self):
        parte = self.partes[self.idx_parte]
        img, ruta = cargar_imagen(parte["rutas"])
        self.imagen_original = img

        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("end", f"{parte['nombre']}\n\n{parte['Descripción']}")
        if img is None:
            self.txt.insert("end", f"\n\n⚠ Imagen no encontrada.\nRevisa la ruta: {ruta}")
        self.txt.configure(state="disabled")

        self._render_to_canvas()

    def _on_resize_canvas(self, event):
        self._render_to_canvas()

    def _render_to_canvas(self):
        self.canvas.delete("all")
        if not self.imagen_original:
            return

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw <= 2 or ch <= 2:
            return

        img = self.imagen_original.copy()
        img.thumbnail((cw, ch), Image.LANCZOS)
        self.imagen_mostrada = ImageTk.PhotoImage(img)
        self.canvas.create_image(cw // 2, ch // 2, image=self.imagen_mostrada, anchor="center")


if __name__ == "__main__":
    app = VisorFloristeria()
    app.mainloop()
