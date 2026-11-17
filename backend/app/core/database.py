"""数据库引擎、会话与声明式基类。"""
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

_connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def enable_sqlite_foreign_keys(target_engine: Engine) -> None:
    """让 SQLite 真正执行外键约束。

    SQLite 默认关闭外键检查，模型里写的 ondelete="CASCADE" 会静默失效，
    删除主表后留下孤儿行。连接级打开 PRAGMA 即可，MySQL 不需要这一步。
    测试里也要对自己的引擎调用一次。
    """

    @event.listens_for(target_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


if settings.DATABASE_URL.startswith("sqlite"):
    enable_sqlite_foreign_keys(engine)


def get_db():
    """FastAPI 依赖：提供请求级数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
