#!/usr/bin/python

import csv
import MySQLdb
import MySQLdb.cursors
import json
import sys


with open('config.json') as fh:
	config = json.load(fh)

mysql_conn = MySQLdb.connect(
	host=config['mysql']['host'],
	port=config['mysql']['port'],
	user=config['mysql']['user'],
	passwd=config['mysql']['password'],
	db=config['mysql']['database'],
	use_unicode=True,
	charset="utf8mb4",
	cursorclass = MySQLdb.cursors.DictCursor)
mysql_conn.autocommit(True)

mysql_cur = mysql_conn.cursor()
mysql_cur.execute("SET time_zone='+0:00'")

with open(sys.argv[1]) as fh:
	reader = csv.DictReader(fh)
	mysql_cur.execute("TRUNCATE TABLE goals")
	for row in reader:
		mysql_cur.execute("INSERT INTO goals (hashtag,flavor_text,headline,url) VALUES (%s,%s,%s,%s)",
			(row["Hashtag"][1:],row["Square"],row["Headline"],row["URL"]))