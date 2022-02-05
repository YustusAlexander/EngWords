from aiogram.dispatcher.filters.state import StatesGroup, State


class showing(StatesGroup):
    last = State()
    rand = State()

class edition(StatesGroup):
    set_fav = State()
    rem_fav = State()
    add_word = State()
    del_word = State()

class game(StatesGroup):
    match_question = State()
    match_answer = State()
    type_question = State()
    type_answer = State()
    remember_question = State()
    remember_answer = State()