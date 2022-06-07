# Importing Tkinter module
import tkinter as tk
# Importint Tkinter DateEntry Widget
from tkcalendar import Calendar, DateEntry
# Importing datetime to retrieve today's date.
from datetime import date
# Importing pickle for saving goal information objects
import pickle

""" PURPOSE: this app is designed as a one-stop place to store and keep track of personal goals
Goal information is stored as strings belonging to "Goal" objects
Goal objects have the following attributes: Name, Finish Date (date object), Description, Roadblocks, Resources, Action Plan, Progress Reports
The program asks user to create a unique username, which is used to store goal information (Ex: "username".pkl)
Usernames are stored in a line-seperated list named users.txt
This program uses a three letter prefix in front of the names of all variables that store
GUI widgets, according to this list:
frm: a frame (window) widget
lbl: a label widget that displays text for the user to see
ent: an entry widget where a user will type text or numbers
btn: a button widget that the user will click
txt: a text widget where a user will type muilti-line text or numbers
cal: a calendar widget where a user will select a date
"""

# Make a list to store goal objects
GOALS_LIST = []

# define goal class


class Goal:
    def __init__(goal, name, date, description, roadblocks, resources, plan, report):
        goal.name = name
        goal.date = date
        goal.description = description
        goal.roadblocks = roadblocks
        goal.resources = resources
        goal.plan = plan
        goal.report = report


def main():

    # Create the Tk root object.
    root = tk.Tk()
    # Create the main window/frame
    frm_main = tk.Frame(root)
    frm_main.master.geometry("1032x800")
    frm_main.master.title("Goal Planner")
    frm_main.configure(background='lightgray')
    frm_main.pack(padx=1, pady=1, fill=tk.BOTH, expand=1)

    # Call the populate_gui function, which will add
    # labels, text entry boxes, and buttons to the main window.
    populate_gui(frm_main)

    # Start the tkinter loop that processes user events
    # such as key presses and mouse button clicks.
    root.mainloop()


