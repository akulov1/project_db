from django.urls import path
from . import views

urlpatterns = [
    path("create_user/", views.create_user, name="create_user"),
    path("user/<str:user_id>/", views.user_detail, name="user_detail"),
    path("create_airline/", views.create_airline, name="create_airline"),
    path("airline/<str:airline_id>/", views.airline_detail, name="airline_detail"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("ticket/<str:ticket_id>/", views.ticket_detail, name="ticket_detail"),
]