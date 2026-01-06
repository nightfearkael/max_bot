import asyncio
import requests
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageCreated, BotStarted

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message_created(F.message.body.attachments)
async def attachment_handler(event: MessageCreated):
    for attach in event.message.body.attachments:

        match attach.type:
            case 'image':
                file_name = f'{attach.payload.token[0:15]}.riff'
            case 'video':
                file_name = f'{attach.payload.token[0:15]}.mp4'
            case 'file':
                file_name = attach.filename
            case 'audio':
                file_name = f'{attach.payload.token[0:15]}.wav'
            case _:
                await event.message.answer('Не могу распознать файл')
                return None
        file_name = file_name.replace('/', '_')
        file_data = requests.get(url=attach.payload.url)
        with open(file_name, 'wb') as new_file:
            new_file.write(file_data.content)

    await event.message.answer(f'Файлы успешно скачаны!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
