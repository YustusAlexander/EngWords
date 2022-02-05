from app import dp
from states import *
from keyboard import *
from functions import *


@dp.callback_query_handler(callback_numbers.filter(action=["showing", "game", "edition"]))
async def callbacks_main_keyboard(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "showing":
        await call.message.edit_text("➔ Show words:", reply_markup=get_showing_keyboard())
        await call.answer()
    elif action == "game":
        await call.message.edit_text("➔ Play game:", reply_markup=get_game_keyboard())
        await call.answer()
    elif action == "edition":
        await call.message.edit_text("➔ Edit words:", reply_markup=get_edition_keyboard())
        await call.answer()
    await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["last", "random", "favour", "all_list", "back"]))
async def callbacks_showing_keyboard(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "last":
        await showing.last.set()
        await call.message.edit_text("Введите количество слов:")
        await call.answer()
    elif action == "random":
        await showing.rand.set()
        await call.message.edit_text("Введите количество слов:")
        await call.answer()
    elif action == "favour":
        await call.message.edit_text(favour())
        await call.answer()
    elif action == "all_list":
        await call.message.edit_text(all_list())
        await call.answer()
    elif action == "back":
        await call.message.edit_text("⇛ Choose mode", reply_markup=get_main_keyboard())
        await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["match", "remember", "type", "back"]))
async def callbacks_game_keyboard(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "match":
        await game.match_question.set()
        await call.message.edit_text("Пришли любое сообщение для начала")
        await call.answer()
    elif action == "remember":
        await game.remember_question.set()
        await call.message.edit_text("Нажмите любую клавишу для начала")
        await call.answer()
    elif action == "type":
        await game.type_question.set()
        await call.message.edit_text("Нажмите любую клавишу для начала")
        await call.answer()
    elif action == "back":
        await call.message.edit_text("⇛ Choose mode", reply_markup=get_main_keyboard())
        await call.answer()


@dp.callback_query_handler(callback_numbers.filter(action=["add", "delete", "set_favour", 'rem_fav', "back"]))
async def callbacks_edition_keyboard(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "add":
        await call.answer(text="Для добавления слов напишите слова через '-'. Каждую пару слов с новой строчки.")
        await edition.add_word.set()
        await call.answer()
    elif action == "delete":
        await call.message.edit_text(list_num())
        await call.answer(text="Для удаления напишите номера из списка через запятую:")
        await edition.del_word.set()
        await call.answer()
    elif action == "set_favour":
        await call.message.edit_text(list_num())
        await call.answer(text="Для добавления в избранное напишите номера слов из списка через запятую:")
        await edition.set_fav.set()
        await call.answer()
    elif action == "rem_fav":
        await call.message.edit_text(favour_num())
        await call.answer(text="Для удаления слов из избранного напишите их номера из списка через запятую:")
        await edition.rem_fav.set()
        await call.answer()
    elif action == "back":
        await call.message.edit_text("⇛ Choose mode", reply_markup=get_main_keyboard())
        await call.answer()


