import time


class Pizza:
    """
    represent a pizza (...)
    the job attribute used as queue for the workers using the next_job()
    """
    def __init__(self, order: list[str]):
        self.toppings = order
        self.jobs = ['dough',
                     # another 'topping' job for each topping
                     *['topping' for _ in order],
                     'oven',
                     'serving',
                     'table'
                     ]
        self.start_time = self.end_time = None

    def __str__(self) -> str:
        return ','.join(self.toppings)

    def next_job(self):
        return self.jobs.pop(0)

    def record_service_time(self):
        self.end_time = time.time()

    def record_start_time(self):
        self.start_time = time.time()
