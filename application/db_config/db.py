from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from env_config import settings as stg

url = f"postgresql+asyncpg://{stg.db_user}:{stg.db_user}@postgres/{stg.db_user}"

engine = create_async_engine(url)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
