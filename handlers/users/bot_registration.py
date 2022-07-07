from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
# from keyboards.default import kb_menu
from loader import dp

from filters import IsPrivate
from states import registration\
    # , accept
from utils.db_api import register_commands


@dp.message_handler(text='Отменить регистрацию', state=[registration.name, registration.lastname, registration.fname,
                                                        registration.phone, registration.email])
async def quit(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация отменена.')


@dp.message_handler(IsPrivate(), Command('register'))
async def bot_register(message: types.Message):
    await message.answer(f'Введите ваше имя:')
    await registration.name.set()


@dp.message_handler(IsPrivate(), state=registration.name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Введите фамилию:', reply_markup=markup)
    await registration.lastname.set()


@dp.message_handler(IsPrivate(), state=registration.lastname)
async def get_lastname(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(lastname=answer)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Введите отчество:', reply_markup=markup)
    await registration.fname.set()


@dp.message_handler(IsPrivate(), state=registration.fname)
async def get_fname(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(fname=answer)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Введите номер телефона:', reply_markup=markup)
    await registration.phone.set()


@dp.message_handler(IsPrivate(), state=registration.phone)
async def get_phone(message: types.Message, state: FSMContext):
    answer = message.text
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    try:
        if answer.replace('+', '').isnumeric():
            await state.update_data(phone=answer)
            await message.answer(f'Введите электронную почту:', reply_markup=markup)
            await registration.email.set()
        else:
            await message.answer(f'Введите корректный номер телефона', reply_markup=markup)
    except Exception:
        await message.answer(f'Введите корректный номер телефона', reply_markup=markup)


@dp.message_handler(IsPrivate(), state=registration.email)
async def get_email(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(email=answer)
    data = await state.get_data()
    name = data.get('name')
    lastname = data.get('lastname')
    fname = data.get('fname')
    phone = data.get('phone')
    email = data.get('email')
    await register_commands.new_registration(user_id=message.from_user.id,
                                             tg_first_name=message.from_user.first_name,
                                             tg_last_name=message.from_user.last_name,
                                             name=name,
                                             lastname=lastname,
                                             fname=fname,
                                             phone=phone,
                                             email=email,
                                             status='created')
    await message.answer(f'Регистрация успешно завершена!\n\n'
                         f'Имя: {name}\n'
                         f'Фамилия: {lastname}\n'
                         f'Отчество: {fname}\n'
                         f'Телефон: {phone}\n'
                         f'Электронная почта: {email}')
    await state.finish()


# @dp.message_handler(IsPrivate(), text='/registrations', user_id=admins)
# async def get_reg(message: types.Message):
#     reg = await register_commands.select_registration()
#     ikb = InlineKeyboardMarkup(row_width=1,
#                                inline_keyboard=[
#                                    [
#                                        InlineKeyboardButton(text='accept', callback_data='accept')
#                                    ]
#                                ])
#     await message.answer(f'Дата создания: {reg.created_at}\n'
#                          f'id: {reg.user_id}\n'
#                          f'tg_first_name: {reg.tg_first_name}\n'
#                          f'tg_lat_name: {reg.tg_last_name}\n'
#                          f'Имя: {reg.name}\n'
#                          f'Телефон: {reg.phone}\n', reply_markup=ikb)
#
#
# @dp.callback_query_handler(state='accept')
# async def accept_reg(call: types.CallbackQuery):
#     await call.message.answer(f'введите айди для подтверждения: ')
#     await accept.user_id.set()
#
#
# @dp.message_handler(state=accept.user_id)
# async def accept_reg(message: types.Message, state: FSMContext):
#     await register_commands.accept_registration(message.text)
#     await message.answer(f'подтвержден')
#     await state.finish()
