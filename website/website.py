from flask import Flask, render_template
import json
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

# app.debug = True

with open('../config.json') as fh:
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

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/card/<screen_name>')
def card(screen_name):
	user_id = None
	mysql_cur.execute("SELECT user_id FROM users WHERE screen_name = %s",(screen_name,))
	for row in mysql_cur:
		user_id = row['user_id']
	if user_id is None:
		return "user not found"
	mysql_cur.execute("""SELECT flavor_text,hashtag,position,image_url
			FROM user_card_squares as ucs
			JOIN goals USING(goal_id)
			LEFT JOIN daub_tweets USING(daub_tweet_id)
			WHERE ucs.user_id = %s
			ORDER BY position ASC""",(user_id,))
	squares=list(mysql_cur.fetchall())
	squares.insert(12,{"free":"woot"})
	return render_template('card.html', squares=squares)


if __name__ == '__main__':
    app.run()
