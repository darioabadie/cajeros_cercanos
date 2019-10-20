# API Cajeros ercanos
En el siguiente documento se describe el funcionamiento de la aplicación **Cajeros Cercanos**. La misma tiene como objetivo mostrarle al usuario la dirección de los cajeros automáticos más cercanos en tiempo real.

## Características
* El acceso a la aplicación es a través de un **bot** de **Telegram**.
* La aplicación muestra los cajeros dentro de un radio de 500m en función de la red de cajeros elegida (Banelco o Link).
* La cantidad máxima de cajeros que se muestran son 3.
* La información se muestra con el formato **Banco - Dirección**. Ejemplo: *Banco Santander Río - JUSTO, JUAN B. AV. Y PARAGUAY* 

## Instalación

### Dependencias
Para poder hacer uso del sistema es necesario instalar las siguientes dependencias:

* Python Telegram Bot - `pip install python-telegram-bot `
* Geopy - `pip install geopy `


### Bot de Telegram
El usuario se comunicará con el bot **@jampp_bot**, el cual está configurado para acceder a la aplicación. 

No obstante, el usuario puede configurar su propio bot y vincularlo con la aplicación. Para ello debe crear un bot como se explica en el siguiente [tutorial](https://core.telegram.org/bots) y luego reemplazar el contenido de la variable `TOKEN` que se encuentra en el archivo `main.py` de acuerdo al código generado con la creación del bot.

Ejemplo:

`TOKEN = '935739772:AAEbQdhuWxUjUH3NSZwrEi4A0EnQTnKidAA'`


## Uso de la aplicación
EL primer paso consiste en ejecutar el script `main.py ` el cual pondrá en funcionamiento el bot.

Mientras se está ejecutando el algoritmo anterior, es posible acceder desde Telegram a través de los comandos **/banelco** y **/link**, los cuales muestran los cajeros más cercanos de acuerdo a la red de cajeros elegida.

Luego la aplicación le requerirá al usuario compartir su ubicación a través del siguiente mensaje: 

*Por favor serías tan amable de compartir tu ubicación?*

El usuario debe hacer click sobre el botón **Enviar ubicación** que aparecerá en su pantalla.

Finalmente el usuario recibirá el listado de los cajeros automáticos más cercanos.

 



