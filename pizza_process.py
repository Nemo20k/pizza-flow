from multiprocessing import Pool, Manager, Queue
import logging
import time
from pizza import Pizza
from report import build_report

# logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%M:%S'
)


def worker(station: str, worker_number: int, queues: dict[str: Queue], duration_in_sec: int):
    """
    represent a worker in pool of workers. 
    constantly look for next station in the matching queue and move it to the next queue.
    """
    worker_name = f'{station}_{worker_number}'
    while not (queues[Pizza.last_station].full()):
        pizza: Pizza = queues[station].get()
        if pizza:
            if station == Pizza.first_station:
                pizza.record_start_time()
            logging.error(f'{worker_name}: starting on pizza {pizza}')
            time.sleep(duration_in_sec)
            logging.error(f'{worker_name}: done on pizza {pizza}')
            next_station = pizza.next_station()
            if next_station == Pizza.last_station:
                pizza.record_service_time()
            queues[next_station].put(pizza)


def init_pizzeria_workers_and_queues(workers_config: dict, number_of_pizzas: int) -> tuple:
    """
    init the queues and workers pool of the pizzeria
    """
    manager = Manager()
    queues = {
        **{station_name: manager.Queue() for station_name in workers_config},
        # defining the maxsize of the last queue so we can know when it full
        Pizza.last_station: manager.Queue(maxsize=number_of_pizzas),
    }
    pools = []
    for station, worker_config in workers_config.items():
        # We use manager.queue for shared queue
        pool = Pool(worker_config['amount'])
        for i in range(worker_config['amount']):
            pool.apply_async(worker,
                             args=(station, i, queues, worker_config['duration_in_sec']))

    return pools, queues, manager


def run_pizzeria(queues: dict[str: Queue], pizzas: list[Pizza]) -> dict:
    """
    adding the orders into te initial queue, and looping while workers are moving the pizzas between the station queues
    return the report data as dict
    """
    # recording for the report
    start_time = time.time()

    logging.info('The Pizza Flow is open!')
    # starting by inserting the pizzas to the first queue (dough queue)
    for pizza in pizzas:
        queues[pizza.next_station()].put(pizza)

    # Main loop - ends when all the pizza are in the last queue
    while not queues[Pizza.last_station].full():
        pass

    logging.info('Done!')
    pizzas = [queues[Pizza.last_station].get() for _ in pizzas]
    return build_report(start_time, pizzas)


def close_pools(pools: list[Pool]) -> None:
    for pool in pools:
        pool.close()
    time.sleep(5)
