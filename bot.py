import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

API_URL = 'http://127.0.0.1:5000'
user_api_keys = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in user_api_keys:
        keyboard = [
            [
                InlineKeyboardButton("Turn it ON", callback_data='ON'),
                InlineKeyboardButton("Turn it OFF", callback_data='OFF'),
            ],
            [InlineKeyboardButton("See STATUS", callback_data='STATUS')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Hi! With this bot you can control your lamp!', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Please enter your API key using /apikey command.')







async def api_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    api_key = update.message.text.split(' ', 1)[1] if len(update.message.text.split(' ', 1)) > 1 else None
    
    if api_key:

        headers = {"Authorization": api_key}
        response = requests.get(f'{API_URL}/client/status', headers=headers)
        
        if response.status_code == 200:
            user_api_keys[chat_id] = api_key
            await update.message.reply_text('API key validated and saved! Now you can use the bot commands.')
            await start(update, context)
        else:
            await update.message.reply_text('Invalid API key. Please provide a valid API key using /apikey <your api key>.')
    else:
        await update.message.reply_text('Please provide a valid API key using /apikey <your api key>.')







async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action = query.data
    chat_id = query.message.chat_id

    if chat_id not in user_api_keys:
        await query.edit_message_text(text="API key is missing. Please set it using /apikey <your api key>.")
        return
    
    api_key = user_api_keys[chat_id]
    headers = {"Authorization": api_key}

    if action in ['ON', 'OFF']:
        response = requests.post(f'{API_URL}/client/requests', json={'order': action}, headers=headers)
        if response.status_code == 200:
            await query.edit_message_text(text=f"{response.json()}")
        else:
            await query.edit_message_text(text="Failed to process the request. Please try again.")
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text='/start') 
        
    elif action == 'STATUS':
        response = requests.get(f'{API_URL}/client/status', headers=headers)
        if response.status_code == 200:
            await query.edit_message_text(text=f"{response.json()}")
        else:
            await query.edit_message_text(text="Failed to retrieve status. Please try again.")
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text='/start') 
    






def main():
    application = ApplicationBuilder().token("6889361630:AAGY7YPlM_pCT1xlWhj2dQKdHVPMCEFqoZo").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("apikey", api_key))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
