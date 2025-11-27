from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

#  File Paths
STUDENT_FILE = r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\studentMarks.txt"  # this is the file where all student marks are stored
BACKGROUND_IMAGE = r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\images\Student records extended task.jpg"  # background image path for GUI

# Window Setup 
root = Tk()  # creating main window
root.title("Student Records Manager - Ashraf")  # window title
root.geometry("1000x700")  # set window size
root.resizable(False, False)  # can't resize window

#  Colors and Theme 
BUTTON_BG = "#F1E3C9"  # button background color
BUTTON_FG = "black"  # button text color
BUTTON_ACTIVE = "#A0522D"  # button color when clicked
ROW_ODD = "#F1E3C9"  # odd row color in table
ROW_EVEN = "#D8C4A1"  # even row color in table
TABLE_BG = "#F1E3C9"  # table background color

# Background Image 
bg_img = Image.open(BACKGROUND_IMAGE)  # open the image
bg_img = bg_img.resize((1000, 700))  # resize image to window size
bg_photo = ImageTk.PhotoImage(bg_img)  # convert image to tkinter format
bg_label = Label(root, image=bg_photo)  # create label to show image
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # place it to cover whole window

# Calculation Functions
def calc_coursework_total(a, b, c):
    """Calculate total coursework marks"""
    return a + b + c  # just sum all 3 coursework marks

def calc_overall_total(coursework, exam):
    """Calculate overall marks including exam"""
    return coursework + exam  # add coursework total + exam marks

def calc_percentage(overall, max_marks=160):
    """Convert overall marks into percentage"""
    return (overall / max_marks) * 100  # simple percentage calculation

def calc_grade(percentage):
    """Assign grade based on percentage"""
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"  # classic grading system

# File Handling 
def load_students(file_path):
    """Read student records from file"""
    students = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:  # open file
            for line in f:  # read line by line
                line = line.strip()  # remove extra spaces
                if not line:  # skip empty lines
                    continue
                parts = line.split(",")  # split by comma
                if len(parts) < 6:  # check if line has all info
                    continue
                try:
                    student_id = parts[0].strip()
                    name = parts[1].strip()
                    c1, c2, c3, exam = map(int, parts[2:6])  # convert marks to int
                except ValueError:
                    continue  # skip invalid lines
                coursework_total = calc_coursework_total(c1, c2, c3)  # calculate coursework
                overall_total = calc_overall_total(coursework_total, exam)  # calculate overall
                percentage = calc_percentage(overall_total)  # percentage
                grade = calc_grade(percentage)  # grade
                students.append({  # save all info in dict
                    "id": student_id,
                    "name": name,
                    "c1": c1,
                    "c2": c2,
                    "c3": c3,
                    "coursework_total": coursework_total,
                    "exam": exam,
                    "overall_total": overall_total,
                    "percentage": percentage,
                    "grade": grade
                })
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Cannot find file:\n{file_path}")  # error if file missing
    return students  # return list of student dicts

def save_students(students):
    """Save students back to file"""
    try:
        with open(STUDENT_FILE, "w", encoding="utf-8") as f:
            for s in students:  # write each student back
                line = f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
                f.write(line)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save file:\n{e}")  # show error if can't save

#  Treeview Setup 
table_frame = Frame(root, bg=BUTTON_BG, bd=2, relief=RAISED)  # frame for table
table_frame.place(x=200, y=105, width=760, height=520)

columns = ("Name", "ID", "Coursework", "Exam", "Overall", "Percentage", "Grade")  # table columns
style = ttk.Style()
style.theme_use("default")  # default style
style.configure("Treeview", background=TABLE_BG, foreground="black", rowheight=35, fieldbackground=TABLE_BG)
style.configure("Treeview.Heading", background=BUTTON_BG, foreground=BUTTON_FG, relief="raised")
style.map('Treeview', background=[('selected', '#ececec')])  # change color when row selected

tree = ttk.Treeview(table_frame, columns=columns, show="headings")  # create table
tree.pack(fill=BOTH, expand=True)

# set column widths and alignment
tree.column("Name", width=180, anchor=W)
tree.column("ID", width=90, anchor=CENTER)
tree.column("Coursework", width=90, anchor=CENTER)
tree.column("Exam", width=70, anchor=CENTER)
tree.column("Overall", width=80, anchor=CENTER)
tree.column("Percentage", width=90, anchor=CENTER)
tree.column("Grade", width=60, anchor=CENTER)

for col in columns:
    tree.heading(col, text=col)  # set column headings

tree.tag_configure('oddrow', background=ROW_ODD)  # color for odd rows
tree.tag_configure('evenrow', background=ROW_EVEN)  # color for even rows

