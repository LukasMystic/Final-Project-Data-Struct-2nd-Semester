import ctypes
import os
import csv
import tkinter as tk
import ctypes.util
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import messagebox, filedialog, Text, Toplevel, Button, Label, Entry
from PIL import Image, ImageTk
from ctypes import cdll, c_void_p, c_char_p, c_int, POINTER


# Load the shared library
if os.name == 'nt':
    gabung = ctypes.CDLL('./gabung.dll')
    libc = ctypes.CDLL('msvcrt.dll')
else:
    gabung = ctypes.CDLL('./libgabung.so')
    libc = ctypes.CDLL(ctypes.util.find_library('c'))

# Load the teacher class
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

# Load the students class
class DataSiswa(ctypes.Structure):
    _fields_ = [("studentID", ctypes.c_char * 20),
                ("fullname", ctypes.c_char * 100),
                ("nilaiMat", ctypes.c_int),
                ("nilaiFis", ctypes.c_int),
                ("nilaiKim", ctypes.c_int),
                ("nilaiBio", ctypes.c_int),
                ("nilaiBindo", ctypes.c_int),
                ("kelas", ctypes.c_int),
                ("rata2", ctypes.c_double),
                ("grade", ctypes.c_char)]

class AVLSiswa(ctypes.Structure):
    pass

class StudentArray(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(DataSiswa) * 800),
                ("count", ctypes.c_int)]

AVLSiswa._fields_ = [("data", ctypes.POINTER(DataSiswa)),
                    ("height2", ctypes.c_int),
                    ("left", ctypes.POINTER(AVLSiswa)),
                    ("right", ctypes.POINTER(AVLSiswa))]

class Student(ctypes.Structure):
    _fields_ = [("studentID", ctypes.c_char * 100),
                ("name", ctypes.c_char * 100),
                ("kelas", ctypes.c_char * 10),
                ("nilai_matematika", ctypes.c_int),
                ("nilai_fisika", ctypes.c_int),
                ("nilai_kimia", ctypes.c_int),
                ("nilai_biologi", ctypes.c_int),
                ("nilai_bahasa_indonesia", ctypes.c_int),
                ("rata_rata", ctypes.c_double),
                ("grade", ctypes.c_char)]

##############################################################################

# Define function prototypes
# Teachers
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

##############################################################################

# Students
# Function prototypes
gabung.createDataSiswa.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
gabung.createDataSiswa.restype = ctypes.POINTER(DataSiswa)

gabung.insertDataSiswa.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.POINTER(DataSiswa)]
gabung.insertDataSiswa.restype = ctypes.POINTER(AVLSiswa)

gabung.searchID.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_char_p]
gabung.searchID.restype = ctypes.POINTER(DataSiswa)

gabung.deleteDataSiswa.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_char_p]
gabung.deleteDataSiswa.restype = ctypes.POINTER(AVLSiswa)

gabung.generateID.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
gabung.generateID.restype = None

gabung.formatNameDisplay.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
gabung.formatNameDisplay.restype = None

gabung.generateGrade.argtypes = [ctypes.c_double]
gabung.generateGrade.restype = ctypes.c_char

gabung.initializeRandom.argtypes = []
gabung.initializeRandom.restype = None

gabung.searchIDContaining.argtypes = [
    ctypes.POINTER(AVLSiswa), 
    ctypes.c_char_p, 
    ctypes.POINTER(ctypes.POINTER(DataSiswa)), 
    ctypes.POINTER(ctypes.c_int)
]
gabung.searchIDContaining.restype = ctypes.c_int

gabung.search2.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.POINTER(ctypes.c_char)]
gabung.search2.restype = ctypes.c_int

gabung.inorderTraversal.argtypes = [ctypes.POINTER(AVLSiswa)]
gabung.inorderTraversal.restype = None

gabung.searchByFullName.argtypes = [ctypes.POINTER(AVLSiswa)]
gabung.searchByFullName.restype = None

gabung.searchByName.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_char_p, ctypes.POINTER(StudentArray)]
gabung.searchByName.restype = None

gabung.displaySearchResults.argtypes = [ctypes.POINTER(StudentArray)]
gabung.displaySearchResults.restype = None

gabung.exportToCSV.argtypes = [ctypes.POINTER(Student), ctypes.c_int, ctypes.c_char_p]
gabung.exportToCSV.restype = None

gabung.searchByClassHelper.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_int, ctypes.POINTER(StudentArray)]
gabung.searchByClassHelper.restype = None

gabung.searchByClass.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_int]
gabung.searchByClass.restype = None

gabung.loadStudentsFromFile.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_char_p]
gabung.loadStudentsFromFile.restype = ctypes.POINTER(AVLSiswa)

gabung.writeStudentToFile.argtypes = [c_void_p, c_void_p]
gabung.writeStudentToFile.restype = None

gabung.writeStudentsInOrder.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.POINTER(ctypes.c_void_p)]
gabung.writeStudentsInOrder.restype = None

gabung.writeStudentsToFile.argtypes = [ctypes.POINTER(AVLSiswa), ctypes.c_char_p]
gabung.writeStudentsToFile.restype = None

gabung.generateExportName.argtypes = [c_char_p]
gabung.generateExportName.restype = c_char_p

gabung.readStudentsFromCSV.argtypes = [ctypes.POINTER(Student), ctypes.POINTER(ctypes.c_int), ctypes.c_char_p]
gabung.readStudentsFromCSV.restype = None

gabung.eksportarr.argtypes = [ctypes.POINTER(Student), ctypes.c_int, ctypes.POINTER(ctypes.c_char)]
gabung.eksportarr.restype = None

gabung.exportToCSV.argtypes = [ctypes.POINTER(Student), ctypes.c_int, ctypes.c_char_p]
gabung.exportToCSV.restype = None

##############################################################################

# Comparison
gabung.compareNameAsc.argtypes = [c_void_p, c_void_p]
gabung.compareNameAsc.restype = c_int

gabung.compareNameDesc.argtypes = [c_void_p, c_void_p]
gabung.compareNameDesc.restype = c_int

gabung.compareMathAsc.argtypes = [c_void_p, c_void_p]
gabung.compareMathAsc.restype = c_int

gabung.compareMathDesc.argtypes = [c_void_p, c_void_p]
gabung.compareMathDesc.restype = c_int

gabung.comparePhysicsAsc.argtypes = [c_void_p, c_void_p]
gabung.comparePhysicsAsc.restype = c_int

gabung.comparePhysicsDesc.argtypes = [c_void_p, c_void_p]
gabung.comparePhysicsDesc.restype = c_int

gabung.compareChemistryAsc.argtypes = [c_void_p, c_void_p]
gabung.compareChemistryAsc.restype = c_int

gabung.compareChemistryDesc.argtypes = [c_void_p, c_void_p]
gabung.compareChemistryDesc.restype = c_int

gabung.compareBiologyAsc.argtypes = [c_void_p, c_void_p]
gabung.compareBiologyAsc.restype = c_int

gabung.compareBiologyDesc.argtypes = [c_void_p, c_void_p]
gabung.compareBiologyDesc.restype = c_int

gabung.compareIndonesianAsc.argtypes = [c_void_p, c_void_p]
gabung.compareIndonesianAsc.restype = c_int

