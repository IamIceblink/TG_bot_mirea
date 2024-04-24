from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Hi Petro")


@user_private_router.message(Command('menu'))
async def menu_handler(message: types.Message):
    await message.answer("Here's menu:")


@user_private_router.message(Command('make_task'))
async def make_task_handler(message: types.Message):
    await message.answer("Here's your task:")


@user_private_router.message(Command('about'))
async def make_task_handler(message: types.Message):
    await message.answer("Authors: Ryabov V.M. Gilas A.D. Tuzhenkov K.G. IVBO-03-21 MIREA")


@user_private_router.message(F.audio)
async def audio_handler(message: types.Message):
    await message.answer("Bot doesn't support audio.")


@user_private_router.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("Bot doesn't recognise photos.")


@user_private_router.message(F.sticker)
async def sticker_handler(message: types.Message):
    await message.answer(message.text)




