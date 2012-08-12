from datetime import date


class LloydsParser:

	@staticmethod
	def parse_row(row):
		data = {}
		splitted_date = row[0].split("/")
		date_info = map(
			int, [splitted_date[2], splitted_date[1], splitted_date[0]])
		data["date"] = date(*date_info)
		data["account_number"] = "%s %s" % (row[2].replace("'", ""), row[3])
		data["description"] = row[4]
		data["balance"] = float(row[7])
		if row[5]:
			data["amount"] = - float(row[5])
		if row[6]:
			data["amount"] = float(row[6])
		return data


ENTITY_TO_PARSER = {
	"lloyds": LloydsParser,
	"halifax": LloydsParser,
}