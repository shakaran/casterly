import csv


def parse_csv(raw_csv, parser):
	reader = csv.reader(raw_csv, delimiter=',', quotechar='"')
	rows = []

	for row in reader:
		if row:
			rows.append(parser.parse_row(row))
	return rows
