# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 23:33:54 2025

@author: Cisneros
"""

import numpy as np


def calcular_reflectancia(data, referencia, offset, wl_min, wl_max):


    def datas(ruta_archivo):
        datos = np.loadtxt(ruta_archivo, skiprows=4)
        return datos[:, 0], datos[:, 1]


    wl, I = datas(data)
    refwl, refI = datas(referencia)
    offsetwl, offsetI = datas(offset)
    mask = (wl >= wl_min) & (wl <= wl_max)
    wl = wl[mask]
    I = I[mask]
    refI = refI[mask]
    offsetI = offsetI[mask]

    reflectancia = (I - offsetI) / refI

    return wl, reflectancia



data = "Set_0_Azi_0_Ele_15.txt"
referencia = "../Data_Reference/Set_0_Reference_Normal.txt"
offset = "../Data_Offsets/Set_0_Offset.txt"

wl_min, wl_max = 250.0, 400.0

wl, R = calcular_reflectancia(data, referencia, offset, wl_min, wl_max)

for L, r in zip(wl, R):
    print( L, "-> ", r)



