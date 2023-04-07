from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter

class Private(BoundFilter):
    async def check(self, message: Message):
        return message.chat.type == ChatType.PRIVATE
