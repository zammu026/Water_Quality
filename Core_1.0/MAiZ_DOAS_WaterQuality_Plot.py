import MAiZ_DOAS_WaterQuality_IPM as ipm
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = False # Cambiar a True solo si LaTeX está configurado en Windows
plt.rcParams["axes.linewidth"] = 4.0
plt.rcParams["xtick.labelsize"] = 24
plt.rcParams["ytick.labelsize"] = 24
plt.rcParams["font.weight"] = 'bold'
plt.rcParams["xtick.major.pad"] = 10
plt.rcParams["ytick.major.pad"] = 10

class Plt_Fit:
    def __init__(self, fig, ax, wav, rf_mea, rf_sim):
        # Se eliminó plt.ion() y plt.show()
        self.fig_fit = fig
        self.ax_fit = ax
        self.ax_fit.clear()
        
        self.axs_specs = {'family': 'serif', 'color': 'black', 'size': 20}
        self.tit_specs = {'family': 'serif', 'color': 'black', 'size': 24}
        
        self.ax_fit.set_xlim(ipm.wav_sta, ipm.wav_end)
        self.ax_fit.set_ylim(ipm.ref_sta, ipm.ref_end)
        self.ax_fit.set_xlabel("Wavelength (nm)", fontdict=self.axs_specs)
        self.ax_fit.set_ylabel("Reflectance (%)", fontdict=self.axs_specs)
        
        self.ln_mea, = self.ax_fit.plot(wav, rf_mea, c="b", lw=5.0, label="Measured WQ")
        self.ln_sim, = self.ax_fit.plot(wav, rf_sim, c="r", lw=5.0, label="Simulated MA&Z-DOAS")
        self.ite_fit = 0
        self.ax_fit.legend(fontsize=18)

    def Plt_Upd(self, par, rf_upt, rf_typ):
        self.ite_fit += 1
        self.ax_fit.set_title("Iteration fit " + str(self.ite_fit) + "\n" + par, fontdict=self.tit_specs)
        
        if rf_typ == 0: 
            self.ln_mea.set_ydata(rf_upt)
        else: 
            self.ln_sim.set_ydata(rf_upt)
            
        # Actualiza eventos sin bloquear el bucle principal de la GUI
        self.fig_fit.canvas.draw_idle()
        self.fig_fit.canvas.flush_events()
