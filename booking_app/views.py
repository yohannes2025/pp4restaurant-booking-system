# booking_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Table, Restaurant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {'restaurants': restaurants})


@login_required
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.clean()
                booking.save()
                messages.success(request, 'Your booking was successful!')
                return redirect('view_bookings')
            except Exception as e:
                messages.error(request, f'There was an error: {e}')
    else:
        form = BookingForm()
    return render(request, 'book_table.html', {'form': form})


@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by(
        '-booking_date', '-booking_time')
    return render(request, 'view_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('view_bookings')
    return render(request, 'cancel_booking.html', {'booking': booking})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
