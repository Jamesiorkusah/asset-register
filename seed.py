from database import SessionLocal, engine
import models
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
starters = [
    {"tag": "NIT-001", "type": "Laptop", "model": "HP EliteBook 840", "status": "In Use"},
    {"tag": "NIT-002", "type": "Router", "model": "MikroTik hEX", "status": "In Use"},
    {"tag": "NIT-003", "type": "Printer", "model": "HP LaserJet Pro", "status": "Faulty"},
]
for s in starters:
    if not db.query(models.Asset).filter(models.Asset.tag == s["tag"]).first():
        db.add(models.Asset(**s))
db.commit()
print("Seeded:", db.query(models.Asset).count(), "assets")
db.close()