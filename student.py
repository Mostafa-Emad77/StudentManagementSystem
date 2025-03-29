import re
import logging

# Single logging configuration
logging.basicConfig(filename='student_management.log', level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class Contact:
    """Class representing contact information for a student."""
    
    def __init__(self, phone, email):
        """
        Initialize a Contact object with phone and email.
        
        Args:
            phone (str): Student's phone number (must be 11 digits)
            email (str): Student's email address
        
        Raises:
            ValueError: If phone or email format is invalid
        """
        self.validate_phone(phone)
        self.validate_email(email)
        self.phone = phone
        self.email = email
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        if not isinstance(phone, str) or len(phone) != 11 or not phone.isdigit():
            raise ValueError("Phone number must be an 11-digit number")
    
    @staticmethod
    def validate_email(email):
        """Validate email address format."""
        if not isinstance(email, str) or not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValueError("Invalid email address format")
    
    def update_details(self, phone, email):
        """
        Update contact details.
        
        Args:
            phone (str): New phone number
            email (str): New email address
            
        Raises:
            ValueError: If phone or email format is invalid
        """
        self.validate_phone(phone)
        self.validate_email(email)
        self.phone = phone
        self.email = email
    
    def get_details(self):
        """Return contact details as a dictionary."""
        return {"phone": self.phone, "email": self.email}


class Student:
    """Class representing a student in the management system."""
    
    def __init__(self, student_id, name, age, grade, contact=None):
        """
        Initialize a Student object.
        
        Args:
            student_id (int): Unique identifier for the student
            name (str): Student's name
            age (int): Student's age
            grade (str): Student's grade
            contact (Contact, optional): Student's contact information
            
        Raises:
            ValueError: If any input is invalid
        """
        self.validate_id(student_id)
        self.validate_name(name)
        self.validate_age(age)
        self.validate_grade(grade)
        
        self.id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.contact = contact
    
    @staticmethod
    def validate_id(student_id):
        """Validate student ID."""
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer")
    
    @staticmethod
    def validate_name(name):
        """Validate student name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if any(char.isdigit() for char in name):
            raise ValueError("Name must not contain numbers")
    
    @staticmethod
    def validate_age(age):
        """Validate student age."""
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer")
    
    @staticmethod
    def validate_grade(grade):
        """Validate student grade."""
        if not isinstance(grade, str) or not grade.strip():
            raise ValueError("Grade must be a non-empty string")
    
    def update_details(self, details):
        """
        Update student details.
        
        Args:
            details (dict): Dictionary containing updated student information
                Required keys: 'name', 'age', 'grade'
                Optional keys: 'contact'
                
        Raises:
            ValueError: If required keys are missing or values are invalid
            TypeError: If contact is not a Contact object
        """
        try:
            if not all(k in details for k in ['name', 'age', 'grade']):
                raise ValueError('Missing required details (name, age, grade)')
            
            self.validate_name(details['name'])
            self.validate_age(details['age'])
            self.validate_grade(details['grade'])
            
            self.name = details['name']
            self.age = details['age']
            self.grade = details['grade']
            
            if 'contact' in details:
                contact = details['contact']
                if not isinstance(contact, Contact):
                    raise TypeError("Contact must be a Contact object")
                self.contact = contact
                
            logging.info(f"Updated details for student ID: {self.id}")
        except (ValueError, TypeError) as e:
            logging.error(f"Error updating details: {e}")
            raise
    
    def get_details(self):
        """Return student details as a dictionary."""
        details = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "contact": self.contact.get_details() if self.contact else None
        }
        return details