gabung.compareIndonesianDesc.argtypes = [c_void_p, c_void_p]
gabung.compareIndonesianDesc.restype = c_int

gabung.compareClassAsc.argtypes = [c_void_p, c_void_p]
gabung.compareClassAsc.restype = c_int

gabung.compareClassDesc.argtypes = [c_void_p, c_void_p]
gabung.compareClassDesc.restype = c_int

gabung.compareGradeAsc.argtypes = [c_void_p, c_void_p]
gabung.compareGradeAsc.restype = c_int

gabung.compareGradeDesc.argtypes = [c_void_p, c_void_p]
gabung.compareGradeDesc.restype = c_int

gabung.compareRataRataAsc.argtypes = [c_void_p, c_void_p]
gabung.compareRataRataAsc.restype = c_int

gabung.compareRataRataDesc.argtypes = [c_void_p, c_void_p]
gabung.compareRataRataDesc.restype = c_int

gabung.isValidNumber.argtypes = [c_char_p]
gabung.isValidNumber.restype = c_int

gabung.isValidName.argtypes = [c_char_p]
gabung.isValidName.restype = c_int

#end comparison

##############################################################################

# Global variables
root_node = None
current_user = None
root_siswa = None
current_siswa = None  

def close_sort_export_window():
    global sort_export_window
    if sort_export_window:
        sort_export_window.destroy()
        sort_export_window = None

def destroy_all_children(window):
    for widget in window.winfo_children():
        widget.destroy()

def reload_avl_tree():
    global root_node
    root_node = gabung.loadTeachersFromFile(root_node, b"DataGuru.csv")
    
def format_name_display(name_bytes):
    formatted_name = ctypes.create_string_buffer(50)  # Assuming 50 is the maximum length
    gabung.formatNameDisplay(name_bytes, formatted_name)
    return formatted_name.value.decode('utf-8')

##############################################################################

# Sorting

qsort = libc.qsort
qsort.argtypes = [c_void_p, ctypes.c_size_t, ctypes.c_size_t, ctypes.CFUNCTYPE(ctypes.c_int, c_void_p, c_void_p)]

##############################################################################



# GUI setup
##############################################################################

# Siswa
def load_students_from_file():
    global root_siswa
    root_siswa = gabung.loadStudentsFromFile(None, b"sma_students_data1.csv")
    return root_siswa

def read_students_from_csv(filename):
    students = (Student * 800)()
    count = ctypes.c_int()
    gabung.readStudentsFromCSV(students, ctypes.byref(count), filename)
    return students, count.value


# main menu (after login) 
def main_datasiswa_window(previous_window, current_user):
    previous_window.withdraw()  # Close the previous window
    global root_siswa
    root_siswa = load_students_from_file()
    
    main_window = Toplevel()
    main_window.title("Main Data Assessment Menu")
    main_window.geometry("1000x900")
    main_window.configure(bg="#102c57")
    
    Label(main_window, text=f"Logged in as: {current_user}", font=("Arial", 12), anchor="e", justify="right", fg="#f0f0f0", bg="#102c57").pack(side="top", fill="x")
   
    global global_photo
    image = Image.open("teacher.png")
    image = image.resize((200, 200), Image.LANCZOS)
    global_photo = ImageTk.PhotoImage(image)  # Assign to global_photo to prevent garbage collection

    image_label = Label(main_window, image=global_photo, bg="#f0f0f0")
    image_label.pack(pady=20)
    
    Label(main_window, text="Welcome To Homepage", font=("Arial", 20), fg="#f0f0f0", bg="#102c57").pack(pady=20)
    Label(main_window, text="HIGH SCHOOL TEACHER ASSESSMENT SYSTEM", font=("Arial", 16), fg="#f0f0f0", bg="#102c57").pack(pady=10)

    

    # Final case lolz
    def close_program():
        # Close the program
        main_window.destroy()

    # Button styling
    button_font = ("Arial", 12, 'bold')
    button_bg = "#4CAF50"
    button_fg = "white"
    button_width = 35  # Adjust as needed
    button_height = 2   # Adjust as needed
    button_padx = 20    # Adjust padding as needed
    button_pady = 5    # Adjust padding as needed

    # Add buttons for each option with updated styling
    Button(main_window, text="1. Insert Student Information and Grades", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=lambda: insert_student(current_user)).pack(pady=10)
    Button(main_window, text="2. Sort, View, Search, and Export Student Grades", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=sort_view_export_students).pack(pady=10)
    Button(main_window, text="3. Edit Student Information and Grades", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=lambda: update_student_info(root_siswa, current_user)).pack(pady=10)
    Button(main_window, text="4. Delete Student Data", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=lambda: delete_student(current_user)).pack(pady=10)
    Button(main_window, text="5. Plot", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=lambda: create_plotting_window(current_user)).pack(pady=10)
    Button(main_window, text="6. Close the Program", font=button_font, bg=button_bg, fg=button_fg, width=button_width, height=button_height, padx=button_padx, pady=button_pady, command=close_program).pack(pady=10)

    

##############################################################################


