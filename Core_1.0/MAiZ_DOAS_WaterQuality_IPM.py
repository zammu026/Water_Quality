from pathlib import Path

# Rutas estáticas eliminadas.
WQ_Model = "PeterGege"
# WQ_Model = "JumanjiWolo"

# Ruta dinámica relativa al directorio donde se ejecuta el script
WQ_AW = Path(__file__).resolve().parent / "a_water_pope_fry.txt"

WQ_Theta_Sun = 60 # Solar Zenith Angle
WQ_Theta_V = 30   # Surface Viewing Angle

pix = 200
wav_sta = 400
wav_end = 800
wav_val = None
ref_sta = 0
ref_end = 15
Wz_dpht = 3