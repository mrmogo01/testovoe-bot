from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_TICKETS_SOLD = 0.005

PROBABILITY_REGULAR_TICKETS = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "tickets": {
        "regular": 0,
        "vip": 0
    }
}


def generate_stamp(previous_value):
    tickets_sold = random.random() < PROBABILITY_TICKETS_SOLD
    regular_tickets_sold = 1 if tickets_sold and random.random() < PROBABILITY_REGULAR_TICKETS else 0
    vip_tickets_sold = 1 if tickets_sold and regular_tickets_sold == 0 else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "tickets": {
            "regular": previous_value["tickets"]["regular"] + regular_tickets_sold,
            "vip": previous_value["tickets"]["vip"] + vip_tickets_sold
        }
    }


def generate_sales():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


sales_stamps = generate_sales()

pprint(sales_stamps)

def get_tickets(sales_stamps, offset):
    low, high = 0, len(sales_stamps) - 1
    best_match = None

    while low <= high:
        mid = (low + high) // 2
        if sales_stamps[mid]["offset"] == offset:
            best_match = mid
            break
        elif sales_stamps[mid]["offset"] < offset:
            best_match = mid
            low = mid + 1
        else:
            high = mid - 1

    if best_match is not None:
        return sales_stamps[best_match]["tickets"]["regular"], sales_stamps[best_match]["tickets"]["vip"]
    else:
        return 0, 0  # В случае, если точный offset не найден, возвращаем 0, 0

# Пример вызова функции
offset = 100
sales_stamps = generate_sales()
regular, vip = get_tickets(sales_stamps, offset)
print(f"Regular tickets: {regular}, VIP tickets: {vip}")