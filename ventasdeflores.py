import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Floristeria:
    def __init__(self, root):
        self.root = root
        self.root.title(" Floristería Rossbella ")
        self.root.geometry("700x600")
        self.root.configure(bg="#f9f9f9")

        # Diccionarios base
        self.inventario = {}
        self.ventas = []
        self.total_ventas = 0

        self.crear_interfaz_registro()

    def crear_interfaz_registro(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=" Registro Inicial de Flores ",
            bg="#f9f9f9",
            fg="#3d7a33",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        frame_registro = tk.LabelFrame(self.root, text="Agregar Flor", bg="#f9f9f9", font=("Arial", 12, "bold"))
        frame_registro.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_registro, text="Nombre de la Flor:", bg="#f9f9f9").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_registro, width=20)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_registro, text="Precio:", bg="#f9f9f9").grid(row=0, column=2, padx=5, pady=5)
        self.entry_precio = tk.Entry(frame_registro, width=10)
        self.entry_precio.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_registro, text="Cantidad:", bg="#f9f9f9").grid(row=0, column=4, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(frame_registro, width=10)
        self.entry_cantidad.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(frame_registro, text="Agregar Flor", command=self.agregar_flor, bg="#b6e2a1").grid(row=0, column=6, padx=10, pady=5)

        self.texto_flores = tk.Text(self.root, height=10, width=80, bg="#fff", font=("Arial", 10))
        self.texto_flores.pack(padx=10, pady=10)

        tk.Button(self.root, text="Iniciar Ventas", command=self.iniciar_ventas, bg="#add8e6", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit, bg="#f4a3a3", font=("Arial", 11)).pack(pady=5)

    def agregar_flor(self):
        nombre = self.entry_nombre.get().strip().capitalize()
        precio = self.entry_precio.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if not nombre or not precio or not cantidad:
            messagebox.showwarning("Datos incompletos", "Por favor complete todos los campos ")
            return

        try:
            precio = int(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser números enteros ")
            return

        if nombre in self.inventario:
            messagebox.showinfo("Ya existe", f"La flor {nombre} ya está registrada ")
            return

        self.inventario[nombre] = {"precio": precio, "cantidad": cantidad}
        messagebox.showinfo("Flor agregada", f" Se agregó {nombre} (${precio}, {cantidad} unidades)")
        self.actualizar_lista_flores()

        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)

    def actualizar_lista_flores(self):
        self.texto_flores.delete(1.0, tk.END)
        self.texto_flores.insert(tk.END, " Flores registradas:\n\n")
        for flor, datos in self.inventario.items():
            self.texto_flores.insert(tk.END, f"{flor}: ${datos['precio']} | Cantidad: {datos['cantidad']}\n")


    def iniciar_ventas(self):
        if not self.inventario:
            messagebox.showwarning("Sin flores", "Debe registrar al menos una flor para comenzar ")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=" Floristería Rossbella - Ventas del Día ",
            bg="#f9f9f9",
            fg="#3d7a33",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        frame_inventario = tk.LabelFrame(self.root, text="Inventario Actual", bg="#f9f9f9", font=("Arial", 12, "bold"))
        frame_inventario.pack(padx=20, pady=10, fill="both", expand=True)

        self.texto_inventario = tk.Text(frame_inventario, height=10, width=70, bg="#fff", font=("Arial", 10))
        self.texto_inventario.pack(padx=10, pady=10)

        frame_venta = tk.LabelFrame(self.root, text="Vender Flores", bg="#f9f9f9", font=("Arial", 12, "bold"))
        frame_venta.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_venta, text="Flor:", bg="#f9f9f9").grid(row=0, column=0, padx=5, pady=5)
        self.combo_flor = ttk.Combobox(frame_venta, values=list(self.inventario.keys()), state="readonly", width=20)
        self.combo_flor.grid(row=0, column=1, padx=5, pady=5)
        self.combo_flor.set("Seleccione una flor")

        tk.Label(frame_venta, text="Cantidad:", bg="#f9f9f9").grid(row=0, column=2, padx=5, pady=5)
        self.cantidad_entry = tk.Spinbox(frame_venta, from_=1, to=100, width=10)
        self.cantidad_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(frame_venta, text="Realizar Venta", command=self.vender, bg="#b6e2a1", font=("Arial", 10)).grid(row=0, column=4, padx=10, pady=5)

        frame_botones = tk.Frame(self.root, bg="#f9f9f9")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Cerrar Tienda", command=self.cerrar_tienda, bg="#f4a3a3").pack(side="left", padx=5)
        tk.Button(frame_botones, text="Salir", command=self.root.quit, bg="#e88b8b").pack(side="left", padx=5)

        self.label_total = tk.Label(self.root, text="Total Ganado: $0", bg="#f9f9f9", fg="#3d7a33", font=("Arial", 12, "bold"))
        self.label_total.pack(pady=5)

        self.actualizar_inventario()

    def actualizar_inventario(self):
        self.texto_inventario.delete(1.0, tk.END)
        self.texto_inventario.insert(tk.END, " FLORES DISPONIBLES \n\n")
        for flor, datos in self.inventario.items():
            self.texto_inventario.insert(
                tk.END, f"{flor}: ${datos['precio']} | Cantidad disponible: {datos['cantidad']}\n"
            )
        self.texto_inventario.insert(tk.END, f"\n Total acumulado: ${self.total_ventas}")

        self.combo_flor["values"] = list(self.inventario.keys())

    def vender(self):
        flor = self.combo_flor.get()
        if flor not in self.inventario:
            messagebox.showerror("No disponible", f"La flor '{flor}' no está disponible 🌾")
            return

        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        stock = self.inventario[flor]["cantidad"]
        precio = self.inventario[flor]["precio"]

        if cantidad > stock:
            messagebox.showwarning("Stock insuficiente", f"Solo quedan {stock} unidades de {flor}.")
            return

        total = cantidad * precio
        self.total_ventas += total
        self.ventas.append((flor, cantidad, total))
        self.inventario[flor]["cantidad"] -= cantidad

        messagebox.showinfo("Venta exitosa", f" Vendiste {cantidad} {flor}\n Total: ${total}")

        if self.inventario[flor]["cantidad"] == 0:
            messagebox.showinfo("Sin stock", f" {flor} se ha agotado.")
            del self.inventario[flor]

        self.label_total.config(text=f"Total Ganado: ${self.total_ventas}")
        self.actualizar_inventario()

    def cerrar_tienda(self):
        if not self.ventas:
            messagebox.showinfo("Cierre", "Hoy no se realizaron ventas ")
            return

        fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"ventas_del_dia_{fecha}.txt"

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(" FLORISTERÍA ROSSBELLA \n")
            archivo.write(f"🗓 Fecha: {datetime.datetime.now()}\n\n")
            archivo.write("VENTAS DEL DÍA:\n")
            archivo.write("---------------------------------\n")
            for flor, cantidad, total in self.ventas:
                archivo.write(f"{flor} - {cantidad} unidades - Total: ${total}\n")
            archivo.write("---------------------------------\n")
            archivo.write(f" TOTAL GANADO: ${self.total_ventas}\n")

        messagebox.showinfo("Cierre de Tienda", f" Total del día: ${self.total_ventas}")
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = Floristeria(root)
    root.mainloop()