# case 1 (insert)
def insert_student(current_user):
    global root_siswa

    # Function to destroy previous window if it's a Tkinter object
    def destroy_previous_window(window):
        if isinstance(window, tk.Toplevel) or isinstance(window, tk.Tk):
            window.destroy()

    # Close the previous window if it exists
    if current_user:
        destroy_previous_window(current_user)

    # Create the insert student data window
    insert_window = tk.Tk()
    insert_window.title("Insert Student Data")
    insert_window.geometry("800x800")
    insert_window.configure(bg="#102c57")

    def create_label_and_entry(window, text, width=50):
        label = tk.Label(window, text=text, font=("Arial", 12), bg="#102c57", fg="#f0f0f0", pady=10)
        label.pack()
        entry = tk.Entry(window, width=width, font=("Arial", 12), bg="#f0f0f0")
        entry.pack(pady=3) 
        return entry

    fullname_entry = create_label_and_entry(insert_window, "Fullname")
    kelas_entry = create_label_and_entry(insert_window, "Class")
    nilaiMat_entry = create_label_and_entry(insert_window, "Math Score")
    nilaiFis_entry = create_label_and_entry(insert_window, "Physics Score")
    nilaiKim_entry = create_label_and_entry(insert_window, "Chemistry Score")
    nilaiBio_entry = create_label_and_entry(insert_window, "Biology Score")
    nilaiBindo_entry = create_label_and_entry(insert_window, "Indonesian Score")

    def get_student_data():
        global root_siswa

        # Retrieve data from GUI elements
        fullname = fullname_entry.get()
        kelas = kelas_entry.get()
        nilaiMat = nilaiMat_entry.get()
        nilaiFis = nilaiFis_entry.get()
        nilaiKim = nilaiKim_entry.get()
        nilaiBio = nilaiBio_entry.get()
        nilaiBindo = nilaiBindo_entry.get()

        # Validate input data
        if not validate_input(fullname, kelas, nilaiMat, nilaiFis, nilaiKim, nilaiBio, nilaiBindo):
            return

        # Calculate average and grade
        rata2 = (int(nilaiMat) + int(nilaiFis) + int(nilaiKim) + int(nilaiBio) + int(nilaiBindo)) / 5.0
        grade = gabung.generateGrade(rata2)

        # Create student node
        student_node = gabung.createDataSiswa(fullname.encode(), int(nilaiMat), int(nilaiFis), int(nilaiKim), int(nilaiBio), int(nilaiBindo), int(kelas))

        # Insert student node into AVL tree
        if root_siswa is None or not ctypes.cast(root_siswa, ctypes.c_void_p).value:
            root_siswa = ctypes.POINTER(AVLSiswa)

        try:
            new_root_siswa = gabung.insertDataSiswa(root_siswa, student_node)
            if new_root_siswa:
                root_siswa = new_root_siswa
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert student data: {e}")
            return

        # Export to CSV file
        export_filename = "sma_students_data1.csv"
        try:
            gabung.writeStudentsToFile(root_siswa, export_filename.encode())
            messagebox.showinfo("Export Success", f"Student data exported to {export_filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export student data: {e}")

        # Show success message and navigate back
        messagebox.showinfo("Success", "Student data successfully added!")
        insert_window.destroy()
        main_datasiswa_window(current_user)

    def validate_input(fullname, kelas, nilaiMat, nilaiFis, nilaiKim, nilaiBio, nilaiBindo):
        if not fullname or not kelas or not nilaiMat or not nilaiFis or not nilaiKim or not nilaiBio or not nilaiBindo:
            messagebox.showerror("Error", "Please fill in all fields")
            return False

        if len(fullname) < 2 or len(fullname) > 90:
            messagebox.showerror("Error", "Fullname must be between 2 and 90 characters")
            return False
        
        # Validate fullname using isValidName
        fullname_bytes = fullname.encode()
        if not gabung.isValidName(fullname_bytes):
            messagebox.showerror("Error", "Invalid fullname format")
            return False
        
        try:
            kelas = int(kelas)
            nilaiMat = int(nilaiMat)
            nilaiFis = int(nilaiFis)
            nilaiKim = int(nilaiKim)
            nilaiBio = int(nilaiBio)
            nilaiBindo = int(nilaiBindo)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for class and scores")
            return False

        if kelas not in [10, 11, 12]:
            messagebox.showerror("Error", "Class must be 10, 11, or 12")
            return False

        if any(not (0 <= score <= 100) for score in [nilaiMat, nilaiFis, nilaiKim, nilaiBio, nilaiBindo]):
            messagebox.showerror("Error", "Scores must be between 0 and 100")
            return False

        return True
    
    submit_button = tk.Button(insert_window, text="Submit", font=("Arial", 12, 'bold'), bg="#4CAF50", fg="white", width=20, height=2, padx=10, command=get_student_data)
    submit_button.pack(pady=10)

    def go_back():
        insert_window.destroy()
        main_datasiswa_window(current_user)

    back_button = tk.Button(insert_window, text="Back", font=("Arial", 12, 'bold'), bg="#f0f0f0", fg="#102c57", width=20, height=2, padx=10, command=go_back)
    back_button.pack(pady=10)  # Increased padding around back_button

    insert_window.mainloop()


##############################################################################

# Case 2 (Menu)
def sort_view_export_students():
    global root_siswa

    global sort_export_window

    # Create the main window
    sort_export_window = Toplevel()
    sort_export_window.title("Sort, View, and Export Student Grades")
    sort_export_window.geometry("800x600")
    # Define a function to handle window close event
    def on_close():
        close_sort_export_window()

    # Set the window close event to call the on_close function
    sort_export_window.protocol("WM_DELETE_WINDOW", on_close)

    # Add buttons for each sorting and exporting option
    Button(sort_export_window, text="Sort by Name", command=sort_by_name).pack() # Case 1
    Button(sort_export_window, text="Sort by Score", command=sort_by_score).pack() # Case 2
    Button(sort_export_window, text="Sort by Ranking", command=sort_by_ranking).pack() # Case 3
    Button(sort_export_window, text="Sort by Class", command=sort_by_class).pack() # Case 4
    Button(sort_export_window, text="View All Students", command=display_unsorted_students).pack() # Case 5
    Button(sort_export_window, text="Search Students", command=lambda: searching_siswa(root_siswa, sort_export_window)).pack() # Case 6
    Button(sort_export_window, text="Export Grades (Unsorted)", command=lambda: export(b"Unsorted_", "Unsorted File")).pack() # Case 7
    Button(sort_export_window, text="Back", command=close_sort_export_window).pack()


    
# Case 2 (Case 1)
def sort_by_name():
    # Create a new window for sorting options
    close_sort_export_window()
    sort_window = Toplevel()
    sort_window.title("Sorting Options")
    sort_window.geometry("800x600")

    # Create a label and radio buttons for sorting options
    label = Label(sort_window, text="Sort by name:")
    label.pack(pady=10)

    sorting_options = IntVar()
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareNameAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareNameDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareNameAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByName_", "Sorted Students by Name")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_export():
        sort_window.destroy()
        sort_view_export_students()

    back_button = Button(sort_window, text="Back", command=back_to_sort_export)
    back_button.pack(pady=10)
    
    
# Case 2 (Case 2)
def sort_by_score():
    close_sort_export_window()
    window = Toplevel()
    window.title("Sort by Score")
    window.geometry("800x600")  
    label = tk.Label(window, text="Sort by Score")
    label.pack()
    button_frame = tk.Frame(window)
    button_frame.pack()
    matematika_button = tk.Button(button_frame, text="Matematika", command=lambda: change_window(window, matematika_window))
    fisika_button = tk.Button(button_frame, text="Fisika", command=lambda: change_window(window, fisika_window))
    kimia_button = tk.Button(button_frame, text="Kimia", command=lambda: change_window(window, kimia_window))
    biologi_button = tk.Button(button_frame, text="Biologi", command=lambda: change_window(window, biologi_window))
    b_indonesia_button = tk.Button(button_frame, text="B. Indonesia", command=lambda: change_window(window, b_indonesia_window))
    back_button = tk.Button(button_frame, text="Back", command=lambda: change_window(window, sort_view_export_students))
    matematika_button.pack()
    fisika_button.pack()
    kimia_button.pack()
    biologi_button.pack()
    b_indonesia_button.pack()
    back_button.pack()
    window.mainloop()

def change_window(window, new_window):
    window.destroy()
    new_window()

def matematika_window():
    sort_window = Toplevel()
    sort_window.title("Matematika")
    sort_window.geometry("800x600")  # Set the window size to 800x600

    # Create a label and radio buttons for sorting options
    label = tk.Label(sort_window, text="Sort by Math Score:")
    label.pack(pady=10)

    sorting_options = IntVar(value=0)
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareMathAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareMathDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareMathAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByMatematika_", "Sorted Students by Math Score")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = tk.Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_by_score():
        sort_window.destroy()
        sort_by_score()

    back_button = tk.Button(sort_window, text="Back", command=back_to_sort_by_score)
    back_button.pack(pady=10)

    sort_window.mainloop()

def fisika_window():
    sort_window = Toplevel()
    sort_window.title("Physics")
    sort_window.geometry("800x600")  # Set the window size to 800x600

    # Create a label and radio buttons for sorting options
    label = tk.Label(sort_window, text="Sort by Physics Score:")
    label.pack(pady=10)

    sorting_options = IntVar(value=0)
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.comparePhysicsAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.comparePhysicsDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.comparePhysicsAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByFisika_", "Sorted Students by Physics Score")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = tk.Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_by_score():
        sort_window.destroy()
        sort_by_score()

    back_button = tk.Button(sort_window, text="Back", command=back_to_sort_by_score)
    back_button.pack(pady=10)

    sort_window.mainloop()


