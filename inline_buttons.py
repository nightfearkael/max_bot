import asyncio
import logging

from maxapi import Bot, Dispatcher, F
from config import bot_token
from maxapi.types import Command, MessageCreated, BotStarted
from maxapi.types import InputMedia

from maxapi.types import CallbackButton, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.message_created(Command('kb'))
async def keyboard_message(event: MessageCreated):
    photo = InputMedia('blank_user.jpg')

    kb = InlineKeyboardBuilder()

    kb.row(CallbackButton(text='Callback button 1', payload='test1'),
           CallbackButton(text='Callback button 2', payload='test2'))

    await event.bot.send_message(user_id=event.from_user.user_id, text='test message',
                                 attachments=[photo, kb.as_markup()])


@dp.message_callback(F.callback.payload == 'test1')
async def message_callback(callback: MessageCallback):
    await callback.message.answer(f'Вы нажали на Callback! Payload: {callback.callback.payload}')


@dp.message_callback(F.callback.payload == 'test2')
async def message_callback(callback: MessageCallback):
    await callback.message.edit(text='pressed callback', attachments=[])
    await callback.message.answer(f'Вы нажали на Callback! Payload: {callback.callback.payload}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
