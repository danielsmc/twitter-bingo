#!/usr/bin/python

import dateutil.parser
import json
import MySQLdb
import MySQLdb.cursors
import subprocess
import random
import traceback
import twitter

class UserCard:
	def __init__(self,user):
		self.user = user
		self.tiles = []
		self.goals = {}
		self.refreshFromDB()
		return

	def hasCard(self):
		return len(self.tiles) > 0

	def refreshFromDB(self):
		mysql_cur.execute("""SELECT user_card_square_id,ucs.goal_id,hashtag,position,daub_tweet_id,embed_code,image_url
			FROM user_card_squares as ucs
			JOIN goals USING(goal_id)
			LEFT JOIN daub_tweets USING(daub_tweet_id)
			WHERE ucs.user_id = %s
			ORDER BY position ASC""",(self.user['id'],))
		self.tiles=list(mysql_cur.fetchall())
		self.goals = {t['hashtag'].lower():t for t in self.tiles}

	def createCard(self):
		mysql_cur.execute("SELECT goal_id FROM goals")
		tile_goals = random.sample(mysql_cur.fetchall(),24)
		insert_squares = [(self.user['id'],tile_goals[i]['goal_id'],i) for i in xrange(24)]
		mysql_cur.executemany("INSERT INTO user_card_squares (user_id,goal_id,position) VALUES (%s,%s,%s)",insert_squares)
		mysql_cur.execute("INSERT INTO users (user_id,screen_name,profile_image_url) VALUES (%s,%s,%s)",
			(self.user['id'],self.user['screen_name'],self.user['profile_image_url']))
		self.refreshFromDB()

	def hasGoal(self,goal):
		return goal in self.goals

	def findHashtag(self,hashtags):
		for h in hashtags:
			if self.hasGoal(h.lower()):
				return h.lower()
		return None

	def goalDaubed(self,goal):
		return (goal in self.goals) and (self.goals[goal]['daub_tweet_id'] is not None)

	def getBingoLines(self):
		return [[0,1,2,3,4],
				[5,6,7,8,9],
				[10,11,12,13],
				[14,15,16,17,18],
				[19,20,21,22,23],
				[0,5,10,14,19],
				[1,6,11,15,20],
				[2,7,16,21],
				[3,8,12,17,22],
				[4,9,13,18,23],
				[0,6,17,23],
				[4,8,15,19]]

	def daubsLeft(self):
		daubs_left=4
		for line in self.getBingoLines():
			daubs_left = min(daubs_left,len([True for tile in line if self.tiles[tile]['daub_tweet_id'] is None]))
		return daubs_left


	def hasBingo(self):
		if not self.hasCard():
			return False
		return self.daubsLeft()==0

	def totalDaubs(self):
		return len([True for tile in self.tiles if tile['daub_tweet_id'] is not None])

	def hasBlackout(self):
		if not self.hasCard():
			return False
		return self.totalDaubs() == 24
	
	def markSquare(self,hashtag,tweet):
		if not self.hasCard():
			return
		daub_tweet = (tweet.getID(),tweet.getUser()['id'],self.goals[hashtag]['goal_id'],tweet.getCreatedAt(),tweet.getPic())
		mysql_cur.execute("INSERT INTO daub_tweets (daub_tweet_id,user_id,goal_id,created_at,image_url) VALUES (%s,%s,%s,%s,%s)",daub_tweet)
		mysql_cur.execute("UPDATE user_card_squares SET daub_tweet_id = %s WHERE user_card_square_id = %s",(tweet.getID(),self.goals[hashtag]['user_card_square_id']))
		self.refreshFromDB()
		mysql_cur.execute("UPDATE users SET daubs_left=%s,total_daubs=%s WHERE user_id = %s",(self.daubsLeft(),self.totalDaubs(),self.user['id']))

	def suggestions(self):
		return None

	def renderCard(self):
		# tilehtml = []
		# for t in self.tiles:
		# 	if t['daub_tweet_id'] is None:
		# 		tilehtml.append('#%s'%t['hashtag'])
		# 	else:
		# 		tilehtml.append('<img src="%s"/>'%t['image_url'])
		# tilehtml = tuple(tilehtml)
		# with open("foo.html","wb") as fh:
		# 	fh.write("""<html><head>
		# 					<style>
		# 					* {
		# 						margin:0;
		# 						border:0;
		# 						padding:0;
		# 						background:white;
		# 					}
		# 					table {
		# 						border:1px solid black;
		# 					}
		# 					td {
		# 						width:150px;
		# 						height:150px;
		# 						max-width:150px;
		# 						max-height:150px;
		# 						border:1px solid black;
		# 						text-align: center;
		# 					}
		# 					img {
		# 						max-height:100%%;
		# 						max-width:100%%;
		# 					}
		# 					</style>
		# 				</head><body><table>
		# 				<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
		# 				<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
		# 				<tr><td>%s</td><td>%s</td><td>FREE</td><td>%s</td><td>%s</td></tr>
		# 				<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
		# 				<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
		# 				</table></body></html>""" % tilehtml)
		# subprocess.call(["phantomjs", "rasterize.js", "foo.html", "foo.png", "750px*750px"])
		subprocess.call(["phantomjs", "rasterize.js", "http://localhost:5000/card/"+self.user['screen_name']+"?fortwitter", "foo.png", "750px*870px"])
		with open("foo.png") as fh:
			img_data = fh.read()
		return img_data

