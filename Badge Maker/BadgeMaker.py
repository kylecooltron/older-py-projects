# Importing Tkinter module
from tkinter import *
from tkinter import ttk
# Importing regex
import re
# Importing pickle
import pickle


# create employee list
employee_list = []
employee_selected = -1
# define employee class


class Employee:
    def __init__(self, firstname, lastname, email, phone, job, id_number, haircolor, eyecolor, monthstarted, training):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.job = job
        self.id_number = id_number
        self.haircolor = haircolor
        self.eyecolor = eyecolor
        self.monthstarted = monthstarted
        self.training = training

# define function


def update_display_list():
    mylist.delete(0, 'end')
    for emp in employee_list:
        mylist.insert(END, "{0:<12}{1:<13}ID: {2:>}".format(
            str(emp.lastname.upper()+", "), str(emp.firstname), str(emp.id_number)))


# Creating master Tkinter window
master = Tk()

# handle form - - - - - - - - - - - - - - - - - - - - - - - -
# draw title / header
Label(master, text="Please input the following information",
      font="ar 10 bold").place(x=70, y=8)

# frame around data entry form
frame = Frame(master, highlightbackground="black",
              highlightcolor="black", highlightthickness=1, bd=10)
frame.place(x=30, y=40)

# draw labels
Label(frame, text="First name: ", anchor="e", width=15).grid(row=1, column=2)
Label(frame, text="Last name: ", anchor="e", width=15).grid(row=2, column=2)
Label(frame, text="Email address: ", anchor="e", width=15).grid(row=3, column=2)
Label(frame, text="Phone number: ", anchor="e", width=15).grid(row=4, column=2)
Label(frame, text="Job title: ", anchor="e", width=15).grid(row=5, column=2)
Label(frame, text="ID Number: ", anchor="e", width=15).grid(row=6, column=2)
Label(frame, text="Hair color: ", anchor="e", width=15).grid(row=7, column=2)
Label(frame, text="Eye color: ", anchor="e", width=15).grid(row=8, column=2)
Label(frame, text="Month started: ", anchor="e", width=15).grid(row=9, column=2)
Label(frame, text="").grid(row=10, column=2)  # placeholder
Label(frame, text="Advanced training complete? ").place(x=10, y=222)

firstname_value = StringVar(frame)
lastname_value = StringVar(frame)
email_value = StringVar(frame)
phone_value = StringVar(frame)
job_value = StringVar(frame)
id_value = StringVar(frame)
haircolor_value = StringVar(frame)
eyecolor_value = StringVar(frame)
monthstarted_value = StringVar(frame)
training_value = StringVar(frame)
# set default values for option menu variables
haircolor_value.set("Not selected")
eyecolor_value.set("Not selected")
monthstarted_value.set("Not selected")
training_value.set("Not selected")

# text entry forms
Entry(frame, textvariable=firstname_value, width=30).grid(row=1, column=3)
Entry(frame, textvariable=lastname_value, width=30).grid(row=2, column=3)
Entry(frame, textvariable=email_value, width=30).grid(row=3, column=3)
Entry(frame, textvariable=phone_value, width=30).grid(row=4, column=3)
Entry(frame, textvariable=job_value, width=30).grid(row=5, column=3)
Entry(frame, textvariable=id_value, width=30).grid(row=6, column=3)

# create option menus
haircolor_entry = OptionMenu(
    frame, haircolor_value, "black", "brown", "blond", "white/gray", "red")
haircolor_entry.config(width=20)
haircolor_entry.grid(row=7, column=3)

eyecolor_entry = OptionMenu(frame, eyecolor_value,
                            "brown", "blue", "hazel", "green", "amber", "red")
eyecolor_entry.config(width=20)
eyecolor_entry.grid(row=8, column=3)

monthstarted_entry = OptionMenu(frame, monthstarted_value, "January", "February", "March",
                                "April", "May", "June", "July", "August", "September", "October", "November", "December")
monthstarted_entry.config(width=20)
monthstarted_entry.grid(row=9, column=3)

# create radio buttons
training_yes_button = Radiobutton(
    frame, text="Yes", variable=training_value, value="Yes")
training_yes_button.place(x=180, y=222)

training_no_button = Radiobutton(
    frame, text="No", variable=training_value, value="No")
training_no_button.place(x=230, y=222)

# end handle form - - - - - - - - - - - - - - - - - - - - - - - -


# define regex to check if input is valid
regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
regex_phone = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
regex_id = '^[0-9-]*$'


def clickSubmitButton():

    # reset error code
    errorcode = "Please fix the following: "

    # check that the user input was valid
    if not firstname_value.get():
        errorcode += " first name is blank  "
    if not lastname_value.get():
        errorcode += " last name is blank  "
    if not re.search(regex_email, email_value.get()) or not email_value.get():
        errorcode += " invalid email  "
    if not re.search(regex_phone, phone_value.get()) or not phone_value.get():
        errorcode += " invalid phone  "
    if not job_value.get():
        errorcode += " job title is blank  "
    if not re.search(regex_id, id_value.get()) or not id_value.get():
        errorcode += " invalid ID number  "

    if errorcode == "Please fix the following: ":  # no changes == no errors!
        # add new instance of employee to employee list
        employee_list.append(
            Employee(firstname_value.get(),
                     lastname_value.get(),
                     email_value.get(), phone_value.get(),
                     job_value.get(), id_value.get(),
                     haircolor_value.get(), eyecolor_value.get(),
                     monthstarted_value.get(), training_value.get())
        )
        # update
        update_display_list()

        # erase error code
        invalid_label.configure(text="")
    else:
        # report errors
        invalid_label.configure(text=errorcode)


