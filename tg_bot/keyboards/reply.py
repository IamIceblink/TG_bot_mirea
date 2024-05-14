from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="New Task 😁"),
            KeyboardButton(text="My tasks 🙏"),   
        ],
        [
            KeyboardButton(text="About 🤓"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your command:'
)


cancel_kb =ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Cancel"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='You may cancel input whether you want...'
)


task_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Edit"),
        KeyboardButton(text="Delete"),
        ],
        [
        KeyboardButton(text="Cancel"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="What do you wish to do with them?"
)


begin_kb =ReplyKeyboardMarkup(
    keyboard=[
        [
        ],
    ],
    input_field_placeholder="What is your name?"
)


new_group_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="New Group"),
        ],
        [
        KeyboardButton(text="Cancel"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="You can create a new group below..."
)