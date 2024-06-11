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

gabung.search.argtypes = [ctypes.POINTER(AVLNode), ctypes.c_char_p]
gabung.search.restype = ctypes.POINTER(Teacher)

# GUI setup
def load_teachers():
    filename = "DataGuru.csv"
    root = ctypes.POINTER(AVLNode)()
    root = gabung.loadTeachersFromFile(root, filename.encode('utf-8'))
    if not root:
        messagebox.showerror("Error", "Failed to load teachers.")
        return None, False
    return root, True

def search_teacher():
    global root
    root, loaded = load_teachers()
    if not loaded:
        return
    code_guru = code_entry.get().encode('utf-8')
    teacher = gabung.search(root, code_guru)
    if teacher:
        result.set(f"Teacher: {teacher.contents.fullname.decode('utf-8')}, Email: {teacher.contents.email.decode('utf-8')}")
    else:
        result.set("Teacher not found.")




root = Tk()
root.title("Teacher Search")

Label(root, text="Enter Teacher ID:").grid(row=0, column=0)
code_entry = Entry(root)
code_entry.grid(row=0, column=1)

Button(root, text="Search", command=search_teacher).grid(row=1, column=0, columnspan=2)
result = StringVar()
Label(root, textvariable=result).grid(row=2, column=0, columnspan=2)

root.mainloop()
