"""
bot/utils/states.py — FSM state groups.
"""
from aiogram.fsm.state import State, StatesGroup


class LangSelect(StatesGroup):
    choosing = State()


class Captcha(StatesGroup):
    solving = State()


class Registration(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()


class ChannelVerification(StatesGroup):
    waiting_for_join = State()
