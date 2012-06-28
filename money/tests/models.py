from datetime import date

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
    """
    Test case for work over the BankAccount model, checking that the amounts
    are correct, and the data have been properly assigned
    """
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
    """
    Tests for checking the correct creation of the Movement model,
    as it's repercussion over its related BankAccount
    """
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
        """
        This concrete test is for checking that we are not having problems
        working with the CurrencyField and Python's Decimal, with issues like
        getting 7.5000000001 instead of 7.5.
        """
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

    def test_negative_balance(self):
        self.assertEqual(20.0, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Dinner",
            amount=-22.5,
            date=date(2012, 5, 31),
        )
        self.assertEqual(-2.5, self.bank_account.current_balance)


class IntenseMovementModelTest(TestCase):
    def setUp(self):
        super(IntenseMovementModelTest, self).setUp()
        self.user = User.objects.create(
            username="foouser", email="foo@example.com")
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        data["current_balance"] = 340.0
        self.bank_account = BankAccount.objects.create(**data)

    def tearDown(self):
        self.bank_account.delete()
        self.user.delete()
        super(IntenseMovementModelTest, self).tearDown()

    def test_two_months_movements(self):
        self.assertEqual(340.0, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2011, 12, 25),
            amount=-134.3,
            description="Christmas presents",
        )
        self.assertEqual(205.7, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account, date=date(2011, 12, 31),
            amount=-42.56,
            description="New years eve party",
        )
        self.assertEqual(163.14, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2011, 12, 31),
            amount=1567,
            description="Salary December",
        )
        self.assertEqual(1730.14, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 3),
            amount=300,
            description="Football bet",
        )
        self.assertEqual(2030.14, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 7),
            amount=-43.2,
            description="Dinner and beers",
        )
        self.assertEqual(1986.94, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 10),
            amount=-78.95,
            description="Present for Rosa",
        )
        self.assertEqual(1907.99, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 12),
            amount=-800,
            description="Flat rental January",
        )
        self.assertEqual(1107.99, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 13),
            amount=-60.4,
            description="Muse Concert",
        )
        self.assertEqual(1047.59, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 18),
            amount=1.76,
            description="Account interest",
        )
        self.assertEqual(1049.35, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 21),
            amount=-18,
            description="Barber shop",
        )
        self.assertEqual(1031.35, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 23),
            amount=-40,
            description="Cash for Canmden Town",
        )
        self.assertEqual(991.35, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 28),
            amount=-32.48,
            description="Cinema",
        )
        self.assertEqual(958.87, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 30),
            amount=-231.93,
            description="Flights back to Spain",
        )
        self.assertEqual(726.94, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 1, 31),
            amount=1567,
            description="Salary January",
        )
        self.assertEqual(2293.94, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 2),
            amount=-213.45,
            description="Some clothes",
        )
        self.assertEqual(2080.49, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 2),
            amount=-112.12,
            description="New glasses",
        )
        self.assertEqual(1968.37, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 8),
            amount=-79.8,
            description="Accountant",
        )
        self.assertEqual(1888.57, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 10),
            amount=-800,
            description="Flat rental February",
        )
        self.assertEqual(1088.57, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 14),
            amount=-120,
            description="DjangoCon tickets",
        )
        self.assertEqual(968.57, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 18),
            amount=-89.87,
            description="DjangoCon hotel",
        )
        self.assertEqual(878.7, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 22),
            amount=-37.8,
            description="Dinner and beers",
        )
        self.assertEqual(840.9, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 27),
            amount=-97.3,
            description="Shopping at Amazon",
        )
        self.assertEqual(743.6, self.bank_account.current_balance)
        Movement.objects.create(
            bank_account=self.bank_account,
            date=date(2012, 2, 29),
            amount=1567,
            description="Salary February",
        )
        self.assertEqual(2310.6, self.bank_account.current_balance)


# class MovementManagerTest(TestCase):
    # expenses/earnings/benefits in a date range
    # categorized expenses/earnings/benefits in a date range
    # expenses/earnings/benefits per week and per month


# TODO: tests about movements and categories. Probably when managers