def populate_gui(frm_main):
    """Populate the gui of this program. In other words, put
    the labels, text entry boxes, and buttons into the main window.
    This function then calls populate_user_ which loads a pop-up frame to select a user.
    Most of the other program logic happens here, for instance
    some widget functions are defined that handle buttons and text entry.
    Parameter
        frm_main: the main window
    Return: nothing
    """

    # variable for keeping track of the last goal the user clicked on
    listbox_goals_last_selection = -1

    #  ·  ·  ·  ·  ·  ·  ·  DEFINE FUNCTIONS  ·  ·  ·  ·  ·  ·  ·
    #  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·

    def switch_user_button_press():
        """ Called when the user clicks the "Switch User" button. 
        This function disables the main windows, and pops-up the sign-in window again.
        Return: nothing
        """
        # clear the current user's goal information
        clear_goal_info_widgets()
        # clear the curren't user's goal list
        GOALS_LIST.clear()
        # clear "My Goals" listbox
        update_display_list()

        # disable all menu's in the program
        enable_or_disable_children(frm_main, 'disable')
        # enable just the sign-in menu
        enable_or_disable_children(frm_user_sign_in, 'normal')
        # place / reveal the sign-in menu again
        frm_user_sign_in.place(relx=.5, rely=.5, anchor="center")

    def update_goal_selection(event):
        """ when the user selects a goal, populate the widgets in the "Goal Info" window
        with this goals information. Looks up the selected goal object by index.
        """
        # because this is an "event" function we need to declare
        # outside variable's we're using as "nonlocal"
        nonlocal listbox_goals_last_selection

        # now that we've selected a goal, enable the "Goal Information" window
        enable_or_disable_children(frm_goal_info, 'normal')

        # find the index of the selected goal
        listbox_goals_last_selection = listbox_goals.get(
            0, tk.END).index(listbox_goals.get(tk.ANCHOR))

        # access the associated Goal object from the GOALS_LIST
        selected_goal_object = GOALS_LIST[listbox_goals_last_selection]

        # clear all the goal info widgets current values
        clear_goal_info_widgets()

        # Update widgets to match this Goal's information:
        # (Name, Date, Descripption, Roadblocks, Resources, Action Plan, Progress Report)
        ent_goal_name.insert(0, listbox_goals.get(
            listbox_goals_last_selection))
        cal_finish_date.set_date(selected_goal_object.date)
        txt_goal_description.insert("1.0", selected_goal_object.description)
        txt_roadblocks.insert("1.0", selected_goal_object.roadblocks)
        txt_resources.insert("1.0", selected_goal_object.resources)
        txt_action_plan.insert("1.0", selected_goal_object.plan)
        txt_progress_report.insert("1.0", selected_goal_object.report)

    def add_goal_button_pressed():
        """Adds a new goal item to the 'My Goals' list with a unique name.
        Then creates an empty Goal object and adds it to the GOALS_LIST
        """
        # Call get_unique_goal_name to get a unique name for this new goal
        new_goal_name = get_unique_goal_name(listbox_goals.get(0, tk.END))

        # Add it to the "My Goals" listbox
        listbox_goals.insert(tk.END, new_goal_name)

        # Add a new empty goal object to our GOALS_LIST of objects
        GOALS_LIST.append(
            Goal(new_goal_name, date.today(), "", "", "", "", ""))

    def update_display_list():
        """updates the "My Goals" listbox to display the names of each goal object
        found in the GOALS_LIST
        """
        # clear the listbox
        listbox_goals.delete(0, 'end')
        for goal in GOALS_LIST:
            # add each goal's name to the listbox
            listbox_goals.insert(tk.END, goal.name)

        # disable the goal info window until we click on a goal
        enable_or_disable_children(frm_goal_info, 'disable')

    def save_goal_button_pressed():
        """updates the Goal objects in GOALS_LIST to match the new user input
        """
        # access the selected object from the GOALS_LIST
        active_goal_selection = GOALS_LIST[listbox_goals_last_selection]

        # update the goal objects information to match the new user input
        active_goal_selection.name = ent_goal_name.get()
        active_goal_selection.date = cal_finish_date.get_date()
        active_goal_selection.description = txt_goal_description.get(
            "1.0", tk.END)
        active_goal_selection.roadblocks = txt_roadblocks.get("1.0", tk.END)
        active_goal_selection.resources = txt_resources.get("1.0", tk.END)
        active_goal_selection.plan = txt_action_plan.get("1.0", tk.END)
        active_goal_selection.report = txt_progress_report.get("1.0", tk.END)

        # save all of this user's goals to "username".pkl
        save_objects_to_file(GOALS_LIST, "Goal Planner/userdata/" +
                             lbl_user.cget("text") + '.pkl')

    def update_goal_name(event):
        """updates the current goal's name in the display list as the user is typing
        """
        # because this is an "event" function we need to declare
        # outside variable's we're using as "nonlocal"
        nonlocal listbox_goals_last_selection

        # If there is a valid goal selected
        if ent_goal_name.get() != "" and listbox_goals_last_selection != -1:
            # clear it's current name
            listbox_goals.delete(listbox_goals_last_selection)
            # replace it with the new user input
            listbox_goals.insert(
                listbox_goals_last_selection, ent_goal_name.get())

    def clear_goal_info_widgets():
        """clears all the "Goal Information" widgets
        """
        # (Name, Finish Date, Description, Roadblocks, Resources, Action Plan, Progress Report)
        ent_goal_name.delete(0, tk.END)
        cal_finish_date.set_date(date.today())
        txt_goal_description.delete("1.0", tk.END)
        txt_roadblocks.delete("1.0", tk.END)
        txt_resources.delete("1.0", tk.END)
        txt_action_plan.delete("1.0", tk.END)
        txt_progress_report.delete("1.0", tk.END)

    # Make this function global so we can call it from inside populate_user_window()
    # (This function is inside of populate_gui so that it can call update_display_list and access widgets)
    global load_user_info

    def load_user_info(user_name, new=False):
        """loads the selected user's goals from "username".pkl
        """
        if not new:
            # First, clear the current goal list
            GOALS_LIST.clear()

            # Call the load_objects_from_file function to load this user's goal information
            GOALS_LIST.extend(load_objects_from_file(
                "Goal Planner/userdata/" + user_name + '.pkl'))

            # After we've loaded the objects, update the display listbox
            update_display_list()
        else:
            # We're a new user, so just disable the goal information window
            enable_or_disable_children(frm_goal_info, 'disabled')

    #  ·  ·  ·  ·  ·  ·  ·  END DEFINING FUNCTIONS  ·  ·  ·  ·  ·
    #  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·

    # Create the main windows widgets:

    #  ·  ·  ·  ·  ·  ·  TOP BAR WIDGETS
    # Create a label that displays current username
    lbl_user = tk.Label(frm_main, text="No user selected", font="ar 12")
    # Create a button with text "switch user"
    btn_switch_user = tk.Button(
        frm_main, text='Switch User ▼', command=switch_user_button_press, font="ar 8")

    #  ·  ·  ·  ·  ·  ·  GOAL LIST WIDGETS
    # Create a frame that contains the "My Goals" labels, listbox, etc.
    frm_goals = tk.Frame(frm_main, width=400, height=730)
    # Create a label that displays "My Goals:"
    lbl_goals_box = tk.Label(
        frm_goals, text="My Goals", font="ar 12 underline")
    # Create a frame to hold the list of current user's goals (see below)
    frm_goals_listbox = tk.Frame(
        frm_goals, highlightbackground="lightgray", highlightcolor="lightgray", highlightthickness=1)
    # Create and configue listbox with a scrollbar to display a list of the current user's goals
    listbox_goals = create_listbox_with_scrollbar(frm_goals_listbox)
    listbox_goals.configure(width=45, height=34, borderwidth=0,
                            highlightthickness=0, bg="lightgray", font="ar 10")
    # Create a button for adding new goals
    btn_add_goal = tk.Button(
        frm_goals, text=' ┼ New Goal ', command=add_goal_button_pressed)

    #  ·  ·  ·  ·  ·  ·  GOAL INFORMATION WIDGETS
    textbox_font = "ar 9"
    # Create a frame that contains the "Goal Information" labels, listbox, etc.
    frm_goal_info = tk.Frame(frm_main, width=600, height=730)
    # Create a label that displays "Goal Information:"
    lbl_goal_info = tk.Label(
        frm_goal_info, text="Goal Information", font="ar 12 underline")
    # Create a label that displays "Goal Name:"
    lbl_goal_name = tk.Label(frm_goal_info, text="Goal Name:")
    # Create an entry box for (Goal Name)
    ent_goal_name = tk.Entry(frm_goal_info, width=25)
    # Create a label that displays "Goal Description:"
    lbl_goal_description = tk.Label(frm_goal_info, text="Goal Description:")
    # Create an text box for (Goal Description)
    txt_goal_description = tk.Text(
        frm_goal_info, width=35, height=6, font=textbox_font)
    # Create a label that displays "Finish Date:"
    lbl_finish_date = tk.Label(frm_goal_info, text="Finish Date:")
    # Create a calandar for finish date selection
    cal_finish_date = DateEntry(
        frm_goal_info, width=18, background='darkgray', foreground='white', borderwidth=2)
    # Create a label that displays "Roadblocks:"
    lbl_roadblocks = tk.Label(frm_goal_info, text="Roadblocks:")
    # Create an text box for (Roadblocks)
    txt_roadblocks = tk.Text(frm_goal_info, width=28,
                             height=5, font=textbox_font)
    # Create a label that displays "Resources:"
    lbl_resources = tk.Label(frm_goal_info, text="Resources:")
    # Create an text box for (Resources)
    txt_resources = tk.Text(frm_goal_info, width=28,
                            height=5, font=textbox_font)
    # Create a label that displays "Action Plan:"
    lbl_action_plan = tk.Label(frm_goal_info, text="Action Plan:")
    # Create an text box for (Action Plan)
    txt_action_plan = tk.Text(frm_goal_info, width=61,
                              height=7, font=textbox_font)
    # Create a label that displays "Progress Report:"
    lbl_progress_report = tk.Label(frm_goal_info, text="Progress Report:")
    # Create an text box for (Progress Report)
    txt_progress_report = tk.Text(
        frm_goal_info, width=61, height=7, font=textbox_font)
    # Create a button for saving the current goals information
    btn_save_goal = tk.Button(
        frm_goal_info, text=' ✓ Save Goal ', command=save_goal_button_pressed)

    #  ·  ·  ·  ·  ·  ·  ·  CREATE USER SIGN-IN WINDOW
    # Create a frame for user sign-in
    frm_user_sign_in = tk.Frame(frm_main, width=300, height=400, highlightbackground="black",
                                highlightcolor="black", highlightthickness=2, bd=10)

    # Place the main windows widgets:

    #  ·  ·  ·  ·  ·  ·  ·  PLACE TOP BAR WIDGETS
    # Layout the labels, entry boxes, and buttons in a grid.
    lbl_user.place(relx=0.9, y=20, anchor="e")
    btn_switch_user.place(relx=0.99, y=20, anchor="e")
    #  ·  ·  ·  ·  ·  ·  ·  PLACE GOAL LIST WIDGETS
    frm_goals.grid(row=2, column=0, padx=10, pady=40)
    lbl_goals_box.place(relx=0.5, y=30, anchor="center")
    frm_goals_listbox.place(relx=.5, rely=.5, anchor="center")
    btn_add_goal.place(relx=.5, rely=.95, anchor="center")

    #  ·  ·  ·  ·  ·  ·  ·  PLACE GOAL INFORMATION WIDGETS
    frm_goal_info.grid(row=2, column=1, padx=0, pady=40)
    lbl_goal_info.place(relx=0.5, y=30, anchor="center")
    lbl_goal_name.place(relx=.1, rely=.08)
    ent_goal_name.place(relx=.108, rely=.12)
    lbl_goal_description.place(relx=.45, rely=.08)
    txt_goal_description.place(relx=.45, rely=.12)
    lbl_finish_date.place(relx=.1, rely=.18)
    cal_finish_date.place(relx=.108, rely=.22)
    lbl_roadblocks.place(relx=.1, rely=.28)
    txt_roadblocks.place(relx=.108, rely=.32)
    lbl_resources.place(relx=.545, rely=.28)
    txt_resources.place(relx=.545, rely=.32)
    lbl_action_plan.place(relx=.1, rely=.46)
    txt_action_plan.place(relx=.1, rely=.5)
    lbl_progress_report.place(relx=.1, rely=.68)
    txt_progress_report.place(relx=.1, rely=.72)
    btn_save_goal.place(relx=.5, rely=.95, anchor="center")

    #  ·  ·  ·  ·  ·  ·  ·  PLACE sign-in window
    frm_user_sign_in.place(relx=.5, rely=.5, anchor="center")

    # Bind "My Goals" listbox to call the update_goal_selection function
    # when the user clicks on a goal
    listbox_goals.bind("<<ListboxSelect>>", update_goal_selection)

    # Bind the goal name entry box to update it's name in the "My Goals" listbox as the user types
    ent_goal_name.bind("<KeyRelease>", update_goal_name)

    # Disable all windows for now, until we are done selecting a user
    enable_or_disable_children(frm_main, 'disable')
    # Enable only the user sign-in window
    enable_or_disable_children(frm_user_sign_in, 'normal')
    # Last, call the populate_user_window function to handle everything else about the user sign-in process
    # (pass in certain widgets as arguments so that they can be changed within that function)
    populate_user_window(frm_main, frm_user_sign_in, lbl_user)


