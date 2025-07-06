from src.services.publishe_chat_id_service import publish_chat_id

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("register_chat"))
async def register_chat(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("Ця команда працює тільки в групах.")
        return

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("administrator", "creator"):
        await message.reply("Тільки адміністратор може зареєструвати цей чат.")
        return

    await publish_chat_id(message.chat.id)
    await message.reply("✅ Запит на реєстрацію чату надіслано.")
