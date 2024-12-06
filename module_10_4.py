
import random
import queue
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number: int):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self):
        sleep(random.randint(3, 10))
        # sleep(0.01)


class Cafe:
    def __init__(self, *tables: Table):
        self.tables = tables
        self.q = queue.Queue()

    def guest_arrival(self, *guests: Guest):
        has_free_table = False
        number_free_table = 0

        for guest in guests:
            for table in self.tables:
                if table.guest is None:
                    has_free_table = True
                    number_free_table = table.number
                    break
            if has_free_table:
                tables[number_free_table - 1].guest = guest
                guest.start()
                print(f'{guest.name} сел(-а) за стол номер {number_free_table}')
                has_free_table = False
            else:
                self.q.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        all_tables_free = False
        while not self.q.empty() or not all_tables_free:

            for table in tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None

                if not self.q.empty() and table.guest is None:
                    guest = self.q.get()
                    table.guest = guest
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    guest.start()
                    all_tables_free = False

                if sum(table.guest is not None for table in self.tables) == 0:
                    all_tables_free = True


if __name__ == '__main__':
    # Создание столов:
    tables = [Table(number) for number in range(1, 6)]
    # Гости:
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]
    # Создание гостей:
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами:
    cafe = Cafe(*tables)
    # Приём гостей:
    cafe.guest_arrival(*guests)
    # Обслуживание гостей:
    cafe.discuss_guests()


