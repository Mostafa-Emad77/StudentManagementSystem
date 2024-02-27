from student import Student, Contact
import re
import logging

class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.next_id = 1
        logging.basicConfig(filename='student_management.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def add_student(self):
        while True:
            try:
                name = input("Enter student name: ")
                if not isinstance(name, str) or not name.strip():
                    raise ValueError("Name must be a non-empty string")
                if any(char.isdigit() for char in name):
                    raise ValueError("Name must not contain numbers")

                while True:
                    age_input = input("Enter student age: ")
                    try:
                        age = int(age_input)
                        break  
                    except ValueError:
                        print("Invalid age. Please enter a valid integer.")
                
                while True:
                    grade = input("Enter student grade: ")
                    if not isinstance(grade, str) or not grade.strip():
                        raise ValueError("Grade must be a non-empty string")
                    break
                while True: 
                    phone = input("Enter student phone number (11 digits): ")
                    if len(phone) != 11 or not phone.isdigit():
                        print("Invalid phone number. Please enter a valid 11-digit number.")
                    else:
                        break
                    
                while True:
                    email = input("Enter student email: ")
                    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                        print("Invalid email address format. Please enter a valid email address.")
                    else:
                        break
                
                contact = Contact(phone, email)
                student = Student(self.next_id, name, age, grade, contact)
                self.students[self.next_id] = student
                self.next_id += 1 
                contact = Contact(phone, email)
                student = Student(name, age, grade, contact)
                self.students[student.name] = student
                logging.info(f"Added new student: {student.name}")
                print("Student added.")
                break
            except ValueError as e:
                logging.error(f"Error adding student: {e}")
                print(f"Error: {e}")
                print("Please try again.\n")
    
    def display_student_info(self, student_id):
        if student_id in self.students:
            student = self.students[student_id]
            details = student.get_details()
            print("Student Information:")
            for key, value in details.items():
                if key == 'contact':
                    print("Contact Information:")
                    for k, v in value.items():
                        print(f"{k}: {v}")
                else:
                    print(f"{key}: {value}")
        else:
            logging.warning(f"Student not found with ID: {student_id}")
            print("Student not found.")

    def update_student_details(self, student_id, details):
        if student_id in self.students:
            student = self.students[student_id]
            try:
                student.update_details(details)
                logging.info(f"Updated details for student with ID: {student_id}")
                print("Student details updated successfully.")
            except ValueError as e:
                logging.error(f"Error updating details: {e}")
                print(f"Error: {e}")
        else:
            logging.warning(f"Student not found with ID: {student_id}")
            print("Student not found.")



def main():
    sms = StudentManagementSystem()

    while True:
        print("\nMenu:")
        print("1. Add New Student")
        print("2. Display Student Information")
        print("3. Update Student Details")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            sms.add_student()

        elif choice == '2':
            student_id = int(input("Enter student ID: "))
            sms.display_student_info(student_id)

        elif choice == '3':
            student_id = int(input("Enter student ID: "))
            if student_id in sms.students:
                details = {}
                details['name'] = input("Enter updated name: ")
                details['age'] = int(input("Enter updated age: "))
                details['grade'] = input("Enter updated grade: ")
                phone = input("Enter updated phone number (11 digits): ")
                email = input("Enter updated email: ")
                contact = Contact(phone, email)
                details['contact'] = contact
                sms.update_student_details(student_id, details)
            else:
                logging.warning(f"Student not found with ID: {student_id}")
                print("Student not found.")

        elif choice == '4':
            logging.info("Exiting program...")
            print("Exiting program...")
            break

        else:
            logging.warning("Invalid choice.")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
