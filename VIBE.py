#Michael Flaherty
#CIS 261
#WK10  VIBE CODING

from datetime import datetime


class Student:
    def __init__(self, name, student_id, test1, test2, test3):
        self.name = name
        self.student_id = student_id
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = 0.0
        self.grade = ""
        self.calculate_average()
        self.calculate_grade()

    def calculate_average(self):
        self.average = (self.test1 + self.test2 + self.test3) / 3

    def calculate_grade(self):
        if self.average >= 90:
            self.grade = "A"
        elif self.average >= 80:
            self.grade = "B"
        elif self.average >= 70:
            self.grade = "C"
        elif self.average >= 60:
            self.grade = "D"
        else:
            self.grade = "F"

    def to_file_string(self):
        return (
            f"{self.name}|{self.student_id}|"
            f"{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|"
            f"{self.average:.2f}|{self.grade}"
        )

    def __str__(self):
        return (
            f"{self.name:<20} {self.student_id:<12} "
            f"{self.test1:7.2f} {self.test2:7.2f} {self.test3:7.2f} "
            f"{self.average:8.2f} {self.grade:>5}"
        )


def get_student_name():
    name = input("Enter student name (or 'ESC' to finish): ").strip()
    return name


def get_student_id():
    return input("Enter student ID: ").strip()


def get_test_score(test_number):
    while True:
        try:
            score = float(input(f"Enter Test {test_number} score (0-100): "))
            if 0 <= score <= 100:
                return score
            print("Score must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def add_student(students):
    name = get_student_name()
    if name.upper() == "ESC":
        return False

    student_id = get_student_id()
    test1 = get_test_score(1)
    test2 = get_test_score(2)
    test3 = get_test_score(3)

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)

    print("\n" + "-" * 50)
    print("STUDENT RECORD ADDED")
    print("-" * 50)
    print(f"Name     : {student.name}")
    print(f"ID       : {student.student_id}")
    print(f"Test 1   : {student.test1:.2f}")
    print(f"Test 2   : {student.test2:.2f}")
    print(f"Test 3   : {student.test3:.2f}")
    print(f"Average  : {student.average:.2f}")
    print(f"Grade    : {student.grade}")
    print("-" * 50)
    return True


def display_all_students(students):
    print("\n" + "=" * 80)
    print("ALL STUDENT RECORDS")
    print("=" * 80)

    if not students:
        print("No student records found.")
        print("=" * 80)
        return

    header = (
        f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} "
        f"{'Average':>8} {'Grade':>5}"
    )
    print(header)
    print("-" * 80)

    for student in students:
        print(student)

    print("=" * 80)


def display_class_statistics(students):
    print("\n" + "=" * 60)
    print("CLASS STATISTICS")
    print("=" * 60)

    if not students:
        print("No students available to calculate statistics.")
        print("=" * 60)
        return

    averages = [s.average for s in students]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    highest_student = next(s for s in students if s.average == highest)
    lowest_student = next(s for s in students if s.average == lowest)

    print(f"Total Students      : {len(students)}")
    print(f"Class Average       : {class_avg:.2f}")
    print(f"Highest Average     : {highest:.2f} ({highest_student.name})")
    print(f"Lowest Average      : {lowest:.2f} ({lowest_student.name})")
    print("=" * 60)


def search_student_by_name(students):
    if not students:
        print("\nNo student records to search.")
        return

    search_name = input("\nEnter student name to search: ").strip().lower()
    matches = [s for s in students if search_name in s.name.lower()]

    print("\n" + "=" * 80)
    print(f"SEARCH RESULTS FOR: '{search_name}'")
    print("=" * 80)

    if not matches:
        print("No matching students found.")
    else:
        header = (
            f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} "
            f"{'Average':>8} {'Grade':>5}"
        )
        print(header)
        print("-" * 80)
        for student in matches:
            print(student)

    print("=" * 80)


def save_students_to_file(students, filename):
    try:
        with open(filename, "w") as file:
            for student in students:
                file.write(student.to_file_string() + "\n")
        print(f"\nSuccessfully saved {len(students)} student record(s) to '{filename}'.")
    except Exception as e:
        print(f"\nError saving records to file: {e}")


def load_students_from_file(filename):
    students = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    continue
                try:
                    student = Student(
                        name=parts[0],
                        student_id=parts[1],
                        test1=float(parts[2]),
                        test2=float(parts[3]),
                        test3=float(parts[4]),
                    )
                    # Use stored average/grade for consistency
                    student.average = float(parts[5])
                    student.grade = parts[6]
                    students.append(student)
                except (ValueError, IndexError):
                    continue
        print(f"Loaded {len(students)} student record(s) from '{filename}'.")
        return students
    except FileNotFoundError:
        print(f"No existing file '{filename}' found. Starting with empty records.")
        return []
    except Exception as e:
        print(f"Error loading records from file: {e}")
        return []


def display_menu():
    print("\n" + "=" * 60)
    print("STUDENT GRADE CALCULATOR - MENU")
    print("=" * 60)
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. Display Class Statistics")
    print("4. Search Student by Name")
    print("5. Exit (and Save)")
    print("=" * 60)


def main():
    filename = "student_grades.txt"
    print("=" * 60)
    print("WELCOME TO THE STUDENT GRADE CALCULATOR")
    print("=" * 60)

    students = load_students_from_file(filename)

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Add Student(s) ---")
            print("Type 'ESC' for the name when finished adding students.")
            while True:
                if not add_student(students):
                    break
            save_students_to_file(students, filename)

        elif choice == "2":
            display_all_students(students)

        elif choice == "3":
            display_class_statistics(students)

        elif choice == "4":
            search_student_by_name(students)

        elif choice == "5":
            save_students_to_file(students, filename)
            print("\nExiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
