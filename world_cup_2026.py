import random

teams = [
    "Portugal",
    "Argentina",
    "Brazil",
    "England",
    "France",
    "Germany",
    "Spain"
]


def print_menu():
    print("World Cup 2026 Winner Simulator")
    print("=" * 40)
    print("1. Show participating teams")
    print("2. Simulate winner")
    print("3. Exit")


def show_teams():
    print("\nParticipating teams:")
    for index, team in enumerate(teams, start=1):
        print(f"  {index}. {team}")
    print()


def simulate_winner():
    winner = random.choice(teams)
    print("\nSimulating the World Cup 2026 champion...")
    print(f"The winner is: {winner} \U0001F3C6")
    print()


def main():
    while True:
        print_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            show_teams()
        elif choice == "2":
            simulate_winner()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
