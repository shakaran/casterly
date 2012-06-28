from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from money.models import BankAccount, Movement


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


class MovementModelTest(TestCase):
    def setUp(self):
        super(MovementModelTest, self).setUp()
        self.user = User.objects.create(
            username="foouser", email="foo@example.com")
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        self.bank_account = BankAccount.objects.create(**data)

    def tearDown(self):
        self.bank_account.delete()
        self.user.delete()
        super(MovementModelTest, self).tearDown()

    def test_basic_movement(self):
        self.assertEqual(20.0, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Beers",
            amount=-12.5,
            date=date(2012, 5, 30),
        )
        self.assertEqual(7.5, self.bank_account.current_balance)
        movement = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Returning",
            amount=6.89,
            date=date(2012, 5, 31),
        )
        self.assertEqual(14.39, self.bank_account.current_balance)
        movement.delete()
        self.assertEqual(7.5, self.bank_account.current_balance)

    def test_a_lot_of_movements(self):
        self.assertEqual(20.0, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Salary",
            amount=1650,
            date=date(2012, 5, 30),
        )
        self.assertEqual(1670.0, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Beers",
            amount=-12.5,
            date=date(2012, 5, 31),
        )
        self.assertEqual(1657.5, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Rent",
            amount=-1005.56,
            date=date(2012, 6, 10),
        )
        self.assertEqual(651.94, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Bonus",
            amount=450.23,
            date=date(2012, 6, 15),
        )
        self.assertEqual(1102.17, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Holidays",
            amount=-1102.16,
            date=date(2012, 6, 16),
        )
        self.assertEqual(0.01, self.bank_account.current_balance)

# TODO: tests about movements and categories. Probably when managers