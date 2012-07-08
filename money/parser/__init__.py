import csv


def parse_csv(raw_csv, parser, header_lines=0):
	reader = csv.reader(raw_csv, delimiter=',', quotechar='"')
	rows = []

	for row in reader:
		if reader.line_num > header_lines and row:
			rows.append(parser.parse_row(row))
	return rows
