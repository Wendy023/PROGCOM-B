import tkinter as tk
import random
from tkinter import messagebox

class JuegoAritmetico:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego Educativo de Matematicas")
        self.root.geometry("400x350")
        self.puntaje = 0
        self.intentos = 0
        self.crear_interfaz()
        self.nueva_pregunta()

    def crear_interfaz(self):
        # Fondo colorido
        self.root.configure(bg="#e0f7fa")
        # Título
        self.label_titulo = tk.Label(self.root, text="¡Aprende sumas, restas, multiplicaciones y divisiones!", font=("Comic Sans MS", 15, "bold"), wraplength=380, bg="#e0f7fa", fg="#00796b")
        self.label_titulo.pack(pady=10)
        # Pregunta
        self.label_pregunta = tk.Label(self.root, text="", font=("Comic Sans MS", 22, "bold"), bg="#e0f7fa", fg="#3949ab")
        self.label_pregunta.pack(pady=20)
        # Entrada
        self.entry_respuesta = tk.Entry(self.root, font=("Comic Sans MS", 18), justify="center", bg="#fffde7", fg="#263238", relief="solid", bd=2)
        self.entry_respuesta.pack(pady=10)
        # Botón comprobar
        self.boton_comprobar = tk.Button(self.root, text="✔ Comprobar", font=("Comic Sans MS", 14, "bold"), command=self.comprobar_respuesta, bg="#4dd0e1", fg="#004d40", activebackground="#00bcd4", activeforeground="#fff", relief="groove", bd=3, cursor="hand2")
        self.boton_comprobar.pack(pady=10, ipadx=10, ipady=3)
        # Feedback
        self.label_feedback = tk.Label(self.root, text="", font=("Comic Sans MS", 16, "bold"), bg="#e0f7fa")
        self.label_feedback.pack(pady=10)
        # Puntaje
        self.label_puntaje = tk.Label(self.root, text="Puntaje: 0 | Intentos: 0", font=("Comic Sans MS", 13, "bold"), bg="#e0f7fa", fg="#00796b")
        self.label_puntaje.pack(pady=10)
        # Botón siguiente
        self.boton_nueva = tk.Button(self.root, text="⏭ Siguiente", font=("Comic Sans MS", 13, "bold"), command=self.nueva_pregunta, bg="#ffd54f", fg="#6d4c41", activebackground="#ffb300", activeforeground="#fff", relief="groove", bd=3, cursor="hand2")
        self.boton_nueva.pack(pady=5, ipadx=8, ipady=2)

    def nueva_pregunta(self):
        self.entry_respuesta.delete(0, tk.END)
        self.label_feedback.config(text="")
        operaciones = ['+', '-', '×', '÷']
        self.operacion = random.choice(operaciones)
        if self.operacion == '+':
            a, b = random.randint(1, 50), random.randint(1, 50)
            self.respuesta = a + b
        elif self.operacion == '-':
            a, b = random.randint(1, 50), random.randint(1, 50)
            if b > a:
                a, b = b, a
            self.respuesta = a - b
        elif self.operacion == '×':
            a, b = random.randint(2, 12), random.randint(2, 12)
            self.respuesta = a * b
        else:  # División
            b = random.randint(2, 12)
            self.respuesta = random.randint(2, 12)
            a = self.respuesta * b
        self.label_pregunta.config(text=f"¿Cuánto es {a} {self.operacion} {b}?")

    def comprobar_respuesta(self):
        try:
            user = float(self.entry_respuesta.get())
            correcto = abs(user - self.respuesta) < 0.01
        except:
            self.label_feedback.config(text="Por favor ingresa un número válido", fg="orange", bg="#e0f7fa")
            return
        self.intentos += 1
        if correcto:
            self.puntaje += 1
            self.label_feedback.config(text="¡Correcto! 🎉", fg="#388e3c", bg="#c8e6c9")
        else:
            self.label_feedback.config(text=f"Incorrecto. La respuesta era {self.respuesta}", fg="#d32f2f", bg="#ffcdd2")
        self.label_puntaje.config(text=f"Puntaje: {self.puntaje} | Intentos: {self.intentos}")
        # Nueva pregunta automática tras 1.2 segundos
        self.root.after(1200, self.nueva_pregunta)

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoAritmetico(root)
    root.mainloop()
