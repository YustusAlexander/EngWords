from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from app import dp
from states import *
from keyboard import *
from functions import *


@dp.message_handler(Command("menu"), state=None)
async def main_menu(message: types.Message):
    # await message.answer('Добро пожаловать! Это программа изучения английского языка!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Выбрать режим изучения:', reply_markup=get_main_keyboard())


################################## showing ############################################

@dp.message_handler(Command("last"))
async def start_last(message: types.Message, state: FSMContext):
    await showing.last.set()
    await message.answer('Введите количество слов:')


@dp.message_handler(state=showing.last)
async def start_last(message: types.Message, state: FSMContext):
    num = message.text.strip()
    if num.isdigit and int(num) <= len(available_row()):
        await message.answer(last(int(num)))
    else:
        await message.answer('Вне допустимого диапазона!')
        await showing.last.set()
        await message.answer(f'Введите количество слов, меньше чем {len(available_row())-1}:')


@dp.message_handler(Command("rand"))
async def start_last(message: types.Message, state: FSMContext):
    await message.answer('Введите количество слов:')
    await showing.rand.set()

@dp.message_handler(state=showing.rand)
async def start_last(message: types.Message, state: FSMContext):
    num = message.text.strip()
    if num.isdigit and int(num) <= len(available_row()):
        await message.answer(rand(int(num)))
    else:
        await message.answer('Вне допустимого диапазона')
    await state.finish()


################################# game match #############################################

@dp.message_handler(Command("match"))
async def start_last(message: types.Message):
    await game.match_question.set()
    await message.answer(f"Пришли любое сообщение для продолжения")

@dp.message_handler(state=game.match_question)
async def question(message: types.Message, state: FSMContext):

    val_row = random.sample(available_row(), 4)
    options = [ws.cell(row=i, column=1).value.strip() for i in val_row]
    match_keyboard(options)
    right_row = random.choice(val_row)
    right_en = ws.cell(row=right_row, column=1).value
    right_ru = ws.cell(row=right_row, column=2).value
    await message.answer(f'выберите перевод слова "{right_ru}"', reply_markup=match_keyboard(options))
    await state.update_data({
        'ans_en': right_en,
        'ans_ru': right_ru })
    await game.match_question.set()
    await game.match_answer.set()


@dp.message_handler(state=game.match_answer)
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    right_en = data.get("ans_en")
    right_ru = data.get("ans_ru")
    txt = message.text
    if txt == right_en:
        await message.answer(f"Верно! \n{right_en} - {right_ru}", reply_markup=types.ReplyKeyboardRemove())
        await game.match_question.set()
        await message.answer(f"Пришли любое сообщение для продолжения")

    elif txt == "finish":
        await message.answer("Отличная игра!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Поиграем ещё?",  reply_markup=get_main_keyboard())
        await state.finish()

    elif txt == "next":
        await message.answer("Дaльше...", reply_markup=types.ReplyKeyboardRemove())
        await game.match_question.set()

    elif txt != right_en or txt != "finish" or txt != "next":
        await message.answer(f"неверно, попробуйте ещё раз")
        return


# @dp.message_handler(state=game.match_question)
# async def question(message: types.Message, state: FSMContext):
#     val_row = random.sample(available_row(), 4)
#     options = [ws.cell(row=i, column=1).value.strip() for i in val_row]
#     match_keyboard(options)
#     right_row = random.choice(val_row)
#     right_en = ws.cell(row=right_row, column=1).value
#     right_ru = ws.cell(row=right_row, column=2).value
#     await state.update_data({
#                 'ans_en': right_en,
#                 'ans_ru': right_ru })
#     await message.answer(f'выберите перевод слова "{right_ru}"', reply_markup=match_keyboard(options))
#     txt = message.text
#
#     # await asyncio.sleep(5)
#     if txt == state.get_data("ans_ru"):
#         await message.answer(f"Верно! \n{right_en} - {right_ru}")
#         await message.answer(f"Пришли любое сообщение для продолжения")
#         return
#     elif txt == "next":
#         return
#
#     # elif txt !=right_en or txt != "finish" or txt != "next":
#     #     await message.answer(f"неверно, попробуйте ещё раз")
#     #     return
#
#     elif txt in options:
#         await message.answer(f"неверно, попробуйте ещё раз")
#
#     elif txt == "finish":
#         await message.answer("Отличная игра!", reply_markup=types.ReplyKeyboardRemove())
#         await message.answer("Поиграем ещё?",  reply_markup=get_main_keyboard())
#         await state.finish()




################################# game remember #############################################

@dp.message_handler(Command("remember"))
async def start_last(message: types.Message):
    await game.remember_question.set()
    await message.answer(f"Пришли любое сообщение для продолжения")

@dp.message_handler(state=game.remember_question)
async def question(message: types.Message, state: FSMContext):
    await game.remember_answer.set()
    right_row = random.choice(available_row())
    right_en = ws.cell(row=right_row, column=1).value
    right_ru = ws.cell(row=right_row, column=2).value
    await message.answer(f'вспомни перевод слова "{right_ru}"', reply_markup=type_keyboard())
    await state.update_data({
        'ans_en': right_en,
        'ans_ru': right_ru })

