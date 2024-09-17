from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),  # Event list
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Event details
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),  # Event registration
    path('ticket/<int:ticket_id>/', views.view_ticket, name='view_ticket'),  # Ticket and QR code view
]
