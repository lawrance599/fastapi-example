from fastapi import APIRouter, Depends, Path, HTTPException, Form
from sqlmodel import select
from app.database import User, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def read_user(
    id: int = Path(..., title="用户ID"), session: AsyncSession=Depends(get_session)
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
    session: AsyncSession=Depends(get_session)
):
    # 创建用户的语句
    user = User(username=username, password=password, created_at=None)
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user
