from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

users_db: Dict[int, User] = {}
current_id = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI REST API"}

@app.get("/users", response_model=List[User])
def get_all_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users", response_model=User)
def create_user(user: User):
    global current_id
    user.id = current_id
    users_db[current_id] = user
    current_id += 1
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user.id = user_id
    users_db[user_id] = user
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
