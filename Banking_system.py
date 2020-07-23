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


class Account:

    def __init__(self, ac_num1):
        self.ac_num = ac_num1
        self.pin = str(''.join(["{}".format(random.randint(0, 9)) for i in range(4)]))
        self.balance = 0


def account_generator():
    pt_1 = "400000"
    pt_2 = ''.join(["{}".format(random.randint(0, 9)) for i in range(9)])
    num = [int(i) for i in (pt_1 + pt_2)]
    for i in range(0, 15, 2):
        num[i] *= 2
        if num[i] > 9:
            num[i] -= 9
    check_sum = 10-(sum(num) % 10)
    return pt_1+pt_2+str(check_sum)


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
            check_acnt = db_retrieve(check_num)
        if check_acnt[1] != check_pin:
            print("\nWrong card number or PIN!")
            continue
        print("\nYou have successfully logged in!")

        while True:
            choice_2 = int(input("\n1. Balance\n2. Log out\n0. Exit\n"))
            if choice_2 == 1:
                print(f"Balance: {check_acnt[2]}\n")
            elif choice_2 == 2:
                print("\nYou have successfully logged out!\n")
                break
            elif choice_2 == 0:
                choice = 0
                print("\nBye")
                break
















