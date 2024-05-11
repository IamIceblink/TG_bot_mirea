from aiogram.types import BotCommand

"""This file is responsible for all bot commands."""

private = [
    BotCommand(command='about', description='About the developers'),
    BotCommand(command='my_lists', description='Show lists of your tasks'),
    BotCommand(command='start', description='Start again'),
]