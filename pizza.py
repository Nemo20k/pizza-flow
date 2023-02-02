import time


class Pizza:
    """
    represent a pizza (...)
    the station attribute used as queue for the workers using the next_station()
    """

    # using the first & last the pipeline can reach start/end
    first_station = 'dough'
    last_station = 'table'

    def __init__(self, order: list[str]):
        self.toppings = order
        self.stations = ['dough',
                         # another 'topping' station for each topping
                         *['topping' for _ in order],
                         'oven',
                         'serving',
                         'table'
                         ]
        self.start_time = self.end_time = None

    def __str__(self) -> str:
        return ','.join(self.toppings)

    def next_station(self):
        return self.stations.pop(0)

    def record_service_time(self):
        self.end_time = time.time()

    def record_start_time(self):
        self.start_time = time.time()
