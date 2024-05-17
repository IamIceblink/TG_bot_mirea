from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_group, orm_add_task, orm_delete_group, orm_edit_group, orm_delete_task, set_user, orm_your_name, orm_change_your_name, orm_get_name 

from keyboards import reply, inline

from database.models import Task, User, Group


user_private_router = Router()


#FSM

class NewTask(StatesGroup):
    group = State()
    name = State()
    newgroup = State()


class MyTask(StatesGroup):
    lists = State()
    edit = State()
    delete = State()
    new_name = State()


class NewUser(StatesGroup):
    begin = State()
    your_name = State()


class ChangeName(StatesGroup):
    change = State()
    acceptance = State()


#FSM




@user_private_router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.clear()
    if await set_user(session, message.from_user.id) == True:
        await message.answer(("Hello " + str(await orm_get_name(session, message.from_user.id)) + "!"), reply_markup=inline.start_kb)
    else:
        await message.answer("СЮДА ДОБАВИТЬ ИНТРО", reply_markup=reply.begin_kb)
        await state.set_state(NewUser.begin)


@user_private_router.message(NewUser.begin, F.text)
async def your_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(your_name=message.text)
    data = await state.get_data()
    try:
        await orm_your_name(session, message.from_user.id, data)
        await message.answer("Your name was saved")
        await message.answer(("Hello " + str(await orm_get_name(session, message.from_user.id)) + "!"), reply_markup=inline.start_kb)
        await state.clear() 
    except Exception as e:
        await message.answer(
            "Error! Write shorter name"
        )
        


@user_private_router.message(StateFilter('*'), F.text.lower() == "cancel")
async def cancel_handler(message:types.Message, state:FSMContext) -> None:
    
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer("Your operations were canceled.", reply_markup=reply.start_kb)
 

#---------------------------------------------------------------------------------------





@user_private_router.message(NewTask.group, F.text != "New Group")
async def choose_group_handler(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)#ВМЕСТО MESSAGE.TEXT ВЫБРАННАЯ ГРУППА ИЗ СПИСКА 
    await message.answer("Here's your task groups:", reply_markup=reply.new_group_kb)
    await state.set_state(NewTask.name)


# Добавление новых групп
#---------------------------------------------------------------------------------------


@user_private_router.message(NewTask.group, F.text == "New Group")
async def new_group_name_handler(message: types.Message, state: FSMContext):
    await message.answer("What is the name of your new group?", reply_markup=reply.cancel_kb)
    await state.set_state(NewTask.newgroup)





#---------------------------------------------------------------------------------------    


@user_private_router.message(NewTask.name, F.text)
async def call_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    try:
        await orm_add_task(session,data)
        await message.answer("The task is added", reply_markup=inline.start_kb)
        await state.clear()
    except Exception as e:
        await message.answer(
            "Error! Write other name."
        )



#@user_private_router.message(StateFilter(None), F.text == "My tasks 🙏")
#async def get_task_handler(message: types.Message, session: AsyncSession, state: FSMContext):
#    for task in await orm_get_tasks(session):
#        await message.answer(str(task.group), reply_markup=reply.task_kb) 
#   await state.set_state(MyTask.lists)





@user_private_router.message(Command('change_name'))
async def change_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("What is your new name?", reply_markup=reply.cancel_kb)
    await state.set_state(ChangeName.acceptance)




@user_private_router.message(ChangeName.acceptance, F.text)
async def accept_new_name_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(acceptance=message.text)
    data = await state.get_data()
    try:
        await orm_change_your_name(session, message.from_user.id, data)
        await message.answer("Your name was changed")
        await state.clear() 
        await message.answer(("Hello " + str(await orm_get_name(session, message.from_user.id)) + "!"), reply_markup=inline.start_kb)
    except Exception as e:
        await message.answer(
            "Error! Write shorter name", reply_markup=reply.begin_kb
        )
    

@user_private_router.message(StateFilter('*'), F.audio)
async def audio_handler(message: types.Message):
    await message.answer("Bot doesn't support audio.")




@user_private_router.message(StateFilter('*'), F.photo)
async def photo_handler(message: types.Message):
    await message.answer("Bot doesn't recognise photos.")




@user_private_router.message(StateFilter('*'), F.sticker)
async def sticker_handler(message: types.Message):
    await message.answer("Bot doesn't recognise stickers.")




@user_private_router.message(StateFilter(None), F.text)
async def start_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.clear()
    if await set_user(session, message.from_user.id) == True:
        await message.answer(("Hello " + str(await orm_get_name(session, message.from_user.id)) + "!"), reply_markup=inline.start_kb)
    else:
        await message.answer("Вы перешли в телеграм бота списка дел. Здесь вы можете хранить свои задания. Пожалуйста, назовите своё имя 👋", reply_markup=reply.begin_kb)
        await state.set_state(NewUser.begin)


#Callbacks
#-------------------------------------------------------------------------------------------------------------------------------

@user_private_router.callback_query(F.data == "about")
async def about(callback: types.CallbackQuery):
    await callback.message.edit_text("Authors: Ryabov V.M. Gilas A.D. Tuzhenkov K.G. IVBO-03-21 MIREA", reply_markup=inline.cancel_about_kb)




