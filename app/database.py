import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Načtení přihlašovacích údajů z proměnných prostředí (Environment Variables)
# Pokud proměnná neexistuje (např. při lokálním testování), použije se výchozí hodnota vpravo.
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "tajneheslo")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB", "watchdog_db")

# 2. Sestavení URL pro připojení k databázi
# Formát: postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

# Poznámka: Pokud bys chtěl pro začátek jen SQLite (soubor na disku), odkomentuj toto:
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 3. Vytvoření "Engine"
# Engine je továrna na spojení. Udržuje tzv. Connection Pool.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Pro SQLite bys musel přidat argument: connect_args={"check_same_thread": False}
# Pro PostgreSQL to nech takto čisté.

# 4. Vytvoření "SessionLocal"
# Toto je třída, kterou budeme volat, když budeme chtít nové spojení pro konkrétní request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Deklarativní báze
# Od této třídy budou dědit všechny tvé modely (tabulky) v souboru models.py.
Base = declarative_base()

# 6. Dependency (Pomocná funkce pro FastAPI)
# Tuto funkci budeš volat v main.py u každého endpointu.
# Zajistí, že se databáze otevře, provede dotaz a pak se bezpečně zavře.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()