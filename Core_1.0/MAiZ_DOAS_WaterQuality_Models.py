import MAiZ_DOAS_WaterQuality_IPM as ipm
import MAiZ_DOAS_WaterQuality_RaW as raw

import numpy as np
from scipy.optimize import curve_fit
from functools import partial

#Model ?
A1=1.0546
A2=0.9755
k0=1.0546
k1W=1.9991
k2W=1.9991
k1B=1.2441
k2B=0.5182
Kd_coff=1.0546
cos_sun=np.cos(ipm.WQ_Theta_Sun*2*np.pi/360)
cos_v=np.cos(ipm.WQ_Theta_V*2*np.pi/360)
kuw_n=3.5421
kuw_nmrtr=0.2786
kus_n=2.2658
kus_nmrtr=0.0577
kuw_coeff=(1-kuw_nmrtr/cos_sun)/cos_v
kus_coeff=(1+kus_nmrtr/cos_sun)/cos_v
#Model abs pure water
#Model abs phytoplankton (ph)
aph_n=2
aph_acs0=[
    [6.312e-9,4.332e-10,3.146e-10,3.078e-11],
    [1.0228e-8,6.044e-10,5.664e-11,5.392e-12]
    ]
aph_wc=[
    [300,445,640,680],
    [300,445,640,680]
       ]
aph_ww=[
    [60,40,66,120],
    [40,60,40,60]
    ]
#Model abs detritus (d)
sigma_d=1e-5
wc_d=510 #650
ww_d=60
#Model abs Color Disolved Organic Matter (CDOM) (cdom)
sigma_cdom=1e-2
wc_cdom=730 #710
ww_cdom=150
#Model retro pure water Morel (w)
b_aw_mrl=3.5
b_nw_mrl=-4.32
b_wc_mrl=450
#Model retro Suspended Matter (SM)
b_A=0.0006
b_B=-0.37
b_mie=0.0042
b_wavmie=500
def u_ra(a_w,wav,c_ph1,c_ph2,c_d,c_cdom,c_sm,c_mie):
    u_val=np.zeros(shape=(ipm.pix),dtype=float)
    #Calculation of diferent abs terms
    a_ph=0
    c_ph=[c_ph1,c_ph2]
    for typ in range(aph_n):
        for gss in range(len(aph_acs0[typ])):
            a_ph+=(c_ph[typ]/aph_acs0[typ][gss])*np.exp(-1*np.pow((wav-aph_wc[typ][gss])/aph_ww[typ][gss],2))
    a_d=(c_d/sigma_d)*np.exp(-1*((wav-wc_d)/ww_d)**2)
    a_cdom=(c_cdom/sigma_cdom)*np.exp(-1*((wav-wc_cdom)/ww_cdom)**2)
    #Calculation of diferent retro terms
    b_w=b_aw_mrl*np.pow(wav/b_wc_mrl,b_nw_mrl)
    b_sm=c_sm*b_A*np.pow(c_sm,b_B)+c_mie*b_mie*(wav/b_wavmie)
    #Evaluation of abs and retro
    a_val=a_w+a_ph+a_d+a_cdom
    b_val=b_w+b_sm
    #Evaluation of U
    ab_val=a_val+b_val
    u_val=b_val/ab_val
    up1_val=1+b_val/ab_val
    #print(u_val,ab_val,up1_val)
    return u_val,ab_val,up1_val

def Model_PeterGege(wav,prmtrs,a_w):
    rf_sim=np.zeros(shape=(ipm.pix),dtype=float)
    print("Test parameters",prmtrs)
    #input("try?")
    f_rs,c_ph1,c_ph2,c_d,c_dom,c_sm,c_mie=prmtrs[0],prmtrs[1],prmtrs[2],prmtrs[3],prmtrs[4],prmtrs[5],prmtrs[6]
    u,ab,up1=u_ra(a_w,wav,c_ph1,c_ph2,c_d,c_dom,c_sm,c_mie)
    K_d=Kd_coff*ab/cos_sun
    k_uw=ab*np.pow(up1,kuw_n)*kuw_coeff
    k_us=ab*np.pow(up1,kus_n)*kus_coeff
    #Reflectance calculation
    term_deeps=f_rs*u*(1-A1*np.exp(-1*(K_d+k_uw)*ipm.Wz_dpht))
    term_bs=A2*np.exp(-1*(K_d+k_us)*ipm.Wz_dpht)
    rf_sim=100*term_deeps+term_bs
    return rf_sim

