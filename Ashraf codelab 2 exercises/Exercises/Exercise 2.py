from tkinter import *
from PIL import ImageTk, Image
import random

# tkinter
APP_WIDTH = 400  # set the width of the app window
APP_HEIGHT = 700  # set the height of the app window

root = Tk()
root.title("Ashraf's alexa app")  # this is the window title
root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")  # set the size of the window
root.resizable(0, 0)  

# Fonts and Colors
LABEL_FONT = ("Helvetica", 10, "bold")  
BUTTON_FONT = ("Helvetica", 10, "bold")  
LABEL_BG = "#E38475"  #  background color
LABEL_FG = "#000000"  # text color

# background image 
bg_img = Image.open("C:\\Users\\Ashraf Bin Shiful\\OneDrive\\Desktop\\Ashraf codelab 2 exercises\\resources\\images\\iphonesetup.png")
bg_img = bg_img.resize((APP_WIDTH, APP_HEIGHT))  # make the image fit the window
bg_photo = ImageTk.PhotoImage(bg_img)  # convert it, so tkinter can use it

bg_label = Label(root, image=bg_photo)  # make a label to hold the image
bg_label.place(x=0, y=0)  # put it at the top left corner

# Load Jokes from File
with open("C:\\Users\\Ashraf Bin Shiful\\OneDrive\\Desktop\\Ashraf codelab 2 exercises\\resources\\randomJokes.txt", "r") as f:
    joke_list = f.readlines()  # read all jokes from file, each joke is a line

# Gv
joke_stage = "setup"  # start with the setup stage
current_question = ""  # here we will store the joke setup
current_answer = ""  # here we will store the punchline
JOKE_BOX_HEIGHT = 80  # height of the joke box

# labels
joke_label = Label(root, text="", font=LABEL_FONT, wraplength=218, bg=LABEL_BG, fg=LABEL_FG, bd=0, relief="flat")
# this label will show the joke

#Functions
def choose_random_joke():
    """pick a random joke and split it if it has a question mark"""
    global current_question, current_answer
    joke_text = random.choice(joke_list).strip()  # pick a random joke and remove spaces
    if "?" in joke_text:
        parts = joke_text.split("?")  # split it at the question mark
        current_question = parts[0] + "?"  # this is what we show first
        current_answer = parts[1]  # this is what we show after pressing button
    else:
        current_question = joke_text  # if no question mark, just show full text
        current_answer = ""  # no punchline

def show_setup():
    """show the joke setup first"""
    joke_label.config(text=current_question)  # show the setup in the label
    joke_label.place(x=98, y=200, width=215, height=JOKE_BOX_HEIGHT)  # put the label in place
    main_button.config(text="answer")  # change button text so next press shows punchline

def show_punchline():
    """show the punchline after pressing button"""
    joke_label.config(text=current_answer)  # show the punchline
    joke_label.place(x=98, y=200, width=215, height=JOKE_BOX_HEIGHT)  # keep it in same spot
    main_button.config(text="hahaha next ")  # press again to move to next joke

def reset_joke_box():
    """clear everything and go back to start"""
    joke_label.config(text="")  # remove text from label
    joke_label.place_forget()  # hide the label
    main_button.config(text="tell me a joke")  # button goes back to start
    # after this press, it will pick a new joke

def handle_button_click():
    """this runs whenever you press the main button"""
    global joke_stage
    if joke_stage == "setup":
        choose_random_joke()  # pick a new joke
        show_setup()  # show the setup first
        joke_stage = "punchline"  # next press will show punchline
    elif joke_stage == "punchline":
        show_punchline()  # show the punchline now
        joke_stage = "next"  # next press will reset
    else:
        reset_joke_box()  # clear everything
        joke_stage = "setup"  # get ready for a new joke

# Main Button
main_button = Button(root, text="tell me a joke", font=BUTTON_FONT, bg="#E38475", fg="#000000",
                     activebackground="#E38475", command=handle_button_click)
main_button.place(x=105, y=590, width=200, height=40)  # the big button you press

root.mainloop()  # start the app and keep it running
