from fastapi import APIRouter, HTTPException
from config.db import conn
from models.user import users
from schemas.user import User
from sqlalchemy import func, select, insert, update, delete
from cryptography.fernet import Fernet

# Generate an encryption key for securing passwords
key = Fernet.generate_key()
f = Fernet(key)

# Create a router for user-related API endpoints
user = APIRouter()

# Endpoint to retrieve all users
@user.get("/users")
def get_users():
    # Execute the query to select all users and map the result to a dictionary
    result = conn.execute(users.select()).mappings().all()
    # Convert the result to a list of dictionaries
    user_list = [dict(row) for row in result]
    return user_list

# Endpoint to create a new user
@user.post("/users")
def create_user(user: User):
    # Encrypt the user's password
    encrypted_password = f.encrypt(user.password.encode("utf-8")).decode("utf-8")
    # Create a dictionary with the new user's data
    new_user = {"name": user.name, "email": user.email, "password": encrypted_password}
    # Execute the insert query to add the new user to the database
    result = conn.execute(users.insert().values(new_user))
    # Commit the transaction to save changes
    conn.commit()
    # Return the new user's data, including the assigned ID
    return {"id": result.lastrowid, **new_user}


# Endpoint to retrieve a specific user by ID
@user.get("/users/{id}")
def get_user(id: int):
    # Execute the query to select the user with the specified ID
    result = conn.execute(users.select().where(users.c.id == id)).mappings().first()
    # Raise an HTTP 404 error if the user is not found
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Return the user's data as a dictionary
    return dict(result)

# Endpoint to delete a specific user by ID
@user.delete("/users/{id}")
def delete_user(id: int):
    try:
        # Execute the delete query to remove the user with the specified ID
        result = conn.execute(users.delete().where(users.c.id == id))
        # Commit the transaction to save changes
        conn.commit()
        # Raise an HTTP 404 error if no rows were affected (user not found)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        # Raise an HTTP 400 error with the exception message
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to update a specific user by ID
@user.put("/users")
def update_user(id: int, user: User):
    # Encrypt the user's password
    encrypted_password = f.encrypt(user.password.encode("utf-8")).decode("utf-8")
    try:
        # Execute the update query to modify the user's data
        result = conn.execute(
            update(users)
            .values(name=user.name, email=user.email, password=encrypted_password)
            .where(users.c.id == id)
        )
        # Commit the transaction to save changes
        conn.commit()
        # Raise an HTTP 404 error if no rows were affected (user not found)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail" : "User updated successfully"}
    except Exception as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        # Raise an HTTP 400 error with the exception message
        raise HTTPException(status_code=400, detail=str(e))