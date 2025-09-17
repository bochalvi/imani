import random
import string
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import SavingsAccount, Transaction


@receiver(pre_save, sender=SavingsAccount)
def set_account_number(sender, instance, **kwargs):
    if not instance.account_number:
        instance.account_number = generate_account_number(
            instance.account_type)


@receiver(pre_save, sender=Transaction)
def set_transaction_ref(sender, instance, **kwargs):
    if not instance.reference:
        instance.reference = generate_transaction_ref()


def generate_account_number(account_type):
    while True:
        prefix = account_type
        random_part = ''.join(random.choices(string.digits, k=8))
        account_num = f"{prefix}-{random_part}"
        if not SavingsAccount.objects.filter(account_number=account_num).exists():
            return account_num


def generate_transaction_ref():
    date_part = datetime.now().strftime("%y%m%d")
    random_part = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=6))
    return f"TXN-{date_part}-{random_part}"
