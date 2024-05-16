"""
这里采用sqlalchemy包实现数据库相关操作
"""
from sqlalchemy import update, delete
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.future import select

from app.config import db_conf, app_conf


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_conf.DB_USERNAME}:{db_conf.DB_SECRET}" \
                          f"@{db_conf.DB_HOST}:{db_conf.DB_PORT}/{db_conf.DB_NAME}"

if app_conf.LEVEL == "DEBUG":
    echo = True
else:
    echo = False
    
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=echo, future=True, poolclass=NullPool)

async_session = sessionmaker(bind=engine, 
                             expire_on_commit=False, 
                             class_=AsyncSession)

Base = declarative_base()


async def get_db():
    yield async_session


async def insert_one(db: Session, model):
    async with db() as session:
        async with session.begin():
            session.add(model)
            await session.flush()
            session.expunge(model)
            return model
        

async def insert_many(db: Session, models):
    async with db() as session:
        async with session.begin():
            session.add_all(models)
            await session.flush()
            return models
        

async def _update(db: Session, model, filters, value):
    async with db() as session:
        stmt = update(model).where(filters).values(value)
        await session.execute(stmt)
        await session.commit()
        

async def search_one(db: Session, model, filters=None):
    async with db() as session:
        stmt = select(model).where(filters)
        result = await session.execute(stmt)
        result = result.scalars().first()
    return result


async def search(db: Session, model, filters=None):
    async with db() as session:
        if filters is not None:
            stmt = select(model).where(filters)
        else:
            stmt = select(model)
        result = await session.execute(stmt)
        result = result.scalars()
    return result
        

async def _delete(db: Session, model, filters=None):
    async with db() as session:
        stmt = delete(model).where(filters)
        await session.execute(stmt)
        await session.commit()