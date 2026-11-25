import os
import json

ORDERS_HISTORY = "pizza_orders.json"

MENUS = {
    "kid": {
        "name": "меню для детей",
        "items": {
            "1": {
                "name": "пицца с томатная",
                "price": 299,
                "ingredients": ["основа из теста", "томатный соус", "моцарелла"]
            },
            "2": {
                "name": "сладкая пицца с шоколадом",
                "price": 349,
                "ingredients": ["основа из теста", "шоколад", "банан"]
            },
            "3": {
                "name": "маленькая картошка фри",
                "price": 159,
                "ingredients": ["картофель"]
            },
            "4": {
                "name": "сок мультифруктовый 0.5л",
                "price": 209,
                "ingredients": ["сок мультифрукт"]
            },
        }
    },
    "teenager": {
        "name": "меню для подростков",
        "items": {
            "1": {
                "name": "пицца пеперони",
                "price": 599,
                "ingredients": ["основа из теста", "томатный соус", "моцарелла", "пеперони"]
            },
            "2": {
                "name": "пицца 4 сыра",
                "price": 549,
                "ingredients": ["основа из теста", "4 сыра"]
            },
            "3": {
                "name": "картошка фри",
                "price": 209,
                "ingredients": ["картофель"]
            },
            "4": {
                "name": "газява 0.5л",
                "price": 229,
                "ingredients": ["газировка"]
            },
        }
    },
    "adult": {
        "name": "взрослое меню",
        "items": {
            "1": {
                "name": "пицца пеперони",
                "price": 799,
                "ingredients": ["основа из теста", "томатный соус", "моцарелла", "пеперони"]
            },
            "2": {
                "name": "пицца 4 сыра",
                "price": 719,
                "ingredients": ["основа из теста", "4 сыра"]
            },
            "3": {
                "name": "пицца пеперони big++maxpro",
                "price": 1199,
                "ingredients": ["большая основа из теста", "томатный соус", "моцарелла", "пеперони", "перец"]
            },
            "4": {
                "name": "картошка фри big+++",
                "price": 459,
                "ingredients": ["картофель", " томатный соус"]
            },
            "5": {
                "name": "газява 0.5л",
                "price": 229,
                "ingredients": ["газировка"]
            }
        }
    }
}


def get_age_category(age):
    if age < 14:
        return "kid"
    elif 14 <= age < 18:
        return "teenager"
    return "adult"


def get_menu_by_category(category):
    return MENUS[category]


def load_orders():
    if os.path.exists(ORDERS_HISTORY):
        try:
            with open(ORDERS_HISTORY, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_order(order_data):
    orders = load_orders()
    orders.append(order_data)
    with open(ORDERS_HISTORY, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)
