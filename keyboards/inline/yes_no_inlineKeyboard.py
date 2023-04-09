from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def yes_no():
    inline_btn = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text='✅', callback_data='yes')
    no = InlineKeyboardButton(text='❌', callback_data='no')
    return inline_btn.add(no, yes)
