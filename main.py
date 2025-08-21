import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ----------------------------
# Algoritmos de búsqueda
# ----------------------------
def busqueda_lineal(lista, x):
    for i, val in enumerate(lista):
        if val == x:
            return i
    return -1


def busqueda_binaria(lista, x):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == x:
            return medio
        elif lista[medio] < x:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


# ----------------------------
# Clase GUI
# ----------------------------
class BusquedaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación de Búsqueda Lineal vs Binaria")

        # Variables
        self.lista = []
        self.tamanos = [100, 1000, 10000, 100000]
        self.resultados = {"Lineal": [], "Binaria": []}  # Guarda tiempos por algoritmo

        # Widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Selección de tamaño
        tk.Label(self.root, text="Tamaño de la lista:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_tamano = ttk.Combobox(self.root, values=self.tamanos)
        self.combo_tamano.current(0)
        self.combo_tamano.grid(row=0, column=1, padx=5, pady=5)

        # Botón generar datos
        self.btn_generar = tk.Button(self.root, text="Generar datos", command=self.generar_datos)
        self.btn_generar.grid(row=0, column=2, padx=5, pady=5)

        # Mostrar lista generada
        tk.Label(self.root, text="Lista generada:").grid(row=1, column=0, padx=5, pady=5)
        self.text_lista = scrolledtext.ScrolledText(self.root, width=60, height=5)
        self.text_lista.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Entrada de valor a buscar
        tk.Label(self.root, text="Valor a buscar:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_valor = tk.Entry(self.root)
        self.entry_valor.grid(row=2, column=1, padx=5, pady=5)

        # Botón de búsqueda
        self.btn_comparar = tk.Button(self.root, text="Comparar búsquedas", command=self.comparar_busquedas)
        self.btn_comparar.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Resultados
        self.label_resultado = tk.Label(self.root, text="Resultados aparecerán aquí")
        self.label_resultado.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

        # Gráfica
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, pady=10)

    def generar_datos(self):
        try:
            tam = int(self.combo_tamano.get())
            # Generar lista ORDENADA consecutiva
            self.lista = list(range(tam))

            # Mostrar lista en pantalla (solo resumen si es muy grande)
            self.text_lista.delete("1.0", tk.END)
            if tam > 500:
                preview = self.lista[:100] + ["..."] + self.lista[-100:]
            else:
                preview = self.lista
            self.text_lista.insert(tk.END, str(preview))

            # Reiniciar resultados
            self.resultados = {"Lineal": [], "Binaria": []}

            messagebox.showinfo(
                "Datos generados",
                f"Lista ordenada de tamaño {tam} generada exitosamente.\n"
                f"(Rango: 0 hasta {tam-1})"
            )
        except ValueError:
            messagebox.showerror("Error", "Seleccione un tamaño válido.")

    def medir_tiempo(self, funcion, *args):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempo = (fin - inicio) * 1000  # milisegundos
        return resultado, tiempo

    def comparar_busquedas(self):
        if not self.lista:
            messagebox.showerror("Error", "Primero genere los datos.")
            return
        try:
            valor = int(self.entry_valor.get())
            repeticiones = 5  # número de repeticiones
            tiempos_lineal = []
            tiempos_binaria = []
            indice_lineal = indice_binaria = -1

            for _ in range(repeticiones):
                indice_lineal, t_lineal = self.medir_tiempo(busqueda_lineal, self.lista, valor)
                indice_binaria, t_binaria = self.medir_tiempo(busqueda_binaria, self.lista, valor)
                tiempos_lineal.append(t_lineal)
                tiempos_binaria.append(t_binaria)

            # Promedios
            prom_lineal = sum(tiempos_lineal) / repeticiones
            prom_binaria = sum(tiempos_binaria) / repeticiones

            # Guardar resultados
            self.resultados["Lineal"].append(prom_lineal)
            self.resultados["Binaria"].append(prom_binaria)

            # Mostrar resultados en pantalla
            resultado = f"Comparación de búsquedas\n"
            resultado += f"Tamaño de lista: {len(self.lista)}\n"
            resultado += f"Resultado Lineal: {'Índice ' + str(indice_lineal) if indice_lineal != -1 else 'No encontrado'}\n"
            resultado += f"Promedio tiempo Lineal: {prom_lineal:.5f} ms\n"
            resultado += f"Resultado Binaria: {'Índice ' + str(indice_binaria) if indice_binaria != -1 else 'No encontrado'}\n"
            resultado += f"Promedio tiempo Binaria: {prom_binaria:.5f} ms"
            self.label_resultado.config(text=resultado)

            # Actualizar gráfica
            self.actualizar_grafica()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido.")

    def actualizar_grafica(self):
        self.ax.clear()
        x = range(1, len(self.resultados["Lineal"]) + 1)
        self.ax.plot(x, self.resultados["Lineal"], label="Lineal", marker="o")
        self.ax.plot(x, self.resultados["Binaria"], label="Binaria", marker="s")
        self.ax.set_title("Comparación de tiempos (promedios)")
        self.ax.set_xlabel("Ejecuciones")
        self.ax.set_ylabel("Tiempo (ms)")
        self.ax.legend()
        self.canvas.draw()


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedaGUI(root)
    root.mainloop()
