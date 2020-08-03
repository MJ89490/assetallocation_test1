# import csv, sqlite3
# conn = sqlite3.connect("asset_allocation.sql")
# curs = conn.cursor()
# curs.execute("CREATE TABLE times_signals_output  ("TIMES Signals DateTime, US Equities INTEGER,	EU Equities INTEGER,
#                     JP Equities INTEGER, HK Equities INTEGER, US_10y_Bonds INTEGER, 	UK 10y Bonds	Eu 10y Bonds
#                     CA 10y Bonds	JPY	EUR	AUD	CAD	GBP);")
#
#              "id INTEGER PRIMARY KEY, type INTEGER, term TEXT, definition TEXT);")
# reader = csv.reader(open('PC.txt', 'r'), delimiter='|')
# for row in reader:
#     to_db = [unicode(row[0], "utf8"), unicode(row[1], "utf8"), unicode(row[2], "utf8")]
#     curs.execute("INSERT INTO PCFC (type, term, definition) VALUES (?, ?, ?);", to_db)
# conn.commit()