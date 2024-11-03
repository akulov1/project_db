from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class AirlineForm(forms.Form):
    name = forms.CharField(label='Airline Name',max_length=100)
    code = forms.CharField(label='Airline Code', max_length=10)

class TicketForm(forms.Form):
    user_id = forms.CharField(label='User ID')
    airline_id = forms.CharField(label='Airline ID')
    flight_number = forms.CharField(label='Flight Number', max_length=10)
    departure = forms.CharField(label='Departure Airport', max_length=3)
    arrival = forms.CharField(label='Arrival Airport', max_length=3)
    date = forms.DateTimeField(label='Flight Date')
    price = forms.DecimalField(label='Price',max_digits=10,decimal_places=2)