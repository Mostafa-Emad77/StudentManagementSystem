from student import Student, Contact
import logging
import re

class StudentManagementSystem:
    """System for managing student information."""
    
    def __init__(self):
        """Initialize the student management system."""
        self.students = {}
        self.next_id = 1
        # Logging configuration moved to student.py
    
    def get_validated_input(self, prompt, validator, error_message=None):
        """
        Get and validate user input.
        
        Args:
            prompt (str): Input prompt for the user
            validator (callable): Function to validate input
            error_message (str, optional): Custom error message
            
        Returns:
            The validated input
        """
        while True:
            user_input = input(prompt)
            try:
                validated_input = validator(user_input)
                return validated_input
            except ValueError as e:
                print(error_message if error_message else f"Error: {e}")
    
    def validate_name(self, name):
        """Validate student name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if any(char.isdigit() for char in name):
            raise ValueError("Name must not contain numbers")
        return name
    
    def validate_age(self, age_input):
        """Convert and validate age."""
        try:
            age = int(age_input)
            if age <= 0:
                raise ValueError("Age must be a positive integer")
            return age
        except ValueError:
            raise ValueError("Age must be a valid integer")
    
    def validate_grade(self, grade):
        """Validate grade."""
        if not isinstance(grade, str) or not grade.strip():
            raise ValueError("Grade must be a non-empty string")
        return grade
    
    def validate_phone(self, phone):
        """Validate phone number."""
        if len(phone) != 11 or not phone.isdigit():
            raise ValueError("Phone number must be an 11-digit number")
        return phone
    
    def validate_email(self, email):
        """Validate email address."""
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid email address format")
        return email
    
    def add_student(self):
        """Add a new student to the system."""
        try:
            # Get validated inputs
            name = self.get_validated_input("Enter student name: ", self.validate_name)
            age = self.get_validated_input("Enter student age: ", self.validate_age)
            grade = self.get_validated_input("Enter student grade: ", self.validate_grade)
            phone = self.get_validated_input("Enter student phone number (11 digits): ", self.validate_phone)
            email = self.get_validated_input("Enter student email: ", self.validate_email)
            
            # Create contact and student objects
            contact = Contact(phone, email)
            student = Student(self.next_id, name, age, grade, contact)
            
            # Add student to the system
            self.students[self.next_id] = student
            self.next_id += 1
            
            logging.info(f"Added new student: {name} with ID: {student.id}")
            print(f"Student added successfully with ID: {student.id}")
            
        except ValueError as e:
            logging.error(f"Error adding student: {e}")
            print(f"Error: {e}")
    
    def display_student_info(self, student_id):
        """
        Display information for a specific student.
        
        Args:
            student_id (int): ID of the student to display
        """
        if student_id in self.students:
            student = self.students[student_id]
            details = student.get_details()
            
            print("\nStudent Information:")
            print(f"ID: {details['id']}")
            print(f"Name: {details['name']}")
            print(f"Age: {details['age']}")
            print(f"Grade: {details['grade']}")
            
            if details['contact']:
                print("\nContact Information:")
                print(f"Phone: {details['contact']['phone']}")
                print(f"Email: {details['contact']['email']}")
        else:
            logging.warning(f"Student not found with ID: {student_id}")
            print("Student not found.")
    
    def update_student_details(self, student_id):
        """
        Update details for a specific student.
        
        Args:
            student_id (int): ID of the student to update
        """
        if student_id in self.students:
            try:
                # Get validated inputs
                name = self.get_validated_input("Enter updated name: ", self.validate_name)
                age = self.get_validated_input("Enter updated age: ", self.validate_age)
                grade = self.get_validated_input("Enter updated grade: ", self.validate_grade)
                phone = self.get_validated_input("Enter updated phone number (11 digits): ", self.validate_phone)
                email = self.get_validated_input("Enter updated email: ", self.validate_email)
                
                # Create contact object and update details
                contact = Contact(phone, email)
                details = {
                    'name': name,
                    'age': age,
                    'grade': grade,
                    'contact': contact
                }
                
                self.students[student_id].update_details(details)
                print("Student details updated successfully.")
                
            except (ValueError, TypeError) as e:
                logging.error(f"Error updating student: {e}")
                print(f"Error: {e}")
        else:
            logging.warning(f"Student not found with ID: {student_id}")
            print("Student not found.")
    
    def list_all_students(self):
        """Display a list of all students in the system."""
        if not self.students:
            print("No students in the system.")
            return
        
        print("\nAll Students:")
        print("-" * 50)
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Grade':<10}")
        print("-" * 50)
        
        for student_id, student in self.students.items():
            details = student.get_details()
            print(f"{details['id']:<5} {details['name']:<20} {details['age']:<5} {details['grade']:<10}")
    
    def delete_student(self, student_id):
        """
        Delete a student from the system.
        
        Args:
            student_id (int): ID of the student to delete
        """
        if student_id in self.students:
            student_name = self.students[student_id].name
            del self.students[student_id]
            logging.info(f"Deleted student: {student_name} with ID: {student_id}")
            print(f"Student {student_name} deleted successfully.")
        else:
            logging.warning(f"Student not found with ID: {student_id}")
            print("Student not found.")


def get_integer_input(prompt):
    """Get and validate integer input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def main():
    """Main function to run the student management system."""
    sms = StudentManagementSystem()
    
    while True:
        print("\nStudent Management System")
        print("=" * 30)
        print("1. Add New Student")
        print("2. Display Student Information")
        print("3. Update Student Details")
        print("4. List All Students")
        print("5. Delete Student")
        print("6. Exit")
        print("=" * 30)
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            sms.add_student()
            
        elif choice == '2':
            student_id = get_integer_input("Enter student ID: ")
            sms.display_student_info(student_id)
            
        elif choice == '3':
            student_id = get_integer_input("Enter student ID: ")
            sms.update_student_details(student_id)
            
        elif choice == '4':
            sms.list_all_students()
            
        elif choice == '5':
            student_id = get_integer_input("Enter student ID: ")
            sms.delete_student(student_id)
            
        elif choice == '6':
            logging.info("Exiting program...")
            print("Thank you for using the Student Management System. Goodbye!")
            break
            
        else:
            logging.warning("Invalid choice.")
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
