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


def show_message(text):
    print(text)


def ask_input(prompt):
    return input(prompt)


def show_menu_items(menu_section):
    print("\nДоступные позиции:")
    for key, val in menu_section["items"].items():
        ingredients = ", ".join(val.get("ingredients", []))
        ing_text = f" (Состав: {ingredients})" if ingredients else ""
        print(f"[{key}] {val['name']}{ing_text} — {val['price']} руб.")
    print("[0] Завершить выбор")


def show_admin_report(orders):
    print("\nпанель для админа")
    if not orders:
        print("истории заказов нету")
        return
    total_revenue = 0
    for i, order in enumerate(orders, 1):
        print(f"\nЗАКАЗ №{i}")
        print_single_cheque(order)
        total_revenue += order['total_price']
    print(f"\nОБЩАЯ ВЫРУЧКА ЗА ВСЁ ВРЕМЯ: {total_revenue} руб.")
