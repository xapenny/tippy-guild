from base64 import b64decode

import aiohttp
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message


@Commands("查歌")
async def search_song(api: BotAPI, message: Message, params: str = None):
    if params == '':
        await message.reply(content="请输入关键词，例如: /查歌 pandora")
        return
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.get(
                    url=
                    f"http://127.0.0.1:7981/TippyAPI/searchSongApi/{params}",
                    timeout=15,
            ) as response:
                rj = await response.json()
                await message.reply(content=rj['data'].replace(
                    '\n\n若要查询歌曲详细信息，请发送"id 歌曲id"\n例如"id m786"\n若要试听歌曲，请发送"mid 歌曲id"\n例如"mid m786"',
                    '\n若要查询歌曲详细信息，请@提比并发送"/乐曲信息 乐曲id"\n例如"@提比 /乐曲信息 m786"'))
                return
        except Exception as e:
            await message.reply(content=f"出现错误: {e}")
        return


@Commands("乐曲信息")
async def query_song(api: BotAPI, message: Message, params: str = None):
    if not params.lower().startswith(
        ('b', 'p', 'm', 'u', 'c', 'z', 'l', 't', 'a', 'g')):
        await message.reply(content="请输入正确的id， 例如: /乐曲信息 m834")
        return
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.get(
                    url=
                    f"http://127.0.0.1:7981/TippyAPI/getSongDetailApi/{params}",
                    timeout=15,
            ) as response:
                if response.headers['content-type'] != 'image/jpg':
                    rj = await response.json(content_type=None)
                    if rj['success']:
                        await message.reply(content=rj['data'][0])
                        await message.reply(
                            file_image=b64decode(rj['data'][1][9:]))
                        return
                    else:
                        await message.reply(content=rj['data'])
                else:
                    rData = await response.read()
                    await message.reply(file_image=rData)
                    return
        except Exception as e:
            await message.reply(content=f"出现错误: {e}")
        return