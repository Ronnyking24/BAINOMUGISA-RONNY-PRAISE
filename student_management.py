import csv
import json
import logging
import os
from datetime import datetime

CSV_FILE = "students.csv"
JSON_FILE = "students.json"
LOG_FILE = "student_system.log"

# Custom exception for missing student records
class StudentNotFoundError(Exception):
    pass


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def ensure_data_files_exist():
    """Create the CSV and JSON files if they do not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["registration_number", "first_name", "last_name", "email"])
            writer.writeheader()
        logging.info("Created missing CSV file: %s", CSV_FILE)

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, mode="w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)
        logging.info("Created missing JSON file: %s", JSON_FILE)


def load_csv_students():
    """Load the student list from the CSV file."""
    students = []
    try:
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        logging.error("CSV file not found when loading students.")
        ensure_data_files_exist()
    return students


def load_json_details():
    """Load student details from the JSON file."""
    try:
        with open(JSON_FILE, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.error("Failed to read JSON details; initializing empty details.")
        return {}


def save_csv_students(students):
    """Save the student list to the CSV file."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["registration_number", "first_name", "last_name", "email"])
        writer.writeheader()
        writer.writerows(students)
    logging.info("Saved %d student records to %s.", len(students), CSV_FILE)


def save_json_details(details):
    """Save student details to the JSON file."""
    with open(JSON_FILE, mode="w", encoding="utf-8") as file:
        json.dump(details, file, indent=4)
    logging.info("Saved student details for %d records to %s.", len(details), JSON_FILE)


def find_student_by_registration(registration_number):
    """Return a combined student record for the given registration number."""
    students = load_csv_students()
    details = load_json_details()
    for student in students:
        if student["registration_number"] == registration_number:
            merged = {
                **student,
                **details.get(registration_number, {
                    "address": "",
                    "contact": "",
                    "program": "",
                }),
            }
            return merged
    return None


def validate_registration_number(registration_number):
    """Validate registration number format."""
    if not registration_number or not registration_number.strip():
        raise ValueError("Registration number cannot be empty.")
    if not registration_number.strip().isalnum():
        raise ValueError("Registration number must be alphanumeric without spaces.")
    return registration_number.strip().upper()


