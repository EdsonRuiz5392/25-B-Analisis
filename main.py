import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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



class BusquedaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación de Búsqueda Lineal vs Binaria")

       
        self.tamanos = [100, 1000, 10000, 100000]
        self.promedios = {"Lineal": [], "Binaria": []}

       
        self.crear_widgets()

    def crear_widgets(self):
       
        tk.Label(self.root, text="Repeticiones por tamaño:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_reps = tk.Entry(self.root)
        self.entry_reps.insert(0, "5")
        self.entry_reps.grid(row=0, column=1, padx=5, pady=5)

        
        self.btn_ejecutar = tk.Button(self.root, text="Ejecutar comparación en todos los tamaños", command=self.ejecutar_comparacion)
        self.btn_ejecutar.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        
        self.text_resultados = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.text_resultados.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

    def medir_tiempo(self, funcion, *args):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempo = (fin - inicio) * 1000  
        return resultado, tiempo

    def ejecutar_comparacion(self):
        try:
            repeticiones = int(self.entry_reps.get())
            self.promedios = {"Lineal": [], "Binaria": []}
            self.text_resultados.delete("1.0", tk.END)

            for tam in self.tamanos:
                lista = list(range(tam))
                valor = tam - 1  

                tiempos_lineal = []
                tiempos_binaria = []

                for _ in range(repeticiones):
                    _, t_lineal = self.medir_tiempo(busqueda_lineal, lista, valor)
                    _, t_binaria = self.medir_tiempo(busqueda_binaria, lista, valor)
                    tiempos_lineal.append(t_lineal)
                    tiempos_binaria.append(t_binaria)

                prom_lineal = sum(tiempos_lineal) / repeticiones
                prom_binaria = sum(tiempos_binaria) / repeticiones

                self.promedios["Lineal"].append(prom_lineal)
                self.promedios["Binaria"].append(prom_binaria)

                
                self.text_resultados.insert(tk.END, f"Tamaño {tam}:\n")
                self.text_resultados.insert(tk.END, f"  Promedio Lineal: {prom_lineal:.5f} ms\n")
                self.text_resultados.insert(tk.END, f"  Promedio Binaria: {prom_binaria:.5f} ms\n\n")

           
            self.actualizar_graficas()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de repeticiones.")

    def actualizar_graficas(self):
        
        self.ax1.clear()
        x = self.tamanos
        self.ax1.plot(x, self.promedios["Lineal"], label="Lineal", marker="o")
        self.ax1.plot(x, self.promedios["Binaria"], label="Binaria", marker="s")
        self.ax1.set_xscale("log")
        self.ax1.set_title("Promedio por tamaño")
        self.ax1.set_xlabel("Tamaño de lista")
        self.ax1.set_ylabel("Tiempo promedio (ms)")
        self.ax1.legend()

        # ---------------- Gráfica 2: promedio global ----------------
        self.ax2.clear()
        prom_total_lineal = sum(self.promedios["Lineal"]) / len(self.promedios["Lineal"])
        prom_total_binaria = sum(self.promedios["Binaria"]) / len(self.promedios["Binaria"])

        algoritmos = ["Lineal", "Binaria"]
        valores = [prom_total_lineal, prom_total_binaria]
        self.ax2.bar(algoritmos, valores, color=["orange", "blue"])
        self.ax2.set_title("Promedio total global")
        self.ax2.set_ylabel("Tiempo promedio (ms)")

      
        self.canvas.draw()



if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedaGUI(root)
    root.mainloop()
