from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
# Create your models here.


class Invitation(models.Model):
    # User who created the invite
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    # Optional: Restrict invites to specific emails
    email = models.EmailField(blank=True)
    token = models.UUIDField(
        default=uuid.uuid4, unique=True)  # Unique invite token
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Set expiration time
    is_used = models.BooleanField(default=False)  # Track if the


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
