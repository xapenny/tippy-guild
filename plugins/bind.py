from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message
from models.guild_account import GuildQQBind
from service.log import logger


@Commands("绑定")
async def bind(api: BotAPI, message: Message, params: str = None):
    if params == 'bottest':
        userQQ = 550463623
    elif params == '' or not params.isdigit():
        await message.reply(content="请在指令后输入需要绑定的账号")
        # await message.reply(content="请在指令后输入需要绑定的账号\n例如: \"/绑定 bottest\"")
        return False
    else:
        userQQ = int(params)
    await GuildQQBind.bind_qq(user_id=userQQ, guild_id=message.author.id)
    await message.reply(content="绑定成功！")
    return