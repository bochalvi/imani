from django.db import models
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.


class Member(models.Model):
    MEMBER_TYPES = [
        ('REG', 'Regular'),
        ('VIP', 'VIP'),
    ]

    member_id = models.CharField(
        max_length=20,   primary_key=True, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=True)
    member_type = models.CharField(
        max_length=3, choices=MEMBER_TYPES, default='REG')
    id_number = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.member_id} - {self.first_name} {self.last_name}"
