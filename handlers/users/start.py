from aiogram import types
from loader import dp

from filters import IsPrivate


@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}! \n\n'
                         f'Чтобы зарегестрироваться, введите /register')
