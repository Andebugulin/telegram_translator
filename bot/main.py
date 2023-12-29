from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import logging
import os
from .database.main import Database
import asyncio
from aiogram import  types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from .states_dir.statesform import StepsForm
import random
from .markups_dir.markups import *
import time

dp = Dispatcher()

@dp.message(F.text.lower().strip() == 'test')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    global message_id
    chat_id = message.from_user.id 
    message_id = message.message_id
    CONSOLE = f'''\n 
                        CONSOLE: TESTING\n
                        STATE: -\n
                        CHAT_ID: {chat_id}\n
               '''
    print(CONSOLE)

    db.add_new_user(user_id=chat_id)
    time.sleep(3)
    db.check_and_add_word(user_id=chat_id, word='meaw', to_language='eng', from_language='rus')
    time.sleep(2)
    print(db.retrieve_user_history(user_id=chat_id))
    db.remember_word(user_id=chat_id, word='meaw', to_language='eng', from_language='rus')
    time.sleep(2)
    db.remember_word(user_id=chat_id, word='meaw', to_language='rus', from_language='eng')
    time.sleep(2)
    
    await bot.send_message(chat_id, "Testing ended", parse_mode='HTML', disable_notification=True)


@dp.message(Command("start", "restart"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    global message_id
    chat_id = message.from_user.id 
    message_id = message.message_id
    CONSOLE = f'''\n 
                        CONSOLE: start\n
                        STATE: MENU\n
                        CHAT_ID: {chat_id}\n
               '''
    print(CONSOLE)

    db.add_new_user(user_id=chat_id)
    await state.set_state(StepsForm.MENU)

    markup = custom_markup_for_the_menu()

    await bot.send_message(chat_id, "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.lower().strip() == 'deactivate')
async def deactivate_account(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.MENU:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: !DEACTIVATE! account\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
            
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='/start')]], one_time_keyboard=False)
        db.delete_user(user_id=chat_id)
        
        await bot.send_message(chat_id, "<code> Sir, your account, OH NOO, SIR\n\n IT's successfully gone</code>", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.lower().strip() == 'translate')
async def deactivate_account(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.MENU:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: Go to translate scope\n
                        STATE: TRANSLATING\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        await state.set_state(StepsForm.TRANSLATING)
        markup = custom_markup_for_the_translation()
        
        await bot.send_message(chat_id, "Sir, now, you can type words or sentences, that will be translated", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.lower().strip() == 'history')
async def deactivate_account(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.TRANSLATING:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: Go to History scope\n
                        STATE: HISTORY\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        await state.set_state(StepsForm.HISTORY)
        markup = custom_markup_for_the_menu() # wrong one, for testing purposes
        
        await bot.send_message(chat_id, "Sir, now, you can type words or sentences, that will be translated", reply_markup=markup, parse_mode='HTML', disable_notification=True)

@dp.message(F.text.lower().strip() == 'back')
async def deactivate_account(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.HISTORY:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: Go back to TRANSLATING\n
                        STATE: TRANSLATING\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        await state.set_state(StepsForm.TRANSLATING)
        markup = custom_markup_for_the_translation()
        
        await bot.send_message(chat_id, "Sir, now, you can type words or sentences, that will be translated", reply_markup=markup, parse_mode='HTML', disable_notification=True)
   
    elif await state.get_state() == StepsForm.TRANSLATING:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: Go back to MENU\n
                        STATE: MENU\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        await state.set_state(StepsForm.MENU)
        markup = custom_markup_for_the_menu()
        
        await bot.send_message(chat_id, "Sir, what do you want to do?", reply_markup=markup, parse_mode='HTML', disable_notification=True)
    
    elif await state.get_state() == StepsForm.WORD:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: Go back to HISTORY\n
                        STATE: HISTORY\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
        await state.set_state(StepsForm.HISTORY)
        markup = custom_markup_for_the_menu() # wrong one, for testing purposes
        
        await bot.send_message(chat_id, "Sir, you can see your full history here, choose the word you want to delete", reply_markup=markup, parse_mode='HTML', disable_notification=True)

def start_bot():
    # loading env, 
    # you can create .env file and put there your 'BOT_TOKEN' variable
    load_dotenv()

    # logging helps to check follow whether everything is working properly.
    logging.basicConfig(level=logging.INFO)#, filename='logs.log')

    # Initialize your Telegram Bot Token
    # ! don't you ever put a token to the code !!!!!!
    bot_token = str(os.getenv("BOT_TOKEN"))

    # Initialize the bot as a global variable
    global bot
    bot = Bot(token=bot_token)

    # Start the dispatcher
    global dp, db

    db = Database(db_name='database.db')
    db.initialize_database()
    asyncio.run(dp.start_polling(bot))

    


