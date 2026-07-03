from app.core.config import settings, BASE_DIR
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import urlparse

# ---------------------------------------------------------------------
# DATABASE URL (CONFIG DRIVEN WITH SAFE FALLBACK)
# ---------------------------------------------------------------------

DEFAULT_SQLITE_PATH = BASE_DIR / "chat.db"

DATABASE_URL = settings.DATABASE_URL or f"sqlite:///{DEFAULT_SQLITE_PATH}"

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