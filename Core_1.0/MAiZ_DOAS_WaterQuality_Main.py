import MAiZ_DOAS_WaterQuality_IPM as ipm
import MAiZ_DOAS_WaterQuality_RaW as raw
import MAiZ_DOAS_WaterQuality_Plot as plt
import MAiZ_DOAS_WaterQuality_Models as wqm

import numpy as np

#rflc_wav,rflc_mea,rflc_sim=raw.calcular_reflectancia()
rflc_wav,rflc_mea,rflc_sim=raw.medidas_reflectancia()
#rflc_sim=np.zeros(shape=(ipm.pix),dtype=float)
plt_obj=plt.Plt_Fit(rflc_wav,rflc_mea,rflc_mea)
c,c_sigma=wqm.WaterQuality_Fit(plt_obj,rflc_wav,rflc_mea,rflc_sim)
input("Done")
