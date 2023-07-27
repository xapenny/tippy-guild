import asyncio

from botpy import Client, Intents
from botpy.message import Message

from configs.config import config
from plugins.bind import bind
from plugins.chunithm_b30 import chub30
from plugins.jrys import jrys
from plugins.maimaidx_b50 import maib50
from plugins.maimaidx_dsb import dsb
from plugins.maimaidx_score import singleScore, scoreList
from plugins.search_song import query_song, search_song
from service.db_context import disconnect, init


class TippyClient(Client):

    async def on_at_message_create(self, message: Message):
        handlers = [
            bind, maib50, chub30, jrys, search_song, query_song, dsb,
            singleScore, scoreList
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return


if __name__ == '__main__':
    try:
        # init database
        loop = asyncio.get_event_loop()
        # 执行coroutine
        loop.run_until_complete(init())
        intents = Intents(public_guild_messages=True)
        client = TippyClient(intents=intents)
        client.run(appid=config['appid'], token=config['token'])
    except KeyboardInterrupt:
        loop = asyncio.get_event_loop()
        # 执行coroutine
        loop.run_until_complete(disconnect())