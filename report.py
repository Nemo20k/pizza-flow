import pymongo
import datetime
import logging


def print_report(overall_duration: float, pizzas: dict[str, float]) -> None:
    """pretty printing the overall duration in work time for each pizza"""
    pizzas_times_text = '\n'.join(
        f'\t{pizza}: {duration}' for pizza, duration in pizzas.items())
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
        logging.info(f'report sent to mongoDB server at {mongo_uri}/{db_name}.{collection_name}')
    except Exception as e:
        raise f'Failed to send report to mongoDB with exception: {e}'
