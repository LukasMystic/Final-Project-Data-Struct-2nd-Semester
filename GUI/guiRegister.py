import ctypes
import os
from tkinter import *
from tkinter import messagebox

# Load the shared library
if os.name == 'nt':
    gabung = ctypes.CDLL('./gabung.dll')
else:
    gabung = ctypes.CDLL('./libgabung.so')

class Teacher(ctypes.Structure):
    _fields_ = [("codeGuru", ctypes.c_char * 100),
                ("fullname", ctypes.c_char * 100),
                ("email", ctypes.c_char * 100)]

class AVLNode(ctypes.Structure):
    pass

AVLNode._fields_ = [("teacher", ctypes.POINTER(Teacher)),
                    ("height", ctypes.c_int),
                    ("left", ctypes.POINTER(AVLNode)),
                    ("right", ctypes.POINTER(AVLNode))]

# Define function prototypes
gabung.loadTeachersFromFile.argtypes = [ctypes.POINTER(AVLNode), ctypes.c_char_p]
gabung.loadTeachersFromFile.restype = ctypes.POINTER(AVLNode)

gabung.searchByEmail.argtypes = [ctypes.POINTER(AVLNode), ctypes.c_char_p]
gabung.searchByEmail.restype = ctypes.POINTER(Teacher)

gabung.search.argtypes = [ctypes.POINTER(AVLNode), ctypes.c_char_p]
gabung.search.restype = ctypes.POINTER(Teacher)

gabung.insertTeacherAVL.argtypes = [ctypes.POINTER(AVLNode), ctypes.POINTER(Teacher)]
gabung.insertTeacherAVL.restype = ctypes.POINTER(AVLNode)

gabung.appendTeacherToFile.argtypes = [ctypes.c_char_p, ctypes.POINTER(Teacher)]

gabung.verifyCode.argtypes = [ctypes.c_char_p]
gabung.verifyCode.restype = ctypes.c_int

gabung.generateVerificationCode.argtypes = []

# Global variables
root_node = None
current_user = None

# Function to destroy all child windows
def destroy_all_children(window):
    for widget in window.winfo_children():
        widget.destroy()

def reload_avl_tree():
    global root_node
    root_node = gabung.loadTeachersFromFile(root_node, b"DataGuru.csv")

# GUI setup
def main_datasiswa_window(current_user):
    reload_avl_tree()
    main_window = Toplevel()
    main_window.title("Main Data Assessment Menu")
    main_window.geometry("800x600")
    main_window.configure(bg="#f0f0f0")

    Label(main_window, text="Welcome To Homepage", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)
    Label(main_window, text="HIGH SCHOOL TEACHER ASSESSMENT SYSTEM", font=("Arial", 16), bg="#f0f0f0").pack()

    # Display currently logged-in user
    Label(main_window, text=f"Logged in as: {current_user}", font=("Arial", 12), anchor="e", justify="right", bg="#f0f0f0").pack(side="top", fill="x")

    # Tools menu options
    options = [
        "Insert Student Information and Grades",
        "Sort, View, and Export Student Grades",
        "Edit Student Information and Grades",
        "Delete Student Data",
        "Export Grades (Unsorted)",
        "Close the Program"
    ]

    for i, option in enumerate(options, start=1):
        Label(main_window, text=f"{i}. {option}", font=("Arial", 12), bg="#f0f0f0").pack()

def register_teacher(avl_root):
    email = email_entry.get().encode('utf-8')
    code_guru = code_entry.get().encode('utf-8')
    fullname = fullname_entry.get().encode('utf-8')

    # Validate email format
    if len(email) < 6 or b'@' not in email or (b'.com' not in email and b'.id' not in email):
        messagebox.showerror("Error", "Invalid email format! Email must contain '@' symbol and end with '.com' or '.id'.")
        return

    # Check if email already exists
    email_check = gabung.searchByEmail(avl_root, email)
    if email_check:
        messagebox.showerror("Error", "User with this email already exists. Please use another email.")
        return

    # Validate Teacher ID format
    if len(code_guru)!= 10 or not code_guru.isdigit():
        messagebox.showerror("Error", "Invalid Teacher ID format! Teacher ID must have exactly 10 digits and must be integer.")
        return

    # Check if Teacher ID already exists
    teacher_check = gabung.search(avl_root, code_guru)
    if teacher_check:
        messagebox.showerror("Error", "User with this ID already exists. Please choose another ID.")
        return

    # Create newteacher and insert into AVL tree
    new_teacher= Teacher(code_guru, fullname, email)
    gabung.insertTeacherAVL(avl_root, ctypes.byref(new_teacher))
    # Append new teacher to file
    gabung.appendTeacherToFile(b"DataGuru.csv", ctypes.byref(new_teacher))

    messagebox.showinfo("Success", "Registration successful! Please login to continue.")
    reload_avl_tree()
    show_main_menu()

