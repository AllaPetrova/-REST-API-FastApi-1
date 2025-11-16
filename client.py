import requests
import json

BASE_URL = "http://localhost:8000"

def get_all_users():
    response = requests.get(f"{BASE_URL}/users")
    return response.json()

def get_user_by_id(user_id: int):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response.json()

def create_user(name: str, email: str):
    user_data = {"name": name, "email": email}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    return response.json()

def update_user(user_id: int, name: str, email: str):
    user_data = {"name": name, "email": email}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=user_data)
    return response.json()

def delete_user(user_id: int):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    return response.status_code

if __name__ == "__main__":
    print("Создание пользователя:")
    new_user = create_user("John Doe", "john@example.com")
    print(new_user)
    
    print("\nВсе пользователи:")
    users = get_all_users()
    print(users)
    
    print("\nПолучение пользователя по ID:")
    user = get_user_by_id(1)
    print(user)
    
    print("\nОбновление пользователя:")
    updated_user = update_user(1, "John Smith", "johnsmith@example.com")
    print(updated_user)
    
    print("\nУдаление пользователя:")
    delete_status = delete_user(1)
    print(f"Статус удаления: {delete_status}")
