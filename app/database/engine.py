from typing_extensions import Self
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from typing import Any as Any, Generator, Optional
from dotenv import load_dotenv
from os import getenv


class SessionMaker:
    """
    SessionMaker
    数据库会话管理器
    创建数据库会话对象, 用于对数据库进行增删改查操作
    使用异步yield机制自动处理上下文, 保证session的创建和销毁
    之后session会用于依赖注入
    """

    engine: Optional[AsyncEngine] = None

    def __new__(cls) -> Self:
        load_dotenv()
        url = getenv("DATABASE_URL")
        if url is None:
            raise ValueError("未设置环境变量DATABASE_URL")
        engine = create_async_engine(url)
        new_cls = super().__new__(cls)
        new_cls.engine = engine
        return new_cls


maker = SessionMaker()


async def get_session():
    async with AsyncSession(maker.engine) as session:
        yield session
