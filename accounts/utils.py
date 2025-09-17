from django.utils.translation import gettext_lazy as _
from django.contrib import admin
import random
import string
from datetime import datetime


def generate_account_number(account_type):
    """Generate a random savings account number"""
    prefix = "SAV"
    year = datetime.now().strftime("%y")
    random_part = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}{year}{random_part}"
