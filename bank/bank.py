from datetime import datetime
from copy import deepcopy

_users = []
_accounts = []

def add_user(username, account_number, sort_code):
    new_user = User(username, account_number, sort_code)
    _users.append(new_user)

def get_users():
    return deepcopy(_users)

def get_user(username):
    for user in _users:
        if user.username == username:
            return user
    return None 

def get_account(account_number):
    for account in _accounts:
        if account.number == account_number:
            return account
    return None

class User:
    '''
    Represents a Telegram user.
    '''
    def __init__(self, username, account_number, sort_code):
        self.username = username
        self.account = MyAccount(account_number, sort_code)
        self.sort_code = sort_code

    def __str__(self):
        return 'username: %s, account number: %s, sort_code: %s' % (self.username, self.account, self.sort_code)

    def __repr__(self):
        return 'username: %s, my account: %s, sort_code: %s' % (self.username, self.account, self.sort_code)

    def add_card(self, alias, card_number):
        self.account.add_card(card_number, alias)

    def transfer(self, account_number, sort_code, amount):
        self.account.transfer(account_number, sort_code, amount)

    def lock_card(self, alias):
        self.account.lock_card(alias)

class MyAccount:
    '''
    Service interface of an account for a Telegram user.
    '''
    cards = {}

    def __init__(self, account_number, sort_code):
        self.account = Account(account_number, sort_code)
        cards = []

    #def __repr__(self):
    #    return 'account: %s, cards: %s' % (account, )

    def add_card(self, card_number, alias):
        card = Card(card_number)
        self.cards[alias] = card

    def transfer(self, account_number, sort_code, amount):
        target = get_account(account_number)
        self.account.transfer(target, amount)

    def lock_card(self, alias):
        self.cards[alias].lock()

class Account:
    '''
    Represents a bank account.
    '''
    transactions = []

    def __init__(self, account_number, sort_code, transactions=None):
        self.number = account_number
        self.sort_code = sort_code
        self.balance = 5000

    def transfer(self, target, amount):
        if self.balance > amount:
            self.balance -= amount
            target.balance += amount
            self.transactions.append(Transaction(self.number, target.number, amount))
        else:
            raise ValueError('Not enough balance to proceed the transfer.')

class Card:
    '''
    Represents a bank card.
    '''
    def __init__(self, card_number):
        self.number = card_number
        self.is_active = True

    def lock(self):
        self.is_active = False
        print 'Card: %s locked.' % self.number

class Transaction:
    '''
    Represent a bank transaction
    '''
    def __init__(self, source, target, amount, description=None):
        self.source = source
        self.target = target
        self.amount = amount
        self.timestamp = datetime.now()
        if description:
            self.description = description
        else:
            self.description = ''

def create_test_data():
    add_user('john', '12345678', '102030')
    user = get_user('john')
    user.add_card('my maestro', '1234123412341234')
