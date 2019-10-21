from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup


# pip install python-telegram-bot
from cajeros_func import cajeros



#ubicacion = [-34.5835311,-58.4299928]
ubicacion = [0,0]

TOKEN = '935739772:AAEbQdhuWxUjUH3NSZwrEi4A0EnQTnKidAA'

def banelco(bot, update):
    
    global red
    
    red = "BANELCO"

    location_keyboard = KeyboardButton(text="Enviar ubicación",  request_location=True)           #creating location button object
    custom_keyboard = [[ location_keyboard]] 
    reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
    update.message.reply_text(
                    "Por favor serías tan amable de compartir tu ubicación?", 
                    reply_markup=reply_markup)
 
    
def link (bot, update):
    
    global red
    
    red  = "LINK"
    
    location_keyboard = KeyboardButton(text="Enviar ubicación",  request_location=True)           #creating location button object
    custom_keyboard = [[ location_keyboard]] 
    reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
    update.message.reply_text(
                    "Por favor serías tan amable de compartir tu ubicación?", 
                    reply_markup=reply_markup)
 
    
def location(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
   
    ubicacion[0] =  message.location.latitude
    ubicacion[1] =  message.location.longitude
    
    bot.send_message(chat_id=update.message.chat_id,text= "Estos son los cajeros más cercanos: ")
    res = cajeros(ubicacion,red)
    #mapa()
    

    
    
    chat_id = update.message.chat_id
    for ind in range(0,len(res["banco"])):
        bot.send_message(chat_id=update.message.chat_id,text=res["banco"][ind] 
        + " - " + res["ubicacion"][ind]
    )
    bot.send_photo(chat_id=update.message.chat_id, photo=open('fig1.jpg', 'rb'))
    #print(current_pos)
    

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('BANELCO',banelco))
    dp.add_handler(CommandHandler('LINK',link))
    dp.add_handler(MessageHandler(Filters.location, location, edited_updates=True))    

    
    updater.start_polling()
    updater.idle()
    
     

if __name__ == '__main__':
    main()