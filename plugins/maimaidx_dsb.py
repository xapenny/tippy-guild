import aiohttp
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message


@Commands(("定数表"))
async def dsb(api: BotAPI, message: Message, params: str = None):
    level = params
    if level == '':
        await message.reply(content="请输入等级")
        return
    is_plus = False
    if '+' in level:
        is_plus = True
        level = level.replace('+', '')
    if not level.isdigit():
        await message.reply(content="定数输入错误")
        return
    if int(level) > 14:
        await message.reply(content="定数输入错误")
        return
    await message.reply(content="正在生成，请稍候")
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.post(
                    url="http://127.0.0.1:7981/TippyAPI/getMaimaiDsbApi",
                    timeout=15,
                    json={
                        'level': int(level),
                        'is_plus': is_plus
                    }) as response:
                if response.headers['content-type'] != 'image/jpg':
                    rj = await response.json(content_type=None)
                    await message.reply(content=rj['msg'])
                    return
                else:
                    rData = await response.read()
                    await message.reply(file_image=rData)
                    return
        except Exception as e:
            await message.reply(content=f"出现错误: {e}")
        return