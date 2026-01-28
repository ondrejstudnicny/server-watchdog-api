import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Načtení proměnných.
# ZMĚNA: Jako default pro server dáváme None, ne localhost.
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "tajneheslo")
POSTGRES_DB = os.getenv("POSTGRES_DB", "watchdog_db")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

# Rozhodovací logika:
if POSTGRES_SERVER:
    # Jsme v Dockeru nebo v produkci -> Použij Postgres
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # Jsme v testech nebo lokálně bez Dockeru -> Použij SQLite
    # To zajistí, že CI pipeline nespadne
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()