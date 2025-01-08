from django.shortcuts import render,redirect, get_object_or_404
from .forms import UserForm, AirlineForm, TicketForm, FlightForm
from .redis_models import User, Airline, Ticket, Flight


def create_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            flight_id = Flight.create_flight(
                airline_id=form.cleaned_data["airline_id"],
                flight_number=form.cleaned_data["flight_number"],
                departure=form.cleaned_data["departure"],
                arrival=form.cleaned_data["arrival"],
                date=form.cleaned_data["date"],
                price=form.cleaned_data["price"]
            )
            return redirect("/tickets", flight_id=flight_id)
    else:
        form = FlightForm()
    return render(request, "tickets/create_flight.html", {"form": form})

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
    flights = Flight.get_all_flights()
    flight_choices = [(flight["id"], f"{flight['flight_number']} - {flight['departure']} -> {flight['arrival']}") for
                      flight in flights]

    if request.method == "POST":
        form = TicketForm(request.POST)
        form.fields["flight_id"].choices = flight_choices
        if form.is_valid():
            flight_id = form.cleaned_data["flight_id"]
            flight = next((f for f in flights if f["id"] == flight_id), None)
            if not flight:
                return render(request, "tickets/create_ticket.html", {
                    "form": form,
                    "error": "Selected flight not found. Please try again."
                })

            ticket_id = Ticket.create_ticket(
                user_id=form.cleaned_data["user_id"],
                airline_id=None,
                flight_number=flight["flight_number"],
                departure=flight["departure"],
                arrival=flight["arrival"],
                date=flight["date"],
                price=flight["price"]
            )

            if not ticket_id:  # Проверяем, что билет был создан
                return render(request, "tickets/create_ticket.html", {
                    "form": form,
                    "error": "Failed to create ticket. Please try again."
                })

            return redirect("ticket_detail", ticket_id=ticket_id)
    else:
        form = TicketForm()
        form.fields["flight_id"].choices = flight_choices
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

def edit_airline(request, airline_id):
    airline_data = Airline.get_airline(airline_id)
    if request.method == 'POST':
        form = AirlineForm(request.POST, initial=airline_data)
        if form.is_valid():
            Airline.update_airline(
                airline_id=airline_id,
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code']
            )
            return redirect('airline_list')
    else:
        form = AirlineForm(initial=airline_data)
    return render(request, 'tickets/edit_airline.html', {'form': form, 'airline_id': airline_id})



# Представление для редактирования пользователя
def edit_user(request, user_id):
    user_data = User.get_user(user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, initial=user_data)
        if form.is_valid():
            User.update_user(
                user_id=user_id,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'] if form.cleaned_data.get('password') else None
            )
            return redirect('user_list')
    else:
        form = UserForm(initial=user_data)
    return render(request, 'tickets/edit_user.html', {'form': form, 'user_id': user_id})


# Представление для редактирования билета
def edit_ticket(request, ticket_id):
    ticket_data = Ticket.get_ticket(ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, initial=ticket_data)
        if form.is_valid():
            Ticket.update_ticket(
                ticket_id=ticket_id,
                user_id=form.cleaned_data.get("user_id"),
                airline_id=form.cleaned_data.get("airline_id"),
                flight_number=form.cleaned_data.get("flight_number"),
                departure=form.cleaned_data.get("departure"),
                arrival=form.cleaned_data.get("arrival"),
                date=form.cleaned_data.get("date"),
                price=form.cleaned_data.get("price")
            )
            return redirect('ticket_list')
    else:
        form = TicketForm(initial=ticket_data)
    return render(request, 'tickets/edit_ticket.html', {'form': form, 'ticket_id': ticket_id})

def delete_ticket(request, ticket_id):
    Ticket.delete_ticket(ticket_id)
    return redirect('ticket_list')
def delete_user(request, user_id):
    User.delete_user(user_id)
    return redirect('user_list')
def delete_airline(request, airline_id):
    Airline.delete_airline(airline_id)
    return redirect('airline_list')