def kimia_window():
    sort_window = Toplevel()
    sort_window.title("Chemicals")
    sort_window.geometry("800x600")  # Set the window size to 800x600

    # Create a label and radio buttons for sorting options
    label = tk.Label(sort_window, text="Sort by Chemical Score:")
    label.pack(pady=10)

    sorting_options = IntVar(value=0)
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareChemistryAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareChemistryDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareChemistryAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByKimia_", "Sorted Students by Chemical Score")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = tk.Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_by_score():
        sort_window.destroy()
        sort_by_score()

    back_button = tk.Button(sort_window, text="Back", command=back_to_sort_by_score)
    back_button.pack(pady=10)

    sort_window.mainloop()

def biologi_window():
    sort_window = Toplevel()
    sort_window.title("Biology")
    sort_window.geometry("800x600")  # Set the window size to 800x600

    # Create a label and radio buttons for sorting options
    label = tk.Label(sort_window, text="Sort by Biology Score:")
    label.pack(pady=10)

    sorting_options = IntVar(value=0)
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareBiologyAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareBiologyDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareBiologyAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByBiologi_", "Sorted Students by Biology Score")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = tk.Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_by_score():
        sort_window.destroy()
        sort_by_score()

    back_button = tk.Button(sort_window, text="Back", command=back_to_sort_by_score)
    back_button.pack(pady=10)

    sort_window.mainloop()

def b_indonesia_window():
    sort_window = Toplevel()
    sort_window.title("Indonesian Language")
    sort_window.geometry("800x600")  # Set the window size to 800x600

    # Create a label and radio buttons for sorting options
    label = tk.Label(sort_window, text="Sort by Indonesian Language Score:")
    label.pack(pady=10)

    sorting_options = IntVar(value=0)
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareIndonesianAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareIndonesianDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareIndonesianAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByBindo_", "Sorted Students by Indonesian Language Score")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = tk.Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_by_score():
        sort_window.destroy()
        sort_by_score()

    back_button = tk.Button(sort_window, text="Back", command=back_to_sort_by_score)
    back_button.pack(pady=10)

    sort_window.mainloop()

    


# Case 2 (Case 3)
def sort_by_ranking():
    # Create a new window for sorting options
    close_sort_export_window()
    sort_window = Toplevel()
    sort_window.title("Sorting Options")
    sort_window.geometry("800x600")

    # Create a label and radio buttons for sorting options
    label = Label(sort_window, text="Sort by Rank:")
    label.pack(pady=10)

    sorting_options = IntVar()
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareRataRataAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareRataRataDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareRataRataAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByRank_", "Sorted Students by Rank")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_export():
        sort_window.destroy()
        sort_view_export_students()

    back_button = Button(sort_window, text="Back", command=back_to_sort_export)
    back_button.pack(pady=10)


# Case 2 (Case 4)

def sort_by_class():
    # Create a new window for sorting options
    close_sort_export_window()
    sort_window = Toplevel()
    sort_window.title("Sorting Options")
    sort_window.geometry("800x600")

    # Create a label and radio buttons for sorting options
    label = Label(sort_window, text="Sort by Class:")
    label.pack(pady=10)

    sorting_options = IntVar()
    ascending_radio = Radiobutton(sort_window, text="Ascending", variable=sorting_options, value=1)
    ascending_radio.pack()
    descending_radio = Radiobutton(sort_window, text="Descending", variable=sorting_options, value=2)
    descending_radio.pack()

    # Create a button to proceed with sorting
    def proceed_with_sorting():
        # Get the selected sorting option
        sorting_option = sorting_options.get()

        # Read students from CSV
        students, count = read_students_from_csv(b"sma_students_data1.csv")

        # Convert to ctypes array
        students_array = (Student * count)()
        for i in range(count):
            students_array[i] = students[i]

        # Set the comparison function based on the sorting option
        if sorting_option == 1:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareClassAsc)
        elif sorting_option == 2:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareClassDesc)
        else:
            cmp_func = ctypes.CFUNCTYPE(c_int, c_void_p, c_void_p)(gabung.compareClassAsc)

        # Sort the array using qsort
        qsort(students_array, count, ctypes.sizeof(Student), cmp_func)

        # Display sorted students in a table
        display_sorted_students(students_array, count, b"ByKelas_", "Sorted Students by Class")

        # Close the sorting options window
        sort_window.destroy()

    proceed_button = Button(sort_window, text="Proceed", command=proceed_with_sorting)
    proceed_button.pack(pady=10)

    # Create a back button to reopen the sort_export_window
    def back_to_sort_export():
        sort_window.destroy()
        sort_view_export_students()

    back_button = Button(sort_window, text="Back", command=back_to_sort_export)
    back_button.pack(pady=10)

# Display sorted data 
def display_sorted_students(students_array, count, filename_c, title):
    # Create a new window to display the sorted students
    table_window = Toplevel()
    table_window.title(title)
    table_window.geometry("1000x600")

    text_area = Text(table_window, width=120, height=30)
    text_area.pack(pady=20)

    # Insert headers
    text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")
    text_area.insert(tk.END, "| ID Siswa   | %-18s | Kelas | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Rata-Rata | Grade |\n" % "Nama Lengkap")
    text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Insert student data
    for idx, student in enumerate(students_array):
        formatted_name = format_name_display(student.name)
        text_area.insert(tk.END, "| %-10s | %-18s | %-5s | %-10d | %-6d | %-5d | %-7d | %-12d | %-9.2f | %-5c |\n" % (
            student.studentID.decode(),
            formatted_name,
            student.kelas.decode(),
            student.nilai_matematika,
            student.nilai_fisika,
            student.nilai_kimia,
            student.nilai_biologi,
            student.nilai_bahasa_indonesia,
            student.rata_rata,
            student.grade.decode()
        ))
        # Insert separator line after each row, except for the last row
        if idx < count:
            text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Buttons for options
    def go_back():
        table_window.destroy()

    def export_to_csv(filename_c, title):
        generateExportName = gabung.generateExportName
        unique_filename_c = generateExportName(filename_c)

        # Convert C-style string back to Python string
        unique_filename = unique_filename_c.decode()

        # Construct CSV header
        csv_header = "Sorted Students\n"
        csv_header += f"Exported from: {title}\n"
        csv_header += "----------------------------------------------------------------------------------------------------------------------\n"
        csv_header += "| ID Siswa   | %-18s | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Kelas | Rata-Rata | Grade |\n" % "Nama Lengkap"
        csv_header += "----------------------------------------------------------------------------------------------------------------------\n"

        # Now use this unique_filename and csv_header in your export logic
        gabung.eksportarr(students_array, count, unique_filename_c, csv_header)

        # Show success message
        messagebox.showinfo("Export Success", f"File is exported successfully with the filename: {unique_filename}")

    Button(table_window, text="Back", command=go_back).pack(side=tk.LEFT, padx=10)
    Button(table_window, text="Export to CSV", command=lambda: export_to_csv(filename_c, title)).pack(side=tk.LEFT, padx=10)
    
   
