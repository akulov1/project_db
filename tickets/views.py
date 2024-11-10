from django.shortcuts import render,redirect
from .forms import UserForm, AirlineForm, TicketForm
from .redis_models import User, Airline, Ticket

#представление для создания пользователя
def create_user(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = User.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password']
            )
            return redirect('user_detail', user_id=user_id)
    else:
        form = UserForm
    return render(request,'tickets/create_user.html',{'form':form})

#для отображения информации о пользователе
def user_detail(request,user_id):
    user = User.get_user(user_id)
    return render(request,'tickets/user_detail.html',{'user':user})

def create_airline(request):
    if request.method == 'POST':
        form = AirlineForm(request.POST)
        if form.is_valid():
            airline_id = Airline.create_airline(
                form.cleaned_data['name'],
                form.cleaned_data['code']
            )
            return redirect('airline_detail',airline_id=airline_id)
    else:
        form = AirlineForm()
    return render(request,'tickets/create_airline.html',{'form':form})

def airline_detail(request, airline_id):
    airline = Airline.get_airline(airline_id)
    return render(request, "tickets/airline_detail.html", {"airline": airline})

def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"] or None  # Может быть None, если не выбран
            airline_id = form.cleaned_data["airline_id"]
            flight_number = form.cleaned_data["flight_number"]
            departure = form.cleaned_data["departure"]
            arrival = form.cleaned_data["arrival"]
            date = form.cleaned_data["date"]
            price = form.cleaned_data["price"]

            ticket_id = Ticket.create_ticket(
                user_id,
                airline_id,
                flight_number,
                departure,
                arrival,
                date,
                price
            )
            return redirect("ticket_detail", ticket_id=ticket_id)
    else:
        form = TicketForm()
    return render(request, "tickets/create_ticket.html", {"form": form})

# Представление для отображения информации о билете
def ticket_detail(request, ticket_id):
    ticket = Ticket.get_ticket(ticket_id)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})

def ticket_list(request):
    tickets = Ticket.get_all_tickets()
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})

def airline_list(request):
    airlines = Airline.get_all_airlines()
    return render(request, 'tickets/airlines_list.html',{"airlines":airlines})
def user_list(request):
    users = User.get_all_users()
    return render(request,'tickets/users_list.html',{'users':users})