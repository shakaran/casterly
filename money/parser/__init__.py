import csv

from money.models import Movement


def parse_csv(raw_csv, parser, header_lines=0, reverse_order=False):
    reader = csv.reader(raw_csv, delimiter=',', quotechar='"')
    rows = []

    for row in reader:
        if reader.line_num > header_lines and row:
            rows.append(parser.parse_row(row))
    if reverse_order:
        rows.reverse()
    return rows


def import_movements(data, bank_account):
    rejected = []
    accepted = 0
    for row in data:
        obj, created = Movement.objects.get_or_create(
            bank_account=bank_account,
            description=row["description"],
            amount=row["amount"],
            date=row["date"],
            category=row["category"],
        )
        if created:
            accepted += 1
        else:
            rejected.append(row)
    return accepted, rejected
