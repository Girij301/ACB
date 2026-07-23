from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import BASE_DIR, settings

# ---------------------------------------------------------------------
# DATABASE URL (CONFIG DRIVEN WITH SAFE FALLBACK)
# ---------------------------------------------------------------------

DATABASE_URL = settings.DATABASE_URL

# ---------------------------------------------------------------------
# VALIDATE DATABASE URL
# ---------------------------------------------------------------------

parsed_db = urlparse(DATABASE_URL)

if not parsed_db.scheme:
    raise ValueError(f"Invalid DATABASE_URL: {DATABASE_URL}")

db_dialect = parsed_db.scheme.split("+")[0]  # sqlite, postgresql, etc.

# ---------------------------------------------------------------------
# CONNECT ARGS (DB-SPECIFIC)
# ---------------------------------------------------------------------

connect_args = {}

if db_dialect == "sqlite":
    connect_args = {"check_same_thread": False}

elif db_dialect == "postgresql":
    connect_args = {"prepare_threshold": None}

# ---------------------------------------------------------------------
# ENGINE
# ---------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
# ---------------------------------------------------------------------
# SESSION
# ---------------------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ---------------------------------------------------------------------
# BASE
# ---------------------------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------------------------
# DB DEPENDENCY
# ---------------------------------------------------------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
