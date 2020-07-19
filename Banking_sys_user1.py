from random import randint


class Bank:
    def __init__(self):
        self.cards = {}
        self.logged_in = False

    def menu(self):
        while not self.logged_in:
            print('1. Create an account\n2. Log into account\n0. Exit')
            choice = input()
            if choice == '1':
                self.create()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('\nBye!')
                quit()

    def account_menu(self):
        while self.logged_in:
            print('1. Balance\n2. Log out\n0. Exit')
            choice = input()
            if choice == '1':
                print('\nBalance: 0\n')
            elif choice == '2':
                self.logged_in = False
                print('\nYou have successfully logged out!\n')
            elif choice == '0':
                print('\nBye!')
                quit()

    def create(self):
        print()
        card = self.luhn_alg()
        pin = str.zfill(str(randint(0000, 9999)), 4)
        print(f'Your card has been created\nYour card number:\n{card}\nYour card PIN:\n{pin}\n')
        self.cards[card] = pin

    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        if card in self.cards and self.cards[card] == pin:
            print('\nYou have successfully logged in!\n')
            self.logged_in = True
            self.account_menu()
        else:
            print('\nWrong card number or Pin!\n')

    def luhn_alg(self):
        card = '400000' + str.zfill(str(randint(000000000, 999999999)), 9)
        card_check = [int(i) for i in card]
        for index, _ in enumerate(card_check):
            if index % 2 == 0:
                card_check[index] *= 2
            if card_check[index] > 9:
                card_check[index] -= 9
        check_sum = str((10 - sum(card_check) % 10) % 10)
        card += check_sum
        return card


if __name__ == '__main__':
    stage_2 = Bank()
    stage_2.menu()
