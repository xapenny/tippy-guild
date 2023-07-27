import aiohttp
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message

from models.guild_account import GuildQQBind
from service.log import logger


@Commands(("舞萌b40", "舞萌b50"))
async def maib50(api: BotAPI, message: Message, params: str = None):
    userName = params
    userQQ = await GuildQQBind.get_real_qq(guild_id=message.author.id)
    if userQQ is None:
        if userName == '':
            await message.reply(content="请先绑定账号或输入用户名")
            return
        userQQ = message.author.id
    payload = {"userQQ": userQQ}
    if userName != '':
        payload['userName'] = userName
    await message.reply(content="正在生成，请稍候")
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.post(
                    url="http://127.0.0.1:7981/TippyAPI/getMaimaiB50Api",
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
