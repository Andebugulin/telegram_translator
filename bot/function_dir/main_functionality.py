
import asyncio
from aiogram import  types, F
import datetime
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states_dir.statesform import StepsForm
import random
from markups_dir.markups import *


@dp.message(Command("start", "restart"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    global message_id
    chat_id = message.from_user.id 
    message_id = message.message_id
    CONSOLE = f'''\n 
                        CONSOLE: start\n
                        STATE: Menu\n
                        CHAT_ID: {chat_id}\n
               '''
    print(CONSOLE)

    db.add_new_user(user_id=chat_id, db_name=db.db_name)
    await state.set_state(StepsForm.MENU)

    markup = custom_markup_for_the_menu()

    await bot.send_message(chat_id, "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)



@dp.message(F.text.strip() == 'DEACTIVATE')
async def translate(message: types.Message, state: FSMContext) -> None: 

    if await state.get_state() == StepsForm.MENU:        
        chat_id = message.from_user.id
        CONSOLE = f'''\n 
                        CONSOLE: !DEACTIVATE! account\n
                        CHAT_ID: {chat_id}\n
               '''
        print(CONSOLE)
            
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text='/start')]], one_time_keyboard=False)
        del task_dictionary[chat_id]
        
        await bot.send_message(chat_id, "<code> Sir, your account, OH NOO, SIR\n\n IT's successfully gone</code>", reply_markup=markup, parse_mode='HTML', disable_notification=True)

async def if_your_state_is_initial_redirect_to_the_menu(state: FSMContext, chat_id: int) -> None:
    if await state.get_state() not in ( StepsForm.MENU, 
                                        StepsForm.TEMPLATE,
                                        StepsForm.TEMPLATE_ADD,
                                        StepsForm.TEMPLATE_DELETE,
                                        StepsForm.WORKING,
                                        StepsForm.WORKING_START, 
                                        StepsForm.WORKING_ADD, 
                                        StepsForm.WORKING_DELETE):
        
        await state.set_state(StepsForm.MENU)
        
        markup = custom_markup_for_the_menu()
        task_dictionary[chat_id].check(datetime.datetime.now())
        await bot.send_message(chat_id, task_dictionary[chat_id].__str__() + '\n\n\n' + "Menu: \nWhat do you want to do, sir?", reply_markup=markup, parse_mode='HTML', disable_notification=True)

async def on_startup(chat_id:int, task_dictionary:dict) -> None:   
    await bot.send_message(chat_id, "Bot has been started!", disable_notification=True)

    # Schedule the message to be sent daily at 12:00
    asyncio.create_task(scheduled_messages(task_dictionary))

