
# Librerías
import pandas as pd 
from geopy.distance import geodesic  

# Funciones

# Función que calcula distancia a partir de coordenadas
def calc_dist(row):
    origen = (mi_lat, mi_long)
    destino = (row['lat'], row['long'])
    return geodesic(origen,destino).meters

# función que halla cajeros cercanos respecto a la ubicación del usuario
def cajeros(ubicacion,red):
    
    global mi_lat
    global mi_long
    
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
    data_red['distancia'] = data_red.apply(calc_dist, axis=1)

    # Filtrado de los cajeros cercanos (Distancia < 500m) 
    radio = 500
    cajeros_cercanos = data_red[data_red['distancia'] <= radio]
    
    # Obtención de los 3 cajeros más cercanos
    cajeros_cercanos = cajeros_cercanos.sort_values(by=['distancia'],ascending=True)
    top_cajeros = cajeros_cercanos[:3]
    
    # Resultado final
    global cajeros
    cajeros = top_cajeros[['banco','ubicacion',"lat","long"]]
    cajeros = cajeros.reset_index(drop=True)
    
    return cajeros

# Función que genera el mapa con la ubicación del usuario y los cajeros cercanos usando la API de Google   
def mapa(centro_mapa, cajeros):
    
    G_API = "AIzaSyB3LR-c3c3mEJc6xUfYLTdspFFFPJQOYC4" # Google API Key

    centro = str(centro_mapa[0]) + "," + str(centro_mapa[1]) # Se define la ubcación del usuario como punto central del mapa
    punto_centro = "markers=color:green%7Clabel:U%7C" + centro  # Se genera un marcador con la ubicación del usuario
    
    puntos_cajeros = "" # Se genera un marcador por cada cajero cercano al usuario
    for ind in range(0,len(cajeros["banco"])): 
        puntos_cajeros = puntos_cajeros + "&markers=color:red%7Clabel:C%7C" + str(cajeros["lat"][ind])+ "," + str(cajeros["long"][ind])

    # visitar esta página:
    # https://developers.google.com/maps/documentation/maps-static/intro
   

    # La fubnión entrega como resultado el link que contiene la dirección al mapa generado por la API de Google
    return "https://maps.googleapis.com/maps/api/staticmap?center=" + centro+ "&zoom=16&size=600x600&maptype=roadmap&" + punto_centro + puntos_cajeros + "&key="+G_API

