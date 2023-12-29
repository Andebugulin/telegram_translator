from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def custom_markup_for_the_menu() -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_the_menu was used\n'
    print(CONSOLE)
    
    deactivate_account_btn = KeyboardButton(text="Deactivate")
    translate_activity_btn = KeyboardButton(text="Translate")

    first_row = [translate_activity_btn, deactivate_account_btn]
    
    key_board = [first_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

def custom_markup_for_the_translation(from_language, to_language) -> ReplyKeyboardMarkup:
    CONSOLE = '\n CONSOLE: custom_markup_for_the_translation was used\n'
    print(CONSOLE)
    

    history_account_btn = KeyboardButton(text="History")
    from_language_btn = KeyboardButton(text=f"{from_language}")
    to_language_btn = KeyboardButton(text=f"{to_language}")
    back_activity_btn = KeyboardButton(text="back")

    first_row = [history_account_btn]
    second_row = [from_language_btn, to_language_btn]
    third_row = [back_activity_btn]
    
    key_board = [first_row, second_row, third_row]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

    return markup

# def custom_markup_for_the_translation(task_dictionary: dict, chat_id: int) -> ReplyKeyboardMarkup:
#     CONSOLE = '\n CONSOLE: custom_markup_for_template_delete_activity was used\n'
#     print(CONSOLE)
#     key_board = []

#     rows = []
#     buttons_in_one_row = []
#     flag_finished = False
#     for task in task_dictionary[chat_id].tasks_template:
#         if len(task.name) > 25:
#             buttons_in_one_row = [KeyboardButton(text=task.name)]
#             rows.append(buttons_in_one_row)
#             buttons_in_one_row = []
#             flag_finished = True
#         else:
#             if len(buttons_in_one_row) == 0:
#                 buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))
#                 flag_finished = False
#             elif len(buttons_in_one_row) == 1:
#                 if ((sum([len(btn_text) for btn, btn_text in buttons_in_one_row]) + len(task.name)) < 40): # if all task names would fit in a row
#                     buttons_in_one_row.append((KeyboardButton(text=task.name), task.name))

#                     rows.append([btn for btn, btn_text in buttons_in_one_row])
#                     buttons_in_one_row = []
#                     flag_finished = True
#                 else:
#                     rows.append([btn for btn, btn_text in buttons_in_one_row])

#                     buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
#                     flag_finished = False
#             else:
#                 rows.append([btn for btn, btn_text in buttons_in_one_row])

#                 buttons_in_one_row = [(KeyboardButton(text=task.name), task.name)]
#                 flag_finished = False
#     if not flag_finished:
#         rows.append([btn for btn, btn_text in buttons_in_one_row])

#     for row in rows:
#         key_board.append(row)

#     key_board.append([KeyboardButton(text='Menu'), KeyboardButton(text='Back')])

#     markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=key_board, one_time_keyboard=False)

#     return markup
