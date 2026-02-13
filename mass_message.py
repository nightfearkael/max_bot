from maxapi import Bot
import asyncio
from config import bot_token
from maxapi.types import CallbackButton, LinkButton
from maxapi.types import InputMedia
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.utils.message import process_input_media


async def send_mass_message(users: list, message: str, keys: dict, image: str):
    if len(users) > 30:
        raise ValueError('Нельзя передавать больше 30 ID за раз')

    attachment_kb = InlineKeyboardBuilder()
    for key, value in keys.items():
        if 'http' in value:
            new_key = LinkButton(text=key, url=value)
        else:
            new_key = CallbackButton(text=key, payload=value)
        attachment_kb.add(new_key)

    bot = Bot(token=bot_token)

    photo = await process_input_media(bot, bot, InputMedia(image))

    for user in users:
        await bot.send_message(user_id=user, text=f'{message}', attachments=[attachment_kb.as_markup(), photo])
    await bot.close_session()


asyncio.run(send_mass_message(users=[123123123, 123123123, 123123123, 123123123],
                              message='test',
                              keys={'button1': 'test1', 'button2': 'test2', 'url button': 'https://google.com'},
                              image='blank_user.jpg'))