# Case 2 (Case 5)   
def display_unsorted_students():
    # Read students from CSV
    close_sort_export_window()
    students, count = read_students_from_csv(b"sma_students_data1.csv")

    # Convert to ctypes array
    students_array = (Student * count)()
    for i in range(count):
        students_array[i] = students[i]

    # Create a new window to display the unsorted students
    sort_window = Toplevel()
    sort_window.title("Unsorted Data")
    sort_window.geometry("1000x600")

    text_area = Text(sort_window, width=120, height=30)
    text_area.pack(pady=20)

    # Insert headers
    text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")
    text_area.insert(tk.END, "| ID Siswa   | %-18s | Kelas | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Rata-Rata | Grade |\n" % "Nama Lengkap")
    text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Insert student data
    for idx, student in enumerate(students_array):
        formatted_name = format_name_display(student.name)
        text_area.insert(tk.END, "| %-10s | %-18s | %-5s | %-10d | %-6d | %-5d | %-7d | %-12d | %-9.2f | %-5c |\n" % (
            student.studentID.decode(),
            formatted_name,
            student.kelas.decode(),
            student.nilai_matematika,
            student.nilai_fisika,
            student.nilai_kimia,
            student.nilai_biologi,
            student.nilai_bahasa_indonesia,
            student.rata_rata,
            student.grade.decode()
        ))
        # Insert separator line after each row, except for the last row
        if idx < count - 1:
            text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Buttons for options
    def back_to_sort_export():
        sort_window.destroy()
        sort_view_export_students()

    back_button = Button(sort_window, text="Back", command=back_to_sort_export)
    back_button.pack(pady=10)


# Case 2 (Case 6)
def searching_siswa(root_siswa, previous_window):
    def destroy_previous_window(window):
        if isinstance(window, tk.Toplevel) or isinstance(window, tk.Tk):
            window.destroy()

    # Close the previous window if it exists
    destroy_previous_window(previous_window)
    search_window = tk.Toplevel()
    search_window.title("Search Students")
    search_window.geometry("1000x600")

    def handle_search(search_type, entry_widget):
        search_param = entry_widget.get().strip()
        if not search_param:
            messagebox.showwarning("Input Error", f"Please enter a {search_type} to search.")
            return

        try:
            if search_type == "ID":
                result = search_id_containing(root_siswa, search_param.encode())
            elif search_type == "Class":
                result = search_by_class(root_siswa, int(search_param))
            elif search_type == "Name":
                result = search_by_name(root_siswa, search_param.encode())
            else:
                messagebox.showerror("Error", "Invalid search type.")
                return

            if result:
                display_search_result(result)
            else:
                messagebox.showinfo("Search Result", f"No students found with {search_type}: {search_param}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search students: {e}")

    def search_id_containing(root, studentIDSubstring):
        found_students_array = (ctypes.POINTER(DataSiswa) * 800)()
        count = ctypes.c_int(0)

        total_found = gabung.searchIDContaining(
            root,
            studentIDSubstring,
            found_students_array,
            ctypes.byref(count)
        )

        result = [found_students_array[i].contents for i in range(count.value)]
        return result

    def search_by_class(root_siswa, class_id):
        student_array = StudentArray()
        gabung.searchByClassHelper(root_siswa, class_id, ctypes.byref(student_array))
        
        result = []
        for i in range(student_array.count):
            result.append(student_array.data[i].contents)
        
        return result

    def search_by_name(root_siswa, name):
        student_array = StudentArray()
        gabung.searchByName(root_siswa, name, ctypes.byref(student_array))
        
        result = []
        for i in range(student_array.count):
            result.append(student_array.data[i].contents)
        
        return result

    def display_search_result(result):
        result_window = tk.Toplevel()
        result_window.title("Search Result")
        result_window.geometry("1000x600")

        text_area = tk.Text(result_window, width=120, height=30)
        text_area.pack(pady=20)

        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")
        text_area.insert(tk.END, "| ID Siswa   | %-18s | Kelas | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Rata-Rata | Grade |\n" % "Nama Lengkap")
        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

        for student in result:
            formatted_name = format_name_display(student.fullname)
            text_area.insert(tk.END, "| %-10s | %-18s | %-5s | %-10d | %-6d | %-5d | %-7d | %-12d | %-9.2f | %-5s |\n" % (
                student.studentID.decode(),
                formatted_name,
                str(student.kelas),
                student.nilaiMat,
                student.nilaiFis,
                student.nilaiKim,
                student.nilaiBio,
                student.nilaiBindo,
                student.rata2,
                student.grade.decode()
            ))
            text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Labels and entry widgets for inputs
    id_label = tk.Label(search_window, text="Search by ID:")
    id_label.grid(row=0, column=0, padx=10, pady=10)
    id_entry = tk.Entry(search_window)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    class_label = tk.Label(search_window, text="Search by Class:")
    class_label.grid(row=1, column=0, padx=10, pady=10)
    class_entry = tk.Entry(search_window)
    class_entry.grid(row=1, column=1, padx=10, pady=10)

    name_label = tk.Label(search_window, text="Search by Name:")
    name_label.grid(row=2, column=0, padx=10, pady=10)
    name_entry = tk.Entry(search_window)
    name_entry.grid(row=2, column=1, padx=10, pady=10)

    # Buttons for search actions
    tk.Button(search_window, text="Search by ID", command=lambda: handle_search("ID", id_entry)).grid(row=0, column=2, padx=10, pady=10)
    tk.Button(search_window, text="Search by Class", command=lambda: handle_search("Class", class_entry)).grid(row=1, column=2, padx=10, pady=10)
    tk.Button(search_window, text="Search by Name", command=lambda: handle_search("Name", name_entry)).grid(row=2, column=2, padx=10, pady=10)

    # Back button to return to previous window
    def go_back():
        search_window.destroy()  # Destroy the search window
        sort_view_export_students()

    back_button = tk.Button(search_window, text="Back", command=go_back)
    back_button.grid(row=3, column=1, pady=10)

    search_window.protocol("WM_DELETE_WINDOW", go_back)  # Handle window close button

    search_window.mainloop()

# Case 2 (Case 7)

def export(filename_c, title):
    students, count = read_students_from_csv(b"sma_students_data1.csv")

    # Convert to ctypes array
    students_array = (Student * count)()
    for i in range(count):
        students_array[i] = students[i]
        
    generateExportName = gabung.generateExportName
    unique_filename_c = generateExportName(filename_c)

    # Convert C-style string back to Python string
    unique_filename = unique_filename_c.decode()

    # Construct CSV header
    csv_header = "Sorted Students\n"
    csv_header += f"Exported from: {title}\n"
    csv_header += "----------------------------------------------------------------------------------------------------------------------\n"
    csv_header += "| ID Siswa   | %-18s | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Kelas | Rata-Rata | Grade |\n" % "Nama Lengkap"
    csv_header += "----------------------------------------------------------------------------------------------------------------------\n"

    # Now use this unique_filename and csv_header in your export logic
    gabung.eksportarr(students_array, count, unique_filename_c, csv_header.encode('utf-8'))

    # Show success message
    messagebox.showinfo("Export Success", f"File is exported successfully with the filename: {unique_filename}")

##############################################################################

