from decimal import Decimal
import redis
from datetime import datetime
import uuid
from django.conf import settings

# Подключение к Redis
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

class User:
    @staticmethod
    def create_user(username, email, password):
        user_id = str(uuid.uuid4())
        redis_client.hset(f"user:{user_id}", mapping={
            "id":user_id,
            "username": username,
            "email": email,
            "password": password  # Лучше хешировать
        })
        return user_id

    @staticmethod
    def get_user(user_id):
        return redis_client.hgetall(f"user:{user_id}")

    @staticmethod
    def get_all_users():
        users_keys = redis_client.keys("user:*")
        users = [redis_client.hgetall(user_key) for user_key in users_keys]
        return users

    @staticmethod
    def delete_user(user_id):
        redis_client.delete(f"user:{user_id}")

    @staticmethod
    def update_user(user_id, username, email, password=None):
        update_data = {
            "username": username,
            "email": email
        }
        if password:
            update_data["password"] = password
        redis_client.hset(f"user:{user_id}", mapping=update_data)

class Airline:
    @staticmethod
    def create_airline(name, code):
        airline_id = str(uuid.uuid4())
        redis_client.hset(f"airline:{airline_id}", mapping={
            "id":airline_id,
            "name": name,
            "code": code
        })
        return airline_id

    @staticmethod
    def get_airline(airline_id):
        return redis_client.hgetall(f"airline:{airline_id}")

    @staticmethod
    def get_all_airlines():
        airlines_keys = redis_client.keys("airline:*")
        airlines = [redis_client.hgetall(airline_key) for airline_key in airlines_keys]
        return airlines

    @staticmethod
    def delete_airline(airline_id):
        redis_client.delete(f"airline:{airline_id}")

    @staticmethod
    def update_airline(airline_id, name, code):
        redis_client.hset(f"airline:{airline_id}", mapping={
            "name": name,
            "code": code
        })

class Ticket:
    @staticmethod
    def create_ticket(user_id, airline_id, flight_number, departure, arrival, date, price):
        ticket_id = str(uuid.uuid4())  # Уникальный идентификатор для билета
        redis_client.hset(f"ticket:{ticket_id}", mapping={
            "id": ticket_id,
            "user_id": user_id,
            "airline_id": airline_id if airline_id else "",  # Преобразуем None в пустую строку
            "flight_number": flight_number,
            "departure": departure,
            "arrival": arrival,
            "date": date,
            "price": float(price)  # Преобразуем цену в float
        })
        return ticket_id

    @staticmethod
    def get_ticket(ticket_id):
        return redis_client.hgetall(f"ticket:{ticket_id}")

    @staticmethod
    def get_all_tickets():
        ticket_keys = redis_client.keys("ticket:*")
        tickets = [redis_client.hgetall(ticket_key) for ticket_key in ticket_keys]
        return tickets

    @staticmethod
    def update_ticket(ticket_id, user_id, airline_id, flight_number, departure, arrival, date, price):
        # Преобразуем дату и цену в нужные типы
        date_str = date.isoformat() if isinstance(date, datetime) else date
        price_float = float(price) if isinstance(price, Decimal) else price

        redis_client.hset(f"ticket:{ticket_id}", mapping={
            "user_id": user_id,
            "airline_id": airline_id,
            "flight_number": flight_number,
            "departure": departure,
            "arrival": arrival,
            "date": date_str,
            "price": price_float
        })

    @staticmethod
    def delete_ticket(ticket_id):
        redis_client.delete(f"ticket:{ticket_id}")

class Flight:
    @staticmethod
    def create_flight(flight_number,airline_id, departure, arrival, date, price):
        flight_id = str(uuid.uuid4())  # Генерация уникального ID для рейса
        redis_client.hset(f"flight:{flight_id}", mapping={
            "flight_number": flight_number,
            "airline_id": airline_id,
            "departure": departure,
            "arrival": arrival,
            "date": date,
            "price": float(price)
        })
        return flight_id

    @staticmethod
    def get_all_flights():
        keys = redis_client.keys("flight:*")
        flights = []
        for key in keys:
            flight_data = redis_client.hgetall(key)
            flights.append({
                "id": key.split(":")[1],
                "flight_number": flight_data["flight_number"],
                "departure": flight_data["departure"],
                "arrival": flight_data["arrival"],
                "date": flight_data["date"],
                "price": flight_data["price"]
            })
        return flights