import os
import json
from datetime import datetime

orders_histary = "pizza_orders.json"
MENUS = {
    "kid": {
        "name": "меню для детей",
        "items": {
            "1": {"name": "пицца с макаронами", "price": 67},
            "2": {"name": "сладкая с маршмеллоу пицца", "price": 400},
            "3": {"name": "маленькая картошка фри", "price": 119},
        }
    },
    "teenager": {
        "name": "меню для подростков",
        "items": {
            "1": {"name": "пицца пеперони", "price": 600},
            "2": {"name": "пицца 4 сыра", "price": 599},
            "3": {"name": "острые крылышки кфс", "price": 129},
        }
    },
    "adult": {
        "name": "взрослое меню",
        "items": {
            "1": {"name": "пицца 4 мяса", "price": 1200},
            "2": {"name": "пицца золотая", "price": 3949},
            "3": {"name": "пицца пеперони", "price": 600},
        }
    }
}


def cheque_decorator(func):
    def wrapper(*args, **kwargs):
        lines = func(*args, **kwargs)
        max_len = max(len(line) for line in lines) if lines else 20
        border = "-" * max_len
        print(f"\n{border}")
        print("чек")
        print(border)
        for line in lines:
            print(line)
        print(border)
    return wrapper


@cheque_decorator
def print_single_cheque(order):
    lines = [
        f"Время: {order['time']}",
        f"Гостей: {order['guest_count']}",
        "Позиции:"
    ]
    for item in order["items"]:
        lines.append(f" - {item['name']} — {item['price']} руб")
    lines.append(f"Оплата: {order['pay_method']}")
    lines.append(f"ИТОГО: {order['total_price']} руб.")
    return lines


def load_orders():
    if os.path.exists(orders_histary):
        try:
            with open(orders_histary, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_order(order_data):
    orders = load_orders()
    orders.append(order_data)
    with open(orders_histary, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)


def admin_panel():
    print("\nпанель для админа")
    orders = load_orders()
    if not orders:
        print("истории заказов нету")
        return
    total_revenue = 0
    for i, order in enumerate(orders, 1):
        print(f"\nЗАКАЗ №{i}")
        print_single_cheque(order)
        total_revenue += order['total_price']
    print(f"\nОБЩАЯ ВЫРУЧКА ЗА ВСЁ ВРЕМЯ: {total_revenue} руб.")


def get_age(age):
    if age < 14:
        return "kid"
    elif 14 <= age < 18:
        return "teenager"
    else:
        return "adult"


def pay_process(total_sum):
    print(f"\nитого к оплате: {total_sum} руб.")
    while True:
        choice = input("выберите способ оплаты (1 - наличные, 2 - карта): ")
        if choice == "1":
            while True:
                try:
                    cash = float(input(f"введите сумму наличных (не менее {total_sum} руб.): "))
                    if cash >= total_sum:
                        change = cash - total_sum
                        print(f"принято: {cash} руб ваша сдача: {change} руб.")
                        return "наличные"
                    else:
                        print("введенной суммы недостаточно")
                except ValueError:
                    print("введите корректное число.")
        elif choice == "2":
            print("оплата прошла успешно")
            return "карта"
        else:
            print("неверный выбор, введите 1 или 2")


def main():
    print("Приветствуем в нашей пиццерии!")
    name = input("Как вас зовут? (или введите пароль админа): ")
    if name.lower() == "admin":
        admin_panel()
        return
    while True:
        try:
            guest_count = int(input("Сколько человек будет делать заказ? "))
            if guest_count > 0:
                break
            print("Количество гостей должно быть больше 0")
        except ValueError:
            print("Введите число")
    final_cart = []
    total_price = 0
    for i in range(1, guest_count + 1):
        print(f"\nГость №{i}")
        while True:
            try:
                age = int(input("Введите ваш возраст для подбора меню: "))
                if age > 0:
                    break
                print("Возраст должен быть больше 0")
            except ValueError:
                print("Введите число")
        category = get_age(age)
        menu_section = MENUS[category]
        while True:
            print("\nДоступные позиции:")
            for key, val in menu_section["items"].items():
                print(f"[{key}] {val['name']} — {val['price']} руб.")
            print("[0] Завершить выбор")
            choice = input("Выберите номер позиции: ")
            if choice == "0":
                break
            elif choice in menu_section["items"]:
                selected_item = menu_section["items"][choice]
                final_cart.append({
                    "name": selected_item["name"],
                    "price": selected_item["price"],
                    "category": menu_section["name"]
                })
                total_price += selected_item["price"]
                print(f"Добавлено: {selected_item['name']}")
            else:
                print("Неверная позиция меню, попробуйте еще раз")
    pay_method = pay_process(total_price)
    order_data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "guest_count": guest_count,
        "items": final_cart,
        "total_price": total_price,
        "pay_method": pay_method
    }
    save_order(order_data)
    print_single_cheque(order_data)


if __name__ == "__main__":
    main()
