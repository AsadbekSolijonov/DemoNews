from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def put_location_keyboard():
    # This Keyboard for Send User's current Location
    location_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    loc_btn = KeyboardButton(text='Share your Location', request_location=True)
    share_location = location_btn.add(loc_btn)
    return share_location
