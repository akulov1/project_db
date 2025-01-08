from django import forms
from .redis_models import User, Airline

CITIES = [
    ('MOW', 'Москва'),
    ('SPB', 'Санкт-Петербург'),
    ('LED', 'Ленинград'),
    ('NYC', 'Нью-Йорк'),
    ('LON', 'Лондон'),
    ('PAR', 'Париж'),
]


class UserForm(forms.Form):
    username = forms.CharField(label='Никнейм',max_length=100)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class AirlineForm(forms.Form):
    name = forms.CharField(label='Название авиакомпании',max_length=100)
    code = forms.CharField(label='Код авиакомании', max_length=10)


class TicketForm(forms.Form):
    user_id = forms.ChoiceField(
        choices=[("", "Без пользователя")] + [(user["id"], user["username"]) for user in User.get_all_users()],
        required=False,
        label="Пользователь"
    )
    flight_id = forms.ChoiceField(label="Flight", choices=[])

class FlightForm(forms.Form):
    airline_id = forms.CharField(label="Airline id", max_length=10)
    flight_number = forms.CharField(label="Flight Number", max_length=10)
    departure = forms.CharField(label="Departure Airport", max_length=3)
    arrival = forms.CharField(label="Arrival Airport", max_length=3)
    date = forms.CharField(label="Flight Date")
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2)