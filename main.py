from flask import Flask, request, jsonify, make_response
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
    if action == 'block':
        # Card locking logic
        #card_number = 1234123412341234
        user = get_user(username)
        user.lock_card(card_alias)
        return ''

@app.route('/alias', methods=['PUT'])
def add_alias():
    request_json = request.get_json(force=True)
    username = request_json['username']
    alias_name = request_json['useralias']
    account_number = request_json['accountnumber']
    sort_code = request_json['sortcode']
    user = get_user(username)
    if user:
        user.add_alias(alias_name, account_number, sort_code)
        return ''
    else:
        return make_response(jsonify(error='User does not exist.'), 400)

@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    user = get_user(username)
    print(user)
    if user:
        return make_response(jsonify(balance=str(user.get_balance())), 200)
    else:
        return make_response(jsonify(error='User does not exist.'), 400)



@app.route('/transfer', methods=['POST'])
def make_transfer():
    '''
    Make a transfer to another bank account.
    '''

    request_json = request.get_json(force=True)
    username = request_json['from']
    to_alias = request_json['to']
    amount = request_json['amount']
    user = get_user(username)
    print(username)
    print(user)
    if user:
        alias = user.get_alias(to_alias)
        print(alias)
        if alias:
            user.transfer(alias.account.number, alias.account.sort_code, float(amount))
            return make_response(jsonify(senderbalance=user.get_balance(), receiverbalance=alias.get_balance()), 200)
        else:
            return make_response(jsonify(error='alias does not exist'), 400)
    else:
        return make_response(jsonify(error='user does not exist'), 400)

if __name__ == "__main__":
    app.run(debug=True)
