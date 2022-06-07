from goalplanner import get_unique_goal_name, load_objects_from_file, read_list, write_list, enable_or_disable_children,\
    save_objects_to_file, load_objects_from_file

import pytest
import os

# Importing Tkinter module
import tkinter as tk
# Importing pickle for saving goal information objects
import pickle
# Importing random to help with testing load/save objects function
import random


# define test goal class (This must be defined globally because pickle "cannot pickle local object")
class Goal:
    def __init__(goal, name, date, description, roadblocks, resources, plan, report):
        goal.name = name
        goal.date = date
        goal.description = description
        goal.roadblocks = roadblocks
        goal.resources = resources
        goal.plan = plan
        goal.report = report


def test_save_and_load_objects_to_and_from_file():
    """Verify that the save_objects_to_file, and load_objects_from_file functions works correctly.
    Create a sample list of goal objects, save that to a .pkl file, then load it
    into a new list of objects and compare it to the original.
    """

    # file for testing
    filename = "test_username.pkl"

    # Make a test version of goals list
    GOALS_LIST = []

    # Add 100 Goal objects with unique names to the GOALS_LIST
    for i in range(0, 100):
        GOALS_LIST.append(Goal("New Goal " + str(i), "date.today()", random.choice(
            ["Personal", "Financial", "Hobby", "Health"]), "", "", "", ""))

    # Attempt to save the list containing these objects to the file "test_username.pkl"
    save_objects_to_file(GOALS_LIST, filename)

    # Create a new list and load back the objects from "test_username.pkl" into it
    NEW_LIST = load_objects_from_file(filename)

    # Delete the test_write_list.txt file.
    os.remove(filename)

    for i in range(0, 100):
        # Make sure both list's object attributes match
        assert GOALS_LIST[i].name == NEW_LIST[i].name
        assert GOALS_LIST[i].date == NEW_LIST[i].date
        # Make sure the loaded list contains the exact same randomly chosen descriptions
        assert GOALS_LIST[i].description == NEW_LIST[i].description
        # Make sure the loaded list has correctly named Goal objects
        assert NEW_LIST[i].name == "New Goal " + str(i)

    # Make sure both list's are the same length
    assert len(NEW_LIST) == len(GOALS_LIST)
    # Make sure both list's contain 100 objects
    assert len(NEW_LIST) == 100


def test_write_list():
    """Verify that the write_list function works correctly."""
    lines = [
        "I'm confused about how to best organize a project that uses GUI elements.",
        "I'm just concerned about how big my populate_gui, and populate_user_window functions are",
        "Most of the functions interact closely with the tkinter widgets, which are all stored locally",
        "I could pass the widget variables in as arguments just to avoid having so many nested functions",
        "However, that would just be adding a bunch of extra arguments for no real reason",
        "I don't think it would make any of those functions easier to test anyways.",
        "I've given a lot of thought to how to reorganize this project.",
        "I think it will take time, and experience for me to learn a better way."
    ]
    filename = "test_write_list.txt"

    # Call the write_list function to write a file named test_write_list.txt.
    write_list(filename, lines)

    # Read the contents of the test_write_list.txt file.
    with open(filename, "rt") as infile:

        # Read all the characters in the file into a string.
        string = infile.read()

    # Split the string into a list
    line_list = string.splitlines()

    # Delete the test_write_list.txt file.
    os.remove(filename)

    # Verify that write_list correctly wrote the text into the test_write_list.txt file.
    assert lines == line_list


def test_read_list():
    """Verify that the read_list function works correctly."""

    lines = [
        "I'm confused about how to best organize a project that uses GUI elements.",
        "I'm just concerned about how big my populate_gui, and populate_user_window functions are",
        "Most of the functions interact closely with the tkinter widgets, which are all stored locally",
        "I could pass the widget variables in as arguments just to avoid having so many nested functions",
        "However, that would just be adding a bunch of extra arguments for no real reason",
        "I don't think it would make any of those functions easier to test anyways.",
        "I've given a lot of thought to how to reorganize this project.",
        "I think it will take time, and experience for me to learn a better way."
    ]
    filename = "test_read_list.txt"

    # Call the write_list function to write a file named test_read_list.txt.
    write_list(filename, lines)

    returned_list = read_list(filename)

    test_list = []

    # Open the text file for reading
    with open(filename, "rt") as text_file:

        for line in text_file:
            # Remove white space
            clean_line = line.strip()
            # Append onto the end of the list.
            test_list.append(clean_line)

    # Delete the test_read_list.txt file.
    os.remove(filename)

    # Verify that read_list correctly read the text into a list from the test_read_list.txt file.
    assert returned_list == test_list


