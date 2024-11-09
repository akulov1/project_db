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

class Ticket:
    @staticmethod
    def create_ticket(user_id, airline_id, flight_number, departure, arrival, date, price):
        ticket_id = str(uuid.uuid4())
        # Преобразуем дату в строку формата ISO 8601
        date_str = date.isoformat() if isinstance(date, datetime) else date
        price_float = float(price) if isinstance(price, Decimal) else price

        redis_client.hset(f"ticket:{ticket_id}", mapping={
            "ticket_id": ticket_id,
            "user_id": user_id,
            "airline_id": airline_id,
            "flight_number": flight_number,
            "departure": departure,
            "arrival": arrival,
            "date": date_str,  # Сохраняем дату как строку
            "price": price_float
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