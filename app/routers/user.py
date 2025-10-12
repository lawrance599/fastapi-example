from fastapi import APIRouter, Depends, Path, HTTPException, Form
from sqlmodel import select
from app.database import User, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from hashlib import sha256
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def read_user(
    id: int = Path(..., title="用户ID"),
    session: AsyncSession = Depends(get_session),
):
    # 查询用户的语句
    statement = select(User).where(User.id == id)
    # 使用execute方法执行查询语句
    user = (await session.execute(statement)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/add")
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    # 不存储用户密码明文
    hashed_password = sha256(password.encode()).hexdigest()
    # 新用户实例
    user = User(
        username=username,
        password=hashed_password,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    try:
        # 添加用户
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except SQLAlchemyError as e:
        # 发生错误时回滚事务
        # TODO: 增加错误处理粒度, 对于某些错误, 可以返回更详细的错误信息与错误码
        await session.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user
