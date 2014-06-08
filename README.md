Install:

$ sudo apt-get install -y mysql-server libmysqlclient-dev git python-pip python-dev phantomjs

$ sudo pip install virtualenv

$ virtualenv ve
$ . ve/bin/activate
$ pip install -r requirements.txt

You'll need to hack the python twitter library a little-- uploading image data causes unicode problems.
In ve/lib/python2.7/site-packages/twitter/api.py, comment out the seocnd line: "from __future__ import unicode_literals"

You'll need to create a config.json file patterned after config-sample.json, but there are a lot of things that are still hardcoded in various python files. Sorry.

The html markup is fed from https://github.com/putneydm/newshack (not automatically)