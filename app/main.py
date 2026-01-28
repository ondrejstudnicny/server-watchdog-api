from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from . import models, schemas, database

# Vytvoření tabulek (pro dev účely, v produkci použijeme Alembic)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Server Watchdog API")


# Dependency pro získání DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/heartbeat")
def receive_heartbeat(heartbeat: schemas.HeartbeatCreate, db: Session = Depends(get_db)):
    # Zde vytvoříš záznam v DB
    db_heartbeat = models.Heartbeat(**heartbeat.dict())
    db.add(db_heartbeat)
    db.commit()
    return {"msg": "Heartbeat received"}


@app.get("/status/{service_name}")
def get_status(service_name: str, db: Session = Depends(get_db)):
    # 1. Najdi poslední záznam pro danou službu
    last_record = db.query(models.Heartbeat).filter(
        models.Heartbeat.service_name == service_name
    ).order_by(models.Heartbeat.created_at.desc()).first()

    if not last_record:
        raise HTTPException(status_code=404, detail="Service not found")

    # 2. Porovnej čas
    # Pozor na časová pásma! Používej UTC.
    now = datetime.now(timezone.utc)
    # Předpoklad: last_record.created_at je "aware" datetime nebo UTC
    diff = now - last_record.created_at

    is_critical = diff > timedelta(minutes=5)

    status_msg = "CRITICAL" if is_critical else last_record.status

    return {
        "service_name": service_name,
        "last_seen": last_record.created_at,
        "status": status_msg,
        "seconds_since_last_beat": diff.total_seconds()
    }