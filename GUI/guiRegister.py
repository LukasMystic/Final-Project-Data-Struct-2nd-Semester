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

# Global variables
root_node = None

# GUI setup
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
    if len(code_guru) != 10 or not code_guru.isdigit():
        messagebox.showerror("Error", "Invalid Teacher ID format! Teacher ID must have exactly 10 digits and must be integer.")
        return

    # Check if Teacher ID already exists
    teacher_check = gabung.search(avl_root, code_guru)
    if teacher_check:
        messagebox.showerror("Error", "User with this ID already exists. Please choose another ID.")
        return

    # Create new teacher and insert into AVL tree
    new_teacher = Teacher(code_guru, fullname, email)
    gabung.insertTeacherAVL(avl_root, ctypes.byref(new_teacher))
    # Append new teacher to file
    gabung.appendTeacherToFile(b"DataGuru.csv", ctypes.byref(new_teacher))

    messagebox.showinfo("Success", "Registration successful! Please login to continue.")

def show_registration_page(avl_root):
    register_window = Toplevel()
    register_window.title("Register Teacher")

    global email_entry, code_entry, fullname_entry
    Label(register_window, text="Enter Email:").grid(row=0, column=0)
    email_entry = Entry(register_window)
    email_entry.grid(row=0, column=1)

    Label(register_window, text="Enter Teacher ID (10 digits):").grid(row=1, column=0)
    code_entry = Entry(register_window)
    code_entry.grid(row=1, column=1)

    Label(register_window, text="Enter Fullname:").grid(row=2, column=0)
    fullname_entry = Entry(register_window)
    fullname_entry.grid(row=2, column=1)

    Button(register_window, text="Register", command=lambda: register_teacher(avl_root)).grid(row=3, column=0, columnspan=2)

root_node = gabung.loadTeachersFromFile(root_node, b"DataGuru.csv")

root = Tk()
root.title("Teacher Management System")

Button(root, text="Register Teacher", command=lambda: show_registration_page(root_node)).grid(row=0, column=0)

root.mainloop()
