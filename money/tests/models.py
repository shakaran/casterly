from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from money.models import (BankAccount, Movement, MovementCategory,
                          CategorySuggestion, InvalidOperationError)


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
        movement = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Beers",
            amount=-12.5,
            date=date(2012, 5, 30),
        )
        self.assertEqual(7.5, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement.current_balance)
        movement = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Returning",
            amount=6.89,
            date=date(2012, 5, 31),
        )
        self.assertEqual(14.39, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement.current_balance)
        self.assertRaises(InvalidOperationError, movement.delete)
        self.assertEqual(14.39, self.bank_account.current_balance)

    def test_a_lot_of_movements(self):
        """
        This concrete test is for checking that we are not having problems
        working with the CurrencyField and Python's Decimal, with issues like
        getting 7.5000000001 instead of 7.5.
        """
        self.assertEqual(20.0, self.bank_account.current_balance)
        m = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Salary",
            amount=1650,
            date=date(2012, 5, 30),
        )
        self.assertEqual(1670.0, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            m.current_balance)
        m = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Beers",
            amount=-12.5,
            date=date(2012, 5, 31),
        )
        self.assertEqual(1657.5, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            m.current_balance)
        m = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Rent",
            amount=-1005.56,
            date=date(2012, 6, 10),
        )
        self.assertEqual(651.94, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            m.current_balance)
        m = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Bonus",
            amount=450.23,
            date=date(2012, 6, 15),
        )
        self.assertEqual(1102.17, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            m.current_balance)
        m = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Holidays",
            amount=-1102.16,
            date=date(2012, 6, 16),
        )
        self.assertEqual(0.01, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            m.current_balance)

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


class MovementCategoryModelTest(TestCase):

    def setUp(self):
        super(MovementCategoryModelTest, self).setUp()
        self.user = User.objects.create(
            username="foouser", email="foo@example.com")
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        self.bank_account = BankAccount.objects.create(**data)

        # Remove categories assigned with fixtures
        MovementCategory.objects.all().delete()

    def tearDown(self):
        self.bank_account.delete()
        self.user.delete()
        super(MovementCategoryModelTest, self).tearDown()

    def test_category_create_and_delete(self):
        self.assertEqual(0, MovementCategory.objects.count())
        category_1 = MovementCategory.objects.create(name="Category 1")
        category_2 = MovementCategory.objects.create(name="Category 2")
        category_3 = MovementCategory.objects.create(name="Category 3")
        self.assertEqual(3, MovementCategory.objects.count())

        self.assertEqual("Category 1", MovementCategory.objects.get(
            pk=category_1.pk).name)
        self.assertEqual("Category 2", MovementCategory.objects.get(
            pk=category_2.pk).name)
        self.assertEqual("Category 3", MovementCategory.objects.get(
            pk=category_3.pk).name)

        category_2_pk = category_2.pk
        category_2.delete()
        self.assertEqual(2, MovementCategory.objects.count())
        self.assertEqual("Category 1", MovementCategory.objects.get(
            pk=category_1.pk).name)
        self.assertRaises(MovementCategory.DoesNotExist,
            MovementCategory.objects.get, pk=category_2_pk)
        self.assertEqual("Category 3", MovementCategory.objects.get(
            pk=category_3.pk).name)

        category_3 = MovementCategory.objects.get(pk=category_3.pk)
        category_3.name += " modified"
        category_3.save()
        self.assertEqual(2, MovementCategory.objects.count())
        self.assertEqual("Category 1", MovementCategory.objects.get(
            pk=category_1.pk).name)
        self.assertRaises(MovementCategory.DoesNotExist,
            MovementCategory.objects.get, pk=category_2_pk)
        self.assertEqual("Category 3 modified", MovementCategory.objects.get(
            pk=category_3.pk).name)

    def test_category_assigned(self):
        category_1 = MovementCategory.objects.create(name="Category 1")
        category_2 = MovementCategory.objects.create(name="Category 2")
        category_3 = MovementCategory.objects.create(name="Category 3")
        self.assertEqual(20.0, self.bank_account.current_balance)
        movement_1 = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Beers",
            amount=-12.5,
            date=date(2012, 5, 30),
            category=category_1,
        )
        self.assertEqual(7.5, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement_1.current_balance)
        movement_2 = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Returning",
            amount=6.89,
            date=date(2012, 5, 31),
            category=category_2,
        )
        self.assertEqual(14.39, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement_2.current_balance)
        movement_3 = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Salary",
            amount=588,
            date=date(2012, 6, 1),
            category=category_2,
        )
        self.assertEqual(602.39, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement_3.current_balance)
        movement_4 = Movement.objects.create(
            bank_account=self.bank_account,
            description=u"Some clothes",
            amount=-84.6,
            date=date(2012, 6, 4),
            category=category_3,
        )
        self.assertEqual(517.79, self.bank_account.current_balance)
        self.assertEqual(self.bank_account.current_balance,
            movement_4.current_balance)

        self.assertEqual(4, Movement.objects.count())
        self.assertEqual(1, Movement.objects.filter(
            category=category_1).count())
        self.assertEqual(2, Movement.objects.filter(
            category=category_2).count())
        self.assertEqual(1, Movement.objects.filter(
            category=category_3).count())
        self.assertEqual([cat.id for cat in category_1.movements.all()],
            [cat.id for cat in Movement.objects.filter(category=category_1)])
        self.assertEqual([cat.id for cat in category_2.movements.all()],
            [cat.id for cat in Movement.objects.filter(category=category_2)])
        self.assertEqual([cat.id for cat in category_2.movements.all()],
            [cat.id for cat in Movement.objects.filter(category=category_2)])


