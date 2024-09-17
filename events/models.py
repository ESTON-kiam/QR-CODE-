from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

    def save(self, *args, **kwargs):
        # Generate a QR code when a ticket is created
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Ticket for {self.event.name} - {self.user.username}')
        qr.make(fit=True)

        # Create an image from the QR code instance
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Save the image to the model
        self.qr_code.save(f'{self.event.name}_ticket_qr.png', File(img_io), save=False)

        super().save(*args, **kwargs)
