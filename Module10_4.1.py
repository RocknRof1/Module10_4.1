from queue import Queue
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Customer:
    def __init__(self, number):
        self.number = number


class Cafe:
    def __init__(self, num_tables):
        self.tables = [Table(i) for i in range(1, num_tables + 1)]
        self.queue = Queue()
        self.customer_count = 0

    def customer_arrival(self):
        while self.customer_count < 20:
            sleep(1)
            self.customer_count += 1
            customer = Customer(self.customer_count)
            print(f'Посетитель {customer.number} прибыл.')
            if customer.number > 3:
                print(f'Посетитель номер {customer.number} ожидает свободный стол.')
            self.queue.put(customer)

    def serve_customer(self, table):
        while True:
            customer = self.queue.get()
            print(f'Посетитель {customer.number} сел за стол {table.number}')
            table.is_busy = True
            sleep(5)
            print(f'Посетитель {customer.number} покушал и ушёл со стола {table.number}.')
            table.is_busy = False
            if customer.number > (self.customer_count - 3):
                exit()


cafe = Cafe(3)

arrival_thread = Thread(target=cafe.customer_arrival)
table_threads = [Thread(target=cafe.serve_customer, args=(table,)) for table in cafe.tables]

arrival_thread.start()
for thread in table_threads:
    thread.start()
arrival_thread.join()
for thread in table_threads:
    thread.join()