class InputTweet:
	def __init__(self, t):
		self.t = t
		if self.isRetweet():
			return # ignore
		if not self.mentionsUs():
			return # ignore
		self.user_card = UserCard(self.getUser())
		tagged_goal = self.user_card.findHashtag(self.getHashtags())
		if not self.user_card.hasCard():
			if self.isDirectlyAtUs():
				self.user_card.createCard()
				self.sendReply("Welcome to the game!")
			else:
				pass # ignore
		elif self.getPic() is None:
			if self.isDirectlyAtUs():
				self.sendReply("Thanks for playing!")
			else:
				pass # ignore
		elif len(self.getHashtags()) == 0:
			self.sendReply("Did you mean to add a hashtag? I can't mark your card without one!")
		elif tagged_goal is None:
			self.sendReply("Whoops, that one's not on your card.")
		elif self.user_card.goalDaubed(tagged_goal):
			self.sendReply("Looks like you've already spotted #%s"%tagged_goal)
		else:
			had_bingo = self.user_card.hasBingo()
			self.user_card.markSquare(tagged_goal,self)
			if had_bingo:
				if self.user_card.hasBlackout():
					self.sendReply("You filled your card! What a champion.")
					self.sendPublic("Wow! @%s just filled their bingo card!",(self.getScreenName(),tagged_goal))
				else:
					self.sendReply("Nice #%s! Why not try these suggestions TK?"%tagged_goal)
			elif self.user_card.hasBingo():
				self.sendReply("Congratulations, that's Bingo! You're welcome to keep going...")
				self.sendPublic("BINGO! @%s just spotted #%s to win bingo."(self.getScreenName(),tagged_goal))
			else:
				self.sendReply("Nice #%s! Why not try these suggestions TK?"%tagged_goal)

	def isRetweet(self):
		if 'retweeted_status' in t:
			return True
		elif t['text'].startswith("RT"):
			return True
		else:
			return False

	def mentionsUs(self):
		for m in t['entities']['user_mentions']:
			if m['screen_name'] == config['twitter']['screen_name']:
				return True
		return False

	def isDirectlyAtUs(self):
		for m in t['entities']['user_mentions']:
			if m['indices'][0]==0 and m['screen_name'] == config['twitter']['screen_name']:
				return True
		return False

	def getID(self):
		return self.t['id']

	def getUser(self):
		return self.t['user']

	def getScreenName(self):
		return self.t['user']['screen_name']

	def getCreatedAt(self):
		ca = dateutil.parser.parse(self.t['created_at'])
		if ca.utcoffset().total_seconds()<1.0:
			ca = ca.replace(tzinfo=None)  # MySQL doesn't know about timezones, so we're doing this so it doesn't show a warning
		else:
			raise ValueError('Tweet created_at is not in UTC.')
		return ca

	def getPic(self):
		if 'media' in t['entities'] and len(t['entities']['media'])>0:
			return t['entities']['media'][0]['media_url']
		else:
			return None

	# def getEmbedCode(self):
	# 	return twit.statuses.oembed(_id = self.t['id'])['html']

	def getHashtags(self):
		return [h['text'].lower() for h in t['entities']['hashtags']]

	def sendReply(self,message):
		img_data = self.user_card.renderCard()
		status = ("@%s %s Your card: http://mbtabingo.com/card/%s " % (self.getScreenName(),message,self.getScreenName())).encode('ascii','ignore')
		status = status.encode('ascii','ignore')
		id_str = self.t['id_str'].encode('ascii','ignore')
		print status, id_str
		# print twit.statuses.update(**{"status":status,"in_reply_to_status_id":self.t['id']})
		print twit.statuses.update_with_media(**{"status":status,"in_reply_to_status_id":id_str,"media[]":img_data})

	def sendPublic(self,message):
		return


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

auth=twitter.OAuth(	config['twitter']['access_token'],
					config['twitter']['access_token_secret'],
					config['twitter']['consumer_key'],
					config['twitter']['consumer_secret'])

twit = twitter.Twitter(auth=auth)
twitstream =  twitter.TwitterStream(auth=auth, domain='userstream.twitter.com')

user_stream = twitstream.user(**{"stall_warnings":True,"with":"user"})

def doTweet(tweet):
	print tweet
	if "text" in tweet:
		try:
			InputTweet(tweet)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			traceback.print_exc()

for t in user_stream:
	doTweet(t)

# print t.help.configuration()
# print t.account.verify_credentials()