# Display Students
def display_students(student_list):
    """Populate table with student records"""
    tree.delete(*tree.get_children())  # clear table first
    for i, s in enumerate(student_list):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'  # alternate row colors
        tree.insert("", END, values=(  # insert row
            s["name"], s["id"], s["coursework_total"], s["exam"],
            s["overall_total"], f"{s['percentage']:.2f}", s["grade"]
        ), tags=(tag,))

#  Form Frame 
form_frame = Frame(root, bg=BUTTON_BG, bd=2, relief=RAISED)  # form for add/update/search
form_frame.place_forget()  # hide initially

def clear_form():
    """Clear all widgets in the form"""
    for widget in form_frame.winfo_children():
        widget.destroy()  # remove all widgets
    form_frame.place_forget()  # hide form

# Button Actions 
def load_action():
    students = load_students(STUDENT_FILE)  # load students from file
    if students:
        display_students(students)  # show all students in table

def highest_action():
    students = load_students(STUDENT_FILE)
    if students:
        top = max(students, key=lambda x: x["percentage"])  # find highest percentage
        display_students([top])  # show only top student

def lowest_action():
    students = load_students(STUDENT_FILE)
    if students:
        low = min(students, key=lambda x: x["percentage"])  # find lowest percentage
        display_students([low])  # show only lowest student