@user_private_router.callback_query(F.data == "cancel_about")
async def cancel_about(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(("Hello " + str(await orm_get_name(session, callback.from_user.id)) + "!"), reply_markup=inline.start_kb)




@user_private_router.callback_query(F.data == "my_tasks")
async def my_tasks(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(("Here's your task groups:"), reply_markup=await inline.inline_groups_my_tasks(session, callback.from_user.id))




@user_private_router.callback_query(F.data == "new_group")
async def new_group(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.message.edit_text(("What's the name of a new group?"), reply_markup=inline.cancel_new_group_kb)
    await state.set_state(NewTask.newgroup)

@user_private_router.message(NewTask.newgroup, F.text)
async def new_group_name_acceptance_handler(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(newgroup=message.text)
    data = await state.get_data()
    try:
        await orm_add_group(session, data, message.from_user.id)
        await message.answer("New group was saved.")
        await state.clear() 
        await message.answer(("Hello " + str(await orm_get_name(session, message.from_user.id)) + "!"), reply_markup=inline.start_kb)
    except Exception as e:
        await message.answer(
            "Error! Write shorter name"
        )


@user_private_router.callback_query(F.data == "cancel_new_group")
async def cancel_new_group(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(("Here's your task groups:"), reply_markup=await inline.inline_groups_my_tasks(session, callback.from_user.id))



@user_private_router.callback_query(F.data == "edit_group")
async def edit_group(callback: types.CallbackQuery):
    await callback.message.edit_text(("What do you want to do?"), reply_markup=inline.options_for_groups_kb)



@user_private_router.callback_query(F.data == "delete_group")
async def delete_group(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(("Which group do you want to delete?"), reply_markup=await inline.inline_delete_groups(session, callback.from_user.id))


@user_private_router.callback_query(F.data.startswith("deleteExactGroup_"))
async def deleteExactGroup_(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MyTask.delete)
    await state.update_data(delete=callback.data.split('_')[1])
    data = await state.get_data()
    try:
        await orm_delete_group(session, data["delete"])
        await callback.answer("The group was deleted")
        await state.clear() 
        await callback.message.edit_text(("Here's your task groups:"), reply_markup=await inline.inline_groups_my_tasks(session, callback.from_user.id))
    except Exception as e:
        await callback.answer(
            "Error!"
        )



@user_private_router.callback_query(F.data == "change_group_name")
async def change_group_name(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.message.edit_text(("Which group do you want to rename?"), reply_markup=await inline.inline_edit_groups(session, callback.from_user.id))



@user_private_router.callback_query(F.data.startswith("group_"))
async def group_(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MyTask.lists)
    await state.update_data(lists = callback.data.split('_')[1])
    await callback.message.edit_text(("Here's your tasks:"), reply_markup=await inline.inline_tasks_from_group(session, callback.data.split('_')[1])) 



@user_private_router.callback_query(F.data.startswith("editExactGroup_"))
async def editExactGroup_(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(MyTask.edit)
    await state.update_data(edit=callback.data.split('_')[1])
    await callback.message.edit_text(("What's a new name of the group?"), reply_markup=inline.cancel_new_group_kb)


@user_private_router.message(MyTask.edit, F.text)
async def editExactGroup_write_name(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.set_state(MyTask.new_name)
    await state.update_data(new_name = message.text)
    data = await state.get_data()
    try:
        await orm_edit_group(session, data, data["edit"])
        await message.answer("New group name was saved.")
        await state.clear() 
        await message.answer(("Here's your task groups:"), reply_markup=await inline.inline_groups_my_tasks(session, message.from_user.id))
    except Exception as e:
        await message.answer(
            "Error!"
        )



#new task

@user_private_router.callback_query(F.data == "new_task")
async def new_task(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.message.edit_text("Choose the group:", reply_markup=await inline.inline_groups_new_task(session, callback.from_user.id))
    




@user_private_router.callback_query(F.data.startswith("myTaskGroup_"))
async def myTaskGroup_(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.set_state(NewTask.group)
    await state.update_data(group = callback.data.split('_')[1])
    await callback.message.edit_text("What is the name of a new task?", reply_markup=inline.cancel_new_task_kb)
    await state.set_state(NewTask.name)





@user_private_router.message(NewTask.name, F.text)
async def myTaskName(message: types.Message, session: AsyncSession, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    try:
        await orm_add_task(session, data)
        await message.answer("New task was created")
        await state.clear() 
        await message.answer(("Here's your task groups:"), reply_markup=await inline.inline_groups_my_tasks(session, message.from_user.id))
    except Exception as e:
        await message.answer(
            "Error in new Task!"
        )
    

#выполнение дел

@user_private_router.callback_query(MyTask.lists, F.data.startswith("isDone_"))
async def isDone(callback: types.CallbackQuery, session: AsyncSession, state:FSMContext):
    await orm_delete_task(session, callback.data.split('_')[1])
    data = await state.get_data()
    await callback.answer("The task is done!")
    await callback.message.edit_text(("Here's your tasks:"), reply_markup=await inline.inline_tasks_from_group(session, data["lists"]))

