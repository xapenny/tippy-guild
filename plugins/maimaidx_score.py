import aiohttp
from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message

from models.guild_account import GuildQQBind
from service.log import logger


@Commands(("单曲成绩"))
async def singleScore(api: BotAPI, message: Message, params: str = None):
    if params == '':
        await message.reply(content="请输入乐曲别名/乐曲名/乐曲id")
        return
    userQQ = await GuildQQBind.get_real_qq(guild_id=message.author.id)
    if userQQ is None:
        await message.reply(content="请先绑定账号")
        return
    payload = {"user_qq": userQQ, "title": params}
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.post(
                    url=
                    "http://127.0.0.1:7981/TippyAPI/getMaimaiSingleScoreApi",
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


@Commands(("成绩列表"))
async def scoreList(api: BotAPI, message: Message, params: str = None):
    if params == '':
        await message.reply(content="""欢迎使用maimai分数查询功能 (beta)
用法: 成绩列表 查询关键词 页码
""")
        return

    userQQ = await GuildQQBind.get_real_qq(guild_id=message.author.id)
    if userQQ is None:
        await message.reply(content="请先绑定账号")
        return
    payload = {"user_qq": userQQ, "title": params}
    await message.reply(content="正在生成，请稍候")
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=15) as session:
        try:
            async with session.post(
                    url="http://127.0.0.1:7981/TippyAPI/getMaimaiScoreApi",
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
