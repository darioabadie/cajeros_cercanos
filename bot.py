
# Librerías

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
from cajeros_func import cajeros, mapa

# Token de Telegram

TOKEN = '935739772:AAEbQdhuWxUjUH3NSZwrEi4A0EnQTnKidAA'

# Función que responde al comando "Banelco" ingresado por el usuario
def banelco(bot, update):
    
    global red
    
    red = "BANELCO"
    bot.send_message(chat_id=update.message.chat_id,text= "¡Bienvenido! A continuación verás los próximos a tu ubicación.")

    location_keyboard = KeyboardButton(text="Enviar ubicación",  request_location=True) #Creación del boton para enviar ubicación
    custom_keyboard = [[ location_keyboard]] 
    reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
    update.message.reply_text(
                    "¿Por favor serías tan amable de compartir tu ubicación?", 
                    reply_markup=reply_markup)
 

# Función que responde al comando "Link" ingresado por el usuario    
def link (bot, update):
    
    global red
    
    red  = "LINK"
    bot.send_message(chat_id=update.message.chat_id,text= "¡Bienvenido! A continuación verás los próximos a tu ubicación.")

    location_keyboard = KeyboardButton(text="Enviar ubicación",  request_location=True) #Creación del boton para enviar ubicación
    custom_keyboard = [[ location_keyboard]] 
    reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
    update.message.reply_text(
                    "¿Por favor serías tan amable de compartir tu ubicación?", 
                    reply_markup=reply_markup)
 
# Función que se ejecuta cuando el usuario comparte su ubicación    
def location(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
   
    ubicacion = [0,0] # Ubicación del usuario (Latitud y longitud)
    ubicacion[0] =  message.location.latitude
    ubicacion[1] =  message.location.longitude
    
    bot.send_message(chat_id=update.message.chat_id,text= "Estos son los cajeros más cercanos: ")
    res = cajeros(ubicacion,red) # Se ejecuta la función "cajeros()" que identifica los cajeros cercanos a la ubicación del usuario.
    
    
    #chat_id = update.message.chat_id
    for ind in range(0,len(res["banco"])): # Se muestran en pantalla los cajeros cercanos (Banco y dirección) 
        bot.send_message(chat_id=update.message.chat_id,text=res["banco"][ind] 
        + " - " + res["ubicacion"][ind]
    )
    
    mensaje = mapa(ubicacion,res) # Se ejecuta la función "mapa()" que genera un mapa con los cajeros usando la API de Google
    bot.send_message(chat_id=update.message.chat_id,text= mensaje) # Como resultado se envía al usuario el link con el mapa generado.
    

def main():
    
    # Funciones encargadas de recibir los comandos ingresados por el usuario y asignar una función a cada uno.
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('BANELCO',banelco))
    dp.add_handler(CommandHandler('LINK',link))
    dp.add_handler(MessageHandler(Filters.location, location, edited_updates=True))      
    updater.start_polling()
    updater.idle()
   
    
     

if __name__ == '__main__':
    main()
    print("hola")