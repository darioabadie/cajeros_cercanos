
#Librerías
import pandas as pd 
from geopy.distance import geodesic # pip install geopy 

# Funciones

#Calcular distancia
def calc_dist(row):
    origen = (mi_lat, mi_long)
    destino = (row['lat'], row['long'])
    return geodesic(origen,destino).meters

def cajeros(ubicacion,red):
    
    global mi_lat
    global mi_long
    
    # Importar datos
    data = pd.read_csv("cajeros-automaticos.csv") 
    #data.head()
    
    # Seleccionar cajeros en CABA
    data_caba = data[data['localidad']== "CABA"]
    
    # Definir red de cajeros (Banelco o Link)
    #red_cajeros = "BANELCO"
    red_cajeros = red
    
    # Filtrar por red de cajeros
    index = data_caba['red']== red_cajeros 
    data_red = data_caba[index]
    #data_red.head()
    
    # Generar ubicación ejemplo
    mi_lat = ubicacion[0]
    mi_long =ubicacion[1]
    
    
    # Cálculo de la distancia
    data_red['distancia'] = data_red.apply(calc_dist, axis=1)
    
    
    # Filtrado de los cajeros cercanos (Distancia < 500m)
    
    radio = 500
    cajeros_cercanos = data_red[data_red['distancia'] <= radio]
    
    # Obtención de los 3 cajeros más cercanos
    cajeros_cercanos = cajeros_cercanos.sort_values(by=['distancia'],ascending=True)
    top_cajeros = cajeros_cercanos[:3]
    
    # Resultado final
    
    cajeros = top_cajeros[['banco','ubicacion',"lat","long"]]
    cajeros = cajeros.reset_index(drop=True)
    
    return cajeros
    
    
