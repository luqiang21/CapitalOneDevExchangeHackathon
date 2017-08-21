import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from capital_one import *

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

global account_detail
account_detail = return_rewards()

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("PointsIntent")

def return_points():
    item = 'rewardsBalance'
    currency = 'points'
    if currency == 'points':
        i = 1
    elif currency == 'miles':
        i = 0 # Miles
    balance = inqury(account_detail, i, item)
    round_msg = render_template('round', numbers=balance)
    session.attributes['numbers'] = balance
    return question(round_msg)


@ask.intent("MilesIntent")

def return_miles():
    item = 'rewardsBalance'
    currency = 'miles'
    if currency == 'points':
        i = 1
    elif currency == 'miles':
        i = 0 # Miles
    balance = inqury(account_detail, i, item)
    round_msg = render_template('round', numbers=balance)
    session.attributes['numbers'] = balance
    return question(round_msg)

@ask.intent("YesIntent")

def next_round():

    item = 'rewardsBalance'
    currency = 'miles'
    if currency == 'points':
        i = 1
    elif currency == 'miles':
        i = 0 # Miles
    balance = inqury(account_detail, i, item)
    round_msg = render_template('round', numbers=balance)
    session.attributes['numbers'] = balance


    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    # winning_numbers = session.attributes['numbers']

    print 'winning:',winning_numbers

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)
