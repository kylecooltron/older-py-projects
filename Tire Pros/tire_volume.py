# Importing Tkinter module
from tkinter import *
from tkinter import ttk

import math
from datetime import date

# Creating master Tkinter window
master = Tk()

# check what day it is
current_date = date.today()

# define variables
w = 0
a = 0
d = 0
v = 0

# handle tire specs frame - - - - - - - - - - - - - - - - - - - - - - - -
# draw title / header
Label(master, text="New Tire Order", font="ar 12 bold").place(x=32, y=8)
# frame around tire specs
frame = Frame(master, highlightbackground="black",
              highlightcolor="black", highlightthickness=1, bd=10)
frame.place(x=32, y=40)
# create labels for tire info
Label(frame, text="Enter the width of the tire in mm (ex 205): ",
      width=45, anchor="e", justify=LEFT).grid(row=0, column=0)
Label(frame, text="Enter the aspect ratio of the tire (ex 60): ",
      width=45, anchor="e", justify=LEFT).grid(row=1, column=0)
Label(frame, text="Enter the diameter of the wheel in inches (ex 15): ",
      width=45, anchor="e", justify=LEFT).grid(row=2, column=0)
# create text box variables
width_value = IntVar(frame)
aspect_value = IntVar(frame)
diameter_value = IntVar(frame)
# text entry forms
Entry(frame, textvariable=width_value, width=30).grid(row=0, column=1)
Entry(frame, textvariable=aspect_value, width=30).grid(row=1, column=1)
Entry(frame, textvariable=diameter_value, width=30).grid(row=2, column=1)

# click calculate button


def clickCalculateButton():
    global w
    global a
    global d
    global v
    w = width_value.get()
    a = aspect_value.get()
    d = diameter_value.get()
    if w > 0 and a > 0 and d > 0:
        v = (math.pi * w ** 2 * a * (w*a + 2540 * d)) / 10000000
        volume_label.configure(
            text=f"The approximate volume is {v:.1f} milliliters")
    else:
        volume_label.configure(text=f"Invalid input")


# create button
Label(frame, text="").grid(row=3, column=1)  # blank for spacing
Button(frame, text="Calculate Tire Volume", command=clickCalculateButton,
       width=25, bg='lightyellow').grid(row=4, column=0)
# display the calculated tire volume
volume_label = Label(frame, text="<nothing selected yet>", width=55)
volume_label.grid(row=4, column=1)
# end handle tire specs frame - - - - - - - - - - - - - - - - - - - - - -


# handle customer frame - - - - - - - - - - - - - - - - - - - - - - - -
# draw title / header
Label(master, text="New Customer Info", font="ar 12 bold").place(x=32, y=180)
# frame around customer info
frame_customer = Frame(master, highlightbackground="black",
                       highlightcolor="black", highlightthickness=1, bd=10)
frame_customer.place(x=32, y=212)
# create labels for customer info
Label(frame_customer, text="Enter customer name: ", width=25,
      anchor="e", justify=LEFT).grid(row=0, column=0)
Label(frame_customer, text="Enter customer phone number: ",
      width=25, anchor="e", justify=LEFT).grid(row=1, column=0)
# customer text box vars
customer_name = StringVar(frame)
customer_phone = StringVar(frame)
# text entry forms
Entry(frame_customer, textvariable=customer_name, width=20).grid(row=0, column=1)
Entry(frame_customer, textvariable=customer_phone,
      width=20).grid(row=1, column=1)

# save customer order button


def clickSaveOrderButton():
    if v != 0:
        if customer_name.get() != "" and customer_phone.get() != "":
            # Open a text file named volumes.txt in append mode.
            with open("Tire Pros/data/volumes.txt", "at") as volumes_file:
                # Print current date and tire specs to file
                print(f"{current_date}, {w}, {a}, {d}, {v:.1f}",
                      file=volumes_file)
                print(f"{customer_name.get()}, {customer_phone.get()}",
                      file=volumes_file)
            customer_message_label.configure(text=f"Customer Saved")
        else:
            customer_message_label.configure(
                text=f"Customer information is invalid")
    else:
        customer_message_label.configure(text=f"No tire volume calculated")


# createsave customer button
Label(frame_customer, text="").grid(row=2, column=1)  # blank for spacing
Button(frame_customer, text="Save customer order", command=clickSaveOrderButton,
       width=25, bg='lightyellow').grid(row=3, column=1)

# display a message when customer is saved
customer_message_label = Label(frame_customer, text="", width=25)
customer_message_label.grid(row=5, column=1)
# end handle customer frame - - - - - - - - - - - - - - - - - - - - - -

# Set window size, icon, title
master.iconphoto(False, PhotoImage(file='Tire Pros/data/tirepros.png'))
master.geometry("800x380")
master.wm_title("Tire Log")
mainloop()
