from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """Represents a client company in the vehicle monitoring system"""

    id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    user1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_user1",
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_user2",
    )
    user3 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="company_user3",
    )

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
