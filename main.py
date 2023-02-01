from pizza_process import init_pizzeria_workers_and_queues, run_pizzeria, close_pools
from report import print_report, send_to_mongo
from pizza import Pizza
import tomllib
import logging


def load_toml_file(file_path: str) -> dict():
    try:
        with open(file_path, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        raise Exception(
            f'failed to load toml  file with exception: {e}')


def main(workers_config: dict, pizzas_order: dict, mongo_uri: str) -> None:
    """
    args:
        worker_config: dict, with worker names as keys and setting dict {'amount': int, 'duration_in_sec': int}
        pizzas_order: list of lists representing the order
        mongo_uri: uri to the mongoDB server
    """
    pizzas = [Pizza(order) for order in pizzas_order]
    pools, queues = init_pizzeria_workers_and_queues(
        workers_config, number_of_pizzas=len(pizzas))
    report = run_pizzeria(queues, pizzas)
    close_pools(pools)
    print_report(**report)
    send_to_mongo(report, mongo_uri)


if __name__ == '__main__':
    try:
        workers_config: dict = load_toml_file('./workers.toml')
        pizzas_order = load_toml_file('./order.toml ').get('order', [])
        main(workers_config, pizzas_order, 'mongodb://localhost:27017/')
    except Exception as e:
        logging.exception(f'running failed :(  with exception: {e}')
