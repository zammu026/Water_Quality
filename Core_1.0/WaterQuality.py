import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import MAiZ_DOAS_WaterQuality_RaW as raw
import MAiZ_DOAS_WaterQuality_Plot as plot_wq
import MAiZ_DOAS_WaterQuality_Models as wqm

# Herencia múltiple obligatoria para fusionar Drag&Drop con CustomTkinter
class CTkDOAS(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Configuración visual global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DOASApp(CTkDOAS):
    def __init__(self):
        super().__init__()
        self.title("MAiZ DOAS - Water Quality Analysis System")
        self.geometry("1280x800")
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        self.ruta_offset = None
        self.ruta_referencia = None
        
        # Estructura de cuadrícula: 1 fila, 2 columnas (Sidebar y Main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._construir_sidebar()
        self._construir_panel_central()

    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        lbl_titulo = ctk.CTkLabel(self.sidebar, text="Calibración\nÓptica", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_titulo.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        # Bloque Offset
        self.btn_offset = ctk.CTkButton(self.sidebar, text="1. Cargar Offset", height=40, font=ctk.CTkFont(weight="bold"), command=self.seleccionar_offset)
        self.btn_offset.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.lbl_offset = ctk.CTkLabel(self.sidebar, text="Ausente", text_color="#ff4d4d", font=ctk.CTkFont(size=12))
        self.lbl_offset.grid(row=2, column=0, padx=20, pady=(2, 20))
        
        # Bloque Referencia
        self.btn_ref = ctk.CTkButton(self.sidebar, text="2. Cargar Referencia", height=40, font=ctk.CTkFont(weight="bold"), command=self.seleccionar_referencia)
        self.btn_ref.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.lbl_ref = ctk.CTkLabel(self.sidebar, text="Ausente", text_color="#ff4d4d", font=ctk.CTkFont(size=12))
        self.lbl_ref.grid(row=4, column=0, padx=20, pady=(2, 20))
        
        # Indicador de estado del sistema
        self.lbl_status = ctk.CTkLabel(self.sidebar, text="Sistema en espera...", font=ctk.CTkFont(size=12, slant="italic"))
        self.lbl_status.grid(row=7, column=0, padx=20, pady=20, sticky="s")

    def _construir_panel_central(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Zona de Drag & Drop rediseñada
        self.lbl_drop = ctk.CTkLabel(
            self.main_frame, 
            text="ARRASTRA LOS ESPECTROS DE MEDIDA AQUÍ", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#999999",
            fg_color="#1a1a1a",
            corner_radius=10,
            height=100
        )
        self.lbl_drop.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.lbl_drop.drop_target_register(DND_FILES)
        self.lbl_drop.dnd_bind('<<Drop>>', self.procesar_medidas)
        
        # Gráfico incrustado
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='#2b2b2b')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def seleccionar_offset(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Offset", filetypes=[("Archivos TXT", "*.txt")])
        if ruta:
            self.ruta_offset = ruta
            self.lbl_offset.configure(text=Path(ruta).name, text_color="#00cc66")

    def seleccionar_referencia(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Referencia", filetypes=[("Archivos TXT", "*.txt")])
        if ruta:
            self.ruta_referencia = ruta
            self.lbl_ref.configure(text=Path(ruta).name, text_color="#00cc66")

    def procesar_medidas(self, event):
        if not self.ruta_offset or not self.ruta_referencia:
            messagebox.showwarning("Advertencia", "Los archivos de calibración (Offset y Referencia) son obligatorios.")
            return

        archivos = self.tk.splitlist(event.data)
        for ruta_medida in archivos:
            self.ejecutar_fiteo(ruta_medida)

    def ejecutar_fiteo(self, ruta_medida):
        try:
            nombre = Path(ruta_medida).name
            self.lbl_drop.configure(text=f"Procesando algoritmo para: {nombre}", text_color="#ffcc00")
            self.lbl_status.configure(text=f"Ajustando {nombre}...")
            self.update()

            rflc_wav, rflc_mea, rflc_sim = raw.calcular_reflectancia(
                ruta_medida=ruta_medida,
                ruta_referencia=self.ruta_referencia,
                ruta_offset=self.ruta_offset
            )

            plt_obj = plot_wq.Plt_Fit(self.fig, self.ax, rflc_wav, rflc_mea, rflc_mea)
            self.canvas.draw()

            c, c_sigma = wqm.WaterQuality_Fit(plt_obj, rflc_wav, rflc_mea, rflc_sim)

            self.lbl_drop.configure(text="MODELO CONVERGIDO. ARRASTRA MÁS MEDIDAS.", text_color="#00cc66")
            self.lbl_status.configure(text="En espera...")
        except Exception as e:
            messagebox.showerror("Error Matemático", f"Falla de convergencia o lectura en {Path(ruta_medida).name}:\n\n{str(e)}")
            self.lbl_drop.configure(text="ARRASTRA LOS ESPECTROS DE MEDIDA AQUÍ", text_color="#999999")

    def cerrar_aplicacion(self):
        try:
            plt.close('all')
            self.quit()
            self.destroy()
        except Exception:
            pass
        finally:
            sys.exit(0)

if __name__ == "__main__":
    app = DOASApp()
    app.mainloop()