# invalid input label
invalid_label = Label(master, text="", fg='#f00')
invalid_label.place(x=20, y=310)

# submit button
submitButton = Button(master, text="Submit",
                      command=clickSubmitButton, width=25, bg='lightyellow')
submitButton.place(x=100, y=340)


# handle selection box - - - - - - - - - - - - - - - - - - - - - - - -
# draw title / header
Label(master, text="Select an employee to view",
      font="ar 10 bold").place(x=450, y=8)


# sort by stuff

def sortby_select_event(event):
    if event.widget.get() == 'first name':
        employee_list.sort(key=lambda x: x.firstname)
    if event.widget.get() == 'last name':
        employee_list.sort(key=lambda x: x.lastname)
    if event.widget.get() == 'id number':
        employee_list.sort(key=lambda x: x.id_number)
    # update
    update_display_list()


Label(master, text="Sort list by:").place(x=540, y=40)

sortby_value = StringVar(master)
sortby_value.set("none")
sortby_menu = ttk.Combobox(master, width=10, textvariable=sortby_value)
# Adding combobox drop down list
sortby_menu['values'] = ('last name',
                         'first name',
                         'id number')
sortby_menu.place(x=610, y=40)
sortby_menu.bind("<<ComboboxSelected>>", sortby_select_event)


# frame around selection box / list
frame2 = Frame(master, highlightbackground="black",
               highlightcolor="black", highlightthickness=1, bd=17)
frame2.place(x=400, y=70)

# create scrollbar
sb = Scrollbar(frame2)
sb.pack(side=RIGHT, fill=Y)

# clicked on an employee


def employee_select_button(event):
    if event.widget.curselection():
        employee_selected = event.widget.curselection()
        this_employee = employee_list[employee_selected[0]]
        this_text = f"The ID Card is:\n----------------------------------------"
        this_text += " "*10 + f"\n"
        this_text += this_employee.lastname.upper() + ", " + this_employee.firstname
        this_text += f"\n{this_employee.job.title()}"
        this_text += f"\nID: {this_employee.id_number}\n"
        this_text += f"\n{this_employee.email.lower()}"
        this_text += f"\n{this_employee.phone}\n\n"
        this_text += f"Hair: {this_employee.haircolor}\n"
        this_text += f"Month: {this_employee.monthstarted}"
        this_text += f"\n----------------------------------------"
        display_name.configure(text=this_text)
        this_text = f"Eyes: {this_employee.eyecolor}\n"
        this_text += f"Training: {this_employee.training}"
        display_name_end.configure(text=this_text)


# create list
mylist = Listbox(frame2, yscrollcommand=sb.set,
                 width=35, height=12, font="Monaco 9")
mylist.bind('<<ListboxSelect>>', employee_select_button)
mylist.pack(side=LEFT)
sb.config(command=mylist.yview)


# handle save data
file_name = StringVar(frame)
file_name.set("data")

Label(master, text="Save/open local data file:").place(x=480, y=308)
Entry(master, textvariable=file_name, width=12).place(x=420, y=340)
Label(master, text=".pkl", fg='grey').place(x=500, y=340)


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def click_save_file_button():
    save_object(employee_list, "Badge Maker/data/" + file_name.get() + '.pkl')


def click_open_file_button():
    with open("Badge Maker/data/" + file_name.get() + '.pkl', "rb") as f:
        employee_list.clear()
        for emp in pickle.load(f):
            employee_list.append(emp)
        update_display_list()


save_button = Button(master, text="Save",
                     command=click_save_file_button, width=8)
save_button.place(x=550, y=335)

open_button = Button(master, text="Open",
                     command=click_open_file_button, width=8)
open_button.place(x=620, y=335)


# end handle selection box - - - - - - - - - - - - - - - - - - - - - -


# handle badge box - - - - - - - - - - - - - - - - - - - - - - - -
# draw title / header
Label(master, text="Employee Badge", font="ar 10 bold").place(x=820, y=8)

# frame around id badge
frame3 = Frame(master, highlightbackground="black",
               highlightcolor="black", highlightthickness=1, bd=10, height=200)
frame3.place(x=740, y=40)
# create labels to contain id badge text
display_name = Label(frame3, text="No employee selected" +
                     " "*20, width=35, anchor="e", justify=LEFT)
display_name.grid(row=0, column=0)
# second label to contain additional id badge text
display_name_end = Label(frame3, text="", anchor="e", justify=LEFT)
display_name_end.place(x=135, y=135)

# end handle badge box - - - - - - - - - - - - - - - - - - - - - -


# Set window size, icon, title
#master.iconphoto(False, PhotoImage(file = 'badge.png'))
master.geometry("1045x380")
master.wm_title("ID Badge")
mainloop()
