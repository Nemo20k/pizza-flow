import time
import json

report_data = {
    'start_time': None,
    'end_time': None,
    'pizzas': {}
}

def generate_report(start_time: float, end_time: float, pizzas: dict[str, float]) -> str:
    pizzas_times_text = '\n'.join(f'\t{pizza}: {duration:.2f}' for pizza, duration in pizzas.items())
    report_text = '\n'.join([
        f'{12*"*"} PIZZA REPORT (in seconds) {12*"*"}',
        f'Overall preparation time: {(end_time-start_time):.2f}',
         'Pizzas preparation time:',
        pizzas_times_text])
    print(report_text)
    return report_text
