import MAiZ_DOAS_WaterQuality_IPM as ipm
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = False
plt.rcParams["axes.linewidth"] = 2.0
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["font.weight"] = 'bold'

# Forzar estilo profesional oscuro
plt.style.use('dark_background')

class Plt_Fit:
    def __init__(self, fig, ax, wav, rf_mea, rf_sim):
        self.fig_fit = fig
        self.ax_fit = ax
        self.ax_fit.clear()
        
        # Sincronizar el color de fondo exacto con CustomTkinter
        self.fig_fit.patch.set_facecolor('#2b2b2b')
        self.ax_fit.set_facecolor('#2b2b2b')
        
        self.axs_specs = {'family': 'sans-serif', 'color': 'white', 'size': 14}
        self.tit_specs = {'family': 'sans-serif', 'color': 'white', 'size': 16}
        
        self.ax_fit.set_xlim(ipm.wav_sta, ipm.wav_end)
        self.ax_fit.set_ylim(ipm.ref_sta, ipm.ref_end)
        self.ax_fit.set_xlabel("Wavelength (nm)", fontdict=self.axs_specs)
        self.ax_fit.set_ylabel("Reflectance (%)", fontdict=self.axs_specs)
        
        # Colores de línea de alto contraste para proyecciones
        self.ln_mea, = self.ax_fit.plot(wav, rf_mea, c="#00ffcc", lw=3.0, label="Measured WQ", alpha=0.8)
        self.ln_sim, = self.ax_fit.plot(wav, rf_sim, c="#ff3366", lw=3.0, label="Simulated Fit")
        self.ite_fit = 0
        
        # Leyenda sin fondo para no tapar datos
        self.ax_fit.legend(fontsize=12, frameon=False, loc="upper right")
        self.ax_fit.grid(True, color='#555555', linestyle='--', alpha=0.5)

    def Plt_Upd(self, par, rf_upt, rf_typ):
        self.ite_fit += 1
        self.ax_fit.set_title(f"Fit Iteration {self.ite_fit}\n{par}", fontdict=self.tit_specs, pad=15)
        
        if rf_typ == 0: 
            self.ln_mea.set_ydata(rf_upt)
        else: 
            self.ln_sim.set_ydata(rf_upt)
            
        self.fig_fit.canvas.draw_idle()
        self.fig_fit.canvas.flush_events()