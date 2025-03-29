import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime
from student import Student, Contact
import logging
import re
from PIL import Image, ImageTk  # You'll need to install Pillow: pip install Pillow

class StudentManagementGUI:
    """GUI for the Student Management System."""
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize student data
        self.students = {}
        self.next_id = 1
        self.attendance_records = {}
        self.current_student_id = None
        self.student_photos = {}
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.add_student_frame = ttk.Frame(self.notebook)
        self.view_students_frame = ttk.Frame(self.notebook)
        self.attendance_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.add_student_frame, text="Add Student")
        self.notebook.add(self.view_students_frame, text="View Students")
        self.notebook.add(self.attendance_frame, text="Attendance")
        self.notebook.add(self.reports_frame, text="Reports")
        
        # Setup each tab
        self.setup_dashboard()
        self.setup_add_student()
        self.setup_view_students()
        self.setup_attendance()
        self.setup_reports()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load data if exists
        self.load_data()
    
    def setup_dashboard(self):
        """Setup the dashboard tab."""
        frame = ttk.Frame(self.dashboard_frame, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="Student Management System", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Stats variables
        self.total_students_var = tk.StringVar(value="0")
        self.avg_age_var = tk.StringVar(value="0")
        
        # Stats labels
        ttk.Label(stats_frame, text="Total Students:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_frame, textvariable=self.total_students_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Average Age:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(stats_frame, textvariable=self.avg_age_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(frame, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.X, pady=10)
        
        # Action buttons
        ttk.Button(actions_frame, text="Add New Student", command=lambda: self.notebook.select(1)).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(actions_frame, text="View All Students", command=lambda: self.notebook.select(2)).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_frame, text="Take Attendance", command=lambda: self.notebook.select(3)).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(actions_frame, text="Generate Reports", command=lambda: self.notebook.select(4)).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(actions_frame, text="Export Data", command=self.export_data).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(actions_frame, text="Import Data", command=self.import_data).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(actions_frame, text="Refresh Dashboard", command=self.update_dashboard).grid(row=1, column=2, padx=5, pady=5)
        
        # Recent activities frame
        recent_frame = ttk.LabelFrame(frame, text="Recent Activities", padding=10)
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Activity log
        self.activity_log = tk.Text(recent_frame, height=10, width=80, state=tk.DISABLED)
        self.activity_log.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to activity log
        scrollbar = ttk.Scrollbar(self.activity_log, command=self.activity_log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.activity_log.config(yscrollcommand=scrollbar.set)
    
    def setup_add_student(self):
        """Setup the add student tab."""
        frame = ttk.Frame(self.add_student_frame, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="Add New Student", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Student info frame
        info_frame = ttk.LabelFrame(frame, text="Student Information", padding=10)
        info_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        
        # Student info fields
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Age:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.age_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.age_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Grade:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.grade_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.grade_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
        # Contact info frame
        contact_frame = ttk.LabelFrame(frame, text="Contact Information", padding=10)
        contact_frame.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        
        # Contact info fields
        ttk.Label(contact_frame, text="Phone:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(contact_frame, textvariable=self.phone_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(contact_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(contact_frame, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Photo frame
        photo_frame = ttk.LabelFrame(frame, text="Student Photo", padding=10)
        photo_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        
        # Default photo
        self.photo_path = None
        self.photo_label = ttk.Label(photo_frame, text="No photo selected")
        self.photo_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Photo buttons
        ttk.Button(photo_frame, text="Select Photo", command=self.select_photo).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(photo_frame, text="Clear Photo", command=self.clear_photo).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def setup_view_students(self):
        """Setup the view students tab."""
        frame = ttk.Frame(self.view_students_frame, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="View Students", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Search frame
        search_frame = ttk.LabelFrame(frame, text="Search", padding=10)
        search_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search by:").grid(row=0, column=0, padx=5, pady=5)
        
        self.search_by = tk.StringVar(value="name")
        ttk.Radiobutton(search_frame, text="Name", variable=self.search_by, value="name").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(search_frame, text="ID", variable=self.search_by, value="id").grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(search_frame, text="Grade", variable=self.search_by, value="grade").grid(row=0, column=3, padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_students).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(row=0, column=6, padx=5, pady=5)
        
        # Students list frame
        list_frame = ttk.LabelFrame(frame, text="Students List", padding=10)
        list_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for students list
        columns = ("id", "name", "age", "grade", "phone", "email")
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.students_tree.heading("id", text="ID")
        self.students_tree.heading("name", text="Name")
        self.students_tree.heading("age", text="Age")
        self.students_tree.heading("grade", text="Grade")
        self.students_tree.heading("phone", text="Phone")
        self.students_tree.heading("email", text="Email")
        
        # Define columns
        self.students_tree.column("id", width=50)
        self.students_tree.column("name", width=150)
        self.students_tree.column("age", width=50)
        self.students_tree.column("grade", width=100)
        self.students_tree.column("phone", width=120)
        self.students_tree.column("email", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.students_tree.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        # Bind select event
        self.students_tree.bind("<<TreeviewSelect>>", self.on_student_select)
        
        # Student details frame
        details_frame = ttk.LabelFrame(frame, text="Student Details", padding=10)
        details_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)
        
        # Photo display
        self.detail_photo_frame = ttk.Frame(details_frame)
        self.detail_photo_frame.pack(fill=tk.X, pady=10)
        
        self.detail_photo_label = ttk.Label(self.detail_photo_frame, text="No photo")
        self.detail_photo_label.pack()
        
        # Details display
        self.detail_info_frame = ttk.Frame(details_frame)
        self.detail_info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons
        self.detail_buttons_frame = ttk.Frame(details_frame)
        self.detail_buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(self.detail_buttons_frame, text="Edit", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.detail_buttons_frame, text="Delete", command=self.delete_student).pack(side=tk.LEFT, padx=5)
    
    def setup_attendance(self):
        """Setup the attendance tab."""
        frame = ttk.Frame(self.attendance_frame, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="Attendance Tracking", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Date selection
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT, padx=5)
        
        # Date entry (you could use a calendar widget instead)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.date_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(date_frame, text="Today", command=lambda: self.date_var.set(datetime.now().strftime("%Y-%m-%d"))).pack(side=tk.LEFT, padx=5)
        
        # Attendance list frame
        attendance_frame = ttk.LabelFrame(frame, text="Mark Attendance", padding=10)
        attendance_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        frame.rowconfigure(2, weight=1)
        
        # Create treeview for attendance
        columns = ("id", "name", "grade", "status")
        self.attendance_tree = ttk.Treeview(attendance_frame, columns=columns, show="headings")
        
        # Define headings
        self.attendance_tree.heading("id", text="ID")
        self.attendance_tree.heading("name", text="Name")
        self.attendance_tree.heading("grade", text="Grade")
        self.attendance_tree.heading("status", text="Status")
        
        # Define columns
        self.attendance_tree.column("id", width=50)
        self.attendance_tree.column("name", width=200)
        self.attendance_tree.column("grade", width=100)
        self.attendance_tree.column("status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(attendance_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscroll=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to toggle attendance
        self.attendance_tree.bind("<Double-1>", self.toggle_attendance)
        
        # Action buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Mark All Present", command=self.mark_all_present).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Mark All Absent", command=self.mark_all_absent).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Save Attendance", command=self.save_attendance).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Load Attendance", command=self.load_attendance).pack(side=tk.LEFT, padx=5)
    
    def setup_reports(self):
        """Setup the reports tab."""
        frame = ttk.Frame(self.reports_frame, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(frame, text="Reports", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Report types frame
        report_types_frame = ttk.LabelFrame(frame, text="Report Types", padding=10)
        report_types_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        
        # Report type buttons
        ttk.Button(report_types_frame, text="Student List", command=lambda: self.generate_report("student_list")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(report_types_frame, text="Attendance Summary", command=lambda: self.generate_report("attendance")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(report_types_frame, text="Grade Distribution", command=lambda: self.generate_report("grades")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(report_types_frame, text="Age Distribution", command=lambda: self.generate_report("ages")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Report display frame
        report_display_frame = ttk.LabelFrame(frame, text="Report", padding=10)
        report_display_frame.grid(row=1, column=1, rowspan=2, sticky=tk.NSEW, padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Report text widget
        self.report_text = tk.Text(report_display_frame, wrap=tk.WORD)
        self.report_text.pack(fill=tk.BOTH, expand=True)
        
        # Export options frame
        export_frame = ttk.LabelFrame(frame, text="Export Options", padding=10)
        export_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
        
        # Export buttons
        ttk.Button(export_frame, text="Export to CSV", command=self.export_report_csv).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(export_frame, text="Export to Text", command=self.export_report_text).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(export_frame, text="Print Report", command=self.print_report).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    
    # Helper methods
    def log_activity(self, message):
        """Log an activity to the activity log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.activity_log.config(state=tk.NORMAL)
        self.activity_log.insert(tk.END, log_message)
        self.activity_log.see(tk.END)
        self.activity_log.config(state=tk.DISABLED)
        
        # Also log to file
        logging.info(message)
    
    def update_dashboard(self):
        """Update dashboard statistics."""
        # Update total students
        self.total_students_var.set(str(len(self.students)))
        
        # Calculate average age
        if self.students:
            total_age = sum(student.age for student in self.students.values())
            avg_age = total_age / len(self.students)
            self.avg_age_var.set(f"{avg_age:.1f}")
        else:
            self.avg_age_var.set("0")
        
        self.status_var.set("Dashboard updated")
    
    def validate_inputs(self):
        """Validate form inputs."""
        try:
            # Get values
            name = self.name_var.get().strip()
            age_str = self.age_var.get().strip()
            grade = self.grade_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()
            
            # Validate name
            if not name:
                raise ValueError("Name cannot be empty")
            if any(char.isdigit() for char in name):
                raise ValueError("Name must not contain numbers")
            
            # Validate age
            try:
                age = int(age_str)
                if age <= 0:
                    raise ValueError("Age must be a positive integer")
            except ValueError:
                raise ValueError("Age must be a valid integer")
            
            # Validate grade
            if not grade:
                raise ValueError("Grade cannot be empty")
            
            # Validate phone
            if len(phone) != 11 or not phone.isdigit():
                raise ValueError("Phone number must be an 11-digit number")
            
            # Validate email
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise ValueError("Invalid email address format")
            
            return True
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return False
    
    def add_student(self):
        """Add a new student."""
        if not self.validate_inputs():
            return
        
        try:
            # Get values
            name = self.name_var.get().strip()
            age = int(self.age_var.get().strip())
            grade = self.grade_var.get().strip()
            phone = self.phone_var.get().strip()
            email = self.email_var.get().strip()
            
            # Create contact and student objects
            contact = Contact(phone, email)
            student = Student(self.next_id, name, age, grade, contact)
            
            # Add student to the system
            self.students[self.next_id] = student
            
            # Save photo if selected
            if self.photo_path:
                self.student_photos[self.next_id] = self.photo_path
            
            # Increment ID
            self.next_id += 1
            
            # Log activity
            self.log_activity(f"Added new student: {name} with ID: {student.id}")
            
            # Update dashboard
            self.update_dashboard()
            
            # Update students list
            self.refresh_students_list()
            
            # Clear form
            self.clear_form()
            
            # Show success message
            messagebox.showinfo("Success", f"Student {name} added successfully with ID: {student.id}")
            
            # Switch to view students tab
            self.notebook.select(2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding student: {str(e)}")
    
    def clear_form(self):
        """Clear the add student form."""
        self.name_var.set("")
        self.age_var.set("")
        self.grade_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.clear_photo()
    
    def select_photo(self):
        """Select a photo for the student."""
        file_path = filedialog.askopenfilename(
            title="Select Student Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Open and resize image
                img = Image.open(file_path)
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Update photo label
                self.photo_label.config(image=photo, text="")
                self.photo_label.image = photo  # Keep a reference
                
                # Save photo path
                self.photo_path = file_path
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {str(e)}")
    
    def clear_photo(self):
        """Clear the selected photo."""
        self.photo_label.config(image="", text="No photo selected")
        self.photo_path = None
    
    def refresh_students_list(self):
        """Refresh the students list in the view tab."""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Add students to the list
        for student_id, student in self.students.items():
            details = student.get_details()
            contact = details["contact"] or {"phone": "", "email": ""}
            
            self.students_tree.insert("", tk.END, values=(
                details["id"],
                details["name"],
                details["age"],
                details["grade"],
                contact["phone"],
                contact["email"]
            ))
    
    def on_student_select(self, event):
        """Handle student selection in the treeview."""
        selected_items = self.students_tree.selection()
        if not selected_items:
            return
        
        # Get the selected student ID
        item = selected_items[0]
        student_id = int(self.students_tree.item(item, "values")[0])
        self.current_student_id = student_id
        
        # Display student details
        self.display_student_details(student_id)
    
    def display_student_details(self, student_id):
        """Display details for the selected student."""
        if student_id not in self.students:
            return
        
        # Clear previous details
        for widget in self.detail_info_frame.winfo_children():
            widget.destroy()
        
        # Get student details
        student = self.students[student_id]
        details = student.get_details()
        contact = details["contact"] or {"phone": "", "email": ""}
        
        # Display photo if available
        if student_id in self.student_photos:
            try:
                img = Image.open(self.student_photos[student_id])
                img = img.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.detail_photo_label.config(image=photo, text="")
                self.detail_photo_label.image = photo  # Keep a reference
            except Exception:
                self.detail_photo_label.config(image="", text="Photo not available")
        else:
            self.detail_photo_label.config(image="", text="No photo")
        
        # Display details
        ttk.Label(self.detail_info_frame, text=f"ID: {details['id']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
        ttk.Label(self.detail_info_frame, text=f"Name: {details['name']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
        ttk.Label(self.detail_info_frame, text=f"Age: {details['age']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
        ttk.Label(self.detail_info_frame, text=f"Grade: {details['grade']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
        
        if contact:
            ttk.Label(self.detail_info_frame, text="Contact Information:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
            ttk.Label(self.detail_info_frame, text=f"Phone: {contact['phone']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
            ttk.Label(self.detail_info_frame, text=f"Email: {contact['email']}", font=("Arial", 12)).pack(anchor=tk.W, pady=2)
    
    def edit_student(self):
        """Edit the selected student."""
        if not self.current_student_id:
            messagebox.showinfo("Info", "Please select a student to edit")
            return
        
        # Create a new window for editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student")
        edit_window.geometry("500x500")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Get student details
        student = self.students[self.current_student_id]
        details = student.get_details()
        contact = details["contact"] or {"phone": "", "email": ""}
        
        # Create form
        frame = ttk.Frame(edit_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Student info
        ttk.Label(frame, text="Edit Student", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        name_var = tk.StringVar(value=details["name"])
        ttk.Entry(frame, textvariable=name_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Age:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        age_var = tk.StringVar(value=str(details["age"]))
        ttk.Entry(frame, textvariable=age_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Grade:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        grade_var = tk.StringVar(value=details["grade"])
        ttk.Entry(frame, textvariable=grade_var, width=30).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        phone_var = tk.StringVar(value=contact["phone"])
        ttk.Entry(frame, textvariable=phone_var, width=30).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Email:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        email_var = tk.StringVar(value=contact["email"])
        ttk.Entry(frame, textvariable=email_var, width=30).grid(row=5, column=1, padx=5, pady=5)
        
        # Photo
        photo_frame = ttk.LabelFrame(frame, text="Student Photo", padding=10)
        photo_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        
        # Display current photo if available
        photo_label = ttk.Label(photo_frame, text="No photo")
        photo_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        if self.current_student_id in self.student_photos:
            try:
                img = Image.open(self.student_photos[self.current_student_id])
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                photo_label.config(image=photo, text="")
                photo_label.image = photo  # Keep a reference
            except Exception:
                pass
        
        # Photo path variable
        photo_path_var = tk.StringVar(value=self.student_photos.get(self.current_student_id, ""))
        
        # Photo buttons
        def select_edit_photo():
            file_path = filedialog.askopenfilename(
                title="Select Student Photo",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            
            if file_path:
                try:
                    # Open and resize image
                    img = Image.open(file_path)
                    img = img.resize((100, 100), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update photo label
                    photo_label.config(image=photo, text="")
                    photo_label.image = photo  # Keep a reference
                    
                    # Save photo path
                    photo_path_var.set(file_path)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error loading image: {str(e)}")
        
        ttk.Button(photo_frame, text="Select Photo", command=select_edit_photo).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save button
        def save_changes():
            try:
                # Validate inputs
                name = name_var.get().strip()
                age_str = age_var.get().strip()
                grade = grade_var.get().strip()
                phone = phone_var.get().strip()
                email = email_var.get().strip()
                
                # Validate name
                if not name:
                    raise ValueError("Name cannot be empty")
                if any(char.isdigit() for char in name):
                    raise ValueError("Name must not contain numbers")
                
                # Validate age
                try:
                    age = int(age_str)
                    if age <= 0:
                        raise ValueError("Age must be a positive integer")
                except ValueError:
                    raise ValueError("Age must be a valid integer")
                
                # Validate grade
                if not grade:
                    raise ValueError("Grade cannot be empty")
                
                # Validate phone
                if len(phone) != 11 or not phone.isdigit():
                    raise ValueError("Phone number must be an 11-digit number")
                
                # Validate email
                if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                    raise ValueError("Invalid email address format")
                
                # Create contact and update details
                contact = Contact(phone, email)
                details = {
                    'name': name,
                    'age': age,
                    'grade': grade,
                    'contact': contact
                }
                
                # Update student
                self.students[self.current_student_id].update_details(details)
                
                # Update photo if changed
                photo_path = photo_path_var.get()
                if photo_path:
                    self.student_photos[self.current_student_id] = photo_path
                
                # Log activity
                self.log_activity(f"Updated student: {name} with ID: {self.current_student_id}")
                
                # Update dashboard and list
                self.update_dashboard()
                self.refresh_students_list()
                
                # Display updated details
                self.display_student_details(self.current_student_id)
                
                # Close window
                edit_window.destroy()
                
                # Show success message
                messagebox.showinfo("Success", "Student details updated successfully")
                
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
        
        ttk.Button(frame, text="Save Changes", command=save_changes).grid(row=7, column=0, columnspan=2, pady=20)
    
    def delete_student(self):
        """Delete the selected student."""
        if not self.current_student_id:
            messagebox.showinfo("Info", "Please select a student to delete")
            return
        
        # Get student name
        student_name = self.students[self.current_student_id].name
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete student {student_name} (ID: {self.current_student_id})?"
        )
        
        if confirm:
            # Delete student
            del self.students[self.current_student_id]
            
            # Delete photo if exists
            if self.current_student_id in self.student_photos:
                del self.student_photos[self.current_student_id]
            
            # Log activity
            self.log_activity(f"Deleted student: {student_name} with ID: {self.current_student_id}")
            
            # Update dashboard and list
            self.update_dashboard()
            self.refresh_students_list()
            
            # Clear details
            for widget in self.detail_info_frame.winfo_children():
                widget.destroy()
            self.detail_photo_label.config(image="", text="No photo")
            
            # Reset current student ID
            self.current_student_id = None
            
            # Show success message
            messagebox.showinfo("Success", f"Student {student_name} deleted successfully")
    
    def search_students(self):
        """Search for students based on criteria."""
        search_text = self.search_var.get().strip()
        search_by = self.search_by.get()
        
        if not search_text:
            self.refresh_students_list()
            return
        
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Search and add matching students
        for student_id, student in self.students.items():
            details = student.get_details()
            contact = details["contact"] or {"phone": "", "email": ""}
            
            match = False
            
            if search_by == "name" and search_text.lower() in details["name"].lower():
                match = True
            elif search_by == "id" and search_text == str(details["id"]):
                match = True
            elif search_by == "grade" and search_text.lower() in details["grade"].lower():
                match = True
            
            if match:
                self.students_tree.insert("", tk.END, values=(
                    details["id"],
                    details["name"],
                    details["age"],
                    details["grade"],
                    contact["phone"],
                    contact["email"]
                ))
        
        self.status_var.set(f"Search results for: {search_text}")
    
    def clear_search(self):
        """Clear search and show all students."""
        self.search_var.set("")
        self.refresh_students_list()
        self.status_var.set("Search cleared")
    
    def toggle_attendance(self, event):
        """Toggle attendance status for a student."""
        item = self.attendance_tree.identify_row(event.y)
        if not item:
            return
        
        # Get current status
        current_status = self.attendance_tree.item(item, "values")[3]
        
        # Toggle status
        new_status = "Absent" if current_status == "Present" else "Present"
        
        # Update treeview
        values = list(self.attendance_tree.item(item, "values"))
        values[3] = new_status
        self.attendance_tree.item(item, values=values)
    
    def mark_all_present(self):
        """Mark all students as present."""
        for item in self.attendance_tree.get_children():
            values = list(self.attendance_tree.item(item, "values"))
            values[3] = "Present"
            self.attendance_tree.item(item, values=values)
    
    def mark_all_absent(self):
        """Mark all students as absent."""
        for item in self.attendance_tree.get_children():
            values = list(self.attendance_tree.item(item, "values"))
            values[3] = "Absent"
            self.attendance_tree.item(item, values=values)
    
    def load_attendance(self):
        """Load attendance for the selected date."""
        date = self.date_var.get()
        
        # Clear existing items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        # Load attendance records for the date
        attendance = self.attendance_records.get(date, {})
        
        # Add students to the list
        for student_id, student in self.students.items():
            details = student.get_details()
            
            # Get attendance status
            status = attendance.get(student_id, "Absent")
            
            self.attendance_tree.insert("", tk.END, values=(
                details["id"],
                details["name"],
                details["grade"],
                status
            ))
        
        self.status_var.set(f"Loaded attendance for {date}")
    
    def save_attendance(self):
        """Save attendance for the selected date."""
        date = self.date_var.get()
        
        # Create attendance record for the date
        attendance = {}
        
        # Get attendance status for each student
        for item in self.attendance_tree.get_children():
            values = self.attendance_tree.item(item, "values")
            student_id = int(values[0])
            status = values[3]
            
            attendance[student_id] = status
        
        # Save attendance record
        self.attendance_records[date] = attendance
        
        # Log activity
        self.log_activity(f"Saved attendance for {date}")
        
        # Show success message
        messagebox.showinfo("Success", f"Attendance for {date} saved successfully")
    
    def generate_report(self, report_type):
        """Generate a report based on the selected type."""
        self.report_text.delete(1.0, tk.END)
        
        if report_type == "student_list":
            self.generate_student_list_report()
        elif report_type == "attendance":
            self.generate_attendance_report()
        elif report_type == "grades":
            self.generate_grade_distribution_report()
        elif report_type == "ages":
            self.generate_age_distribution_report()
    
    def generate_student_list_report(self):
        """Generate a student list report."""
        report = "Student List Report\n"
        report += "=" * 50 + "\n\n"
        
        report += f"{'ID':<5} {'Name':<20} {'Age':<5} {'Grade':<10} {'Phone':<15} {'Email':<30}\n"
        report += "-" * 85 + "\n"
        
        for student_id, student in self.students.items():
            details = student.get_details()
            contact = details["contact"] or {"phone": "", "email": ""}
            
            report += f"{details['id']:<5} {details['name']:<20} {details['age']:<5} {details['grade']:<10} {contact['phone']:<15} {contact['email']:<30}\n"
        
        report += "\n" + "=" * 50 + "\n"
        report += f"Total Students: {len(self.students)}\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.report_text.insert(tk.END, report)
    
    def generate_attendance_report(self):
        """Generate an attendance report."""
        report = "Attendance Summary Report\n"
        report += "=" * 50 + "\n\n"
        
        if not self.attendance_records:
            report += "No attendance records found.\n"
        else:
            # Calculate attendance statistics
            student_attendance = {}
            
            for date, attendance in self.attendance_records.items():
                report += f"Date: {date}\n"
                report += f"{'ID':<5} {'Name':<20} {'Status':<10}\n"
                report += "-" * 35 + "\n"
                
                for student_id, status in attendance.items():
                    if student_id in self.students:
                        student_name = self.students[student_id].name
                        report += f"{student_id:<5} {student_name:<20} {status:<10}\n"
                        
                        # Update student attendance stats
                        if student_id not in student_attendance:
                            student_attendance[student_id] = {"present": 0, "absent": 0}
                        
                        if status == "Present":
                            student_attendance[student_id]["present"] += 1
                        else:
                            student_attendance[student_id]["absent"] += 1
                
                report += "\n"
            
            # Overall statistics
            report += "Overall Attendance Statistics\n"
            report += "-" * 50 + "\n"
            report += f"{'ID':<5} {'Name':<20} {'Present':<10} {'Absent':<10} {'Attendance %':<15}\n"
            report += "-" * 60 + "\n"
            
            for student_id, stats in student_attendance.items():
                if student_id in self.students:
                    student_name = self.students[student_id].name
                    total_days = stats["present"] + stats["absent"]
                    attendance_percent = (stats["present"] / total_days * 100) if total_days > 0 else 0
                    
                    report += f"{student_id:<5} {student_name:<20} {stats['present']:<10} {stats['absent']:<10} {attendance_percent:.2f}%\n"
        
        report += "\n" + "=" * 50 + "\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.report_text.insert(tk.END, report)
    
    def generate_grade_distribution_report(self):
        """Generate a grade distribution report."""
        report = "Grade Distribution Report\n"
        report += "=" * 50 + "\n\n"
        
        # Count students by grade
        grade_counts = {}
        
        for student in self.students.values():
            grade = student.grade
            if grade not in grade_counts:
                grade_counts[grade] = 0
            grade_counts[grade] += 1
        
        # Sort grades
        sorted_grades = sorted(grade_counts.keys())
        
        # Display distribution
        report += "Grade Distribution:\n"
        report += "-" * 30 + "\n"
        report += f"{'Grade':<15} {'Count':<10} {'Percentage':<15}\n"
        report += "-" * 40 + "\n"
        
        for grade in sorted_grades:
            count = grade_counts[grade]
            percentage = (count / len(self.students) * 100) if self.students else 0
            report += f"{grade:<15} {count:<10} {percentage:.2f}%\n"
        
        report += "\n" + "=" * 50 + "\n"
        report += f"Total Students: {len(self.students)}\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.report_text.insert(tk.END, report)
    
    def generate_age_distribution_report(self):
        """Generate an age distribution report."""
        report = "Age Distribution Report\n"
        report += "=" * 50 + "\n\n"
        
        # Count students by age
        age_counts = {}
        
        for student in self.students.values():
            age = student.age
            if age not in age_counts:
                age_counts[age] = 0
            age_counts[age] += 1
        
        # Sort ages
        sorted_ages = sorted(age_counts.keys())
        
        # Display distribution
        report += "Age Distribution:\n"
        report += "-" * 30 + "\n"
        report += f"{'Age':<10} {'Count':<10} {'Percentage':<15}\n"
        report += "-" * 35 + "\n"
        
        for age in sorted_ages:
            count = age_counts[age]
            percentage = (count / len(self.students) * 100) if self.students else 0
            report += f"{age:<10} {count:<10} {percentage:.2f}%\n"
        
        # Calculate statistics
        if self.students:
            ages = [student.age for student in self.students.values()]
            min_age = min(ages)
            max_age = max(ages)
            avg_age = sum(ages) / len(ages)
            
            report += "\nAge Statistics:\n"
            report += "-" * 30 + "\n"
            report += f"Minimum Age: {min_age}\n"
            report += f"Maximum Age: {max_age}\n"
            report += f"Average Age: {avg_age:.2f}\n"
        
        report += "\n" + "=" * 50 + "\n"
        report += f"Total Students: {len(self.students)}\n"
        report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.report_text.insert(tk.END, report)
    
    def export_report_csv(self):
        """Export the current report to CSV."""
        file_path = filedialog.asksaveasfilename(
            title="Export Report to CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Get report text
                    report_text = self.report_text.get(1.0, tk.END)
                    
                    # Parse and write to CSV
                    lines = report_text.split('\n')
                    for line in lines:
                        if line and not line.startswith('=') and not line.startswith('-'):
                            writer.writerow(line.split())
                
                messagebox.showinfo("Success", f"Report exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting report: {str(e)}")
    
    def export_report_text(self):
        """Export the current report to a text file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Report to Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.report_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"Report exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting report: {str(e)}")
    
    def print_report(self):
        """Print the current report."""
        messagebox.showinfo("Print", "Printing functionality would be implemented here.")
    
    def export_data(self):
        """Export all student data to a CSV file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Student Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(["ID", "Name", "Age", "Grade", "Phone", "Email"])
                    
                    # Write student data
                    for student_id, student in self.students.items():
                        details = student.get_details()
                        contact = details["contact"] or {"phone": "", "email": ""}
                        
                        writer.writerow([
                            details["id"],
                            details["name"],
                            details["age"],
                            details["grade"],
                            contact["phone"],
                            contact["email"]
                        ])
                
                self.log_activity(f"Exported student data to {file_path}")
                messagebox.showinfo("Success", f"Student data exported to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting data: {str(e)}")
    
    def import_data(self):
        """Import student data from a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Import Student Data",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    
                    # Skip header
                    next(reader)
                    
                    # Read student data
                    for row in reader:
                        if len(row) >= 6:
                            student_id = int(row[0])
                            name = row[1]
                            age = int(row[2])
                            grade = row[3]
                            phone = row[4]
                            email = row[5]
                            
                            # Create contact and student objects
                            contact = Contact(phone, email)
                            student = Student(student_id, name, age, grade, contact)
                            
                            # Add student to the system
                            self.students[student_id] = student
                            
                            # Update next_id if needed
                            if student_id >= self.next_id:
                                self.next_id = student_id + 1
                
                self.log_activity(f"Imported student data from {file_path}")
                self.update_dashboard()
                self.refresh_students_list()
                messagebox.showinfo("Success", f"Student data imported from {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error importing data: {str(e)}")
    
    def load_data(self):
        """Load data from files if they exist."""
        # This would typically load from a database or files
        # For this example, we'll just add some sample data
        self.add_sample_data()
        
        # Update dashboard and lists
        self.update_dashboard()
        self.refresh_students_list()
        self.load_attendance()
    
    def add_sample_data(self):
        """Add sample data for demonstration."""
        # Only add if no students exist
        if not self.students:
            # Sample students
            contact1 = Contact("12345678901", "john.doe@example.com")
            student1 = Student(1, "John Doe", 18, "Grade 12", contact1)
            self.students[1] = student1
            
            contact2 = Contact("23456789012", "jane.smith@example.com")
            student2 = Student(2, "Jane Smith", 17, "Grade 11", contact2)
            self.students[2] = student2
            
            contact3 = Contact("34567890123", "bob.johnson@example.com")
            student3 = Student(3, "Bob Johnson", 16, "Grade 10", contact3)
            self.students[3] = student3
            
            # Set next ID
            self.next_id = 4
            
            # Sample attendance
            today = datetime.now().strftime("%Y-%m-%d")
            self.attendance_records[today] = {
                1: "Present",
                2: "Present",
                3: "Absent"
            }
            
            # Log activity
            self.log_activity("Loaded sample data")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
