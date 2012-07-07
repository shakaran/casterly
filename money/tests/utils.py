import cStringIO
from datetime import date

from django.test import TestCase

from money.banks import LloydsParser
from money.utils import parse_csv


LLOYDS_SIMPLE_EXAMPLE_PAY_ROW = """
25/12/2011,DEB,'00-00-00,0000000,Christmas presents,134.3,,200"""

LLOYDS_SIMPLE_EXAMPLE_EARN_ROW = """
06/01/2012,TFR,'00-00-00,0000000,Tickets,,134.3,200"""


class CSVParserTest(TestCase):

	def setUp(self):
		super(CSVParserTest, self).setUp()

	def tearDown(self):
		super(CSVParserTest, self).tearDown()

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