# Case 3 (Update)
def update_student_info(root_siswa, previous_window):
    def destroy_previous_window(window):
        if isinstance(window, tk.Toplevel) or isinstance(window, tk.Tk):
            window.destroy()

    # Close the previous window if it exists
    destroy_previous_window(previous_window)

    update_window = tk.Toplevel()
    update_window.title("Update Student Information")
    update_window.geometry("500x600")

    # Function to search by name
    def handle_search(search_type, entry_widget):
        search_param = entry_widget.get().strip()
        if not search_param:
            messagebox.showwarning("Input Error", f"Please enter a {search_type} to search.")
            return
        search_type == "Name"
        try:
            if search_type == "ID":
                result_ptr = gabung.searchID(root_siswa, search_param.encode())
                if result_ptr:
                    result = [result_ptr.contents]
                else:
                    result = None
            elif search_type == "Name":
                result = search_by_name(root_siswa, search_param.encode())
            else:
                messagebox.showerror("Error", "Invalid search type.")
                return

            if result:
                display_search_result(result)
            else:
                messagebox.showinfo("Search Result", f"No students found with {search_type}: {search_param}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search students: {e}")

    def search_by_name(root_siswa, name):
        student_array = StudentArray()
        gabung.searchByName(root_siswa, name, ctypes.byref(student_array))
        
        result = []
        for i in range(student_array.count):
            result.append(student_array.data[i].contents)
        
        return result

    def display_search_result(result):
        result_window = tk.Toplevel()
        result_window.title("Search Result")
        result_window.geometry("1000x600")

        text_area = tk.Text(result_window, width=120, height=30)
        text_area.pack(pady=20)

        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")
        text_area.insert(tk.END, "| ID Siswa   | %-18s | Kelas | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Rata-Rata | Grade |\n" % "Nama Lengkap")
        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

        for student in result:
            formatted_name = format_name_display(student.fullname)
            text_area.insert(tk.END, "| %-10s | %-18s | %-5s | %-10d | %-6d | %-5d | %-7d | %-12d | %-9.2f | %-5s |\n" % (
                student.studentID.decode(),
                formatted_name,
                str(student.kelas),
                student.nilaiMat,
                student.nilaiFis,
                student.nilaiKim,
                student.nilaiBio,
                student.nilaiBindo,
                student.rata2,
                student.grade.decode()
            ))
            text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    # Labels and entry widgets for searching by name
    name_search_label = tk.Label(update_window, text="Search by Name:")
    name_search_label.grid(row=0, column=0, padx=10, pady=10)
    name_search_entry = tk.Entry(update_window)
    name_search_entry.grid(row=0, column=1, padx=10, pady=10)

    # Button for searching by name
    search_name_button = tk.Button(update_window, text="Search by Name", command=lambda: handle_search("Name", name_search_entry))
    search_name_button.grid(row=0, column=2, padx=10, pady=10)

    # Labels and entry widgets for updating fields
    fields = [("Full Name", "fullname"), 
              ("Class", "kelas"), 
              ("Mathematics", "nilaiMat"), 
              ("Physics", "nilaiFis"), 
              ("Chemistry", "nilaiKim"), 
              ("Biology", "nilaiBio"), 
              ("B. Indonesia", "nilaiBindo")]

    entries = {}

    for i, (label_text, field_name) in enumerate(fields, start=1):
        label = tk.Label(update_window, text=f"{label_text}:")
        label.grid(row=i, column=0, padx=10, pady=10)
        entry = tk.Entry(update_window)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries[field_name] = entry

    def handle_update():
        try:
            student_id = id_entry.get().strip()
            if not student_id:
                messagebox.showwarning("Input Error", "Please enter the student ID.")
                return

            update_ptr = gabung.searchID(root_siswa, student_id.encode())
            if not update_ptr:
                messagebox.showerror("Error", "Student ID not found.")
                return

            update = update_ptr.contents

            for field_name, entry in entries.items():
                value = entry.get().strip()
                if value:
                    if field_name == "fullname":
                        if 2 <= len(value) <= 90:
                            if gabung.isValidName(value.encode()):
                                formatted_name = format_name_display(value.encode())
                                ctypes.memmove(update.fullname, formatted_name.encode(), len(formatted_name)+1)
                            else:
                                messagebox.showwarning("Input Error", "Invalid name format.")
                                return
                        else:
                            messagebox.showwarning("Input Error", "Full name must be between 2 and 90 characters.")
                            return
                    elif field_name == "kelas":
                        try:
                            kelas = int(value)
                            if kelas in [10, 11, 12]:
                                update.kelas = kelas
                            else:
                                messagebox.showwarning("Input Error", "Class must be 10, 11, or 12.")
                                return
                        except ValueError:
                            messagebox.showwarning("Input Error", "Invalid class format.")
                            return
                    else:
                        try:
                            score = int(value)
                            if 0 <= score <= 100:
                                setattr(update, field_name, score)
                            else:
                                messagebox.showwarning("Input Error", f"{field_name} score must be between 0 and 100.")
                                return
                        except ValueError:
                            messagebox.showwarning("Input Error", f"Invalid {field_name} score format.")
                            return

            update.rata2 = (update.nilaiMat + update.nilaiFis + update.nilaiKim + update.nilaiBio + update.nilaiBindo) / 5.0
            update.grade = gabung.generateGrade(update.rata2)
            gabung.writeStudentsToFile(root_siswa, ctypes.c_char_p(b"sma_students_data1.csv"))
            messagebox.showinfo("Success", "Student information updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating student information: {e}")

    # Entry widget for student ID
    id_label = tk.Label(update_window, text="Student ID:")
    id_label.grid(row=len(fields)+1, column=0, padx=10, pady=10)
    id_entry = tk.Entry(update_window)
    id_entry.grid(row=len(fields)+1, column=1, padx=10, pady=10)

    # Update button
    update_button = tk.Button(update_window, text="Update", command=handle_update)
    update_button.grid(row=len(fields)+2, columnspan=2, pady=20)

    # Back button
    def back_to_main_window(update_window, current_user):
        update_window.destroy()
        main_datasiswa_window(current_user)

    back_button = tk.Button(update_window, text="Back", command=lambda: back_to_main_window(update_window, current_user))
    back_button.grid(row=len(fields)+3, columnspan=2, pady=20)

##############################################################################

