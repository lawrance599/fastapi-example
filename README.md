# FASTAPI 后端项目示例

## 项目简介

本项目是一个基于fastapi与sqlmodel的 web 后端用户管理项目示例, 同时使用 alembic 进行数据库迁移.
本项目主要面向新手快速搭建自己的 web 后端项目.
项目内置了路由示例以及模型示例，以及数据库迁移示例。你可以按照自己需求进行修改。

## 前置开发依赖

本项目使用[uv](https://docs.astral.sh/uv/)管理项目, 使用pyproject.toml的方式来进行依赖管理, 使用[ruff](https://docs.astral.sh/ruff/)作为代码格式化工具, [git](https://git-scm.com/)作为版本管理工具, 使用[vsocde]()进行开发.

同时使用postgres或者mysql来持久化数据, 请各位确保开发环境中至少有一个数据库

## 开始使用

### 1.环境搭建

使用包管理安装本项目需要的依赖

#### uv

使用以下指令同步依赖以及版本

```shell
uv sync
```

#### pip

初始化python虚拟环境

```shell
python -m venv
```

安装依赖

```shell
pip install -r pyproject.toml
```

#### 2.运行项目

使用python输入以下指令以运行项目

```shell
python main.py
```

可以看到项目启动, 启动后可以通过[](http:localhost:8888/docs)查看所有的接口

