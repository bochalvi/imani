from django.test import TestCase
from .models import SavingsAccount
from django.utils import timezone
from datetime import timedelta


class AccountNumberTests(TestCase):
    def test_unique_account_numbers(self):
        account1 = SavingsAccount.objects.create(account_type='SAV')
        account2 = SavingsAccount.objects.create(account_type='SAV')
        self.assertNotEqual(account1.account_number, account2.account_number)

    def test_account_number_format(self):
        account = SavingsAccount.objects.create(account_type='CHK')
        self.assertTrue(account.account_number.startswith('CHK-'))
        self.assertEqual(len(account.account_number), 12)  # CHK-12345678
