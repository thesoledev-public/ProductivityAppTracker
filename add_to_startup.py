"""
AutoRun ProductivityAppTracker on Windows Startup

Author: Julius Garcia
Website: https://jubox.dev

Description:
This script creates a shortcut for running the ProductivityAppTracker application on Windows startup.
It identifies the path to pythonw.exe and adds a shortcut to your script in the user's startup folder.

Instructions:
1. Place this script in the same directory as your 'timetracking.py' script.
2. Modify the 'script_name' variable with the name of your Python script.
3. Run this script to create the shortcut.

Note: This script is designed for Windows operating systems.
"""

import os
import shutil
import sys

# Specify the name of your Python script
script_name = "timetracking.py"

# Determine the path to the user's home directory
user_home = os.path.expanduser("~")

# Define the possible locations of pythonw.exe based on common Python installations
possible_pythonw_paths = [
    os.path.join(sys.exec_prefix, "pythonw.exe"),  # Check the current Python environment
    os.path.join(user_home, "AppData", "Local", "Programs", "Python", "PythonXX", "pythonw.exe"),  # Replace XX with your Python version
    os.path.join(user_home, "AppData", "Local", "Programs", "Python", "PythonXX-XX", "pythonw.exe"),  # Replace XX-XX with your Python version
]

# Find the first valid path to pythonw.exe
pythonw_path = None
for path in possible_pythonw_paths:
    if os.path.exists(path):
        pythonw_path = path
        break

if pythonw_path is None:
    print("pythonw.exe not found. Please specify the path to pythonw.exe manually.")
else:
    try:
        # Get the current directory where this script is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Create a shortcut name for your script
        shortcut_name = "ProductivityAppTracker.lnk"

        # Create the full path for the shortcut
        shortcut_path = os.path.join(current_directory, shortcut_name)

        # Specify the command-line arguments for pythonw.exe
        command_args = f"{script_name}"

        # Create the shortcut in the user's startup folder
        startup_folder = os.path.join(user_home, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        startup_shortcut_path = os.path.join(startup_folder, shortcut_name)

        if not os.path.exists(startup_shortcut_path):
            # Create the shortcut
            with open(shortcut_path, "w") as shortcut_file:
                shortcut_file.write(f"{pythonw_path} {command_args}")

            # Move the shortcut to the startup folder
            shutil.move(shortcut_path, startup_shortcut_path)

            print(f"Shortcut created in the startup folder: {startup_shortcut_path}")
        else:
            print("Shortcut already exists in the startup folder.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
