import MAiZ_DOAS_WaterQuality_IPM as ipm

import matplotlib.pyplot as plt
plt.rcParams["text.usetex"] = True
plt.rcParams["axes.linewidth"] = 4.0
plt.rcParams["xtick.labelsize"] = 34
plt.rcParams["ytick.labelsize"] = 34
plt.rcParams["font.weight"] = 'bold'
plt.rcParams["xtick.major.pad"] = 10
plt.rcParams["ytick.major.pad"] = 10

class Plt_Fit:
    def __init__(self,wav,rf_mea,rf_sim):
        plt.ion()  # turning interactive mode on
        self.axs_specs={'family': 'serif', 'color': 'black','size':38}
        self.tit_specs={'family': 'serif', 'color': 'black','size':42}
        self.fig_fit,self.ax_fit=plt.subplots()
        self.ax_fit.set_xlim(ipm.wav_sta,ipm.wav_end)
        self.ax_fit.set_ylim(ipm.ref_sta,ipm.ref_end)
        self.ax_fit.set_xlabel("Wavelength (nm)",fontdict=self.axs_specs)
        self.ax_fit.set_ylabel("Reflectance (\%)",fontdict=self.axs_specs)
        self.ln_mea,=self.ax_fit.plot(wav,rf_mea,c="b",lw=10.0,label="Measured WQ")
        self.ln_sim,=self.ax_fit.plot(wav,rf_sim,c="r",lw=10.0,label="Measured MA\&Z-DOAS")
        self.ite_fit=0
        plt.legend(fontsize=34)
        plt.show() #block=True

    def Plt_Upd(self,par,rf_upt,rf_typ):
        self.ite_fit+=1
        self.ax_fit.set_title("Iteration fit "+str(self.ite_fit)+"\n"+par,fontdict=self.tit_specs)
        if rf_typ==0: self.ln_mea.set_ydata(rf_upt)
        else: self.ln_sim.set_ydata(rf_upt)
        self.fig_fit.canvas.draw()
        plt.pause(0.01)
        plt.show()
