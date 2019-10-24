
# Librerías
import pandas as pd 
from geopy.distance import geodesic  
import pickle
from datetime import datetime, timedelta
from numpy.random import choice
from config import G_API

# Funciones

# Función que halla cajeros cercanos respecto a la ubicación del usuario
def cajeros(ubicacion,red):
    
    # Carga de datos
    data = pd.read_csv("cajeros-automaticos.csv") 
    
    # Selección de cajeros en CABA
    data_caba = data[data['localidad']== "CABA"]
    
    # Elección de red de cajeros (Banelco o Link)
    red_cajeros = red
    index = data_caba['red']== red_cajeros 
    data_red = data_caba[index]

    # Ubicación del usuario
    mi_lat = ubicacion[0]
    mi_long =ubicacion[1]
    
    # Cálculo de la distancia de cada cajero respecto al usuario
    data_red["distancia"] = data_red["lat"]
    for i in range(0,len(data_red["lat"])):
        origen = (mi_lat, mi_long)
        destino = (data_red['lat'].iloc[i], data_red['long'].iloc[i])
        data_red["distancia"].iloc[i] = geodesic(origen,destino).meters

    # Filtrado de los cajeros cercanos (Distancia < 500m) 
    radio = 500
    cajeros_cercanos = data_red[data_red['distancia'] <= radio]
    
    # Filtrado de los cajeros con extracciones disponibles (cargas > 0) 

    cajeros_cercanos = cajeros_cercanos[cajeros_cercanos['cargas'] > 0]
    
    # Obtención de los 3 cajeros más cercanos con extracciones disponibles
    cajeros_cercanos = cajeros_cercanos.sort_values(by=['distancia'],ascending=True)
    top_cajeros = cajeros_cercanos[:3]
 
    # Resultado final
    
    #global cajeros
    cajeros = top_cajeros[['banco','ubicacion',"lat","long"]]
    cajeros = cajeros.reset_index(drop=True)
    
    # Descuento de extracción de un cajero cercano
    if len(cajeros["ubicacion"]) == 3: # Vector de probabilidades 70%, 20% y 10%
        probabilidades = [0.7, 0.2, 0.1]
    elif len(cajeros["ubicacion"]) == 2: # Vector de probabilidades 75% y 25%
        probabilidades = [0.75, 0.25]
    elif len(cajeros["ubicacion"]) == 1: # Vector de probabilidades 100%
        probabilidades = [1]
        
    res = choice(cajeros["ubicacion"],p = probabilidades) # Elección aleatoria de un cajero de acuerdo a las probabilidades
    ind = data.index[data["ubicacion"] == res]
    data["cargas"][ind] = data["cargas"][ind] -1 # Se descuenta 1 extracción al cajero elegido. 
    
    data.to_csv("cajeros-automaticos.csv",index = False) # Se registra esta modificación en la base de datos de cajeros (cajeros-automaticos.csv).    

    return cajeros


# Función que genera el mapa con la ubicación del usuario y los cajeros cercanos usando la API de Google   
def mapa(centro_mapa, cajeros):
    
    centro = str(centro_mapa[0]) + "," + str(centro_mapa[1]) # Se define la ubcación del usuario como punto central del mapa
    punto_centro = "markers=color:green%7Clabel:U%7C" + centro  # Se genera un marcador con la ubicación del usuario
    
    puntos_cajeros = "" # Se genera un marcador por cada cajero cercano al usuario
    for ind in range(0,len(cajeros["banco"])): 
        puntos_cajeros = puntos_cajeros + "&markers=color:red%7Clabel:C%7C" + str(cajeros["lat"][ind])+ "," + str(cajeros["long"][ind])

    # La fubnión entrega como resultado el link que contiene la dirección al mapa generado por la API de Google
    return "https://maps.googleapis.com/maps/api/staticmap?center=" + centro+ "&zoom=16&size=600x600&maptype=roadmap&" + punto_centro + puntos_cajeros + "&key="+G_API


# Función que actualiza el estado de de carga de los cajeros
def carga_cajeros():
    
    with open("ultima_consulta", "rb") as f: # Carga de la fecha y hora de la última consulta
        ultima_consulta = pickle.load(f)

    
    consulta_actual = datetime.now() # Tiempo en que se realiza la consulta actual
    
    interval = [dt.strftime('%a %H:%M') for dt in # Intervalo de minutos entre la úñtima consulta y la actual
       rango_fechas(ultima_consulta, consulta_actual, 
       timedelta(minutes=1))]
       
    S1 = set(interval)
    S2 = set(["Mon 08:00", "Tue 08:00", "Wed 08:00", "Thu 08:00", "Fri 08:00"]) # Días en que se realiza una carga  
    
    if any(S1.intersection(S2)): # Si entre la última consulta y la actual hubo una fecha de carga, se reestablecen las 1000 cargas para todos los cajeros
        data = pd.read_csv("cajeros-automaticos.csv") # Esta modificación tiene lugar sobre la base de datos (cajeros-automaticos.csv)
        data['cargas'] = 1000
        data.to_csv("cajeros-automaticos.csv", index = False)
    
  #Almacenamiento de la última consulta   
    with open("ultima_consulta", "wb") as f:
       pickle.dump(consulta_actual, f)

    
def rango_fechas(comienzo, final, delta):
    actual = comienzo
    while actual < final:
        yield actual
        actual += delta   


