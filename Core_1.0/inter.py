import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

try:
    # 1. Cargar los datos de origen
    df_origen = pd.read_csv('a_water_pope_fry.txt', sep=r'\s+', header=0)
    
    # Extraer los ejes x (longitud de onda) e y (absorción)
    x_origen = df_origen['lambda_nm']
    y_origen = df_origen['a_water_m-1']
    
    print(f"Datos de origen cargados. Rango: {x_origen.min()} nm a {x_origen.max()} nm")

    # 2. Definir la rejilla de destino (USB4000)
    # Basado en el paper: 3648 píxeles, rango 200-890 nm
    pixeles_usb4000 = 3648
    lambda_min = 200.0
    lambda_max = 890.0
    
    # Crear la rejilla lineal de destino
    x_destino = np.linspace(lambda_min, lambda_max, pixeles_usb4000)
    
    print(f"Rejilla de destino creada. Rango: {x_destino.min()} nm a {x_destino.max()} nm, con {len(x_destino)} puntos.")

    # 3. Crear la función de interpolación/extrapolación
    f_interp = interp1d(x_origen, y_origen, kind='linear', fill_value="extrapolate")

    # 4. Calcular los nuevos valores en la rejilla de destino
    y_destino = f_interp(x_destino)

    # 5. Crear el DataFrame con los nuevos datos
    df_interpolado = pd.DataFrame({
        'lambda_nm_usb4000': x_destino,
        'a_water_interpolada': y_destino
    })
    
    # 6. Guardar los nuevos datos en un archivo TXT (separado por tabulaciones)
    output_txt = 'a_water_interpolada_usb4000.txt'
    
    # Usamos to_csv con sep='\t' (tabulador) que es un formato .txt común
    df_interpolado.to_csv(output_txt, sep='\t', index=False, float_format='%.8f')
    
    print(f"\nDatos interpolados guardados exitosamente en: {output_txt}")

except FileNotFoundError:
    print(f"Error: El archivo 'a_water_pope_fry.txt' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error: {e}")