def populate_user_window(frm_main, frm_user_sign_in, lbl_user):
    """Populate a small user selection window. Each user must enter a unique name.
    The names are stored in a file called "users.txt". This function loads that file and displays the list.
    After the user selects a name, they hit the "sign in" button to load their information.
    Parameter
        frm_main: the main window
        frm_user_sign_in: the sign-in window we are populating
        lbl_user: pass in the user display widget so we can change it's
            text value to display the selected user name
        frm_goal_info: pass in the goal information 
    Return: nothing
    """

    # updated by both a listbox selection, or by a text entry
    user_selected = ""
    # used to track if the user just typed a new username into the textbox
    new_user = False

    #  ·  ·  ·  ·  ·  ·  ·  DEFINE FUNCTIONS  ·  ·  ·  ·  ·  ·  ·
    #  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·

    def sign_in_button():
        """Make sure the sign-in name is valid, then load the user's information.
        Afterwards, close the sign-in window and save new usernames to the "users.txt" file
        """
        # remove any whitespace from the desired name
        user_selected.strip()

        # make sure they typed something
        if user_selected != "":

            # If we are a new user make sure we are not using a name that already exists
            # by checking it against the names in the listbox list
            if (new_user and user_selected not in listbox_users.get(0, tk.END)) or not new_user:

                # update the username display label
                lbl_user.configure(text=f"{user_selected}")

                # enable the main window now that we've selected a user
                enable_or_disable_children(frm_main, 'normal')

                if new_user:
                    # if new user, add new name to the listbox list
                    listbox_users.insert(tk.END, user_selected)

                    # save the listbox (user names) list to the "users.txt" file
                    write_list("Goal Planner/userdata/" + "users.txt",
                               listbox_users.get(0, tk.END))

                    # if new, clear the menu's and disable the goal information window
                    load_user_info(user_selected, new=True)

                else:
                    # if user exists, load their goal information
                    load_user_info(user_selected)

                # hide the user sign-in frame
                frm_user_sign_in.place_forget()

    def update_user_listbox(event):
        """This function is called when the user clicks on one of the usernames in the listbox
        Clear the new user name textbox since they selected an existing user.
        """
        # because this is an "event" function we need to declare
        # outside variable's we're changing as "nonlocal"
        nonlocal user_selected, new_user
        # update the variable to match the one they clicked on
        user_selected = listbox_users.get(tk.ANCHOR)
        # clear the new user textbox
        ent_new_user_name.delete(0, tk.END)
        new_user = False

    def update_user_entry(event):
        """This function is called when the types inside the new user textbox
        """
        # because this is an "event" function we need to declare
        # outside variable's we're changing as "nonlocal"
        nonlocal user_selected, new_user
        # update the variable to what they typed
        user_selected = ent_new_user_name.get()
        # this is a new user
        new_user = True

    #  ·  ·  ·  ·  ·  ·  ·  END DEFINING FUNCTIONS  ·  ·  ·  ·  ·
    #  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·

    # Create the user sign-in window's widgets:

    #  ·  ·  ·  ·  ·  ·  USER SIGN-IN
    # Create a label that displays "Select a user:"
    tk.Label(frm_user_sign_in, text="Select a user:").place(
        relx=.5, y=25, anchor="center")
    # Create a label that displays "or create a user:"
    tk.Label(frm_user_sign_in, text=f"or create a user:").place(
        relx=.5, rely=.65, anchor="center")
    # Create an entry box for typing in a new username
    ent_new_user_name = tk.Entry(frm_user_sign_in)
    # Create a "Sign In" button
    btn_user_sign_in = tk.Button(
        frm_user_sign_in, text='Sign in', command=sign_in_button)
    # Create a frame to be a container for the user list scrollbox
    frm_user_sign_user_listbox = tk.Frame(
        frm_user_sign_in, highlightbackground="lightgray", highlightcolor="lightgray", highlightthickness=1)

    # Create a listbox to display a list of previous users that have signed in
    listbox_users = create_listbox_with_scrollbar(frm_user_sign_user_listbox)
    listbox_users.configure(
        width=28, height=10, borderwidth=0, highlightthickness=0, bg="lightgray")

    # Place the user sign-in window's widgets:
    ent_new_user_name.place(relx=.5, rely=.75, anchor="center")
    btn_user_sign_in.place(relx=.5, rely=.9, anchor="center")
    frm_user_sign_user_listbox.place(relx=.5, rely=.35, anchor="center")

    # Load existing users: Get the current users list from a file named "users.txt"
    user_list = read_list("Goal Planner/userdata/users.txt")
    # Update the listbox widget to display the list of user names
    for values in user_list:
        listbox_users.insert(tk.END, values)

    # Bind the user selection listbox to call the update_user_listbox function when we select a username
    listbox_users.bind("<<ListboxSelect>>", update_user_listbox)

    # Bind the new user textbox to call the update_user_entry function when we type in a new username
    ent_new_user_name.bind("<KeyRelease>", update_user_entry)


