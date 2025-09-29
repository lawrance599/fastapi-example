from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

"""
本文件创建了数据库表的orm数据实体, 用来对数据库进行增删改查操作

数据库表定义示例, 每个类对应一个数据库表

class <数据库表名>(SQLModel, table=True):
    主键: 数据类型 = Field(default=None, primary_key=True)
    字段名1: 数据类型1
    ...
    字段名N: 数据类型N
    

注意事项:
    1. 数据库名请改为大驼峰命名法,
    例如数据库内表名为userPermission/user_permission,则类名为UserPermission
    2. 字段名称保持不变, 若字段可以为null, 请使用Optional[数据类型],
    例如数据库字段name可为空, 类型为varchar, 则字段可以写为 name: Optional[str]
    3. 数据库和类字段类型请保持一致, 若字段类型为varchar, 请使用str, 若字段类型为int, 请使用int,
    若字段类型为datetime, 请使用datetime
"""


# 创建用户表
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: Optional[str]
    phone: Optional[str]
    is_active: bool = True
    create_time: datetime


# 创建用户权限表
class UserPermission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    permission: int
