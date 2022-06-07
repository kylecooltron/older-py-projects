# Importing Tkinter module
from tkinter import *
from tkinter import ttk
import time

# Creating master Tkinter window
master = Tk()

# draw title / header
Label(master, text="Kyle's Crazy Mad Lib Story", font="ar 15 bold",
      bg='aqua').place(y=30, relx=0.5, anchor=CENTER)
Label(master, text="Please enter the following:", font="ar 8 bold",
      bg='orange').place(y=60, relx=0.5, anchor=CENTER)


# frame around data entry form
frame = Frame(master, highlightbackground="black",
              highlightcolor="black", highlightthickness=1, bd=10)
frame.place(x=30, y=80)

# define diplay variables
label_width_col_1 = 8
label_width_col_2 = 14

# blank spacing for grid
Label(frame, text="", anchor="e", width=2).grid(row=1, column=1)
Label(frame, text="", anchor="e", width=2).grid(row=1, column=4)
Label(frame, text="", anchor="e", width=2).grid(row=1, column=7)

# draw labels column 1
Label(frame, text="adjective: ", anchor="e",
      width=label_width_col_1).grid(row=1, column=2)
Label(frame, text="animal: ", anchor="e",
      width=label_width_col_1).grid(row=2, column=2)
Label(frame, text="noun: ", anchor="e",
      width=label_width_col_1).grid(row=3, column=2)
Label(frame, text="verb: ", anchor="e",
      width=label_width_col_1).grid(row=4, column=2)
Label(frame, text="exclamation: ", anchor="e",
      width=label_width_col_1).grid(row=5, column=2)
Label(frame, text="verb: ", anchor="e",
      width=label_width_col_1).grid(row=6, column=2)
Label(frame, text="verb: ", anchor="e",
      width=label_width_col_1).grid(row=7, column=2)
Label(frame, text="name ", anchor="e",
      width=label_width_col_1).grid(row=8, column=2)
# draw labels column 2
Label(frame, text="place: ", anchor="e",
      width=label_width_col_2).grid(row=1, column=5)
Label(frame, text="food: ", anchor="e",
      width=label_width_col_2).grid(row=2, column=5)
Label(frame, text="feeling: ", anchor="e",
      width=label_width_col_2).grid(row=3, column=5)
Label(frame, text="things (plural): ", anchor="e",
      width=label_width_col_2).grid(row=4, column=5)
Label(frame, text="verb: ", anchor="e",
      width=label_width_col_2).grid(row=5, column=5)
Label(frame, text="name: ", anchor="e",
      width=label_width_col_2).grid(row=6, column=5)
Label(frame, text="place: ", anchor="e",
      width=label_width_col_2).grid(row=7, column=5)
Label(frame, text="exclamation: ", anchor="e",
      width=label_width_col_2).grid(row=8, column=5)


# define variables
adjective = StringVar(frame)
animal = StringVar(frame)
noun_1 = StringVar(frame)
verb_1 = StringVar(frame)
exclamation_1 = StringVar(frame)
verb_2 = StringVar(frame)
verb_3 = StringVar(frame)
name_1 = StringVar(frame)
# column 2 vars
place_1 = StringVar(frame)
food = StringVar(frame)
feeling = StringVar(frame)
things = StringVar(frame)
verb_4 = StringVar(frame)
name_2 = StringVar(frame)
place_2 = StringVar(frame)
exclamation_2 = StringVar(frame)

# text entry forms
Entry(frame, textvariable=adjective, width=10).grid(row=1, column=3)
Entry(frame, textvariable=animal, width=10).grid(row=2, column=3)
Entry(frame, textvariable=noun_1, width=10).grid(row=3, column=3)
Entry(frame, textvariable=verb_1, width=10).grid(row=4, column=3)
Entry(frame, textvariable=exclamation_1, width=10).grid(row=5, column=3)
Entry(frame, textvariable=verb_2, width=10).grid(row=6, column=3)
Entry(frame, textvariable=verb_3, width=10).grid(row=7, column=3)
Entry(frame, textvariable=name_1, width=10).grid(row=8, column=3)
# text entry forms column 2
Entry(frame, textvariable=place_1, width=10).grid(row=1, column=6)
Entry(frame, textvariable=food, width=10).grid(row=2, column=6)
Entry(frame, textvariable=feeling, width=10).grid(row=3, column=6)
Entry(frame, textvariable=things, width=10).grid(row=4, column=6)
Entry(frame, textvariable=verb_4, width=10).grid(row=5, column=6)
Entry(frame, textvariable=name_2, width=10).grid(row=6, column=6)
Entry(frame, textvariable=place_2, width=10).grid(row=7, column=6)
Entry(frame, textvariable=exclamation_2, width=10).grid(row=8, column=6)

