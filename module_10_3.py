
import random
import threading
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        self.lock.acquire()
        for i in range(100):
            debit = random.randint(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            self.balance += debit
            print(f'Пополнение: {debit}. Баланс: {self.balance}')
            sleep(0.001)

    def take(self):
        for i in range(100):
            credit = random.randint(50, 500)
            print(f'Запрос на {credit}')
            if credit <= self.balance:
                self.balance -= credit
                print(f'Снятие: {credit}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()


if __name__ == '__main__':
    bk = Bank()
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')

