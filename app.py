async def on_startup(dp):

    import filters
    filters.setup(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('connecting to postgresql')
    await on_startup(dp)

    # print('удаление бд')
    # await db.gino.drop_all()

    print('создание таблиц')
    await db.gino.create_all()
    print('done')

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('done')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