def test_get_unique_goal_name():
    """Verify that the get_unique_goal_name function works correctly."""
    # Use a sample list of goal names
    test_goal_name_list = ["New Goal 1", "New Goal 2",
                           "New Goal 3", "New Goal 4", "New Goal 5", "New Goal 6"]
    # Run the function
    returned_unique_goal_name = get_unique_goal_name(test_goal_name_list)
    # See if it returns the correct name
    assert returned_unique_goal_name == "New Goal 7"

    # Use a sample list of goal names
    test_goal_name_list = ["New Goal 1", "New Goal 10",
                           "New Goal 3", "New Goal 5", "New Goal 8", "New Goal 6"]
    # Run the function
    returned_unique_goal_name = get_unique_goal_name(test_goal_name_list)
    # See if it returns the correct name
    assert returned_unique_goal_name == "New Goal 2"

    # Use a sample list of goal names
    test_goal_name_list = [""]
    # Run the function
    returned_unique_goal_name = get_unique_goal_name(test_goal_name_list)
    # See if it returns the correct name
    assert returned_unique_goal_name == "New Goal 1"

    # Use a sample list of goal names
    test_goal_name_list = ["New Goal -1"]
    # Run the function
    returned_unique_goal_name = get_unique_goal_name(test_goal_name_list)
    # See if it returns the correct name
    assert returned_unique_goal_name == "New Goal 1"

    # Use a sample list of goal names
    test_goal_name_list = ["My First Goal",
                           "My Second Goal", "New Goal 2", "New Goal 1"]
    # Run the function
    returned_unique_goal_name = get_unique_goal_name(test_goal_name_list)
    # See if it returns the correct name
    assert returned_unique_goal_name == "New Goal 3"


def test_enable_or_disable_children():
    """Verify that the get_unique_goal_name function works correctly."""

    # Initialize a root tk object for testing
    root = tk.Tk()

    # Create a window/frame
    test_frm_main = tk.Frame(root)

    # Create a new child frame on test_frm_main
    test_frame1 = tk.Frame(test_frm_main)
    # Create another child frame on test_frm_main
    test_frame2 = tk.Frame(test_frm_main)

    # Create a child label of test_frame
    test_label1 = tk.Label(test_frame1)
    # Create a child label of test_frame
    test_label2 = tk.Label(test_frame2)

    # Disable every child of test_frm_main
    enable_or_disable_children(test_frm_main, 'disabled')
    # Check the child labels to see if they're disabled
    assert test_label1.cget('state') == "disabled"
    assert test_label2.cget('state') == "disabled"

    # Set 'state' of every child of test_frm_main to 'normal'
    enable_or_disable_children(test_frm_main, 'normal')
    # Check the child labels to see if they're back to normal
    assert test_label1.cget('state') == "normal"
    assert test_label2.cget('state') == "normal"

    # Disable child of test_frame1
    enable_or_disable_children(test_frame1, 'disabled')
    # Check the child label to see if it's been disabled
    assert test_label1.cget('state') == "disabled"
    # Check the other label to make sure it's still normal
    assert test_label2.cget('state') == "normal"

    # Set 'state' of child of test_frame1 to 'normal'
    enable_or_disable_children(test_frame1, 'normal')
    # Check the child label to see if it's back to normal
    assert test_label1.cget('state') == "normal"

    # Disable every child of test_frame2
    enable_or_disable_children(test_frame2, 'disabled')
    # Check the child label to see if it's been disabled
    assert test_label1.cget('state') == "normal"
    assert test_label2.cget('state') == "disabled"

    # Set 'state' of every child of test_frame to 'normal'
    enable_or_disable_children(test_frame2, 'normal')
    # Check the child label to see if it's back to normal
    assert test_label2.cget('state') == "normal"


# Call the main function that is part of pytest so that
# the test functions in this file will start executing.
pytest.main(["-v", "--tb=line", "-rN", "Goal Planner/goalplanner-tests.py"])
