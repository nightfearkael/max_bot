from maxapi import Bot
from config import bot_token, group_id
import asyncio


async def kick_member(user_id):
    await bot.kick_chat_member(chat_id=group_id, user_id=user_id, block=True)
    await bot.close_session()


async def get_chat_info(group_id):
    chat = await bot.get_chat_by_id(id=group_id)
    await bot.close_session()
    return chat


async def get_all_members(group_id):
    result = await bot.get_chat_members(chat_id=group_id)
    members_list = result.members
    await bot.close_session()
    recipients_list = []
    for member in members_list:
        if not member.is_admin:
            recipients_list.append({'id': member.user_id, 'name': member.first_name})
    return recipients_list


if __name__ == '__main__':
    bot = Bot(token=bot_token)
    #members = asyncio.run(get_all_members(group_id))
    #print(members)
    #chat_info = asyncio.run(get_chat_info(group_id))
    #asyncio.run(kick_member(152784485))
