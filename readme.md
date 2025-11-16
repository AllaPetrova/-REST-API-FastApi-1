# FastAPI REST API

Простое REST API приложение на FastAPI для управления пользователями.

## Функциональность

- Создание пользователя
- Получение списка пользователей
- Получение пользователя по ID
- Обновление пользователя
- Удаление пользователя

## Запуск приложения

### Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt

2. Запустите приложение:
```bash
uvicorn main:app --reload

Запуск с Docker

##  Соберите и запустите контейнеры:

```bash
docker-compose up --build

Приложение будет доступно по адресу: http://localhost:8000

Документация API: http://localhost:8000/docs


**Dockerfile**
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# Домашнее задание к лекции «Создание REST API на FastApi» часть 1

Инструкцию по сдаче домашнего задания Вы найдете на главной странице репозитория.

# Задание 
Вам нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

У объявлений должны быть следующие поля:
 - заголовок
 - описание
 - цена
 - автор
 - дата создания

Должны быть реализованы следующе методы:
 - Создание: `POST /advertisement`
 - Обновление: `PATCH /advertisement/{advertisement_id}`
 - Удаление: `DELETE /advertisement/{advertisement_id}`
 - Получение по id: `GET  /advertisement/{advertisement_id}`
 - Поиск по полям: `GET /advertisement?{query_string}`

Авторизацию и аутентификацию реализовывать **не нужно**
