from fastapi import APIRouter, HTTPException
from config.db import conn
from models.user import users
from schemas.user import User
from sqlalchemy import func, select, insert, update, delete
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users")
def get_users():
    result = conn.execute(users.select()).mappings().all()
    user_list = [dict(row) for row in result]
    return user_list

@user.post("/users")
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email, "password": f.encrypt(user.password.encode("utf8")).decode("utf8")}
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    return {"id": result.lastrowid, **new_user}


@user.get("/users/{id}")
def get_user(id: int):
    result = conn.execute(users.select().where(users.c.id == id)).mappings().first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(result)

@user.delete("/users/{id}")
def delete_user(id: int):
    try:
        result = conn.execute(users.delete().where(users.c.id == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail" : "User deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@user.put("/users")
def update_user(id: int, user: User):
    encrypted_password = f.encrypt(user.password.encode("utf-8")).decode("utf-8")
    try:
        result = conn.execute(
            update(users)
            .values(name=user.name, email=user.email, password=encrypted_password)
            .where(users.c.id == id)
        )
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail" : "User updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))