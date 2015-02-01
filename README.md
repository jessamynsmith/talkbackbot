talkbackbot
===========

[![Build Status](https://travis-ci.org/jessamynsmith/talkbackbot.svg?branch=master)](https://travis-ci.org/jessamynsmith/talkbackbot)
[![Coverage Status](https://coveralls.io/repos/jessamynsmith/talkbackbot/badge.svg?branch=master)](https://coveralls.io/r/jessamynsmith/talkbackbot?branch=master)

Are you tired of "That's what she said" jokes? Then this bot is for you!
It will join a specified channel and respond to the configured trigger phrases
with what she really said, i.e. a quotation from a notable woman. It will also
respond to any direct message with a quotation.

Many quotes taken from this excellent resource:
http://womenshistory.about.com/library/qu/blqulist.htm

Development
-----------

Fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/talkbackbot.git

Create a virtualenv and install dependencies:

    mkvirtualenv talkbackbot
    pip install -r requirements/development.txt

Run tests and view coverage:

    coverage run -m nose
    coverage report

Check code style:

    flake8


Usage
-----

Activate virtualenv

    workon talkbackbot

Copy settings.py.EXAMPLE to settings.py and edit to suit yourself

    cp settings.py.EXAMPLE settings.py
    vim settings.py

Run the bot

    twistd twsrs

Stop the bot

    kill `cat twistd.pid`

