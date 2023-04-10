from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def put_phone_keyboard():
    # This is Keyboard for Sharing phone number
    contact_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    contact = KeyboardButton('Share Phone number', request_contact=True)
    contact_btn.add(contact)
    return contact_btn