@dp.message_handler(state=game.remember_answer)
async def question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    right_en = data.get("ans_en")
    right_ru = data.get("ans_ru")
    txt = message.text.lower()
    if txt == "finish":
        await message.answer("Отличная игра!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Поиграем ещё?", reply_markup=get_main_keyboard())
        await state.finish()

    elif txt == "next":
        await message.answer(f"Пришли любое сообщение для продолжения")
        await game.remember_question.set()

    elif txt == "show right":
        await message.answer(f"{right_en} - {right_ru} ", reply_markup=types.ReplyKeyboardRemove())
        await game.remember_question.set()
        await message.answer(f"Пришли любое сообщение для продолжения")

    elif txt != "show right" or txt != "next" or txt != "right":
        await message.answer(f"неверно задана команда - используйте доступные команды из клавиатуры")
        return



################################# game type #############################################

@dp.message_handler(Command("type"))
async def start_last(message: types.Message):
    await game.type_question.set()
    await message.answer(f"Пришли любое сообщение для продолжения")

@dp.message_handler(state=game.type_question)
async def question(message: types.Message, state: FSMContext):
    await game.type_answer.set()
    right_row = random.choice(available_row())
    right_en = ws.cell(row=right_row, column=1).value
    right_ru = ws.cell(row=right_row, column=2).value
    await message.answer(f'напишите перевод слова "{right_ru}"', reply_markup=type_keyboard())
    await state.update_data({
        'ans_en': right_en,
        'ans_ru': right_ru })

@dp.message_handler(state=game.type_answer)
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    right_en = data.get("ans_en")
    right_ru = data.get("ans_ru")
    txt = message.text.lower()
    if txt == right_en.lower():
        await message.answer(f"Верно! \n{right_en} - {right_ru}", reply_markup=types.ReplyKeyboardRemove())
        await game.type_question.set()
        await message.answer(f"Пришли любое сообщение для продолжения")

    elif txt == "finish":
        await message.answer("Отличная игра!", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Поиграем ещё?", reply_markup=get_main_keyboard())
        await state.finish()

    elif txt == "next":
        await message.answer("Дaльше...", reply_markup=types.ReplyKeyboardRemove())
        await game.type_question.set()

    elif txt == "show right":
        await message.answer(f"{right_en} - {right_ru} \nНапечатайте для закрепления", reply_markup=types.ReplyKeyboardRemove())
        await game.type_answer.set()

    elif txt != right_en.lower() or txt != "finish" or txt != "next":
        await message.answer(f"неверно, попробуйте ещё раз")
        return




################################# edition #############################################

@dp.message_handler(Command("set_fav"))
async def start_last(message: types.Message):
    await edition.set_fav.set()
    await message.answer(list_num())
    await message.answer(f"Для добавления в избранное напишите номера слов из списка через запятую:")

@dp.message_handler(state=edition.set_fav)
async def set_fav_state(message: types.Message, state: FSMContext):
    data_fav = [int(i.strip()) for i in message.text.split(',')]
    for i in data_fav:
        if i in available_fav_row():
            ws['A' + str(i)].font = Font(bold=True)
            wb.save(path_to_file)
            await message.answer(f"'{ws['A' + str(i)].value}' добавлено в избранное")
        else:
            await message.answer(f"ошибка при добавлении слова, возможно слово уже в избранном '{ws['A' + str(i)].value}'")
    await state.finish()
    await message.answer("Продолжаем!", reply_markup=get_main_keyboard())

@dp.message_handler(Command("rem_fav"))
async def start_last(message: types.Message):
    await edition.rem_fav.set()
    await message.answer(favour_num())
    await message.answer(f"Для удаления слов из избранного напишите их номера из списка через запятую:")

@dp.message_handler(state=edition.rem_fav)
async def add_word(message: types.Message, state: FSMContext):
    try:
        [int(i.strip()) for i in message.text.split(',')]
    except:
        await message.answer(f"неверный формат, повторите ввод номеров")

    data_del = [int(i.strip()) for i in message.text.split(',')]
    for i in data_del:
        if i in available_fav_row():
            await message.answer(f"'{ws['A' + str(i)].value}' удалено из избранного")
            ws.delete_rows(idx=1, amount=1)
            wb.save(path_to_file)
        else:
            await message.answer(f"ошибка при удалении слова из избранного: отсутствует номер в списке '{ws['A' + str(i)].value}'")
    await state.finish()
    await message.answer("Продолжаем!", reply_markup=get_main_keyboard())


@dp.message_handler(state=edition.add_word)
async def add_word(message: types.Message, state: FSMContext):
    for i in message.text.splitlines():  #('\n'):
        ws.insert_rows(idx=1, amount=1)
        ws['A1'].value = i.split('-')[0].strip()
        ws['B1'].value = i.split('-')[1].strip()
        wb.save(path_to_file)
        await message.answer(f"В список добавлено '{ws['A1'].value}'")
    await state.finish()
    await message.answer("Продолжаем!", reply_markup=get_main_keyboard())


@dp.message_handler(state=edition.del_word)
async def add_word(message: types.Message, state: FSMContext):
    data_del = [int(i.strip()) for i in message.text.split(',')]
    for i in data_del:
        if i in available_row():
            await message.answer(f"'{ws['A' + str(i)].value}' удалено")
            ws.delete_rows(idx=1, amount=1)
            wb.save(path_to_file)
        else:
            await message.answer(f"ошибка при удалении слова '{ws['A' + str(i)].value}'")
    await state.finish()
    await message.answer("Продолжаем!", reply_markup=get_main_keyboard())


