from getpass import getpass
from database import SessionLocal, engine
from auth import hash_password
import models
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
username = input("Username: ").strip()
role = input("Role (admin/staff) [staff]: ").strip() or "staff"
password = getpass("Password: ")
if db.query(models.User).filter(models.User.username == username).first():
    print("That username already exists.")
else:
    db.add(models.User(
        username=username,
        password_hash=hash_password(password),
        role=role,
    ))
    db.commit()
    print(f"Created {username} ({role})")
db.close()