class MovementCategorySuggestionTest(TestCase):

    def setUp(self):
        super(MovementCategorySuggestionTest, self).setUp()
        self.c1 = MovementCategory.objects.create(name="Category 1")
        self.c2 = MovementCategory.objects.create(name="Category 2")
        self.c3 = MovementCategory.objects.create(name="Category 3")

    def tearDown(self):
        MovementCategory.objects.all().delete()
        super(MovementCategorySuggestionTest, self).tearDown()

    def test_basic_suggestion(self):
        CategorySuggestion.objects.create(
            expression="food", category=self.c2)
        CategorySuggestion.objects.create(
            expression="clothes", category=self.c1)

        sug_category = CategorySuggestion.objects.suggest("some food")
        self.assertEqual(self.c2.id, sug_category.id)
        sug_category = CategorySuggestion.objects.suggest("buying clothes")
        self.assertEqual(self.c1.id, sug_category.id)
        sug_category = CategorySuggestion.objects.suggest("Pub")
        self.assertIsNone(sug_category)


class MovementManagerTest(TestCase):
    # expenses/earnings/benefits in a date range
    # categorized expenses/earnings/benefits in a date range
    # expenses/earnings/benefits per week and per month
    fixtures = ["test_fixtures.json"]

    def test_proper_fixtures_loading(self):
        bank_account = BankAccount.objects.get(pk=1)
        self.assertEqual(2310.6, bank_account.current_balance)
        self.assertEqual(EXAMPLE_BANK_ACCOUNT["entity"], bank_account.entity)
        self.assertEqual(23, Movement.objects.count())

    def test_all_movements(self):
        bank_account = BankAccount.objects.get(pk=1)
        self.assertEqual(23, Movement.objects.count())
        self.assertEqual(18, Movement.objects.get_expenses().count())
        self.assertEqual(5, Movement.objects.get_earnings().count())

        self.assertEqual(3032.16, Movement.objects.expenses())
        self.assertEqual(5002.76, Movement.objects.earnings())
        self.assertEqual(1970.6, Movement.objects.balance())

    def test_movements_per_month(self):
        bank_account = BankAccount.objects.get(pk=1)

        # First, we check the number of movements are corect
        self.assertEqual(23, Movement.objects.count())
        self.assertEqual(3, Movement.objects.per_month(2011, 12).count())
        self.assertEqual(11, Movement.objects.per_month(2012, 1).count())
        self.assertEqual(9, Movement.objects.per_month(2012, 2).count())

        # Then, we check the expenses, earnings and balance
        self.assertEqual(176.86, Movement.objects.per_month(
            2011, 12).expenses())
        self.assertEqual(1567.0, Movement.objects.per_month(
            2011, 12).earnings())
        self.assertEqual(1390.14, Movement.objects.per_month(
            2011, 12).balance())

        self.assertEqual(1304.96, Movement.objects.per_month(
            2012, 1).expenses())
        self.assertEqual(1868.76, Movement.objects.per_month(
            2012, 1).earnings())
        self.assertEqual(563.8, Movement.objects.per_month(
            2012, 1).balance())

        self.assertEqual(1550.34, Movement.objects.per_month(
            2012, 2).expenses())
        self.assertEqual(1567, Movement.objects.per_month(
            2012, 2).earnings())
        self.assertEqual(16.66, Movement.objects.per_month(
            2012, 2).balance())

    def test_movements_per_week(self):
        bank_account = BankAccount.objects.get(pk=1)

        self.assertEqual(1, Movement.objects.per_week(2011, 51).count())
        self.assertEqual(2, Movement.objects.per_week(2011, 52).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 1).count())
        self.assertEqual(3, Movement.objects.per_week(2012, 2).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 3).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 4).count())
        self.assertEqual(4, Movement.objects.per_week(2012, 5).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 6).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 7).count())
        self.assertEqual(1, Movement.objects.per_week(2012, 8).count())
        self.assertEqual(2, Movement.objects.per_week(2012, 9).count())

        self.assertEqual(134.3, Movement.objects.per_week(2011, 51).expenses())
        self.assertEqual(0, Movement.objects.per_week(2011, 51).earnings())
        self.assertEqual(-134.3, Movement.objects.per_week(2011, 51).balance())

        self.assertEqual(42.56, Movement.objects.per_week(2011, 52).expenses())
        self.assertEqual(1567, Movement.objects.per_week(2011, 52).earnings())
        self.assertEqual(1524.44, Movement.objects.per_week(2011, 52).balance())

        self.assertEqual(43.2, Movement.objects.per_week(2012, 1).expenses())
        self.assertEqual(300, Movement.objects.per_week(2012, 1).earnings())
        self.assertEqual(256.8, Movement.objects.per_week(2012, 1).balance())

        self.assertEqual(939.35, Movement.objects.per_week(2012, 2).expenses())
        self.assertEqual(0, Movement.objects.per_week(2012, 2).earnings())
        self.assertEqual(-939.35, Movement.objects.per_week(2012, 2).balance())

        self.assertEqual(18, Movement.objects.per_week(2012, 3).expenses())
        self.assertEqual(1.76, Movement.objects.per_week(2012, 3).earnings())
        self.assertEqual(-16.24, Movement.objects.per_week(2012, 3).balance())

        self.assertEqual(72.48, Movement.objects.per_week(2012, 4).expenses())
        self.assertEqual(0, Movement.objects.per_week(2012, 4).earnings())
        self.assertEqual(-72.48, Movement.objects.per_week(2012, 4).balance())

        self.assertEqual(557.5, Movement.objects.per_week(2012, 5).expenses())
        self.assertEqual(1567, Movement.objects.per_week(2012, 5).earnings())
        self.assertEqual(1009.5, Movement.objects.per_week(2012, 5).balance())

        self.assertEqual(879.8, Movement.objects.per_week(2012, 6).expenses())
        self.assertEqual(0, Movement.objects.per_week(2012, 6).earnings())
        self.assertEqual(-879.8, Movement.objects.per_week(2012, 6).balance())

        self.assertEqual(209.87, Movement.objects.per_week(2012, 7).expenses())
        self.assertEqual(0, Movement.objects.per_week(2012, 7).earnings())
        self.assertEqual(-209.87, Movement.objects.per_week(2012, 7).balance())

        self.assertEqual(37.8, Movement.objects.per_week(2012, 8).expenses())
        self.assertEqual(0, Movement.objects.per_week(2012, 8).earnings())
        self.assertEqual(-37.8, Movement.objects.per_week(2012, 8).balance())

        self.assertEqual(97.3, Movement.objects.per_week(2012, 9).expenses())
        self.assertEqual(1567, Movement.objects.per_week(2012, 9).earnings())
        self.assertEqual(1469.7, Movement.objects.per_week(2012, 9).balance())