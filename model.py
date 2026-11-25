import os
import json

ORDERS_HISTORY = "pizza_orders.json"
WAREHOUSE_FILE = "warehouse.json"

MENU_FILES = {
    "kid": "menu_kid.json",
    "teenager": "menu_teenager.json",
    "adult": "menu_adult.json"
}


def _load_json(filename, default_value):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default_value
    return default_value


def _save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_age_category(age):
    if age < 14:
        return "kid"
    elif 14 <= age < 18:
        return "teenager"
    return "adult"


def get_menu_by_category(category):
    filename = MENU_FILES.get(category)
    if not filename:
        return {"name": "Меню не найдено", "items": {}}
    return _load_json(filename, {"name": "Пустое меню", "items": {}})


def load_warehouse():
    return _load_json(WAREHOUSE_FILE, {})


def save_warehouse(warehouse_data):
    _save_json(WAREHOUSE_FILE, warehouse_data)


def restock_warehouse(amount=10):
    warehouse = load_warehouse()
    for item in warehouse:
        warehouse[item] += amount
    save_warehouse(warehouse)
    return warehouse


def check_ingredients_available(ingredients, reserved_counts):
    warehouse = load_warehouse()
    for item in ingredients:
        already_in_cart = reserved_counts.get(item, 0)
        if warehouse.get(item, 0) - already_in_cart <= 0:
            return False, item
    return True, None


def deduct_ingredients(ingredients_list):
    warehouse = load_warehouse()
    for item in ingredients_list:
        if item in warehouse and warehouse[item] > 0:
            warehouse[item] -= 1
    save_warehouse(warehouse)


def load_orders():
    return _load_json(ORDERS_HISTORY, [])


def save_order(order_data):
    orders = load_orders()
    orders.append(order_data)
    _save_json(ORDERS_HISTORY, orders)
