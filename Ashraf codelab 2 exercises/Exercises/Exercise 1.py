from tkinter import *
from PIL import ImageTk, Image
import random

# functions 

def random_int(min_val, max_val):
    """Return a random integer between min_val and max_val"""
    return random.randint(min_val, max_val)  # pick a random number with in the range

def pick_operation():
    """Randomly choose '+' or '-'"""
    return random.choice(["+", "-"])  # decide randomly if the question is addition or subtraction 

def check_correct(expected, user_input):
    """Check if the user's answer matches the correct answer"""
    try:
        return int(user_input) == expected  # compare numbers safely
    except ValueError:
        return False  # if user typed something wrong 

def quiz_results(score):
    """Return a string showing final score"""
    return f"Quiz Finished! Your score: {score} / 100"  # end of quiz message

def load_image(path):
    """Load an image from file for Tkinter"""
    img = Image.open(path)  # open image
    return ImageTk.PhotoImage(img)  # convert to Tkinter-friendly format

# Tkinter Setup
root = Tk()
root.title("MATH QUIZ")  # window title

# Load images for start, difficulty, and question screens file paths
img_start = load_image(r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\images\START.jpg")
img_difficulty = load_image(r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\images\DIFFICULTY.jpg")
img_question = load_image(r"C:\Users\Ashraf Bin Shiful\OneDrive\Desktop\Ashraf codelab 2 exercises\resources\images\QUESTION.jpg")

root.geometry(f"{img_start.width()}x{img_start.height()}")  # set window size same as start image
root.resizable(False, False)  # prevent resizing

# UI
label_bg = Label(root, image=img_start)  # main background label
label_bg.place(x=0, y=0)  # place at top-left corner

label_question = Label(root, text="", font=('Roboto', 24), bg="white")  # question text
entry_answer = Entry(root, width=10, font=('Roboto', 20), justify="center")  # user input box
label_total_score = Label(root, text="Total Score: 0", font=('Roboto', 14), bg="white", fg="#111")  # score display

# number global variables for quiz

num1 = num2 = correct_answer = 0  # numbers for question and correct answer
current_q = 0  # current question number
score = 0  # points for first attempt
total_score = 0  # total points
attempt = 1  # how many tries user has taken for current question
difficulty_level = None  # chosen difficulty: easy, moderate, hard


# Quiz Logic

def generate_question():
    """Create a new math question"""
    global num1, num2, correct_answer, attempt
    attempt = 1  # reset attempt for new question

    # pick numbers based on difficulty
    if difficulty_level == "easy":
        num1, num2 = random_int(0, 9), random_int(0, 9)
    elif difficulty_level == "moderate":
        num1, num2 = random_int(10, 99), random_int(10, 99)
    else:  # hard
        num1, num2 = random_int(1000, 9999), random_int(1000, 9999)

    operation = pick_operation()  # + or -
    correct_answer = num1 + num2 if operation == "+" else num1 - num2  # calculate answer
    label_question.config(text=f"Q{current_q + 1}: {num1} {operation} {num2} = ?")  # show question
    entry_answer.delete(0, END)  # clear previous answer

def check_answer():
    """Check user's answer and update score"""
    global current_q, score, total_score, attempt
    user_input = entry_answer.get()  # read user input

    if check_correct(correct_answer, user_input):
        points = 10 if attempt == 1 else 5  # first try = 10, second try = 5
        score += points
        total_score += points
        label_total_score.config(text=f"Total Score: {total_score}")  # update score label
        current_q += 1  # move to next question
        if current_q < 10:
            generate_question()  # generate next question
        else:
            end_game()  # finished quiz
    else:
        if attempt == 1:
            attempt = 2  # allow second try
            label_question.config(text="Wrong! Try again (5 points)")  # hint message
            entry_answer.delete(0, END)
        else:
            current_q += 1  # skip to next question after second attempt
            if current_q < 10:
                generate_question()
            else:
                end_game()

def end_game():
    """Display final score and hide quiz widgets"""
    label_question.config(text=quiz_results(score))  # show final score
    entry_answer.place_forget()
    button_submit.place_forget()
    label_total_score.place_forget()
    button_play_again.place(relx=0.5, rely=0.55, anchor="center")  # center play again button

def play_again():
    """Reset quiz variables and start over"""
    global current_q, score, total_score, attempt
    button_play_again.place_forget()  # hide play again button
    current_q = score = total_score = 0
    attempt = 1

    label_total_score.config(text=f"Total Score: {total_score}")  # reset score label
    label_question.place(relx=0.5, rely=0.45, anchor="center")
    entry_answer.place(relx=0.5, rely=0.55, anchor="center")
    button_submit.place(relx=0.5, rely=0.65, anchor="center")
    label_total_score.place(x=20, y=60)

    generate_question()  # start first question

# Navigation Functions

def back_to_start():
    """Go back to start screen"""
    label_bg.config(image=img_start)
    button_easy.place_forget()
    button_medium.place_forget()
    button_hard.place_forget()
    button_go_back.place_forget()
    button_play_again.place_forget()
    label_total_score.place_forget()
    button_start.place(x=320, y=295)

def back_to_difficulty():
    """Go back to difficulty selection screen"""
    label_bg.config(image=img_difficulty)
    label_question.place_forget()
    entry_answer.place_forget()
    button_submit.place_forget()
    button_play_again.place_forget()
    label_total_score.place_forget()
    button_easy.place(x=370, y=195)
    button_medium.place(x=370, y=255)
    button_hard.place(x=370, y=310)
    button_go_back.config(command=back_to_start)

def go_to_question(level):
    """Start quiz at chosen difficulty level"""
    global difficulty_level, current_q, score, total_score, attempt
    difficulty_level = level
    current_q = score = total_score = 0
    attempt = 1

    label_bg.config(image=img_question)
    button_easy.place_forget()
    button_medium.place_forget()
    button_hard.place_forget()

    button_go_back.config(command=back_to_difficulty)
    button_go_back.place(x=20, y=20)

    label_question.place(relx=0.5, rely=0.45, anchor="center")
    entry_answer.place(relx=0.5, rely=0.55, anchor="center")
    button_submit.place(relx=0.5, rely=0.65, anchor="center")
    label_total_score.config(text=f"Total Score: {total_score}")
    label_total_score.place(x=20, y=60)

    button_submit.config(command=check_answer)
    generate_question()

def start_game():
    """Move from start screen to difficulty selection"""
    button_start.place_forget()
    label_bg.config(image=img_difficulty)
    button_easy.place(x=370, y=195)
    button_medium.place(x=370, y=255)
    button_hard.place(x=370, y=310)
    button_go_back.config(command=back_to_start)
    button_go_back.place(x=20, y=20)


# Buttons

button_start = Button(root, text="START", width=18, height=2, bg="#4CAF50", fg="white",
                      font=('Roboto', 16, 'bold'), command=start_game)  # big green start button
button_start.place(x=320, y=295)

button_easy = Button(root, text="Easy", width=28, height=1, bg="#4CAF50", fg="#FFFFFF",
                     font=('Roboto', 12), command=lambda: go_to_question("easy"))  # easy difficulty
button_medium = Button(root, text="Moderate", width=28, height=1, bg="#FF9800", fg="#FFFFFF",
                       font=('Roboto', 12), command=lambda: go_to_question("moderate"))  # medium difficulty
button_hard = Button(root, text="Advanced", width=28, height=1, bg="#F44336", fg="#FFFFFF",
                     font=('Roboto', 12), command=lambda: go_to_question("hard"))  # hard difficulty

button_submit = Button(root, text="Submit", font=('Roboto', 16), bg="#22263d", fg="white")  # submit answer
button_play_again = Button(root, text="Play Again", font=('Roboto', 14), bg="#4CAF50", fg="white", command=play_again)  # restart quiz
button_go_back = Button(root, text="Go Back", font=('Roboto', 12), bg="#111", fg="white")  # back button


root.mainloop()  # now run this app to work
