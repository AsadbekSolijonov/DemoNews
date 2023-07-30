from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def yes_no():
    # This inline keyboard for confirming the weather time
    inline_btn = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text='✅', callback_data='yes')
    no = InlineKeyboardButton(text='❌', callback_data='no')
    return inline_btn.add(no, yes)
