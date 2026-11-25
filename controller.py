from datetime import datetime
import model
import view


def get_positive_int(prompt, error_msg):
    while True:
        try:
            value = int(view.ask_input(prompt))
            if value > 0:
                return value
            view.show_message(error_msg)
        except ValueError:
            view.show_message("Введите число")


def handle_payment(total_sum):
    view.show_message(f"\nитого к оплате: {total_sum} руб.")
    while True:
        choice = view.ask_input("выберите способ оплаты (1 - наличные, 2 - карта): ")
        if choice == "1":
            while True:
                try:
                    cash = float(view.ask_input(f"введите сумму наличных (не менее {total_sum} руб.): "))
                    if cash >= total_sum:
                        change = cash - total_sum
                        view.show_message(f"принято: {cash} руб ваша сдача: {change} руб.")
                        return "наличные"
                    else:
                        view.show_message("введенной суммы недостаточно")
                except ValueError:
                    view.show_message("введите корректное число.")
        elif choice == "2":
            view.show_message("оплата прошла успешно")
            return "карта"
        else:
            view.show_message("неверный выбор, введите 1 или 2")


def run_admin():
    orders = model.load_orders()
    view.show_admin_report(orders)


def run_customer_order():
    guest_count = get_positive_int(
        "Сколько человек будет делать заказ? ",
        "Количество гостей должно быть больше 0"
    )
    final_cart = []
    total_price = 0

    for i in range(1, guest_count + 1):
        view.show_message(f"\nГость №{i}")
        age = get_positive_int(
            "Введите ваш возраст для подбора меню: ",
            "Возраст должен быть больше 0"
        )
        category = model.get_age_category(age)
        menu_section = model.get_menu_by_category(category)

        while True:
            view.show_menu_items(menu_section)
            choice = view.ask_input("Выберите номер позиции: ")
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
                view.show_message(f"Добавлено: {selected_item['name']}")
            else:
                view.show_message("Неверная позиция меню, попробуйте еще раз")

    pay_method = handle_payment(total_price)
    order_data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "guest_count": guest_count,
        "items": final_cart,
        "total_price": total_price,
        "pay_method": pay_method
    }
    model.save_order(order_data)
    view.print_single_cheque(order_data)


def start_app():
    view.show_message("Приветствуем в нашей пиццерии!")
    name = view.ask_input("Как вас зовут? (или введите пароль админа): ")
    if name.lower() == "admin":
        run_admin()
    else:
        run_customer_order()
