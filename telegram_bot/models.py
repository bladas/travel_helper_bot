from telegram import Contact
from django.contrib.gis.db import models

# Create your models here.

class TelegramUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, default="")
    phone_number = models.CharField(max_length=255)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    point = models.PointField(null=True, blank=True, geography=True, default='POINT(0.0 0.0)')

    @classmethod
    def init_from_contact(cls, contact: Contact):
        return cls(
            id=contact.user_id,
            first_name=contact.first_name,
            last_name=contact.last_name or "None",
            phone_number=contact.phone_number,
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
