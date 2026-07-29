import csv
import os

# Global Variables
students = []
next_id = 1

FILE_NAME = "students.csv"

SUBJECTS = [
    "Math",
    "Physics",
    "English",
    "Computer",
    "Urdu"
]

PASS_MARK = 50


# Helper Functions

def line():
    print("-" * 90)


def title(text):
    line()
    print(text.center(90))
    line()


def pause():
    input("\nPress Enter to continue...")


def get_next_id():
    global next_id

    current = next_id
    next_id += 1

    return current


# Input Validation

def get_student_name():

    while True:

        name = input("Enter Student Name: ").strip()

        if name == "":
            print("Name cannot be empty.")
            continue

        duplicate = False

        for student in students:

            if student["name"].lower() == name.lower():
                duplicate = True
                break

        if duplicate:
            print("Student already exists.")
            continue

        return name


def get_grade(subject):

    while True:

        try:

            grade = float(input(f"{subject}: "))

            if 0 <= grade <= 100:
                return grade

            print("Grade must be between 0 and 100.")

        except ValueError:
            print("Enter numbers only.")


def calculate_average(grades):

    total = sum(grades.values())
    average = total / len(grades)

    return average


def get_status(average):

    if average >= PASS_MARK:
        return "PASS"

    return "FAIL"


# Display Functions

def display_table_header():

    print(f"{'ID':<5}{'NAME':<20}", end="")

    for subject in SUBJECTS:
        print(f"{subject[:5]:<8}", end="")

    print(f"{'AVG':<8}{'STATUS'}")

    line()


# Save to CSV

