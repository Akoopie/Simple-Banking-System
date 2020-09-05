import random
import sys
import sqlite3

registry = {}


class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
        self.balance = 0


def main_menu():
    print('1. Create an account', '2. Log into account', '0. Exit', sep='\n')
    option = int(input())
    while option > 2 or option < 0:
        print('Invalid entry!')
        option = int(input())
    else:
        if option == 0:
            exit_bank()
        if option == 1:
            createaccount()
        if option == 2:
            login()


def account_menu(card_number):
    print('1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out', '0. Exit', sep='\n')
    option = int(input())
    while option > 5 or option < 0:
        print('Invalid entry!')
        option = int(input())
    else:
        if option == 0:
            exit_bank()
        if option == 1:
            balance(card_number)
        if option == 2:
            add_income(card_number)
        if option == 3:
            transfer(card_number)
        if option == 4:
            close_account(registry[card_number])
        if option == 5:
            logout()


def add_income(card_number):
    balance = int(input('Enter income:'))
    #print(registry[card_number].balance)
    registry[card_number].balance += balance
    #print(registry[card_number].balance)
    update_database(registry[card_number])
    print('Income was added!')
    account_menu(card_number)


def transfer(card_number):
    print('Transfer')
    acct = input('Enter card number:')
    acct_luhn = str(acct)[:-1]
    #print(acct_luhn)
    #print(luhn(acct_luhn))

    for x in registry.keys():
        if acct_luhn == x[:-1]:
            if acct[-1] != luhn(acct_luhn):
                print('Probably you made a mistake in the card number. Please try again!')
                account_menu(card_number)
            else:
                break
        else:
            continue

    if acct == card_number:
        print("You can't transfer money to the same account!")
        account_menu(card_number)

    elif acct[-1] != luhn(acct_luhn):
        print('Probably you made a mistake in the card number. Please try again!')
        account_menu(card_number)

    elif acct in registry:
        amount = int(input('Enter how much money you want to transfer:'))
        if registry[card_number].balance < amount:
            print('Not enough money!')
            account_menu(card_number)
        else:
            registry[card_number].balance -= amount
            registry[acct].balance += amount
            update_database(registry[card_number])
            update_database(registry[acct])
            print('Success!')
            account_menu(card_number)

    else:
        print('Such a card does not exist.')
        account_menu(card_number)


def close_account(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number="+str(card.card_number))
    conn.commit()
    conn.close()
    main_menu()


def logout():
    print('You have successfully logged out!')
    main_menu()


def balance(card_number):
    print('Balance:', str(registry[card_number].balance))
    account_menu(card_number)


def login():
    card_number = input('Enter your card number:')
    pin = input('Enter your PIN:')
    if card_number in registry and registry[card_number].pin == pin:
        print('You have successfully logged in!')
        account_menu(card_number)
    else:
        print('Wrong card number or PIN!')
        main_menu()


def createaccount():
    account_number_precursor = '400000' + str(random.randint(0, 99999999)).zfill(9)
    pin_number = str(random.randint(0, 9999)).zfill(4)
    account_number = account_number_precursor + luhn(account_number_precursor)
    #print(len(account_number))
    card = Card(account_number, pin_number)
    register(card)
    insert_database(card)
    print('Your card has been created', 'Your card number:', account_number, 'Your card PIN:', pin_number, sep='\n')
    main_menu()


def luhn(account_number_precursor):
    luhn1 = [int(x) for x in account_number_precursor]
    luhn2 = []
    luhn3 = []
    for x, y in enumerate(luhn1):
        if x % 2 == 0:
            y *= 2
            luhn2.append(y)
        else:
            luhn2.append(y)
    for x in luhn2:
        if x > 9:
            x -= 9
            luhn3.append(x)
        else:
            luhn3.append(x)
    luhn_total = sum(luhn3)
   #print(luhn_total)
    if luhn_total > 99:
        luhn_total -= 100

    check_sum = str(10 - luhn_total % 10)
    if luhn_total % 10 == 0:
        check_sum = str(0)
    #print(check_sum)
    return check_sum


def register(card):
    registry[card.card_number] = card


def exit_bank():
    print('Bye!')
    sys.exit()


def create_table():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    #cur.execute('DROP TABLE card')
    cur.execute("CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()


def destroy_database():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('DROP TABLE card')
    conn.close()


def insert_database(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (card.card_number, card.pin))
    conn.commit()
    conn.close()


def update_database(card):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance = "+str(card.balance)+" WHERE number = "+str(card.card_number))
    conn.commit()
    conn.close()


def debug_update_database(num, fum):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (num, fum))
    conn.commit()
    conn.close()

def query_database():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM card")
    print(cur.fetchall())
    conn.close()

destroy_database()
create_table()
main_menu()
#query_database()
