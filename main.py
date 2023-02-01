from pizza_process import init_pizzeria_workers_and_queues, run_pizzeria, close_pools
from report import print_report, send_to_mongo
from pizza import Pizza
import argparse
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
    pools, queues, manager = init_pizzeria_workers_and_queues(
        workers_config, number_of_pizzas=len(pizzas))
    report = run_pizzeria(queues, pizzas)
    # closing the pools and manager
    close_pools(pools)
    manager.shutdown()
    print_report(**report)
    if mongo_uri:
        send_to_mongo(report, mongo_uri)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--mongo_uri', type=str, default='',
                        help='MongoDB URI. if not given does not send')
    parser.add_argument('--order_file', type=str, default='./order.toml',
                        help='The path to the order file.')
    parser.add_argument('--workers_file', type=str, default='./workers.toml',
                        help='The path to the worker settings file.')
    args = parser.parse_args()
    try:
        workers_config: dict = load_toml_file(args.workers_file)
        pizzas_order = load_toml_file(args.order_file).get('order', [])
        main(workers_config, pizzas_order, args.mongo_uri)
    except Exception as e:
        logging.exception(f'running failed :(  with exception: {e}')
