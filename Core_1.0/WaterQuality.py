import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pathlib import Path

import MAiZ_DOAS_WaterQuality_RaW as raw
import MAiZ_DOAS_WaterQuality_Plot as plot_wq
import MAiZ_DOAS_WaterQuality_Models as wqm

class DOASApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("MAiZ DOAS - Water Quality Fitter")
        self.geometry("1100x900")
        
        self.ruta_offset = None
        self.ruta_referencia = None
        
        # Panel superior: Controles de Calibración
        frame_calibracion = tk.Frame(self, pady=10)
        frame_calibracion.pack(fill=tk.X, padx=20)
        
        # Selector de Offset
        btn_offset = tk.Button(frame_calibracion, text="Seleccionar Offset", font=("Arial", 10, "bold"), command=self.seleccionar_offset)
        btn_offset.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_offset = tk.Label(frame_calibracion, text="No cargado", fg="red", anchor="w", font=("Arial", 9))
        self.lbl_offset.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Selector de Referencia
        btn_ref = tk.Button(frame_calibracion, text="Seleccionar Referencia", font=("Arial", 10, "bold"), command=self.seleccionar_referencia)
        btn_ref.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_ref = tk.Label(frame_calibracion, text="No cargado", fg="red", anchor="w", font=("Arial", 9))
        self.lbl_ref.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Zona de Drag & Drop para las Medidas
        self.lbl_drop = tk.Label(
            self, 
            text="ARRASTRA AQUÍ LOS ARCHIVOS DE MEDIDAS (.TXT)", 
            bg="#d3d3d3", 
            font=("Arial", 14, "bold"), 
            height=3,
            relief="groove"
        )
        self.lbl_drop.pack(pady=10, fill=tk.X, padx=20)
        
        # Lienzo de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Enlace del evento Drop
        self.lbl_drop.drop_target_register(DND_FILES)
        self.lbl_drop.dnd_bind('<<Drop>>', self.procesar_medidas)

    def seleccionar_offset(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Offset", filetypes=[("Archivos TXT", "*.txt")])
        if ruta:
            self.ruta_offset = ruta
            self.lbl_offset.config(text=Path(ruta).name, fg="green")

    def seleccionar_referencia(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Referencia", filetypes=[("Archivos TXT", "*.txt")])
        if ruta:
            self.ruta_referencia = ruta
            self.lbl_ref.config(text=Path(ruta).name, fg="green")

    def procesar_medidas(self, event):
        if not self.ruta_offset or not self.ruta_referencia:
            messagebox.showwarning("Faltan Datos", "Debes seleccionar primero los archivos de Offset y Referencia.")
            return

        archivos = self.tk.splitlist(event.data)
        for ruta_medida in archivos:
            self.ejecutar_fiteo(ruta_medida)

    def ejecutar_fiteo(self, ruta_medida):
        try:
            nombre = Path(ruta_medida).name
            self.lbl_drop.config(text=f"Procesando: {nombre}", bg="#ffeb99")
            self.update()

            # Cálculo de reflectancia pasando los tres archivos requeridos
            rflc_wav, rflc_mea, rflc_sim = raw.calcular_reflectancia(
                ruta_medida=ruta_medida,
                ruta_referencia=self.ruta_referencia,
                ruta_offset=self.ruta_offset
            )

            # Ploteo y ajuste
            plt_obj = plot_wq.Plt_Fit(self.fig, self.ax, rflc_wav, rflc_mea, rflc_mea)
            self.canvas.draw()

            c, c_sigma = wqm.WaterQuality_Fit(plt_obj, rflc_wav, rflc_mea, rflc_sim)

            self.lbl_drop.config(text=f"Fiteo completado para {nombre}. Arrastra más medidas.", bg="#c2f0c2")
        except Exception as e:
            messagebox.showerror("Error de Ajuste", f"Fallo al procesar {Path(ruta_medida).name}:\n{str(e)}")
            self.lbl_drop.config(text="ARRASTRA AQUÍ LOS ARCHIVOS DE MEDIDAS (.TXT)", bg="#d3d3d3")

print("Iniciando ventana...")
app = DOASApp()
print("Entrando a mainloop...")
app.mainloop()
print("Ventana cerrada.")