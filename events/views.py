from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Ticket
from django.core.mail import send_mail
from django.conf import settings


# View to list all events
from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'event_list.html', {'events': events})



# View to display event details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


# Register for an event (ticket creation)
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket, created = Ticket.objects.get_or_create(event=event, user=request.user)

    if created:
        # Optionally send an email with ticket confirmation
        send_mail(
            'Your Ticket for ' + event.name,
            'Here is your ticket for the event: ' + event.name,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, f"You have successfully registered for {event.name}!")
    else:
        messages.info(request, f"You are already registered for {event.name}.")

    return redirect('event_list')


# View to display the ticket and QR code
@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'ticket_detail.html', {'ticket': ticket})