def create_listbox_with_scrollbar(frame):
    """Create a listbox and attach a scrollbar to it.
    This function is to minimize repeated code.
        frame: the frame to place the listbox onto
    Return: nothing
    """
    # Create a listbox
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
    listbox.pack(side=tk.LEFT)

    # Creating a Scrollbar on the right side of the listbox
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # attach Listbox to Scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    # setting scrollbar command parameter to listbox_goals.yview method
    scrollbar.config(command=listbox.yview)

    # return the listbox with scrollbar attached
    return listbox


def get_unique_goal_name(list):
    """Find a name that does not already appear in the goals list. 
    Name is found by adding a unique number at the end. (Ex: 'New Goal 1', 'New Goal 2', etc.)
    Returns: a unique goal name
    """
    # Start with the number suffix 1
    new_goal_name_suffix = 1

    while ("New Goal " + str(new_goal_name_suffix)) in list:
        # increase the number suffix until we find one that hasn't been used.
        new_goal_name_suffix += 1

    # Combine "New Goal" with unique suffix to make the complete name
    new_goal_name = "New Goal " + str(new_goal_name_suffix)

    return new_goal_name


def read_list(filename):
    """Read the contents of a text file into a list and
    return the list. Each element in the list will contain
    one line of text from the text file. (Used for loading list of previous users names)
    Parameter
        filename: the name of the text file to read
    Return: a list of strings
    """
    # Create an empty list named text_list.
    text_list = []

    # Open the text file for reading and store a reference
    # to the opened file in a variable named text_file.
    with open(filename, "rt") as text_file:

        for line in text_file:
            # Remove white space
            clean_line = line.strip()
            # Append onto the end of the list.
            text_list.append(clean_line)

    # Return the list that contains the lines of text.
    return text_list