def save_to_csv():

    try:

        with open(FILE_NAME, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(["ID", "Name"] + SUBJECTS)

            for student in students:

                row = [
                    student["id"],
                    student["name"]
                ]

                for subject in SUBJECTS:
                    row.append(student["grades"][subject])

                writer.writerow(row)

        print("\nStudents saved successfully.")

    except Exception as error:

        print("Error while saving.")
        print(error)


# Load From CSV

def load_from_csv():

    global next_id

    if not os.path.exists(FILE_NAME):
        return

    try:

        with open(FILE_NAME, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                grades = {}

                for subject in SUBJECTS:
                    grades[subject] = float(row[subject])

                student = {
                    "id": int(row["ID"]),
                    "name": row["Name"],
                    "grades": grades
                }

                students.append(student)

                if student["id"] >= next_id:
                    next_id = student["id"] + 1

        print(f"Loaded {len(students)} student(s).")

    except Exception as error:

        print("Error while loading.")
        print(error)

# Add Student

def add_student():

    title("ADD NEW STUDENT")

    name = get_student_name()

    grades = {}

    print(f"\nEnter grades for {name}\n")

    for subject in SUBJECTS:

        grades[subject] = get_grade(subject)

    student = {
        "id": get_next_id(),
        "name": name,
        "grades": grades
    }

    students.append(student)

    average = calculate_average(grades)
    status = get_status(average)

    print("\nStudent Added Successfully!")
    print(f"ID      : {student['id']}")
    print(f"Name    : {student['name']}")
    print(f"Average : {average:.2f}")
    print(f"Status  : {status}")

    pause()


# View All Students

def view_all_students():

    title("ALL STUDENTS")

    if not students:
        print("No students available.")
        pause()
        return

    display_table_header()

    for student in students:

        average = calculate_average(student["grades"])
        status = get_status(average)

        print(
            f"{student['id']:<5}"
            f"{student['name']:<20}",
            end=""
        )

        for subject in SUBJECTS:

            print(
                f"{student['grades'][subject]:<8.1f}",
                end=""
            )

        print(
            f"{average:<8.2f}"
            f"{status}"
        )

    line()

    print(f"Total Students : {len(students)}")

    pause()


# Search Student

def search_student():

    title("SEARCH STUDENT")

    if not students:
        print("No students available.")
        pause()
        return

    name = input("Enter Student Name: ").strip().lower()

    found = False

    for student in students:

        if student["name"].lower() == name:

            found = True

            average = calculate_average(student["grades"])
            status = get_status(average)

            print("\nStudent Found\n")

            print(f"ID      : {student['id']}")
            print(f"Name    : {student['name']}")

            line()

            for subject, grade in student["grades"].items():
                print(f"{subject:<12}: {grade}")

            line()

            print(f"Average : {average:.2f}")
            print(f"Status  : {status}")

            break

    if not found:
        print("\nStudent not found.")

    pause()

# Edit Grades


def edit_grades():

    title("EDIT STUDENT GRADES")

    if not students:
        print("No students available.")
        pause()
        return

    view_all_students()

    while True:

        try:
            student_id = int(input("\nEnter Student ID: "))
            break
        except ValueError:
            print("Enter a valid ID.")

    student_found = None

    for student in students:

        if student["id"] == student_id:
            student_found = student
            break

    if student_found is None:
        print("Student not found.")
        pause()
        return

    print(f"\nEditing Grades for {student_found['name']}")

    line()

    for index, subject in enumerate(SUBJECTS, start=1):
        print(f"{index}. {subject}")

    line()

    while True:

        try:

            choice = int(input("Select Subject: "))

            if 1 <= choice <= len(SUBJECTS):
                break

            print("Choose a valid option.")

        except ValueError:
            print("Enter numbers only.")

    subject = SUBJECTS[choice - 1]

    print(f"\nCurrent Grade : {student_found['grades'][subject]}")

    new_grade = get_grade(subject)

    student_found["grades"][subject] = new_grade

    print("\nGrade updated successfully.")

    average = calculate_average(student_found["grades"])

    print(f"New Average : {average:.2f}")
    print(f"Status      : {get_status(average)}")

    pause()


# Delete Student

def delete_student():

    title("DELETE STUDENT")

    if not students:
        print("No students available.")
        pause()
        return

    view_all_students()

    while True:

        try:
            student_id = int(input("\nEnter Student ID: "))
            break
        except ValueError:
            print("Enter numbers only.")

    for student in students:

        if student["id"] == student_id:

            confirm = input(
                f"Delete {student['name']}? (Y/N): "
            ).strip().upper()

            if confirm == "Y":

                students.remove(student)

                print("Student deleted successfully.")

            else:

                print("Deletion cancelled.")

            pause()
            return

    print("Student ID not found.")

    pause()


# Class Report

def class_report():

    title("CLASS REPORT")

    if not students:
        print("No students available.")
        pause()
        return

    ranked = []

    for student in students:

        average = calculate_average(student["grades"])

        ranked.append({
            "name": student["name"],
            "average": average
        })

    ranked.sort(
        key=lambda student: student["average"],
        reverse=True
    )

    averages = []

    for student in ranked:
        averages.append(student["average"])

    class_average = sum(averages) / len(averages)

    highest = max(averages)
    lowest = min(averages)

    passed = 0

    for average in averages:

        if average >= PASS_MARK:
            passed += 1

    failed = len(students) - passed

    print(f"Total Students : {len(students)}")
    print(f"Class Average  : {class_average:.2f}")
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average : {lowest:.2f}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {failed}")

    line()

    print("RANKINGS")

    line()

    rank = 1

    for student in ranked:

        print(
            f"{rank}. "
            f"{student['name']:<20}"
            f"{student['average']:.2f}"
        )

        rank += 1

    pause()


# Main Menu

def show_menu():

    title("STUDENT GRADE MANAGEMENT SYSTEM")

    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Edit Student Grades")
    print("5. Delete Student")
    print("6. Class Report")
    print("7. Save Students")
    print("8. Exit")

    line()


# Main Function

def main():

    load_from_csv()

    while True:

        show_menu()

        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":

            add_student()

        elif choice == "2":

            view_all_students()

        elif choice == "3":

            search_student()

        elif choice == "4":

            edit_grades()

        elif choice == "5":

            delete_student()

        elif choice == "6":

            class_report()

        elif choice == "7":

            save_to_csv()

            pause()

        elif choice == "8":

            save_to_csv()

            print("\nStudents saved successfully.")
            print("Thank you for using Student Grade Management System.")

            break

        else:

            print("\nInvalid choice.")
            print("Please select between 1 and 8.")

            pause()


# Program Entry Point

if __name__ == "__main__":
    main()