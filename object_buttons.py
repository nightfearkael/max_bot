import asyncio
from maxapi import Bot, Dispatcher, F
from maxapi.types import Command, MessageCreated, BotStarted,
from maxapi.types import LinkButton, RequestContactButton, RequestGeoLocationButton

from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message_created(Command('link'))
async def link_message(event: MessageCreated):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(LinkButton(text='Ссылка на документацию',
                            url='https://dev.max.ru/docs-api'))
    await event.message.answer('Message with link button', attachments=[keyboard.as_markup()])


@dp.message_created(Command('contact'))
async def contact_message(event: MessageCreated):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(RequestContactButton(text='Поделиться контактом'))
    await event.message.answer('Поделиться контактом?', attachments=[keyboard.as_markup()])


@dp.message_created(F.message.body.attachments[0].type == 'contact')
async def get_contact(event: MessageCreated):
    await event.message.forward(chat_id=manager_id)
    await event.message.answer('Я переслал ваш контакт менеджеру')


@dp.message_created(Command('geo'))
async def geo_message(event: MessageCreated):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(RequestGeoLocationButton(text='Поделиться геопозицией'))
    await event.message.answer('Поделиться геопозицией?', attachments=[keyboard.as_markup()])


@dp.message_created(F.message.body.attachments[0].type == 'location')
async def get_contact(event: MessageCreated):
    await event.message.forward(chat_id=manager_id)
    await event.message.answer('Я переслал ваш контакт менеджеру')



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
