# booking_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_table, name='book_table'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),  # Add registration URL
]