async def action_over_time(current_time) -> None:
    global task_dictionary
    date_time = current_time
    current_time = current_time.time()
    h, m = current_time.hour, current_time.minute
    if current_time.hour == 21 and current_time.minute == 30: # night message
        # Send the scheduled message
        for chat_ids in list(task_dictionary.keys()):
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <good night message>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            task_dictionary[chat_ids].check(date_time)
            try:
                await bot.send_message(chat_ids, f'''\n 
                                                \U0001FA90 {random.choice(list(good_night_sentences))}
                                                \n\n      ---\n{random.choice(list(pickup_lines))}\n      ---\n
                                                    <strong>I Love You</strong> ''', 
                                    parse_mode='HTML', 
                                    disable_notification=True)  
            except Exception as e:
                if 'forbidden: bot was blocked' in str(e).lower():
                    del task_dictionary[chat_ids]
                    CONSOLE = f'''\n\n\n
                                CHAT_ID blocked us,\n
                                we delete him {chat_ids}\n\n\n''' 
                    print(CONSOLE)
                                       

    if (current_time.hour == 7 and current_time.minute == 0) and \
         (current_time.hour != 11 and current_time.minute == 0) and \
         (current_time.hour != 15 and current_time.minute == 0) and \
         (current_time.hour != 19 and current_time.minute == 0):
        for chat_ids in list(task_dictionary.keys()):
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <success, so far>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            try:
                await bot.send_message(
                chat_ids,
                task_dictionary[chat_ids].__str__() + '\n\n\n\n' + f"      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n<i>your progress</i> \n\n<code>Great job</code>",
                parse_mode='HTML',
                disable_notification=True
                                    ) 
            except Exception as e:
                if 'forbidden: bot was blocked' in str(e).lower():
                    del task_dictionary[chat_ids]
                    CONSOLE = f'''\n\n\n
                                CHAT_ID blocked us,\n
                                we delete him {chat_ids}\n\n\n''' 
                    print(CONSOLE)
            
    if (current_time.hour == 21 and current_time.minute == 40):
        for chat_ids in list(task_dictionary.keys()):
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <success for today>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            try:
                await bot.send_message(
                chat_ids,
                task_dictionary[chat_ids].__str__() + '\n\n\n' + f"      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n<i><b>Today's</b> accomplishments.</i> \n\n<code>Great job</code>",
                parse_mode='HTML',
                disable_notification=True
                                    )   
            except Exception as e:
                if 'forbidden: bot was blocked' in str(e).lower():
                    del task_dictionary[chat_ids]
                    CONSOLE = f'''\n\n\n
                                CHAT_ID blocked us,\n
                                we delete him {chat_ids}\n\n\n''' 
                    print(CONSOLE)
               
    if (current_time.hour == 1 and current_time.minute == 0): # 03:00
        for chat_ids in list(task_dictionary.keys()):
            task_dictionary[chat_ids].check(date_time)
            CONSOLE = f'''\n 
                        CONSOLE: sending user scheduled message <reset today's tasks>\n
                        CHAT_ID: {chat_ids}\n
               '''
            print(CONSOLE)
            task_dictionary[chat_ids].tasks = [Task(task.name, task.remaining_time) for task in task_dictionary[chat_ids].tasks_template]
            
            try:
                await bot.send_message(chat_ids, f"\n      ---\n{random.choice(list(pickup_lines))}\n      ---\n\n Your tasks for today have been set up", parse_mode='HTML', disable_notification=True)
            except Exception as e:
                if 'forbidden: bot was blocked' in str(e).lower():
                    del task_dictionary[chat_ids]
                    CONSOLE = f'''\n\n\n
                                CHAT_ID blocked us,\n
                                we delete him {chat_ids}\n\n\n''' 
                    print(CONSOLE)

async def scheduled_messages(task_dictionary:dict):
    while True:
        # current time
        current_time = datetime.datetime.now()
        
        await action_over_time(current_time) # perform actions at a specific time.

        # Sleep for a minute and check again
        await asyncio.sleep(60)

def save_dict_to_json(data:dict, json_file:str) -> None:
    new_data = data.copy()
    for chat_id, to_do_list in new_data.items():
        new_data[chat_id] = to_do_list.__dict__()
    with open(json_file, 'w') as file:
        json.dump(new_data, file, indent=4)
 
def initial_set_up(json_file:str) -> dict:
    try:
        new_data = {}
        with open(json_file, 'r') as file:
            data = json.load(file)

            if isinstance(data, dict):
                for key, value in data.items():
                    to_do_list = ToDoList(key) # chat id
                    to_do_list.unpacking(dictionary=value)
                    new_data[int(key)] = to_do_list

                return new_data
            else:
                raise ValueError("The JSON file does not contain a valid dictionary.")
    except FileNotFoundError:
        print('\n\n\n\nJSON file was not observed\n\n\n\n')
        return {}
    except json.JSONDecodeError:
        raise ValueError(f"\n\n\n\nThe JSON file '{json_file}' is not valid JSON.\n\n\n\n")
        return {}
    except ValueError as e:
        print('\n\n\n\nCheck initial_set_up() function and JSON file, something is bad here')
        print(e)
        print('\n\n\n')
        return {}
    return {}



