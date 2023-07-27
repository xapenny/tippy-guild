from typing import Optional
from service.db_context import db
from sqlalchemy import Column, Integer, BigInteger, update, String

class GuildQQBind(db.Model):
    __tablename__ = 'guild_qq'
    qq_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    guild_id = Column(String,
                         nullable=False,
                         index=True,
                         unique=True)

    @classmethod
    async def bind_qq(cls, user_id: int, guild_id: str) -> bool:
        """
        说明：
            绑定QQ
        参数：
            :param user_id 用户id
            :param guild_id 频道用户id
        """
        query = cls.query.where(cls.guild_id == guild_id)
        user = await query.gino.first()
        if not user:
            await cls.create(qq_id=user_id, guild_id=guild_id)
        else:
            query = update(cls).where(cls.guild_id == guild_id).values(
            qq_id=user_id)
            await db.status(query)
        return True

    @classmethod
    async def get_real_qq(cls, guild_id: str) -> Optional[int]:
        """
        说明：
            获取真实qq
        参数：
            :param guild_id 频道用户id
        """

        query = await cls.query.where(cls.guild_id == guild_id).gino.first()
        if not query:
            return None
        return query.qq_id

    @classmethod
    async def unbind_qq(cls, guild_id: str) -> bool:
        """
        说明：
            解绑QQ
        参数：
            :param guild_id 频道用户id
        """
        query = cls.query.where(cls.guild_id == guild_id).with_for_update()
        user = await query.gino.first()
        if not user:
            return False
        await user.delete()
        return True