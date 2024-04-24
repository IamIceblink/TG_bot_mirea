from aiogram.types import BotCommand

"""This file is responsible for all bot commands."""

private = [
    BotCommand(command='menu', description='Check out the menu'),
    BotCommand(command='about', description='About the developers'),
    BotCommand(command='newtask', description='Create a new task'),
    BotCommand(command='mytask', description='Show current tasks'),
]