from flask import Flask, request, jsonify
from bank.bank import add_user, get_users, get_user
import sys
import logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
#app.logger.setLevel(logging.WARNING)

@app.route('/')
def index():
    return 'This is a ficiontal bank server.' 

@app.route('/start', methods=['POST'])
def link_account():
    '''
    Link the Telegram account with a bank account.
    '''
    if request.method == 'POST':
        request_json = request.get_json(force=True)
        username = request_json['username']
        account_number = request_json['accountnumber']
        sort_code = request_json['sortcode']
        add_user(username, account_number, sort_code)
        #print get_users()
        return ''

@app.route('/card', methods = ['PUT'])
def add_card():
    '''
    Add a new card.
    '''
    request_json = request.get_json(force=True)
    username = request_json['username']
    card_alias = request_json['cardalias']
    card_number = request_json['cardnumber']
    user = get_user(username)
    user.add_card(card_alias, card_number)
    return ''


@app.route('/card', methods=['POST'])
def change_card_state():
    '''
    Modify the state of a card.
    '''
    request_json = request.get_json(force=True)
    username = request_json['username']
    card_alias = request_json['cardalias']
    action = request_json['action']
    if action == 'lock':
        # Card locking logic
        #card_number = 1234123412341234
        user = get_user(username)
        user.lock_card(card_alias)
        return ''

#@app.route('/aliase', methods=[])

@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    user = get_user(username)
    if user:
        return jsonify(balance=user.get_balance())


@app.route('/transfer', methods=['POST'])
def make_transfer():
    '''
    Make a transfer to another bank account.
    '''
    request_json = request.get_json(force=True)
    username = request_json['username']
    to_alias = request_json['aliasname']

if __name__ == "__main__":
    app.run(debug=True)
