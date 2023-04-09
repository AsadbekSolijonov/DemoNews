from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter


class GroupFilter(BoundFilter):
    async def check(self, message: Message):
        return message.chat.type in (ChatType.GROUP, ChatType.SUPER_GROUP)