# define variables used to write out story one character at a time
start_text = ""
current_char = 0
full_text = "This is going to become the story"
next_wait_time = 30
add_y = 20
updating = False

# write out story one character at a time


def update_loop():
    global current_char
    global start_text
    global next_wait_time
    global add_y
    global updating

    wait_time = next_wait_time
    dynamic_label.config(text=start_text)
    start_text += f'{full_text[current_char]}'
    # wait a little longer after periods and commas.
    if any(char == full_text[current_char] for char in [",", "."]):
        next_wait_time = 200
    else:
        next_wait_time = 30
    current_char += 1
    if not current_char >= len(full_text)-2:
        master.after(wait_time, update_loop)
    else:
        # finished
        updating = False
    if add_y > 0:
        add_y -= 2
        title_label.place(y=340+add_y)


# function check's whether a word should be preceded by "a" or "an"
def return_a_or_an(word):
    if any(letter.lower() == word[0].lower() for letter in ["a", "e", "i", "o"]) or word.lower() == "hourglass":
        return "an"
    else:
        return "a"


def click_submit_button():
    global updating
    if not any(not form.get() for form in [adjective, animal, noun_1, verb_1, exclamation_1, verb_2, verb_3, name_1]) and not updating:
        global full_text
        # create story string
        full_text = f'\nThe other day, I was really in trouble.\n\n It all started when I saw a very {adjective.get()} {animal.get()}. '
        full_text += f'\n\nIt looked just like {return_a_or_an(noun_1.get())} {noun_1.get()}, as it {verb_1.get()} down the hallway. '
        full_text += f'\n\n"{exclamation_1.get()}!" I yelled. But all I could think to do was to {verb_2.get()} over and over. '
        full_text += f'\n\nMiraculously, that caused it to stop,\n\nbut not before it tried to {verb_3.get()} right in front of my friend {name_1.get()}. '
        full_text += f"\n\n{name_1.get().capitalize()}'s parents never wanted us to have to\n\n see {return_a_or_an(animal.get())} {animal.get()} {verb_1.get()} and {verb_3.get()} everywhere like that. "

        full_text += f"\n\nSo next time you are at the {place_1.get()}, just remember that {animal.get()}'s like {food.get()}. "
        full_text += f"\n\n{animal.get().capitalize()}'s are everywhere, and they are {feeling.get()} {things.get()}. "
        full_text += f"\n\nEspecially if your name is {name_2.get()} "
        full_text += f"\n\n{verb_4.get().capitalize()} as fast as you can to the {place_2.get()}, or gee {exclamation_2.get()},\n\n you might start to feel {feeling.get()} too.         "

        title_label.configure(text="Your story is:")
        # reset variables
        global current_char
        global start_text
        global add_y

        updating = True
        current_char = 0
        start_text = ""
        add_y = 20
        update_loop()


submit_button = Button(master, text="Read my story!",
                       command=click_submit_button, width=20, bg='yellow')
submit_button.place(y=300, relx=0.5, anchor=CENTER)

title_label = Label(master, text="", font="ar 14 bold", bg="lightgreen")
title_label.place(y=0, relx=0.5, anchor=CENTER)

dynamic_label = Label(master, text="", bg="lightgreen", font="ar 9")
dynamic_label.place(y=350, relx=0.5, anchor="n")


# Set window size, icon, title
master.configure(bg='lightgreen')
master.geometry("435x780")
master.wm_title("ID Badge")
mainloop()