# Case 4 (Delete)
def delete_student(current_user):
    global root_siswa  # Ensure root_siswa is accessible globally

    # Function to destroy previous window if it's a Tkinter object
    def destroy_previous_window(window):
        if isinstance(window, tk.Toplevel) or isinstance(window, tk.Tk):
            window.destroy()

    # Close the previous window if it exists
    if current_user:
        destroy_previous_window(current_user)

    # Create the delete student data window
    delete_window = tk.Tk()
    delete_window.title("Delete Student Data")
    delete_window.geometry("400x200")
    delete_window.configure(bg="#f0f0f0")

    # Define entry widget for student ID
    student_id_label = tk.Label(delete_window, text="Student ID:")
    student_id_label.grid(row=0, column=0, padx=10, pady=10)
    student_id_entry = tk.Entry(delete_window)
    student_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # Labels and entry widgets for searching by name
    name_search_label = tk.Label(delete_window, text="Search by Name:")
    name_search_label.grid(row=1, column=0, padx=10, pady=10)
    name_search_entry = tk.Entry(delete_window)
    name_search_entry.grid(row=1, column=1, padx=10, pady=10)

    def delete_student_data():
        global root_siswa  # Access root_siswa from the global scope

        student_id = student_id_entry.get()

        # Validate student ID input
        if not student_id:
            messagebox.showerror("Error", "Please enter student ID")
            return

        # Convert student_id to bytes
        student_id_bytes = student_id.encode()

        # Check if student ID exists
        try:
            result_ptr = gabung.searchID(root_siswa, student_id_bytes)
            if not result_ptr:
                raise ValueError(f"Student ID '{student_id}' not found")

            # Delete student node from AVL tree
            if root_siswa is None or not ctypes.cast(root_siswa, ctypes.c_void_p).value:
                root_siswa = ctypes.POINTER(AVLSiswa)
            
            new_root_siswa = gabung.deleteDataSiswa(root_siswa, student_id_bytes)
            
            if new_root_siswa is None:
                raise ValueError(f"Failed to delete student ID '{student_id}'")

            root_siswa = new_root_siswa

            # Write updated AVL tree to CSV file
            export_filename = "sma_students_data1.csv"
            gabung.writeStudentsToFile(root_siswa, export_filename.encode())
            messagebox.showinfo("Export Success", f"Student data exported to {export_filename}")

            # Show success message
            messagebox.showinfo("Success", "Student data successfully deleted!")
            delete_window.destroy()

        except ValueError as ve:
            messagebox.showerror("Delete Error", str(ve))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student data: {e}")

    def handle_search(search_type, entry_widget):
        search_param = entry_widget.get().strip()
        if not search_param:
            messagebox.showwarning("Input Error", f"Please enter a {search_type} to search.")
            return
        try:
            if search_type == "ID":
                result_ptr = gabung.searchID(root_siswa, search_param.encode())
                if result_ptr:
                    result = [result_ptr.contents]
                else:
                    result = None
            elif search_type == "Name":
                result = search_by_name(root_siswa, search_param.encode())
            else:
                messagebox.showerror("Error", "Invalid search type.")
                return

            if result:
                display_search_result(result)
            else:
                messagebox.showinfo("Search Result", f"No students found with {search_type}: {search_param}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search students: {e}")

    def search_by_name(root_siswa, name):
        student_array = StudentArray()
        gabung.searchByName(root_siswa, name, ctypes.byref(student_array))
        
        result = []
        for i in range(student_array.count):
            result.append(student_array.data[i].contents)
        
        return result

    def display_search_result(result):
        result_window = tk.Toplevel()
        result_window.title("Search Result")
        result_window.geometry("1000x600")

        text_area = tk.Text(result_window, width=120, height=30)
        text_area.pack(pady=20)

        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")
        text_area.insert(tk.END, "| ID Siswa   | %-18s | Kelas | Matematika | Fisika | Kimia | Biologi | B. Indonesia | Rata-Rata | Grade |\n" % "Nama Lengkap")
        text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

        for student in result:
            formatted_name = format_name_display(student.fullname)
            text_area.insert(tk.END, "| %-10s | %-18s | %-5s | %-10d | %-6d | %-5d | %-7d | %-12d | %-9.2f | %-5s |\n" % (
                student.studentID.decode(),
                formatted_name,
                str(student.kelas),
                student.nilaiMat,
                student.nilaiFis,
                student.nilaiKim,
                student.nilaiBio,
                student.nilaiBindo,
                student.rata2,
                student.grade.decode()
            ))
            text_area.insert(tk.END, "----------------------------------------------------------------------------------------------------------------------\n")

    def go_back():
        delete_window.destroy()
        # Add navigation back to main window if needed

    # Button for searching by name
    search_name_button = tk.Button(delete_window, text="Search by Name", command=lambda: handle_search("Name", name_search_entry))
    search_name_button.grid(row=1, column=2, padx=10, pady=10)

    # Button for deleting student data
    delete_button = tk.Button(delete_window, text="Delete", command=delete_student_data)
    delete_button.grid(row=2, column=0, padx=10, pady=10)

    # Button for going back
    back_button = tk.Button(delete_window, text="Back", command=go_back)
    back_button.grid(row=2, column=1, padx=10, pady=10)

    delete_window.mainloop()
    
##############################################################################


# Case 5 (plot)
def traverse_and_collect_scores(node, class_filter=None):
    if not node:
        return [], [], [], [], []
    
    data = node.contents.data.contents
    if class_filter is None or data.kelas == class_filter:
        mat_scores = [data.nilaiMat]
        fis_scores = [data.nilaiFis]
        kim_scores = [data.nilaiKim]
        bio_scores = [data.nilaiBio]
        bindo_scores = [data.nilaiBindo]
    else:
        mat_scores, fis_scores, kim_scores, bio_scores, bindo_scores = [], [], [], [], []

    left_scores = traverse_and_collect_scores(node.contents.left, class_filter)
    right_scores = traverse_and_collect_scores(node.contents.right, class_filter)

    return [
        mat_scores + left_scores[0] + right_scores[0],
        fis_scores + left_scores[1] + right_scores[1],
        kim_scores + left_scores[2] + right_scores[2],
        bio_scores + left_scores[3] + right_scores[3],
        bindo_scores + left_scores[4] + right_scores[4]
    ]

