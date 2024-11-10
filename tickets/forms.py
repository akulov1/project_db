from django import forms
from .redis_models import User, Airline

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
    airline_id = forms.ChoiceField(
        choices=[(airline["id"], airline["name"]) for airline in Airline.get_all_airlines()],
        label="Авиакомпания"
    )
    flight_number = forms.CharField(label="Номер рейса", max_length=20)
    departure = forms.CharField(label="Пункт отправления", max_length=50)
    arrival = forms.CharField(label="Пункт прибытия", max_length=50)
    date = forms.DateTimeField(label="Дата и время рейса", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    price = forms.DecimalField(label="Цена", max_digits=10, decimal_places=2)