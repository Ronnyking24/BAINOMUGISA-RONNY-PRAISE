def get_positive_float(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if number > 0:
                return number
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Enter a numeric value.")


def get_positive_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number > 0:
                return number
            print("Please enter an integer greater than zero.")
        except ValueError:
            print("Invalid input. Enter a whole number.")


def get_tip_percentage():
    options = {"1": 0.10, "2": 0.15, "3": 0.20, "4": None}
    print("Tip options:")
    print("  1. 10%")
    print("  2. 15%")
    print("  3. 20%")
    print("  4. Custom")

    while True:
        choice = input("Choose a tip option (1-4): ").strip()
        if choice in options:
            if options[choice] is not None:
                return options[choice]
            else:
                custom = get_positive_float("Enter custom tip percentage: ")
                return custom / 100
        print("Invalid choice. Please select 1, 2, 3, or 4.")


def calculate_bill_split(total_bill, people, tip_rate):
    tip_amount = total_bill * tip_rate
    total_with_tip = total_bill + tip_amount
    per_person = total_with_tip / people
    return tip_amount, total_with_tip, per_person


def print_receipt(total_bill, tip_rate, tip_amount, total_with_tip, per_person, people):
    print("\n--- Bill Split Receipt ---")
    print(f"Bill amount:        ${total_bill:,.2f}")
    print(f"Tip percentage:      {tip_rate * 100:.0f}%")
    print(f"Tip amount:         ${tip_amount:,.2f}")
    print(f"Total with tip:     ${total_with_tip:,.2f}")
    print(f"Number of people:    {people}")
    print(f"Amount per person:  ${per_person:,.2f}")
    print("--------------------------\n")


def main():
    print("Bill Split Calculator")
    total_bill = get_positive_float("Enter the total bill amount: ")
    people = get_positive_int("Enter the number of people: ")
    tip_rate = get_tip_percentage()

    tip_amount, total_with_tip, per_person = calculate_bill_split(total_bill, people, tip_rate)
    print_receipt(total_bill, tip_rate, tip_amount, total_with_tip, per_person, people)


if __name__ == "__main__":
    main()