def write_list(filename, list):
    """Write the contents of a list to a text file.
    Parameters
        fname: the filename to write to
        list: the list to write
    """
    # Open the text file for writing
    with open(filename, "wt") as text_file:

        # write each list value seperated by \n return
        text_file.writelines(line + '\n' for line in list)


def save_objects_to_file(obj, filename):
    """Saves a list of objects to a .pkl file
    Parameters
        obj: list of objects to save
        filename: filename to save objects to
    """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_objects_from_file(filename):
    """Loads a list of objects from a .pkl file
    Parameters
        filename: filename to load list from
    """
    # Create a new list to populate
    NEW_LIST = []

    # Use try block to catch FileNotFoundError
    try:
        # Open file
        with open(filename, "rb") as f:
            for goal in pickle.load(f):
                # append each goal to GOALS_LIST
                NEW_LIST.append(goal)

    except FileNotFoundError:
        # If there's no file this must be a new user.
        # Pass instead of throwing an error
        pass

    # return the new objects list
    return NEW_LIST


def enable_or_disable_children(parent, newstate):
    """Iterates through widget objects belonging to parent and either enables or disables them.
    Disabled widgets turn gray and cannot be clicked on or used.
    Parameters
        parent: parent widget to disable
        newstate: either 'disable' or 'normal'
    """
    for child in parent.winfo_children():
        # check what class this widget is
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe', ''):
            if wtype != "Scrollbar":
                # if it's not a scrollbar or frame, disable it.
                child.configure(state=newstate)
        else:
            if wtype == "Frame":
                if newstate == 'disable':
                    # For frames, give them a gray border if they are disabled
                    child.configure(highlightbackground="lightgray",
                                    highlightcolor="lightgray")
                    parent.configure(
                        highlightbackground="lightgray", highlightcolor="lightgray")
                else:
                    # black border if they are enabled
                    child.configure(highlightbackground="black",
                                    highlightcolor="black")
                    parent.configure(highlightbackground="black",
                                     highlightcolor="black")

            # if this child has children of it's own, recall this function to change them as well
            enable_or_disable_children(child, newstate)


# call main to start program
if __name__ == "__main__":
    main()
