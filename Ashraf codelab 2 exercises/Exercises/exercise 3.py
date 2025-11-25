from tkinter import *  
from tkinter import messagebox, ttk  
from PIL import Image, ImageTk  

# File Paths
FILE_PATH = r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\studentMarks.txt"  # this is where our student data is
BG_IMAGE_PATH = r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\images\Students records.jpg"  # background image

root = Tk()
root.title("Ashraf exercise 3 Student Records")  # window title
root.geometry("1000x700")  # size of window
root.resizable(0, 0)  

# Colors and Theme
BTN_BG = "#F1E3C9"  # button background color
BTN_FG = "black"    # button text color
ROW_ODD = "#F1E3C9"  
ROW_EVEN = "#D8C4A1"  
TABLE_BG = "#F1E3C9"  

# Background Image
bg_img = Image.open(BG_IMAGE_PATH)
bg_img = bg_img.resize((1000, 700))  # resize 
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1) 

frame_output = Frame(root, bg="#F4F4F4")
frame_output.place(x=200, y=105, width=760, height=520)  # position table nicely

columns = ("Name", "Number", "Coursework", "Exam", "Overall", "Percentage", "Grade")  # table columns

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Treeview",
    background=TABLE_BG,  # table background
    foreground="black",   # table text color
    rowheight=35,         # row height
    fieldbackground=TABLE_BG
)
style.configure(
    "Treeview.Heading",
    background=BTN_BG,  # heading background
    foreground=BTN_FG,  # heading text
    relief="raised"
)
style.map('Treeview', background=[('selected', '#ececec')])  

tree = ttk.Treeview(frame_output, columns=columns, show="")  # create table but hide headings for now
tree.pack(fill=BOTH, expand=True)  

# column widths
tree.column("Name", width=180, anchor=W)
tree.column("Number", width=90, anchor=CENTER)
tree.column("Coursework", width=90, anchor=CENTER)
tree.column("Exam", width=70, anchor=CENTER)
tree.column("Overall", width=80, anchor=CENTER)
tree.column("Percentage", width=90, anchor=CENTER)
tree.column("Grade", width=60, anchor=CENTER)

# Add column headers
for col in columns:
    tree.heading(col, text=col)  # set the headings text

tree.tag_configure('oddrow', background=ROW_ODD)
tree.tag_configure('evenrow', background=ROW_EVEN)

# Functions
def read_students_from_file(file_path):
    """Read all students, calculate totals and grades"""
    students = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue  # skip empty lines
                parts = line.split(",")
                if len(parts) < 6:
                    continue 
                try:
                    number = parts[0].strip()
                    name = parts[1].strip()
                    c1 = int(parts[2].strip())
                    c2 = int(parts[3].strip())
                    c3 = int(parts[4].strip())
                    exam = int(parts[5].strip())
                except ValueError:
                    continue  # skip if numbers are not valid

                coursework_total = c1 + c2 + c3  
                overall_total = coursework_total + exam  # total marks
                percentage = (overall_total / 160) * 100  # percentage

                # decide grade
                if percentage >= 70:
                    grade = "A"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C"
                elif percentage >= 40:
                    grade = "D"
                else:
                    grade = "F"

                students.append({
                    "number": number,
                    "name": name,
                    "coursework_total": coursework_total,
                    "exam": exam,
                    "overall_total": overall_total,
                    "percentage": percentage,
                    "grade": grade
                })
    except FileNotFoundError:
        messagebox.showerror("File not found", f"Could not find file:\n{file_path}")  # if file is missing

    return students  # give back the list of students

def populate_tree(students):
    """show students in the table"""
    tree["show"] = "headings"  # make headings visible
    tree.delete(*tree.get_children())  # clear old data
    for i, s in enumerate(students):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'  # alternate colors
        tree.insert(
            "",
            END,
            values=(
                s["name"],
                s["number"],
                s["coursework_total"],
                s["exam"],
                s["overall_total"],
                f"{s['percentage']:.2f}",  
                s["grade"]
            ),
            tags=(tag,)
        )

# Button Actions
def load_data_action():
    """Load all students from file and show"""
    students = read_students_from_file(FILE_PATH)
    if not students:
        messagebox.showinfo("No data", "No student records found.")  # tell user if empty
        tree.delete(*tree.get_children())  # clear table
        return
    populate_tree(students)  # show all students

def get_students_or_alert():
    """helper to get students or show alert if none"""
    students = read_students_from_file(FILE_PATH)
    if not students:
        messagebox.showinfo("No data", "No student records found.")  # alert will appear
        return None
    return students

def highest_action():
    """Show the student with highest percentage"""
    students = get_students_or_alert()
    if not students:
        return
    top = max(students, key=lambda s: s["percentage"])  # find top
    populate_tree([top])  # show only top student

def lowest_action():
    """Show the student with lowest percentage"""
    students = get_students_or_alert()
    if not students:
        return
    low = min(students, key=lambda s: s["percentage"])  # find lowest
    populate_tree([low])  # show only lowest student scores

def search_action():
    """Popup to search student by number or name"""
    popup = Toplevel(root)
    popup.title("Search Student")
    popup.geometry("320x140")
    popup.configure(bg=BTN_BG)

    Label(
        popup,
        text="Enter student number or full name:",
        bg=BTN_BG,
        fg=BTN_FG,
        font=("Helvetica", 10, "bold")
    ).pack(pady=10)

    entry = Entry(popup, font=("Helvetica", 10))
    entry.pack(pady=5)
    entry.focus_set()  

    def do_search():
        key = entry.get().strip()
        popup.destroy()  # close popup after pressing search
        if not key:
            return
        students = get_students_or_alert()
        if not students:
            return
        found = [s for s in students if s["number"] == key or s["name"].lower() == key.lower()]
        if not found:
            messagebox.showinfo("Not found", "Student not found.")  # if nothing matches
            return
        populate_tree(found)  # show only found students

    Button(
        popup,
        text="Search",
        bg=BTN_BG,
        fg=BTN_FG,
        font=("Helvetica", 10, "bold"),
        width=14,
        command=do_search
    ).pack(pady=10)

    popup.transient(root)  # make popup appear above main window
    popup.grab_set()  # focus on popup until closed
    root.wait_window(popup)  # wait until user closes popup

# Buttons
Button(
    root,
    text="Load File",
    bg=BTN_BG,
    fg=BTN_FG,
    font=("Helvetica", 10, "bold"),
    width=15,
    height=1,
    command=load_data_action
).place(x=15, y=50)  # press to load all students

Button(
    root,
    text="Highest",
    bg=BTN_BG,
    fg=BTN_FG,
    font=("Helvetica", 10, "bold"),
    width=15,
    height=1,
    command=highest_action
).place(x=15, y=110)  # press to see top student

Button(
    root,
    text="Lowest",
    bg=BTN_BG,
    fg=BTN_FG,
    font=("Helvetica", 10, "bold"),
    width=15,
    height=1,
    command=lowest_action
).place(x=15, y=175)  # press to see lowest student

Button(
    root,
    text="Search",
    bg=BTN_BG,
    fg=BTN_FG,
    font=("Helvetica", 10, "bold"),
    width=15,
    height=1,
    command=search_action
).place(x=15, y=235)  # press to search student one by one

root.mainloop()  # run the app, now you can press buttons and see students
