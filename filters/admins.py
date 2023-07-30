from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, message: Message):
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()
