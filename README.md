Twitter Bingo is a experiment created by [Daniel McLaughlin](https://twitter.com/mclaughlin), [David Putney](https://twitter.com/putney_dm), and [Andrew Ba Tran](https://twitter.com/abtran) at the June 2014 [#newshack hackathon](http://hackingjournalism.com/). It's a scavenger hunt bingo game, played entirely through Twitter. Though it can be adapted to any theme or event, the demo we set up is [@mbtabingo](https://twitter.com/mbtabingo). To play, tweet at that account, and it'll tweet a card back at you. Each square on the card contains something you might see on the subway, and an identifying hashtag. To claim a square, take a picture and tweet it with the hashtag, mentioning @mbtabingo. There's a [leaderboard](http://mbtabingo.com), too.

###Install:
(Tested on ubuntu 14. You'll need to create a twitter account, and a twitter app, and get the API keys set up. This is left as an excercise for the reader.)
$ sudo apt-get install -y mysql-server libmysqlclient-dev git python-pip python-dev phantomjs

$ sudo pip install virtualenv

$ virtualenv ve
$ . ve/bin/activate
$ pip install -r requirements.txt

You'll need to hack the python twitter library a little-- uploading image data causes unicode problems.
In ve/lib/python2.7/site-packages/twitter/api.py, comment out the seocnd line: "from __future__ import unicode_literals"

You'll need to create a config.json file patterned after config-sample.json, but there are a lot of things that are still hardcoded in various python files. Sorry.

The html markup is fed from https://github.com/putneydm/newshack (not automatically)
