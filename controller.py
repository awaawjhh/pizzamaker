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
    view.show_message(f"\nИтого к оплате: {total_sum} руб.")
    while True:
        choice = view.ask_input("Выберите способ оплаты (1 - наличные, 2 - карта): ")
        if choice == "1":
            while True:
                try:
                    cash = float(view.ask_input(f"Введите сумму наличных (не менее {total_sum} руб.): "))
                    if cash >= total_sum:
                        change = round(cash - total_sum, 2)
                        view.show_message(f"Принято: {cash} руб. Ваша сдача: {change} руб.")
                        return "наличные"
                    else:
                        view.show_message("Введенной суммы недостаточно")
                except ValueError:
                    view.show_message("Введите корректное число.")
        elif choice == "2":
            view.show_message("Оплата прошла успешно")
            return "карта"
        else:
            view.show_message("Неверный выбор, введите 1 или 2")


def run_admin():
    while True:
        view.show_admin_menu()
        choice = view.ask_input("Выберите действие: ")
        if choice == "1":
            orders = model.load_orders()
            view.show_admin_report(orders)
        elif choice == "2":
            warehouse = model.load_warehouse()
            view.show_warehouse(warehouse)
        elif choice == "3":
            updated_warehouse = model.restock_warehouse(10)
            view.show_message("\nСклад успешно пополнен! Каждой позиции добавлено +10 шт.")
            view.show_warehouse(updated_warehouse)
        elif choice == "0":
            view.show_message("Выход из панели администратора.")
            break
        else:
            view.show_message("Неверный пункт меню, попробуйте снова.")


def run_customer_order():
    guest_count = get_positive_int(
        "Сколько человек будет делать заказ? ",
        "Количество гостей должно быть больше 0"
    )
    final_cart = []
    reserved_ingredients = {}
    all_used_ingredients = []
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
                ingredients = selected_item.get("ingredients", [])

                is_available, missing_item = model.check_ingredients_available(
                    ingredients, reserved_ingredients
                )
                if not is_available:
                    view.show_message(
                        f"К сожалению, блюдо «{selected_item['name']}» недоступно — закончился ингредиент: {missing_item}."
                    )
                    continue

                for ing in ingredients:
                    reserved_ingredients[ing] = reserved_ingredients.get(ing, 0) + 1
                    all_used_ingredients.append(ing)

                final_cart.append({
                    "name": selected_item["name"],
                    "price": selected_item["price"],
                    "category": menu_section["name"]
                })
                total_price += selected_item["price"]
                view.show_message(f"Добавлено: {selected_item['name']}")
            else:
                view.show_message("Неверная позиция меню, попробуйте еще раз")

    if not final_cart:
        view.show_message("\nКорзина пуста. Заказ отменён.")
        return

    pay_method = handle_payment(total_price)
    model.deduct_ingredients(all_used_ingredients)

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
