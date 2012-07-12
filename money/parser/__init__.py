import csv

from money.models import Movement


def parse_csv(raw_csv, parser, header_lines=0):
	reader = csv.reader(raw_csv, delimiter=',', quotechar='"')
	rows = []

	for row in reader:
		if reader.line_num > header_lines and row:
			rows.append(parser.parse_row(row))
	return rows


def import_movements(data, bank_account):
	for row in data:
		Movement.objects.create(
			bank_account=bank_account,
			description=row["description"],
			amount=row["amount"],
			date=row["date"],
		)
