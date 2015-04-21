talkbackbot
===========

[![Build Status](https://circleci.com/gh/jessamynsmith/talkbackbot.svg?style=shield)](https://circleci.com/gh/jessamynsmith/talkbackbot)
[![Coverage Status](https://coveralls.io/repos/jessamynsmith/talkbackbot/badge.svg?branch=master)](https://coveralls.io/r/jessamynsmith/talkbackbot?branch=master)

Are you tired of "That's what she said" jokes? Then this bot is for you!
It will join a specified channel and respond to the configured trigger phrases
with what she really said, i.e. a quotation from a notable woman. It will also
respond to any direct message with a quotation.

Many quotes taken from this excellent resource:
http://womenshistory.about.com/library/qu/blqulist.htm

Usage
-----

Activate virtualenv

    workon talkbackbot

Copy settings.py.EXAMPLE to settings.py and edit as desired

    cp settings.py.EXAMPLE settings.py
    vim settings.py

Note: QUOTES_FILE should have one quotation per line. QUOTES_URL must point to a JSON API that
provides data in the following format:

    {"results": [{"author": "Corazon Aquino", "text": "The media's power is frail."}]}

Run the bot

    twistd twsrs

Stop the bot

    kill `cat twistd.pid`

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