def show_registration_page(avl_root):
    destroy_all_children(root)

    global email_entry, code_entry, fullname_entry
    Label(root, text="Enter Email:", font=('Arial', 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky=E)
    email_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Enter Teacher ID (10 digits):", font=('Arial', 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky=E)
    code_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
    code_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Enter Fullname:", font=('Arial', 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky=E)
    fullname_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
    fullname_entry.grid(row=2, column=1, padx=10, pady=10)

    Button(root, text="Register", font=('Arial', 12), bg="#4CAF50", fg="white", command=lambda: register_teacher(avl_root)).grid(row=3, column=0, columnspan=2, pady=20)
    Button(root, text="Back", font=('Arial', 12), bg="#f0f0f0", command=show_main_menu).grid(row=4, column=0, columnspan=2, pady=10)

def verify_code():
    code = verification_code_entry.get().encode('utf-8')
    if gabung.verifyCode(code):
        messagebox.showinfo("Success", "Verification successful!")
        # Redirect to the main system or another part of the application
    else:
        messagebox.showerror("Error", "Verification failed! Incorrect code.")

def login_teacher(avl_root):
    email = login_email_entry.get().encode('utf-8')
    code_guru = login_code_entry.get().encode('utf-8')
    
    reload_avl_tree()

    teacher = gabung.searchByEmail(avl_root, email)
    if teacher and teacher.contents.codeGuru == code_guru:
        global current_user  # Declare current_user as global
        current_user = teacher.contents.fullname.decode('utf-8')  # Store the user's fullname
        # Generate verification code
        gabung.generateVerificationCode()

        destroy_all_children(root)
        global verification_code_entry
        Label(root, text="Enter Verification Code:", font=('Arial', 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky=E)
        verification_code_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
        verification_code_entry.grid(row=0, column=1, padx=10, pady=10)

        Button(root, text="Verify", font=('Arial', 12), bg="#4CAF50", fg="white", command=lambda: verify_code_and_login()).grid(row=1, column=0, columnspan=2, pady=20)
    else:
        messagebox.showerror("Error", "Invalid email or Teacher ID. Please try again.")

def verify_code_and_login():
    code = verification_code_entry.get().encode('utf-8')
    if gabung.verifyCode(code):
        messagebox.showinfo("Success", "Verification successful!")
        main_datasiswa_window(current_user)  # Go to main datasiswa window
        root.withdraw()  # Close only the login window
    else:
        messagebox.showerror("Error", "Verification failed! Incorrect code.")

def show_login_page(avl_root):
    destroy_all_children(root)

    global login_email_entry, login_code_entry
    Label(root, text="Enter Email:", font=('Arial', 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky=E)
    login_email_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
    login_email_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Enter Teacher ID:", font=('Arial', 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky=E)
    login_code_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
    login_code_entry.grid(row=1, column=1, padx=10, pady=10)

    Button(root, text="Login", font=('Arial', 12), bg="#4CAF50", fg="white", command=lambda: login_teacher(avl_root)).grid(row=2, column=0, columnspan=2, pady=20)
    Button(root, text="Back", font=('Arial', 12), bg="#f0f0f0", command=show_main_menu).grid(row=3, column=0, columnspan=2, pady=10)

def show_main_menu():
    destroy_all_children(root)
    Button(root, text="Register Teacher", font=('Arial', 14), bg="#4CAF50", fg="white", command=lambda: show_registration_page(root_node)).pack(pady=20)
    Button(root, text="Login", font=('Arial', 14), bg="#4CAF50", fg="white", command=lambda: show_login_page(root_node)).pack(pady=20)

root_node = gabung.loadTeachersFromFile(root_node, b"DataGuru.csv")

root = Tk()
root.title("Teacher Management System")
root.geometry("600x400")
root.configure(bg="#102c57")

show_main_menu()

root.mainloop()
