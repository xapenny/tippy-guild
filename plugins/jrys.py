import aiohttp
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message

from models.guild_account import GuildQQBind


@Commands("今日运势")
async def jrys(api: BotAPI, message: Message, params: str = None):
    userQQ = await GuildQQBind.get_real_qq(guild_id=message.author.id)
    if userQQ is None:
        await message.reply(content="请先绑定账号")
        return
    payload = {"userQQ": userQQ, "nickName": message.author.username}
    await message.reply(content="正在生成，请稍候")
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.post(
                    url="http://127.0.0.1:7981/TippyAPI/getJrysApi",
                    timeout=15,
                    json=payload) as response:
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