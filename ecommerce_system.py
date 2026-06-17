users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "cashier": {"password": "cashier123", "role": "Cashier"},
    "customer": {"password": "customer123", "role": "Customer"}
}

coupon_discounts = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
    "SAVE30": 0.30
}

tax_rates = {
    "UG": 0.18,
    "US": 0.08,
    "EU": 0.20,
    "OTHER": 0.15
}


def get_tax_rate(location):
    location = location.upper().strip()
    if location in tax_rates:
        return tax_rates[location]
    return tax_rates["OTHER"]


def get_coupon_discount(code):
    code = code.upper().strip()
    if code in coupon_discounts:
        return coupon_discounts[code]
    return 0.0


def get_subtotal_discount(subtotal):
    if subtotal >= 1000:
        return 0.10
    if subtotal >= 500:
        return 0.07
    if subtotal >= 200:
        return 0.05
    return 0.0


def calculate_final_price(subtotal, coupon_code, location):
    if subtotal < 0:
        raise ValueError("Subtotal must be zero or positive.")

    coupon_discount = get_coupon_discount(coupon_code)
    subtotal_discount = get_subtotal_discount(subtotal)

    discount_amount = subtotal * (coupon_discount + subtotal_discount)
    discounted_total = subtotal - discount_amount

    tax_rate = get_tax_rate(location)
    tax_amount = discounted_total * tax_rate
    final_total = discounted_total + tax_amount

    return {
        "subtotal": subtotal,
        "coupon_discount": coupon_discount,
        "subtotal_discount": subtotal_discount,
        "discount_amount": discount_amount,
        "discounted_total": discounted_total,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "final_total": final_total
    }


def login_system():
    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in users and users[username]["password"] == password:
            print(f"Login successful. Role: {users[username]['role']}")
            return users[username]["role"]

        attempts += 1
        print("Invalid credentials. Try again.")

    print("Maximum login attempts reached. Access denied.")
    return None


def order_menu(role):
    print("\nOrder processing")
    subtotal = float(input("Enter product subtotal: "))
    coupon_code = input("Enter coupon code (or press Enter if none): ").strip()
    location = input("Enter location code (UG, US, EU, OTHER): ").strip()

    result = calculate_final_price(subtotal, coupon_code, location)
    print("\n--- Price Summary ---")
    print(f"Subtotal: {result['subtotal']:.2f}")

    if result['coupon_discount'] > 0:
        print(f"Coupon discount: {result['coupon_discount'] * 100:.0f}%")
    else:
        if coupon_code:
            print("Coupon code is invalid or not applicable.")
        else:
            print("No coupon code used.")

    if result['subtotal_discount'] > 0:
        print(f"Subtotal discount: {result['subtotal_discount'] * 100:.0f}%")
    else:
        print("No subtotal discount applied.")

    print(f"Discount amount: {result['discount_amount']:.2f}")
    print(f"Total after discount: {result['discounted_total']:.2f}")
    print(f"Tax rate: {result['tax_rate'] * 100:.0f}%")
    print(f"Tax amount: {result['tax_amount']:.2f}")
    print(f"Final price: {result['final_total']:.2f}")
    print("---------------------\n")


def main():
    role = login_system()
    if role is None:
        return

    if role == "Admin":
        while True:
            print("1. Process order")
            print("2. Show users")
            print("3. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                order_menu(role)
            elif choice == "2":
                print("\nRegistered users:")
                for name, info in users.items():
                    print(f"- {name}: {info['role']}")
                print()
            elif choice == "3":
                break
            else:
                print("Invalid option.")

    elif role == "Cashier":
        order_menu(role)

    else:
        print("Customer access: You can calculate the final price for a purchase.")
        order_menu(role)


if __name__ == "__main__":
    main()
