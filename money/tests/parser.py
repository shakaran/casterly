import cStringIO
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from money.models import BankAccount, Movement
from money.parser import parse_csv, import_movements
from money.parser.banks import LloydsParser
from money.tests.models import EXAMPLE_BANK_ACCOUNT


LLOYDS_SIMPLE_EXAMPLE_PAY_ROW = """
25/12/2011,DEB,'00-00-00,0000000,Christmas presents,134.3,,200"""

LLOYDS_SIMPLE_EXAMPLE_EARN_ROW = """
06/01/2012,TFR,'00-00-00,0000000,Tickets,,134.3,200"""


class SimpleCSVParserTest(TestCase):

    def setUp(self):
        super(SimpleCSVParserTest, self).setUp()

    def tearDown(self):
        super(SimpleCSVParserTest, self).tearDown()

    def test_single_pay_row(self):
        data = parse_csv(
            cStringIO.StringIO(LLOYDS_SIMPLE_EXAMPLE_PAY_ROW),
            parser=LloydsParser,
        )
        self.assertEqual(1, len(data))
        row = data[0]
        self.assertEqual(5, len(row.keys()))

        self.assertTrue('date' in row.keys())
        self.assertTrue('account_number' in row.keys())
        self.assertTrue('description' in row.keys())
        self.assertTrue('amount' in row.keys())
        self.assertTrue('balance' in row.keys())

        self.assertEqual(date(2011, 12, 25), row['date'])
        self.assertEqual("00-00-00 0000000", row['account_number'])
        self.assertEqual("Christmas presents", row['description'])
        self.assertEqual(-134.3, row['amount'])
        self.assertEqual(200, row['balance'])

    def test_single_earn_row(self):
        data = parse_csv(
            cStringIO.StringIO(LLOYDS_SIMPLE_EXAMPLE_EARN_ROW),
            parser=LloydsParser,
        )
        self.assertEqual(1, len(data))
        row = data[0]
        self.assertEqual(5, len(row.keys()))

        self.assertTrue('date' in row.keys())
        self.assertTrue('account_number' in row.keys())
        self.assertTrue('description' in row.keys())
        self.assertTrue('amount' in row.keys())
        self.assertTrue('balance' in row.keys())

        self.assertEqual(date(2012, 1, 6), row['date'])
        self.assertEqual("00-00-00 0000000", row['account_number'])
        self.assertEqual("Tickets", row['description'])
        self.assertEqual(134.3, row['amount'])
        self.assertEqual(200, row['balance'])

    def test_double_rows(self):
        data = parse_csv(
            cStringIO.StringIO(
                LLOYDS_SIMPLE_EXAMPLE_PAY_ROW + LLOYDS_SIMPLE_EXAMPLE_EARN_ROW),
            parser=LloydsParser,
        )
        self.assertEqual(2, len(data))
        row = data[0]
        self.assertEqual(5, len(row.keys()))

        self.assertTrue('date' in row.keys())
        self.assertTrue('account_number' in row.keys())
        self.assertTrue('description' in row.keys())
        self.assertTrue('amount' in row.keys())
        self.assertTrue('balance' in row.keys())

        self.assertEqual(date(2011, 12, 25), row['date'])
        self.assertEqual("00-00-00 0000000", row['account_number'])
        self.assertEqual("Christmas presents", row['description'])
        self.assertEqual(-134.3, row['amount'])
        self.assertEqual(200, row['balance'])

        row = data[1]
        self.assertEqual(5, len(row.keys()))

        self.assertTrue('date' in row.keys())
        self.assertTrue('account_number' in row.keys())
        self.assertTrue('description' in row.keys())
        self.assertTrue('amount' in row.keys())
        self.assertTrue('balance' in row.keys())

        self.assertEqual(date(2012, 1, 6), row['date'])
        self.assertEqual("00-00-00 0000000", row['account_number'])
        self.assertEqual("Tickets", row['description'])
        self.assertEqual(134.3, row['amount'])
        self.assertEqual(200, row['balance'])


class SimpleCSVImporterTest(TestCase):
    def setUp(self):
        super(SimpleCSVImporterTest, self).setUp()
        self.user = User.objects.create(
            username="foouser", email="foo@example.com")
        data = EXAMPLE_BANK_ACCOUNT.copy()
        data["owner"] = self.user
        data["current_balance"] = 340.0
        self.bank_account = BankAccount.objects.create(**data)

    def tearDown(self):
        self.bank_account.delete()
        self.user.delete()
        super(SimpleCSVImporterTest, self).tearDown()

    def test_single_pay_movement(self):
        self.assertEqual(0, Movement.objects.count())
        data = parse_csv(
            cStringIO.StringIO(LLOYDS_SIMPLE_EXAMPLE_PAY_ROW),
            parser=LloydsParser,
        )
        import_movements(data, self.bank_account)
        self.assertEqual(1, Movement.objects.count())

        movement = Movement.objects.all()[0]
        self.assertEqual(data[0]["description"], movement.description)
        self.assertEqual(data[0]["amount"], movement.amount)
        self.assertEqual(data[0]["date"], movement.date)
        self.assertEqual(self.bank_account, movement.bank_account)

    def test_single_earn_movement(self):
        self.assertEqual(0, Movement.objects.count())
        data = parse_csv(
            cStringIO.StringIO(LLOYDS_SIMPLE_EXAMPLE_EARN_ROW),
            parser=LloydsParser,
        )
        import_movements(data, self.bank_account)
        self.assertEqual(1, Movement.objects.count())

        movement = Movement.objects.all()[0]
        self.assertEqual(data[0]["description"], movement.description)
        self.assertEqual(data[0]["amount"], movement.amount)
        self.assertEqual(data[0]["date"], movement.date)
        self.assertEqual(self.bank_account, movement.bank_account)

    def test_multi_movement(self):
        self.assertEqual(0, Movement.objects.count())
        data = parse_csv(
            cStringIO.StringIO(
                LLOYDS_SIMPLE_EXAMPLE_PAY_ROW + LLOYDS_SIMPLE_EXAMPLE_EARN_ROW),
            parser=LloydsParser,
        )
        import_movements(data, self.bank_account)
        self.assertEqual(2, Movement.objects.count())
        movements = Movement.objects.all()
        self.assertEqual(data[0]["description"], movements[0].description)
        self.assertEqual(data[0]["amount"], movements[0].amount)
        self.assertEqual(data[0]["date"], movements[0].date)
        self.assertEqual(self.bank_account, movements[0].bank_account)

        self.assertEqual(data[1]["description"], movements[1].description)
        self.assertEqual(data[1]["amount"], movements[1].amount)
        self.assertEqual(data[1]["date"], movements[1].date)
        self.assertEqual(self.bank_account, movements[1].bank_account)

    def test_avoid_duplicates(self):
        self.assertEqual(0, Movement.objects.count())
        data = parse_csv(
            cStringIO.StringIO(LLOYDS_SIMPLE_EXAMPLE_PAY_ROW),
            parser=LloydsParser,
        )
        imported, rejected = import_movements(data, self.bank_account)
        self.assertEqual(1, Movement.objects.count())
        self.assertEqual(1, imported)
        self.assertEqual(0, len(rejected))
        imported, rejected = import_movements(data, self.bank_account)
        self.assertEqual(1, Movement.objects.count())
        self.assertEqual(0, imported)
        self.assertEqual(1, len(rejected))
        self.assertEqual(data[0]["description"], rejected[0]["description"])
        self.assertEqual(data[0]["amount"], rejected[0]["amount"])
        self.assertEqual(data[0]["date"], rejected[0]["date"])
