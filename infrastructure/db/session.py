from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine= create_async_engine(DABASE_URL, pool_pre_ping=True)
SessionFactory= async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
