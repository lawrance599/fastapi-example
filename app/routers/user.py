from fastapi import APIRouter, Depends, Path, HTTPException, Form
from sqlmodel import select
from app.database import User, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import hashlib
import secrets
import re
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


def validate_username(username: str) -> str:
    """
    验证用户名格式
    - 只允许字母、数字和下划线
    - 长度3-20个字符
    - 必须以字母开头
    """
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        raise HTTPException(
            status_code=400,
            detail="用户名只能包含字母、数字和下划线，且必须以字母开头"
        )
    if len(username) < 3 or len(username) > 20:
        raise HTTPException(
            status_code=400,
            detail="用户名长度必须在3-20个字符之间"
        )
    return username


def hash_password(password: str) -> str:
    """
    使用 PBKDF2 + SHA256 加密密码
    包含随机盐值，提高安全性
    """
    # 生成随机盐值（32字节）
    salt = secrets.token_bytes(32)
    
    # 使用 PBKDF2 进行密码哈希，迭代100000次
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256',  # 哈希算法
        password.encode('utf-8'),  # 密码转为字节
        salt,  # 盐值
        100000  # 迭代次数
    )
    
    # 将盐值和哈希值组合，并转为十六进制字符串
    return salt.hex() + ':' + pwdhash.hex()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    """
    try:
        # 分离盐值和哈希值
        salt_hex, pwdhash_hex = hashed_password.split(':')
        salt = bytes.fromhex(salt_hex)
        stored_pwdhash = bytes.fromhex(pwdhash_hex)
        
        # 使用相同的参数重新计算哈希
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        # 比较哈希值
        return pwdhash == stored_pwdhash
    except ValueError:
        # 如果格式不正确，返回 False
        return False


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
    username: str = Form(..., max_length=20),
    password: str = Form(..., min_length=8, max_length=100),
    session: AsyncSession = Depends(get_session),
):
    # 验证用户名格式
    validate_username(username)
    
    # 加密密码
    hashed_password = hash_password(password)
    
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
