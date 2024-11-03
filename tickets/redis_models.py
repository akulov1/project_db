import redis
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
            "username": username,
            "email": email,
            "password": password  # Лучше хешировать
        })
        return user_id

    @staticmethod
    def get_user(user_id):
        return redis_client.hgetall(f"user:{user_id}")

class Airline:
    @staticmethod
    def create_airline(name, code):
        airline_id = str(uuid.uuid4())
        redis_client.hset(f"airline:{airline_id}", mapping={
            "name": name,
            "code": code
        })
        return airline_id

    @staticmethod
    def get_airline(airline_id):
        return redis_client.hgetall(f"airline:{airline_id}")

class Ticket:
    @staticmethod
    def create_ticket(user_id, airline_id, flight_number, departure, arrival, date, price):
        ticket_id = str(uuid.uuid4())
        redis_client.hset(f"ticket:{ticket_id}", mapping={
            "user_id": user_id,
            "airline_id": airline_id,
            "flight_number": flight_number,
            "departure": departure,
            "arrival": arrival,
            "date": date,
            "price": price
        })
        return ticket_id

    @staticmethod
    def get_ticket(ticket_id):
        return redis_client.hgetall(f"ticket:{ticket_id}")