import MAiZ_DOAS_WaterQuality_IPM as ipm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy import signal

def calcular_reflectancia(ruta_medida, ruta_referencia, ruta_offset):
    def datas(ruta_archivo):
        datos = np.loadtxt(ruta_archivo, skiprows=4)
        return datos[:, 0], datos[:, 1]

    wl, I = datas(ruta_medida)
    refwl, refI = datas(ruta_referencia)
    offsetwl, offsetI = datas(ruta_offset)

    n, m, k = 0, 0, 0
    for pix in range(len(wl)):
        if wl[pix] > ipm.wav_sta:
            n = pix
            break
    for pix in range(n, len(wl)):
        if wl[pix] > ipm.wav_end:
            m = pix
            break
        k += 1

    wl = wl[n:m]
    ipm.wav_val = wl
    ipm.pix = len(wl)

    # Filtrado Savitzky-Golay tal como estaba en tu código original
    I_oft = signal.savgol_filter(offsetI[n:m], window_length=30, polyorder=3)
    I_ref = signal.savgol_filter(refI[n:m], window_length=30, polyorder=3)
    I_mea = signal.savgol_filter(I[n:m], window_length=30, polyorder=3)
    
    rflc = I_mea / I_ref
    rflc = 10 * rflc / np.max(rflc)

    return wl, rflc, I_ref
    """
    reflectancia = (I[n:m] - offsetI[n:m]) / (refI[n:m] - offsetI[n:m])
    print(reflectancia.shape)
    np.nan_to_num(reflectancia,nan=0.0,posinf=0.0, neginf=0.0)
    for p in range(k):
        if np.isfinite(reflectancia[p]): reflectancia[p]=0
    ref=np.array(refI[n:m])# - offsetI[n:m])
    mea=np.array(I[n:m])#-offsetI[n:m]) #
    """
    #reflectancia1=(I[n:m] - offsetI[n:m]) / (refI[n:m] - offsetI[n:m])#I[n:m]/refI[n:m]
    """
    Iref_scf=signal.cspline1d(refI,3)
    Iref_s=signal.cspline1d_eval(Iref_scf,wl)
    Iref_s=Iref_s/np.max(Iref_s)
    I_scf=signal.cspline1d(I,3)
    I_s=signal.cspline1d_eval(I_scf,wl)
    I_s=I_s/np.max(I_s)
    """
    I_oft=signal.savgol_filter(offsetI[n:m],window_length=30, polyorder=3)
    I_ref=signal.savgol_filter(refI[n:m],window_length=30, polyorder=3)
    I_mea=signal.savgol_filter(I[n:m],window_length=30, polyorder=3)
    rflc=I_mea/I_ref#(I_mea-I_oft)/(I_ref-I_oft)
    rflc=10*rflc/np.max(rflc)
    #reflectancia1=reflectancia1/np.max(reflectancia1)
    #reflectancia2=(reflectancia1-np.min(reflectancia1))/np.max(reflectancia1)
    #smooth_coef=signal.cspline1d(reflectancia,3)
    #rflc_smooth = signal.cspline1d_eval(smooth_coef, wl)
    #sos = signal.butter(3,0.1, 'highpass', fs=1000, output='sos')
    #filtered = signal.sosfilt(sos, reflectancia)
    return wl,rflc,I_ref

# Cambia la definición de la función y elimina la variable 'path' interna:
def medidas_reflectancia(path_archivo):
    def load_table(path):
        df = pd.read_csv(path, sep="\t", header=16, encoding='latin1', dtype={'column_a': float, 'column_b': float})
        wl = df.iloc[:,0].values
        val = df.iloc[:, 1].values
        return wl, val
        
    wl, rflc = load_table(path_archivo) # Usa el parámetro de la función
    n,m,k=0,0,0
    
    for pix in range(len(wl)):
        if wl[pix]>ipm.wav_sta:
            n=pix
            break
    for pix in range(n,len(wl)):
        if wl[pix]>ipm.wav_end:
            m=pix
            break
        k+=1
    wl=wl[n:m]
    rflc=rflc[n:m]
    rflc=10*rflc/np.max(rflc)
    return wl,rflc,rflc

def interpolate_data(wav_usb400,fil_dat,fil_colx,fil_coly):
    df_origen = pd.read_csv(fil_dat, sep=r'\s+', header=0)
    x_origen = df_origen[fil_colx]
    y_origen = df_origen[fil_coly]
    f_interp = interp1d(x_origen, y_origen, kind='cubic', fill_value="extrapolate")
    aw_usb4000 = f_interp(wav_usb400)
    return aw_usb4000
