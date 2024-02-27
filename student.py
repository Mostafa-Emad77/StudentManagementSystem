import re
import logging

logging.basicConfig(filename='student_management.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Contact:
    def __init__(self, phone, email):
        self.phone = phone
        self.email = email

    def update_details(self, phone, email):
        self.phone = phone
        self.email = email

    def get_details(self):
        return {"phone": self.phone, "email": self.email}


class Student:
    def __init__(self,ID, name, age, grade, contact=None):
        self.ID = ID
        self.name = name
        self.age = age
        self.grade = grade
        self.contact = contact

    def update_details(self, details):
        try:
            if not all(k in details for k in ['name', 'age', 'grade']):
                logging.error('Invalid details')
                raise ValueError('Invalid details')

            self.name = details['name']
            self.age = details['age']
            self.grade = details['grade']

            if 'contact' in details:
                contact = details['contact']
                if not isinstance(contact, Contact):
                    logging.error("Contact must be a Contact object")
                    raise TypeError("Contact must be a Contact object")
                self.contact = contact
        except (ValueError, TypeError) as e:
            logging.error(f"Error updating details: {e}")
            print(f"Error: {e}")

    def get_details(self):
        details = {
            "ID": self.ID,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "contact": self.contact.get_details() if self.contact else None
        }
        return details