# Add Student
def add_action():
    clear_form()  # clear old form
    form_frame.place(x=200, y=105, width=760, height=300)  # show form
    labels = ["ID", "Name", "Coursework1", "Coursework2", "Coursework3", "Exam"]
    entries = []

    # Create entry fields
    for lbl in labels:
        row = Frame(form_frame, bg=BUTTON_BG)
        row.pack(pady=3, fill="x", padx=10)
        Label(row, text=lbl+":", width=12, anchor=W, bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(side=LEFT)
        e = Entry(row, font=("Helvetica",10))
        e.pack(side=LEFT, fill="x", expand=True)
        entries.append(e)

    def save_new_student():
        try:
            values = [e.get().strip() for e in entries]
            c1, c2, c3, exam = int(values[2]), int(values[3]), int(values[4]), int(values[5])
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for coursework/exam.")
            return

        students = load_students(STUDENT_FILE) or []
        coursework_total = calc_coursework_total(c1, c2, c3)
        overall_total = calc_overall_total(coursework_total, exam)
        percentage = calc_percentage(overall_total)
        grade = calc_grade(percentage)

        students.append({
            "id": values[0],
            "name": values[1],
            "c1": c1,
            "c2": c2,
            "c3": c3,
            "coursework_total": coursework_total,
            "exam": exam,
            "overall_total": overall_total,
            "percentage": percentage,
            "grade": grade
        })
        save_students(students)  # save new student to file
        display_students(students)  # refresh table
        form_frame.place_forget()  # hide form

    Button(form_frame, text="Add Student", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE,
           font=("Helvetica",10,"bold"), width=15, command=save_new_student).pack(pady=10)

# Delete Student 
def delete_action():
    clear_form()
    form_frame.place(x=200, y=105, width=760, height=200)
    Label(form_frame, text="Enter ID or Name to delete:", bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(pady=10)
    entry = Entry(form_frame, font=("Helvetica",10))
    entry.pack(pady=5)
    entry.focus_set()

    def remove_student():
        key = entry.get().strip()
        if not key: return
        students = load_students(STUDENT_FILE)
        if not students: return
        updated = [s for s in students if not (s["id"] == key or s["name"].lower() == key.lower())]
        if len(updated) == len(students):
            messagebox.showinfo("Not Found", "No student found with this ID/Name.")
            return
        save_students(updated)
        display_students(updated)
        form_frame.place_forget()

    Button(form_frame, text="Delete", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE,
           font=("Helvetica",10,"bold"), width=12, command=remove_student).pack(pady=10)

# Update Student 
def update_action():
    clear_form()
    form_frame.place(x=200, y=105, width=760, height=350)
    Label(form_frame, text="Enter ID of student to update:", bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(pady=5)
    entry_id = Entry(form_frame, font=("Helvetica",10))
    entry_id.pack(pady=5)
    entry_id.focus_set()

    labels = ["Name", "Coursework1", "Coursework2", "Coursework3", "Exam"]
    entries = []

    for lbl in labels:
        row = Frame(form_frame, bg=BUTTON_BG)
        row.pack(pady=3, fill="x", padx=10)
        Label(row, text=lbl+":", width=12, anchor=W, bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(side=LEFT)
        e = Entry(row, font=("Helvetica",10))
        e.pack(side=LEFT, fill="x", expand=True)
        entries.append(e)

    def save_update():
        sid = entry_id.get().strip()
        students = load_students(STUDENT_FILE)
        student = next((s for s in students if s["id"] == sid), None)
        if not student:
            messagebox.showinfo("Not Found", "Student not found.")
            return
        try:
            student["name"] = entries[0].get().strip()
            c1, c2, c3, exam = map(int, [e.get().strip() for e in entries[1:]])
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for coursework/exam.")
            return
        student["c1"], student["c2"], student["c3"], student["exam"] = c1, c2, c3, exam
        student["coursework_total"] = calc_coursework_total(c1, c2, c3)
        student["overall_total"] = calc_overall_total(student["coursework_total"], exam)
        student["percentage"] = calc_percentage(student["overall_total"])
        student["grade"] = calc_grade(student["percentage"])
        save_students(students)
        display_students(students)
        form_frame.place_forget()

    Button(form_frame, text="Update", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE,
           font=("Helvetica",10,"bold"), width=12, command=save_update).pack(pady=10)

#  Search Student 
def search_action():
    clear_form()
    form_frame.place(x=200, y=105, width=760, height=200)
    Label(form_frame, text="Enter ID or Name to search:", bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(pady=10)
    entry = Entry(form_frame, font=("Helvetica",10))
    entry.pack(pady=5)
    entry.focus_set()

    def do_search():
        key = entry.get().strip()
        students = load_students(STUDENT_FILE)
        found = [s for s in students if s["id"] == key or s["name"].lower() == key.lower()]
        if not found:
            messagebox.showinfo("Not Found", "Student not found.")
            return
        display_students(found)
        form_frame.place_forget()

    Button(form_frame, text="Search", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE,
           font=("Helvetica",10,"bold"), width=14, command=do_search).pack(pady=10)

# Sort Students 
def sort_action():
    clear_form()
    form_frame.place(x=200, y=105, width=760, height=200)
    students = load_students(STUDENT_FILE)
    if not students: return
    var = StringVar(value="asc")
    Radiobutton(form_frame, text="Ascending", variable=var, value="asc", bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(pady=5)
    Radiobutton(form_frame, text="Descending", variable=var, value="desc", bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica",10,"bold")).pack(pady=5)

    def do_sort():
        reverse = var.get() == "desc"
        sorted_list = sorted(students, key=lambda s: s["percentage"], reverse=reverse)
        display_students(sorted_list)
        form_frame.place_forget()

    Button(form_frame, text="Sort", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE,
           font=("Helvetica",10,"bold"), width=12, command=do_sort).pack(pady=10)

#  Main Buttons 
Button(root, text="Load File", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=load_action).place(x=15, y=50)  # load all students
Button(root, text="Highest", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=highest_action).place(x=15, y=110)  # show highest percentage
Button(root, text="Lowest", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=lowest_action).place(x=15, y=175)  # show lowest percentage
Button(root, text="Add", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=add_action).place(x=15, y=425)  # add new student
Button(root, text="Delete", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=delete_action).place(x=15, y=485)  # delete student
Button(root, text="Update", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=update_action).place(x=15, y=540)  # update student info
Button(root, text="Search", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, font=("Helvetica",10,"bold"), width=15, height=1, command=search_action).place(x=15, y=300)  # search student
Button(root, text="Sort", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, 
       font=("Helvetica",10,"bold"), width=15, height=1, command=sort_action).place(x=15, y=365)  # sort students by percentage

# Toggle Table Display 
def toggle_table():
    """Show or hide the main student table"""
    if table_frame.winfo_ismapped():  # if table is visible
        table_frame.place_forget()  # hide table
        toggle_btn.config(text="SHOW RECORDS", bg="#A0522D")  # update button text/color
    else:
        table_frame.place(x=200, y=105, width=760, height=520)  # show table
        toggle_btn.config(text="HIDE RECORDS", bg=BUTTON_BG)  # update button text/color

toggle_btn = Button(root, text="HIDE RECORDS", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, 
                    font=("Helvetica",10,"bold"), width=15, height=1, command=toggle_table)
toggle_btn.place(x=205, y=645)  # button to hide/show table

# Hide Form Button 
def hide_form():
    """Hide the form frame"""
    form_frame.place_forget()  # just hide the form

Button(root, text="HIDE FORM DISPLAY", bg=BUTTON_BG, fg=BUTTON_FG, activebackground=BUTTON_ACTIVE, 
       font=("Helvetica",9,"bold"), width=17, height=1, command=hide_form).place(x=380, y=645)  # button to hide form

# Run Application 
root.mainloop()  #run the app now