# Function to plot average scores
def plot(class_filter=None):
    global root_siswa

    # Load student data
    load_students_from_file()

    # Collect scores from AVL tree
    mat_scores, fis_scores, kim_scores, bio_scores, bindo_scores = traverse_and_collect_scores(root_siswa, class_filter)

    # Calculate average scores
    categories = ['Math', 'Physics', 'Chemistry', 'Biology', 'Indonesian']
    average_scores = [
        np.mean(mat_scores) if mat_scores else 0,
        np.mean(fis_scores) if fis_scores else 0,
        np.mean(kim_scores) if kim_scores else 0,
        np.mean(bio_scores) if bio_scores else 0,
        np.mean(bindo_scores) if bindo_scores else 0
    ]

    # Plot the average scores
    plt.figure(figsize=(10, 6))
    plt.bar(categories, average_scores, color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.xlabel('Subjects')
    plt.ylabel('Average Score')
    plt.title('Average Scores in Each Subject' + (f' for Class {class_filter}' if class_filter else ''))
    plt.ylim(0, 100)
    plt.show()

# Function to create the plotting window with buttons
def create_plotting_window(current_user):
    plot_window = tk.Toplevel()
    plot_window.title("Plot Average Scores")
    plot_window.geometry("500x300")

    tk.Button(plot_window, text="Plot Whole Average", command=lambda: plot()).pack(pady=10)
    tk.Button(plot_window, text="Plot Average for Class 10", command=lambda: plot(10)).pack(pady=10)
    tk.Button(plot_window, text="Plot Average for Class 11", command=lambda: plot(11)).pack(pady=10)
    tk.Button(plot_window, text="Plot Average for Class 12", command=lambda: plot(12)).pack(pady=10)
    def go_back():
        plot_window.destroy()
        main_datasiswa_window(plot_window, current_user)

    back_button = tk.Button(plot_window, text="Back", command=go_back)
    back_button.pack(pady=10)



##############################################################################
# teachers
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
    Label(root, text="Enter Email:", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
    email_entry = Entry(root, font=('Arial', 12), width=30, bg="#fff")
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Enter Teacher ID (10 digits):", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
    code_entry = Entry(root, font=('Arial', 12), width=30, bg="#fff")
    code_entry.grid(row=2, column=1, padx=10, pady=10)

    Label(root, text="Enter Fullname:", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
    fullname_entry = Entry(root, font=('Arial', 12), width=30, bg="#fff")
    fullname_entry.grid(row=3, column=1, padx=10, pady=10)

    register_button = Button(root, text="Register", font=('Arial', 12), bg="#4CAF50", fg="white", command=lambda: register_teacher(avl_root))
    register_button.grid(row=4, column=0, columnspan=2, pady=20)
    register_button.bind("<Enter>", lambda event, button=register_button: on_enter(event, button))
    register_button.bind("<Leave>", lambda event, button=register_button: on_leave(event, button))

    back_button = Button(root, text="Back", font=('Arial', 12), bg="#f0f0f0", command=show_main_menu)
    back_button.grid(row=5, column=0, columnspan=2, pady=10)
    back_button.bind("<Enter>", lambda event, button=back_button: on_enter(event, button))
    back_button.bind("<Leave>", lambda event, button=back_button: on_leave(event, button))

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(6, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    logo_label = Label(root, image=logo_tk, bg="#f0f0f0")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)

def verify_code():
    code = verification_code_entry.get().encode('utf-8')
    if gabung.verifyCode(code):
        messagebox.showinfo("Success", "Verification successful!")
        # Redirect to the main system or another part of the application
    else:
        messagebox.showerror("Error", "Verification failed! Incorrect code.")

def login_teacher(avl_root):
    username = login_username_entry.get()
    code_guru = login_code_entry.get()

    reload_avl_tree()

    teacher = gabung.search(avl_root, code_guru.encode('utf-8'))
    if teacher and teacher.contents.codeGuru.decode('utf-8') == code_guru and teacher.contents.fullname.decode('utf-8') == username:
        global current_user  # Declare current_user as global
        current_user = teacher.contents.fullname.decode('utf-8')  # Store the user's fullname
        # Generate verification code
        gabung.generateVerificationCode()

        destroy_all_children(root)
        global verification_code_entry
        messagebox.showinfo("Success", "Verification code has been written in verif.csv")
        Label(root, text="Enter Verification Code:", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky=E)
        verification_code_entry = Entry(root, font=('Arial', 12), width=30, bg="#f0f0f0")
        verification_code_entry.grid(row=0, column=1, padx=10, pady=10)

        Button(root, text="Verify", font=('Arial', 12, 'bold'), bg="#4CAF50", fg="white", command=lambda: verify_code_and_login()).grid(row=1, column=0, columnspan=2, pady=20)
    else:
        messagebox.showerror("Error", "Invalid username or Teacher ID. Please try again.")
        
def verify_code_and_login():
    code = verification_code_entry.get().encode('utf-8')
    if gabung.verifyCode(code):
        messagebox.showinfo("Success", "Verification successful!")
        main_datasiswa_window(root, current_user)  # Pass the root window object
    else:
        messagebox.showerror("Error", "Verification failed! Incorrect code.")

def animate_hover_in(button, color="#45a049", steps=10):
    def step_in(current_step):
        if current_step < steps:
            current_color = blend_colors(button.cget("bg"), color, current_step / steps)
            button.config(bg=current_color)
            button.after(10, step_in, current_step + 1)
    step_in(0)

def animate_hover_out(button, original_color, steps=10):
    def step_out(current_step):
        if current_step < steps:
            current_color = blend_colors(button.cget("bg"), original_color, current_step / steps)
            button.config(bg=current_color)
            button.after(10, step_out, current_step + 1)
    step_out(0)

def blend_colors(color1, color2, t):
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    r = int(r1 + (r2 - r1) * t) // 256
    g = int(g1 + (g2 - g1) * t) // 256
    b = int(b1 + (b2 - b1) * t) // 256
    return f"#{r:02x}{g:02x}{b:02x}"

def on_enter(event, button):
    animate_hover_in(button)

def on_leave(event, button):
    original_color = button.original_bg
    animate_hover_out(button, original_color)

def show_login_page(avl_root):
    destroy_all_children(root)

    global login_username_entry, login_code_entry
    Label(root, text="Enter Username:", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
    login_username_entry = Entry(root, font=('Arial', 12), width=30, bg="#fff")
    login_username_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Enter Teacher ID:", font=('Arial', 12, 'bold'), bg="#102c57", fg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
    login_code_entry = Entry(root, font=('Arial', 12), width=30, bg="#fff")
    login_code_entry.grid(row=2, column=1, padx=10, pady=10)

    login_button = Button(root, text="Login", font=('Arial', 12, 'bold'), bg="#4CAF50", fg="white", command=lambda: login_teacher(avl_root))
    login_button.grid(row=3, column=0, columnspan=2, pady=20)
    login_button.original_bg = login_button.cget("bg")
    login_button.bind("<Enter>", lambda event, button=login_button: on_enter(event, button))
    login_button.bind("<Leave>", lambda event, button=login_button: on_leave(event, button))

    back_button = Button(root, text="Back", font=('Arial', 12, 'bold'), bg="#f0f0f0", command=show_main_menu)
    back_button.grid(row=4, column=0, columnspan=2, pady=10)
    back_button.original_bg = back_button.cget("bg")
    back_button.bind("<Enter>", lambda event, button=back_button: on_enter(event, button))
    back_button.bind("<Leave>", lambda event, button=back_button: on_leave(event, button))

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    logo_label = Label(root, image=logo_tk, bg="#f0f0f0")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)

def show_main_menu():
    destroy_all_children(root)

    # Place the logo at the top
    logo_label = Label(root, image=logo_tk, bg="#f0f0f0")
    logo_label.pack(pady=10)

    # Create and place the register button
    register_button = Button(root, text="Register Teacher", font=('Arial', 14,'bold'), bg="#4CAF50", fg="white", command=lambda: show_registration_page(root_node))
    register_button.pack(pady=20)
    register_button.original_bg = register_button.cget("bg")
    register_button.bind("<Enter>", lambda event, button=register_button: on_enter(event, button))
    register_button.bind("<Leave>", lambda event, button=register_button: on_leave(event, button))

    # Create and place the login button
    login_button = Button(root, text="Login", font=('Arial', 14, 'bold'), bg="#4CAF50", fg="white", command=lambda: show_login_page(root_node))
    login_button.pack(pady=20)
    login_button.original_bg = login_button.cget("bg")
    login_button.bind("<Enter>", lambda event, button=login_button: on_enter(event, button))
    login_button.bind("<Leave>", lambda event, button=login_button: on_leave(event, button))

    root.pack_propagate(False)

root_node = gabung.loadTeachersFromFile(root_node, b"DataGuru.csv")



root = Tk()
root.title("Teacher Management System")
root.geometry("600x600")
root.configure(bg="#102c57")

# Load and resize the logo image
image = Image.open("teacher.png")
image = image.resize((200, 200), Image.LANCZOS)
logo_tk = ImageTk.PhotoImage(image)

show_main_menu()

root.mainloop()
