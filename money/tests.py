from django.contrib.auth.models import User
from django.test import TestCase

from money.models import BankAccount


EXAMPLE_BANK_ACCOUNT = {
    "description": u"This is the account for all my fortune",
    "last_digits": u"4321",
    "entity": u"Lannister associates",
    "initial_balance": 100.0,
    "current_balance": 20.0,
}


class BankAccountModelTest(TestCase):
    def setUp(self):
        super(BankAccountModelTest, self).setUp()
        self.user = User.objects.create(
            username="foouser", email="foo@example.com")

    def tearDown(self):
        self.user.delete()
        super(BankAccountModelTest, self).tearDown()

    def test_basic_creation(self):
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        bank_account = BankAccount.objects.create(**data)
        self.assertIsInstance(unicode(bank_account), unicode)
        expected_unicode = u"%s <****%s> - %0.2f" % (
            data["entity"], data["last_digits"], data["current_balance"])
        self.assertEqual(expected_unicode, unicode(bank_account))

        self.assertEqual(data["owner"].id, bank_account.owner_id)
        self.assertEqual(data["description"], bank_account.description)
        self.assertEqual(data["last_digits"], bank_account.last_digits)
        self.assertEqual(data["entity"], bank_account.entity)
        self.assertEqual(data["initial_balance"], bank_account.initial_balance)
        self.assertEqual(data["current_balance"], bank_account.current_balance)

    def test_creation_no_current_balance(self):
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        del data["current_balance"]
        bank_account = BankAccount.objects.create(**data)
        self.assertEqual(data["initial_balance"], bank_account.initial_balance)
        self.assertEqual(data["initial_balance"], bank_account.current_balance)