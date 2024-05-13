from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_get_tasks, set_user, orm_your_name

from keyboards import reply


user_private_router = Router()


#FSM

class NewTask(StatesGroup):
    group = State()
    name = State()
    date = State()


class MyTask(StatesGroup):
    lists = State()
    edit = State()
    delete = State()

class NewUser(StatesGroup):
    begin = State()
    your_name = State()

#FSM




@user_private_router.message(StateFilter(None), CommandStart())
async def start_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    if await set_user(session, message.from_user.id) == True:
        await message.answer("Привет, ", reply_markup=reply.start_kb)
    else:
        await message.answer("СЮДА ДОБАВИТЬ ИНТРО", reply_markup=reply.begin_kb)
        await state.set_state(NewUser.begin)


@user_private_router.message(NewUser.begin, F.text)
async def your_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(your_name=message.text)
    data = await state.get_data()
    try:
        await orm_your_name(session, message.from_user.id, data)
        await message.answer("Your name was saved", reply_markup=reply.start_kb)
        await state.clear() 
    except Exception as e:
        await message.answer(
            "Error! Write shorter name", reply_markup=reply.begin_kb
        )
        await state.set_state(NewUser.begin)


@user_private_router.message(StateFilter('*'), F.text.lower() == "cancel")
async def cancel_handler(message:types.Message, state:FSMContext) -> None:
    
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer("Your operations were canceled.", reply_markup=reply.start_kb)
 



@user_private_router.message(StateFilter(None), F.text == "New Task 😁")
async def new_task_handler(message: types.Message, state: FSMContext):
    await message.answer("Choose a task group", reply_markup=reply.cancel_kb)
    await state.set_state(NewTask.group)




@user_private_router.message(NewTask.group, F.text)
async def choose_group_handler(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer("Call your task", reply_markup=reply.cancel_kb)
    await state.set_state(NewTask.name)


@user_private_router.message(NewTask.group)
async def choose_group_handler(message: types.Message, state: FSMContext):
    await message.answer("Invalid group name", reply_markup=reply.cancel_kb)




@user_private_router.message(NewTask.name, F.text)
async def call_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Choose the date", reply_markup=reply.cancel_kb)
    await state.set_state(NewTask.date)


@user_private_router.message(NewTask.name)
async def call_name_handler(message: types.Message, state: FSMContext):
    await message.answer("Invalid task name", reply_markup=reply.cancel_kb)




@user_private_router.message(NewTask.date, F.text)
async def choose_date_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(date=message.text)
    data = await state.get_data()
    try:
        await orm_add_task(session,data)
        await message.answer("The task is added", reply_markup=reply.start_kb)
        await state.clear()
    except Exception as e:
        await message.answer(
            "Error!", reply_markup=reply.start_kb
        )
        await state.clear()

    
    

@user_private_router.message(NewTask.date)
async def choose_date_handler(message: types.Message, state: FSMContext):
    await message.answer("Invalid date", reply_markup=reply.cancel_kb)



@user_private_router.message(StateFilter(None), F.text == "My tasks 🙏")
async def get_task_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    for task in await orm_get_tasks(session):
        await message.answer(str(task.group), reply_markup=reply.task_kb) 
    await state.set_state(MyTask.lists)




@user_private_router.message(Command('change_name'))
async def your_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(your_name=message.text)
    data = await state.get_data()
    try:
        await orm_your_name(session, message.from_user.id, data)
        await message.answer("Your name was saved", reply_markup=reply.start_kb)
        await state.clear() 
    except Exception as e:
        await message.answer(
            "Error! Write shorter name", reply_markup=reply.begin_kb
        )
        await state.clear()
    




@user_private_router.message(Command('about'))
async def about_handler(message: types.Message):
    await message.answer("Authors: Ryabov V.M. Gilas A.D. Tuzhenkov K.G. IVBO-03-21 MIREA")




@user_private_router.message(F.text == "About 🤓")
async def about_handler(message: types.Message):
    await message.answer("Authors: Ryabov V.M. Gilas A.D. Tuzhenkov K.G. IVBO-03-21 MIREA")




@user_private_router.message(F.audio)
async def audio_handler(message: types.Message):
    await message.answer("Bot doesn't support audio.")




@user_private_router.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("Bot doesn't recognise photos.")




@user_private_router.message(F.sticker)
async def sticker_handler(message: types.Message):
    await message.answer("Task with stickers cannot be created.")




@user_private_router.message(F.emoji)
async def sticker_handler(message: types.Message):
    await message.answer("If you want to create task, please press appropriate button.")










