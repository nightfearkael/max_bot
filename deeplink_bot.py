import asyncio
import json
import requests

from maxapi import Bot, Dispatcher
from config import bot_token
from maxapi.types import BotStarted
from maxapi.types import CallbackButton, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.bot_started()
async def bot_started(event: BotStarted):
    if event.payload:
        data = {'token': event.payload, 'client_max_id': event.user.user_id}
        start_kb = InlineKeyboardBuilder()
        start_kb.row(CallbackButton(text='Согласен', payload=json.dumps(data)))
        await event.bot.send_message(
            chat_id=event.chat_id,
            text='Для продолжения подтвердите согласие на обработку персональных данных',
            attachments=[start_kb.as_markup()])
    else:
        await event.bot.send_message(
            chat_id=event.chat_id,
            text='''Ты начал диалог с ботом. Нажми:
        /start для стартового меню
        /id для вывода твоего id в MAX
        ''')


@dp.message_callback()
async def auth_callback(callback: MessageCallback):
    data = json.loads(callback.callback.payload)
    requests.post(url='API нашей CRM', json=data)
    await callback.answer(notification='passed')
    await callback.message.edit(attachments=[])

        
async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
