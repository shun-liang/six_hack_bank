from flask import Flask, request
from bank.bank import add_user, get_users, get_user, create_test_data

app = Flask(__name__)

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
        username = request_json['user_name']
        account_number = request_json['account_number']
        sort_code = request_json['sort_code']
        add_user(username, account_number, sort_code)
        print get_users()
        return 'Success'

@app.route('/card', methods=['POST'])
def change_card_state():
    if request.method == 'POST':
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

if __name__ == "__main__":
    create_test_data() 
    print get_users()
    app.run(debug=True)
