from multiprocessing import Pool, Manager, Queue
from collections import namedtuple
import logging
from time import sleep
import time
import tomllib
from pizza import Pizza
from report import report_data

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%M:%S'
    )

# using the first & last the pipeline can reach start/end
FIRST_STATION = 'dough'
LAST_STATION = 'table'


def worker(job: str, worker_number: int, queues: dict[str: Queue], duration_in_sec: int):
    worker_name = f'{job}_{worker_number}'
    while True:
        pizza: Pizza = queues[job].get()
        if pizza:
            if job == FIRST_STATION:
                pizza.record_start_time()
            logging.error(f'{worker_name}: starting on pizza {pizza}')
            sleep(duration_in_sec)
            logging.error(f'{worker_name}: done on pizza {pizza}')
            next_job = pizza.next_job()
            if next_job == LAST_STATION:
                pizza.record_service_time()
                #pizza.service_time = time.time()
            queues[next_job].put(pizza)
                

def load_workers_config(file_path: str) -> dict():
    try:
        with open(file_path, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        raise Exception(f'failed to load workers_config.toml with exception: {e}')

def receive_orders(queues: dict[str: Queue], pizza_list: list):
    logging.info('The Pizza Flow is open!')
    pizzas = [Pizza(order) for order in pizza_list]
    for pizza in pizzas:
        queues[pizza.next_job()].put(pizza)

def start_pizzeria(workers_config_path: str, pizza_orders: list):
    workers_config = load_workers_config(workers_config_path)
    manager = Manager()
    queues = {
              **{job_name: manager.Queue() for job_name in workers_config},
              LAST_STATION: manager.Queue(maxsize=len(pizza_orders)),
              }
    for job, worker_config in workers_config.items():
        # We use manager.queue for shared queue
        pool = Pool(worker_config['amount'])
        for i in range(worker_config['amount']):
            pool.apply_async(worker, 
                            args=(job, i, queues, worker_config['duration_in_sec']))
    receive_orders(queues, pizza_orders)

    while not queues[LAST_STATION].full():
        pass
    logging.info('Done!')
    for _ in pizza_orders:
        pizza = queues[LAST_STATION].get()
        print(pizza, pizza.end_time - pizza.start_time)
    

if __name__ == '__main__':
    start_pizzeria('./pizza_chefs.toml', [['a'], ['1']])







