from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_groups, orm_get_tasks_by_group


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="New Task 😁", callback_data="new_task"),
            InlineKeyboardButton(text="My tasks 🙏", callback_data="my_tasks"),   
        ],
        [
            InlineKeyboardButton(text="About 🤓", callback_data="about"),
        ]
    ],
)




cancel_about_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel 🥵", callback_data="cancel_about"),
        ]
    ],
)




cancel_new_group_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel 🥵", callback_data="cancel_new_group"),
        ]
    ],
)


options_for_groups_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Change Group Name", callback_data="change_group_name"),
            InlineKeyboardButton(text="Delete Group", callback_data="delete_group"),   
        ],
        [
            InlineKeyboardButton(text="Cancel 🥵", callback_data="cancel_new_group"),
        ]
    ],
)


cancel_new_task_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cancel 🥵", callback_data="new_task")
        ]
    ],
)





#для my tasks
async def inline_groups_my_tasks(session: AsyncSession, tg_id: int):
    keyboard = InlineKeyboardBuilder()
    for one_group in await orm_get_groups(session, tg_id):
        keyboard.add(InlineKeyboardButton(text = one_group.name, callback_data= f'group_{one_group.id}'))
    keyboard.adjust(1)
    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Edit", callback_data = "edit_group"),
                InlineKeyboardButton(text="New Group", callback_data = "new_group"),
            ],
            [
                InlineKeyboardButton(text="Cancel 🥵", callback_data = "cancel_about"),
            ]
        ],                           
    )
    keyboard.attach(InlineKeyboardBuilder.from_markup(keyboard2))
    return keyboard.as_markup()



#для прогрузки тасков через группы в my tasks

async def inline_tasks_from_group(session: AsyncSession, group_id: int):
    keyboard = InlineKeyboardBuilder()
    for task in await orm_get_tasks_by_group(session, group_id):
        keyboard.add(InlineKeyboardButton(text = task.name, callback_data=f"isDone_{task.id}"))
    keyboard.adjust(1)
    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Cancel 🥵", callback_data="cancel_new_group"),
            ]
        ],                           
    )
    keyboard.attach(InlineKeyboardBuilder.from_markup(keyboard2))
    return keyboard.as_markup()


#для new task

async def inline_groups_new_task(session: AsyncSession, tg_id: int):
    keyboard = InlineKeyboardBuilder()
    for one_group in await orm_get_groups(session, tg_id):
        keyboard.add(InlineKeyboardButton(text = one_group.name, callback_data=f"myTaskGroup_{one_group.id}"))
    keyboard.adjust(1)
    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Cancel 🥵", callback_data=f"cancel_about"),
            ]
        ],                           
    )
    keyboard.attach(InlineKeyboardBuilder.from_markup(keyboard2))
    return keyboard.as_markup()


#для edit groups

async def inline_edit_groups(session: AsyncSession, tg_id: int):
    keyboard = InlineKeyboardBuilder()
    for one_group in await orm_get_groups(session, tg_id):
        keyboard.add(InlineKeyboardButton(text = one_group.name, callback_data=f"editExactGroup_{one_group.id}"))
    keyboard.adjust(1)
    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Cancel 🥵", callback_data="cancel_new_group"),
            ]
        ],                           
    )
    keyboard.attach(InlineKeyboardBuilder.from_markup(keyboard2))
    return keyboard.as_markup()


#для delete groups

async def inline_delete_groups(session: AsyncSession, tg_id: int):
    keyboard = InlineKeyboardBuilder()
    for one_group in await orm_get_groups(session, tg_id):
        keyboard.add(InlineKeyboardButton(text = one_group.name, callback_data=f"deleteExactGroup_{one_group.id}"))
    keyboard.adjust(1)
    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Cancel 🥵", callback_data="edit_group"),
            ]
        ],                           
    )
    keyboard.attach(InlineKeyboardBuilder.from_markup(keyboard2))
    return keyboard.as_markup()





    
