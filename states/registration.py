from aiogram.dispatcher.filters.state import StatesGroup, State


class registration(StatesGroup):
    name = State()
    lastname = State()
    fname = State()
    phone = State()
    email = State()


# class accept(StatesGroup):
#     user_id = State()
