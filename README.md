# Student Management System

A comprehensive student management system with both command-line and graphical user interfaces, built with Python.

## Features

- **Student Management**
  - Add, edit, view, and delete student records
  - Store student details: name, age, grade
  - Comprehensive input validation

- **Contact Information**
  - Store phone numbers and email addresses
  - Validation for phone (11 digits) and email formats

- **Attendance Tracking**
  - Mark students present/absent
  - View attendance history
  - Generate attendance reports

- **Reporting**
  - Student list reports
  - Attendance summary reports
  - Grade distribution analysis
  - Age distribution analysis

- **Data Management**
  - Import/export student data to CSV
  - Export reports to CSV or text
  - Automatic logging of system activities

- **User Interfaces**
  - Command-line interface (CLI) for basic operations
  - Graphical user interface (GUI) with Tkinter for full functionality

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/student-management-system.git
   cd student-management-system
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   (Note: If there's no requirements.txt, install manually:)
   ```bash
   pip install pillow
   ```

## Usage

### Command Line Interface
Run the CLI version:
```bash
python main.py
```

The CLI provides a menu-driven interface for:
- Adding new students
- Viewing student information
- Updating student details
- Listing all students
- Deleting students

### Graphical User Interface
Run the GUI version:
```bash
python gui.py
```

The GUI provides tabs for:
- **Dashboard**: System overview and quick actions
- **Add Student**: Form for adding new students
- **View Students**: Browse and search student records
- **Attendance**: Track student attendance
- **Reports**: Generate various reports

## Screenshots

(Describe the main interface components since we can't include actual images)

- **Main Dashboard**: Shows system statistics and quick access buttons
- **Add Student Form**: Form fields for student details and contact information
- **Student List**: Table view of all students with search functionality
- **Attendance Tracking**: Interface to mark students present/absent by date
- **Report Generation**: Panel to create and export various reports

## Dependencies

- Python 3.x
- Tkinter (usually included with Python)
- Pillow (for image handling in GUI)
- Standard Python libraries: os, csv, datetime, re, logging

