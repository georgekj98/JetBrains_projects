import random
import sqlite3


def db_create():
    create_query = ''' CREATE TABLE IF NOT EXISTS card(
                            id      INT PRIMARY KEY,
                            number  TEXT NOT NULL,
                            pin     TEXT NOT NULL,
                            balance DEFAULT 0
                            );'''
    cursor.execute(create_query)
    connection.commit()


def db_check(check_acc):
    data = cursor.execute("SELECT number FROM card")
    return check_acc in [tup[0] for tup in data.fetchall()]


def db_insert(insert_num,insert_pin,insert_balance):
    data = cursor.execute("SELECT id FROM card")
    insert_id = len(data.fetchall())+1
    insert_query = '''INSERT INTO card VALUES (?,?,?,?)'''
    cursor.execute(insert_query, (insert_id, insert_num, insert_pin, insert_balance))
    connection.commit()


def db_update(update_num, update_bal):
    update_query = f''' UPDATE card SET balance = {update_bal} WHERE number = {update_num}'''
    cursor.execute(update_query)
    connection.commit()


def db_retrieve(ret_number):
    ret_query = '''SELECT 
                        number,
                        pin,
                        balance
                    FROM
                        card
                    WHERE
                        number =?;'''
    data = cursor.execute(ret_query,(ret_number,))
    return data.fetchone()


def db_account_close(close_num):
    del_query = f"DELETE FROM card WHERE number ={close_num}"
    cursor.execute(del_query)
    connection.commit()
    print("The account has been closed!")


def check_luhn(num):
    num = num = [int(i) for i in num]
    for i in range(0, 15, 2):
        num[i] *= 2
        if num[i] > 9:
            num[i] -= 9
    check_sum = str((10 - sum(num) % 10) % 10)
    return check_sum


def account_generator():
    pt_1 = "400000"
    pt_2 = ''.join(["{}".format(random.randint(0, 9)) for i in range(9)])
    check_sum = check_luhn(str(pt_1 + pt_2))
    return pt_1+pt_2+str(check_sum)


class Account:

    def __init__(self, ac_num1):
        self.ac_num = ac_num1
        self.pin = str(''.join(["{}".format(random.randint(0, 9)) for i in range(4)]))
        self.balance = 0


def sub_menu(log_num):

    while True:
        log_num, log_pin, log_bal = db_retrieve(log_num)
        choice_2 = int(input("\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5.Log out\n0. Exit\n"))
        if choice_2 == 1:
            print(f"Balance: {log_bal}\n")

        elif choice_2 == 2:
            deposit = int(input("\nEnter income:"))
            db_update(log_num, int(log_bal+deposit))
            print("Income was added!")

        elif choice_2 == 3:
            trans_num = input("\nTransfer\nEnter card number:")
            if not (check_luhn(trans_num[:-1]) == trans_num[-1]):
                print("\nProbably you made mistake in the card number. Please try again!")
            else:
                if not (db_check(trans_num)):
                    print("\nSuch a card does not exist.")
                else:
                    trans_amt = int(input("\nEnter how much money you want to transfer:"))
                    if trans_amt > log_bal:
                        print("\nNot enough money!")
                    else:
                        trans_num, trans_pin, trans_bal = db_retrieve(trans_num)
                        db_update(log_num, int(log_bal-trans_amt))
                        db_update(trans_num, int(trans_bal+trans_amt))

        elif choice_2 == 4:
            db_account_close(log_num)
            return 1

        elif choice_2 == 5:
            print("\nYou have successfully logged out!\n")
            return 1

        elif choice_2 == 0:
            print("\nBye")
            return 0


# Establishing connection to the local database
connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
# db_create() functions creates a table if it isn't present
db_create()

choice = 123
while choice != 0:
    choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if choice == 0:
        print("\nBye")
        break

    elif choice == 1:
        ac_num = account_generator()
        while():
            if db_check(ac_num):
                ac_num = account_generator()
            else:
                break
        new_accnt = Account(ac_num)
        db_insert(new_accnt.ac_num, new_accnt.pin, 0)
        print("\nYour card has been created")
        print(f"Your card number:\n{new_accnt.ac_num}")
        print(f"Your card PIN:\n{new_accnt.pin}\n")

    elif choice == 2:
        check_num = str(input("\nEnter your card number:"))
        check_pin = str(input("Enter your PIN:"))
        if not db_check(check_num):
            print("\nWrong card number or PIN!")
            continue
        else:
            ac_num, pin, balance = db_retrieve(check_num)
        if pin != check_pin:
            print("\nWrong card number or PIN!")
            continue
        print("\nYou have successfully logged in!")
        choice = sub_menu(ac_num)


















