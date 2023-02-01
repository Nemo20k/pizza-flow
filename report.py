import pymongo
import datetime
import logging
import time
from pizza import Pizza


def build_report(start_time: float, pizzas: list[Pizza]) -> dict:
    return {
        'overall_duration': round((time.time() - start_time), 2),
        'pizzas': [
            {
                'toppings': pizza.toppings,
                'work_time': round(pizza.end_time - pizza.start_time, 2)
            } for pizza in pizzas
        ]
    }


def print_report(overall_duration: float, pizzas: list[dict]) -> None:
    """pretty printing the overall duration in work time for each pizza"""
    pizzas_times_text = '\n'.join(
        [f'\t{i} - {pizza_dict["toppings"]}: {pizza_dict["work_time"]}'
            for i, pizza_dict in enumerate(pizzas)])
    report_text = '\n'.join([
        f'{12*"*"} PIZZA REPORT (in seconds) {12*"*"}',
        f'Overall preparation time: {overall_duration}',
        'Pizzas preparation time:',
        pizzas_times_text])
    print(report_text)


def send_to_mongo(report_json: dict, mongo_uri: str) -> None:
    """sending the report data to mongoDB server"""
    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name := "pizza-flow"]
        report_json['timestamp'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        collection = db[collection_name := "pizza-flow-report"]
        collection.insert_one(report_json)
        logging.info(
            f'report sent to mongoDB server at {mongo_uri}/{db_name}.{collection_name}')
    except Exception as e:
        raise Exception(f'Failed to send report to mongoDB with exception: {e}')