def Model_JumanjiWolo(wav,prmtrs):
    G,c_chl,c_cdom=prmtrs[0],prmtrs[1],prmtrs[2]
    a_w=0.0044*np.exp(0.01*wav-418)
    a_chl=c_chl*(0.015*np.exp(-0.5*np.pow((wav-440)/20,2))+0.045*np.exp(-0.5*np.pow((wav-675)/12,2)))
    a_cdom=c_cdom*0.2
    b_b=5e-4
    b_w=0.005
    a=a_w+a_chl+a_cdom
    b=b_b+b_w
    rf_sim=G*b/(a+b)
    return rf_sim

def WaterQuality_Fit(plt_obj,rf_wav,rf_mea,rf_sim):
    aw=raw.interpolate_data(rf_wav,ipm.WQ_AW,'lambda_nm','a_water_m-1')
    input("Start fit?")
    plbl=None
    par_tot=0
    if ipm.WQ_Model=="PeterGege":
        plbl=["f_rs","c_ph1","c_ph2","c_d","c_cdom","c_sm","c_mie",]
        par_tot=7
    elif ipm.WQ_Model=="JumanjiWolo":
        plbl=["G","a_chl","a_cdom"]
        par_tot=3
    def wq_model_fun(wav,*args):
        fit_par=args
        fit_res=None
        fit_par_str=""
        if ipm.WQ_Model=="PeterGege":
            fit_res=Model_PeterGege(wav,fit_par,aw)
            fit_par_str="f_rs="+'%.2f'%float(abs(fit_par[0]))+"\t\t\t"
            fit_par_str+="c_ph1="+'%.2f'%float(abs(1e6*fit_par[1]))+r"$\mu$g"+"\t\t\t"
            fit_par_str+="c_ph2="+'%.2f'%float(abs(1e6*fit_par[2]))+r"$n$g"+"\t\t\t"
            fit_par_str+="c_d="+'%.2f'%float(abs(fit_par[3]))+r"$\mu$g"+"\t\t\t"+"\n"
            fit_par_str+="c_cdom="+'%.2f'%float(abs(1e0*fit_par[4]))+r"$\mu$g"+"\t\t\t"
            fit_par_str+="c_sm="+'%.2f'%float(abs(1e3*fit_par[5]))+r"$\nu$g"+"\t\t\t"
            fit_par_str+="c_mie="+'%.2f'%float(abs(1e-3*fit_par[6]))+r"$\mu$g"
        elif ipm.WQ_Model=="JumanjiWolo":
            fit_res=Model_JumanjiWolo(wav,fit_par)
            fit_par_str="G="+'%.2f'%float(abs(fit_par[0]))+"\t\t\t"
            fit_par_str+="a_chl="+'%.2f'%float(abs(fit_par[1]))+"\t\t\t"
            fit_par_str+="a_cdom="+'%.2f'%float(abs(fit_par[2]))+"\t\t\t"
        plt_obj.Plt_Upd(fit_par_str,fit_res,1)
        return fit_res
    fit_gss=None
    if ipm.WQ_Model=="PeterGege": fit_gss=[1,1e-6,1e-6,1e-6,1e-6,1e-6,1e-6]
    elif ipm.WQ_Model=="JumanjiWolo": fit_gss=[1,1e-6,1e-6]
    popt,pcov=curve_fit(wq_model_fun,rf_wav,rf_mea,method="lm",p0=fit_gss,nan_policy='omit')
    popt_err=np.diag(pcov)
    print("Optimization report")
    print("Variable","Error")
    for par_n in range(par_tot):
        print(plbl[par_n],'%.2f'%popt[par_n],'%.2f'%popt_err[par_n])
    return popt,pcov