def validate_non_empty(value, field_name):
    """Validate that a value is not empty."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_email(email):
    """Validate a simple email address format."""
    email = validate_non_empty(email, "Email")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Please enter a valid email address.")
    return email


def validate_contact(contact):
    """Validate contact information."""
    contact = validate_non_empty(contact, "Contact")
    digits = [c for c in contact if c.isdigit()]
    if len(digits) < 7:
        raise ValueError("Contact must contain at least 7 digits.")
    return contact


def get_input(prompt_text, validator=None, field_name=None):
    """Read user input and validate it with the provided validator."""
    try:
        value = input(prompt_text).strip()
        if validator:
            return validator(value) if field_name is None else validator(value, field_name)
        return value
    except ValueError as error:
        print(f"Input error: {error}")
        logging.warning("Input validation failed for %s: %s", prompt_text, error)
        return None


def add_student():
    """Add a new student record to the system."""
    print("\n--- Add New Student ---")
    registration_number = None
    while registration_number is None:
        registration_input = get_input("Enter registration number: ", validate_registration_number)
        if registration_input:
            existing_student = find_student_by_registration(registration_input)
            if existing_student:
                print("A student with this registration number already exists.")
                logging.warning("Attempted to add duplicate registration number: %s", registration_input)
            else:
                registration_number = registration_input

    student = {}
    student["registration_number"] = registration_number
    student["first_name"] = get_input("Enter first name: ", validate_non_empty, "First name")
    student["last_name"] = get_input("Enter last name: ", validate_non_empty, "Last name")
    student["email"] = get_input("Enter email address: ", validate_email)

    additional_details = {}
    additional_details["address"] = get_input("Enter address: ", validate_non_empty, "Address")
    additional_details["contact"] = get_input("Enter contact number: ", validate_contact)
    additional_details["program"] = get_input("Enter program of study: ", validate_non_empty, "Program")

    if not all(student.values()) or not all(additional_details.values()):
        print("Student record was not saved because one or more fields are invalid.")
        logging.info("Add student aborted due to invalid input.")
        return

    students = load_csv_students()
    details = load_json_details()
    students.append(student)
    details[registration_number] = additional_details

    save_csv_students(students)
    save_json_details(details)
    print("Student added successfully.")
    logging.info("Added student record: %s", registration_number)


def view_all_students():
    """Display all students stored in the system."""
    print("\n--- View All Students ---")
    students = load_csv_students()
    details = load_json_details()
    if not students:
        print("No students are currently registered.")
        logging.info("Viewed students: none found.")
        return

    for student in students:
        reg_no = student["registration_number"]
        extra = details.get(reg_no, {})
        print(f"Registration: {reg_no}")
        print(f"Name: {student['first_name']} {student['last_name']}")
        print(f"Email: {student['email']}")
        print(f"Program: {extra.get('program', 'N/A')}")
        print(f"Contact: {extra.get('contact', 'N/A')}")
        print(f"Address: {extra.get('address', 'N/A')}")
        print("-" * 40)
    logging.info("Displayed all students (%d records).", len(students))


def search_student():
    """Search for a student by registration number."""
    print("\n--- Search Student ---")
    registration_number = get_input("Enter registration number to search: ", validate_registration_number)
    if not registration_number:
        return

    try:
        student = find_student_by_registration(registration_number)
        if student is None:
            raise StudentNotFoundError(f"Student {registration_number} not found.")

        print(f"\nRegistration: {student['registration_number']}")
        print(f"Name: {student['first_name']} {student['last_name']}")
        print(f"Email: {student['email']}")
        print(f"Program: {student.get('program', 'N/A')}")
        print(f"Contact: {student.get('contact', 'N/A')}")
        print(f"Address: {student.get('address', 'N/A')}")
        logging.info("Searched student record: %s", registration_number)
    except StudentNotFoundError as error:
        print(error)
        logging.warning("Search failed: %s", error)


def update_student():
    """Update an existing student's information."""
    print("\n--- Update Student ---")
    registration_number = get_input("Enter registration number to update: ", validate_registration_number)
    if not registration_number:
        return

    student = find_student_by_registration(registration_number)
    if student is None:
        print("Student not found.")
        logging.warning("Update failed; student not found: %s", registration_number)
        return

    print("Leave a field blank to keep the current value.")
    new_first_name = input(f"First name [{student['first_name']}]: ").strip() or student["first_name"]
    new_last_name = input(f"Last name [{student['last_name']}]: ").strip() or student["last_name"]
    new_email = input(f"Email [{student['email']}]: ").strip() or student["email"]
    new_address = input(f"Address [{student.get('address', '')}]: ").strip() or student.get("address", "")
    new_contact = input(f"Contact [{student.get('contact', '')}]: ").strip() or student.get("contact", "")
    new_program = input(f"Program [{student.get('program', '')}]: ").strip() or student.get("program", "")

    try:
        student["first_name"] = validate_non_empty(new_first_name, "First name")
        student["last_name"] = validate_non_empty(new_last_name, "Last name")
        student["email"] = validate_email(new_email)
        student["address"] = validate_non_empty(new_address, "Address")
        student["contact"] = validate_contact(new_contact)
        student["program"] = validate_non_empty(new_program, "Program")
    except ValueError as error:
        print(f"Update failed: {error}")
        logging.warning("Update validation failed for %s: %s", registration_number, error)
        return

    students = load_csv_students()
    details = load_json_details()
    for entry in students:
        if entry["registration_number"] == registration_number:
            entry["first_name"] = student["first_name"]
            entry["last_name"] = student["last_name"]
            entry["email"] = student["email"]
            break

    details[registration_number] = {
        "address": student["address"],
        "contact": student["contact"],
        "program": student["program"],
    }

    save_csv_students(students)
    save_json_details(details)
    print("Student record updated successfully.")
    logging.info("Updated student record: %s", registration_number)


def delete_student():
    """Delete a student record from both CSV and JSON storage."""
    print("\n--- Delete Student ---")
    registration_number = get_input("Enter registration number to delete: ", validate_registration_number)
    if not registration_number:
        return

    students = load_csv_students()
    details = load_json_details()
    updated_students = [s for s in students if s["registration_number"] != registration_number]

    if len(updated_students) == len(students):
        print("Student not found.")
        logging.warning("Delete failed; student not found: %s", registration_number)
        return

    if registration_number in details:
        del details[registration_number]

    save_csv_students(updated_students)
    save_json_details(details)
    print("Student deleted successfully.")
    logging.info("Deleted student record: %s", registration_number)


def display_menu():
    """Show the main menu and return the selected option."""
    print("\nStudent Record Management System")
    print("1. Add a new student")
    print("2. View all students")
    print("3. Search for a student")
    print("4. Update student details")
    print("5. Delete a student record")
    print("6. Exit")
    try:
        return input("Choose an option (1-6): ").strip()
    except EOFError:
        print("\nNo input available. Exiting.")
        logging.info("No input available at menu prompt; exiting.")
        return "6"


def main():
    setup_logging()
    ensure_data_files_exist()
    print("Welcome to the Student Record Management System.")
    logging.info("Application started.")

    try:
        while True:
            choice = display_menu()
            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                print("Exiting the system. Goodbye.")
                logging.info("Application exited by user.")
                break
            else:
                print("Invalid choice. Please select an option between 1 and 6.")
                logging.warning("Invalid menu choice entered: %s", choice)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        logging.info("Application interrupted by user.")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
        logging.exception("Unexpected error in main loop.")
    finally:
        print("Thank you for using the Student Record Management System.")
        logging.info("Application shutdown completed.")


if __name__ == "__main__":
    main()
