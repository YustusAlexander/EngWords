from aiogram import types
from aiogram.utils.callback_data import CallbackData



callback_numbers = CallbackData("fabnum", "action")

def get_main_keyboard():
    button1 = types.InlineKeyboardButton(text="✅ Show words",
                                   callback_data=callback_numbers.new(action="showing"))
    button2 = types.InlineKeyboardButton(text="👋 Play game",
                                    callback_data=callback_numbers.new(action="game"))
    button3 = types.InlineKeyboardButton(text="✏ Edit words",
                                    callback_data=callback_numbers.new(action="edition"))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button1, button2, button3)
    return keyboard

def get_showing_keyboard():
    button1 = types.InlineKeyboardButton(text="📮 last",
                                   callback_data=callback_numbers.new(action="last"))
    button2 = types.InlineKeyboardButton(text="📱 random",
                                   callback_data=callback_numbers.new(action="random"))
    button3 = types.InlineKeyboardButton(text="⭐ favourites",
                                   callback_data=callback_numbers.new(action="favour"))
    button4 = types.InlineKeyboardButton(text="🌏 all",
                                   callback_data=callback_numbers.new(action="all_list"))
    button5 = types.InlineKeyboardButton(text="↩ back",
                                   callback_data=callback_numbers.new(action="back"))
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(button1, button2, button3, button4)
    keyboard.add(button5)
    return keyboard

def get_game_keyboard():
    button1 = types.InlineKeyboardButton(text="↔ match",
                                   callback_data=callback_numbers.new(action="match"))
    button2 = types.InlineKeyboardButton(text="👀 remember",
                                    callback_data=callback_numbers.new(action="remember"))
    button3 = types.InlineKeyboardButton(text="⌨ type",
                                    callback_data=callback_numbers.new(action="type"))
    button4 = types.InlineKeyboardButton(text="↩ back",
                                   callback_data=callback_numbers.new(action="back"))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(button1, button2, button3, button4)
    return keyboard

def get_edition_keyboard():
    button1 = types.InlineKeyboardButton(text="✳ add word",
                                   callback_data=callback_numbers.new(action="add"))
    button2 = types.InlineKeyboardButton(text="❌ delete word",
                                    callback_data=callback_numbers.new(action="delete"))
    button3 = types.InlineKeyboardButton(text="🌟 set favourites",
                                    callback_data=callback_numbers.new(action="set_favour"))
    button4 = types.InlineKeyboardButton(text="🚫 del favourites",
                                         callback_data=callback_numbers.new(action="rem_fav"))
    button5 = types.InlineKeyboardButton(text="↩ back",
                                   callback_data=callback_numbers.new(action="back"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(button1, button3, button2, button4, button5)
    return keyboard

def match_keyboard(opt):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in opt:
        keyboard.add(name)
    keyboard.add("next", "finish")
    return keyboard

def type_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("show right", "next", "finish")
    return keyboard