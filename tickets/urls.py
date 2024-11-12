from django.urls import path
from . import views

urlpatterns = [
    path("",views.ticket_list, name='ticket_list'),
    path("airline_list/",views.airline_list,name='airline_list'),
    path("user_list",views.user_list,name='user_list'),
    path("create_user/", views.create_user, name="create_user"),
    path("user/<str:user_id>/", views.user_detail, name="user_detail"),
    path("create_airline/", views.create_airline, name="create_airline"),
    path("airline/<str:airline_id>/", views.airline_detail, name="airline_detail"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("ticket/<str:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path('airlines/<str:airline_id>/edit/', views.edit_airline, name='edit_airline'),
    path('airlines/<str:airline_id>/delete/', views.delete_airline, name='delete_airline'),
    path('users/<str:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<str:user_id>/delete/', views.delete_user, name='delete_user'),
    path('tickets/<str:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('tickets/<str:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
]