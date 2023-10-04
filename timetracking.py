"""
Application Time Tracker

Author: Julius Garcia
Website: https://jubox.dev

To run this script, ensure the following Python libraries are installed:
- pygetwindow: for getting the current active window.
- pandas: for data management and to write CSV files.
- pynput: for listening to mouse and keyboard events.
- threading and time are part of the Python Standard Library.

You can install the necessary libraries using pip:
pip install pygetwindow pandas pynput
"""


import pygetwindow as gw # Import the pygetwindow library to interact with native windows
import pandas as pd # Import the pandas library to manage data and write CSV files
from datetime import datetime, timedelta # Import datetime and timedelta from the datetime module to work with dates and times
from pynput import mouse, keyboard # Import mouse and keyboard listeners from the pynput library to detect user activity
import threading # Import the threading library to run multiple threads concurrently
import time # Import the time library to control the sleep state of the while loop in track_active_window function

# Globals to track activity and data
last_activity_time = datetime.now()
data = []
active_window_name = ""
start_time = datetime.now()


def save_to_csv(data, filename):
    """
    Save the tracking data to a CSV file.

    :param data: List of dictionaries containing tracking data.
    :param filename: String, name of the file to save data.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def get_csv_filename():
    """
    Generate a string for the CSV filename based on the current date.

    :return: String, formatted filename.
    """
    date_str = datetime.now().strftime("%Y%m%d")
    return f'application_usage_{date_str}.csv'

def extract_app_name(title):
    """
    Extract an estimated application name from the window title.

    :param title: String, the window title.
    :return: String, estimated application name.
    """
    parts = title.split(' - ')
    if len(parts) > 1:
        return parts[-1]  
    else:
        return title  

def format_timedelta(td):
    """
    Format a timedelta object as HH:MM:SS.

    :param td: timedelta object.
    :return: String, formatted duration.
    """
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)

def format_readable_timedelta(td):
    """
    Format a timedelta object in a readable string format.

    :param td: timedelta object.
    :return: String, formatted readable duration.
    """
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{} hr {} mins {} sec'.format(hours, minutes, seconds)


def track_active_window():
    """
    Continuously tracks the active window title and logs the usage data.

    This function runs in an infinite loop, constantly checking for the active window title. 
    When the active window changes, it logs the usage data to the global `data` list and writes it to a CSV file.
    It also handles idle time by logging it as "Idle" when no activity is detected for a specified period.
    """
    global last_activity_time, data, active_window_name, start_time
    
    try:
        # Main loop to keep checking the active window title
        while True:
            # Get the title of the currently active window
            new_window_name = gw.getActiveWindow().title
            
            # Check if user has been inactive for more than 5 minutes
            if datetime.now() - last_activity_time > timedelta(minutes=5) and active_window_name != "Idle":
                new_window_name = "Idle"  # Set the window name as "Idle"
                start_time = last_activity_time + timedelta(minutes=5)  # Set the start time for idle status
            
            # Check if the active window has changed or if idle status should be logged
            if active_window_name != new_window_name or (active_window_name == "Idle" and new_window_name == "Idle"):
                end_time = datetime.now()  # Note the end time of the previous activity
                if active_window_name != "":
                    # Calculate the total time spent on the previous activity
                    total_time = end_time - start_time
                    formatted_total_time = format_timedelta(total_time)
                    readable_total_time = format_readable_timedelta(total_time)
                    
                    # Append the data to the global list
                    data.append({
                        "Application": extract_app_name(active_window_name),
                        "Title": active_window_name,
                        "Start Time": start_time,
                        "End Time": end_time,
                        "Total Time": formatted_total_time,
                        "Readable Total Time": readable_total_time
                    })
                    
                    # Save the data to a CSV file
                    save_to_csv(data, get_csv_filename())
                    
                    # Update the start time for the next activity
                    start_time = end_time
                
                # Update the active window name if it has changed
                if active_window_name != new_window_name:
                    active_window_name = new_window_name
                
            # Pause the loop for 1 second before checking the active window again
            time.sleep(1)
            
    # Handle the KeyboardInterrupt exception to gracefully end the loop and save data when script is terminated
    except KeyboardInterrupt:
        end_time = datetime.now()
        if active_window_name != "":
            total_time = end_time - start_time
            formatted_total_time = format_timedelta(total_time)
            readable_total_time = format_readable_timedelta(total_time)
            
            # Append the last activity data to the list
            data.append({
                "Application": extract_app_name(active_window_name),
                "Title": active_window_name,
                "Start Time": start_time,
                "End Time": end_time,
                "Total Time": formatted_total_time,
                "Readable Total Time": readable_total_time
            })

        # Save the final data to a CSV file
        save_to_csv(data, get_csv_filename())

def on_activity(*args):
    global last_activity_time
    last_activity_time = datetime.now()



if __name__ == "__main__":
    # Initialize a separate thread to run the active window tracking function
    window_tracking_thread = threading.Thread(target=track_active_window)
    window_tracking_thread.start()
    
    # Start mouse and keyboard listeners to detect user activity
    with mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity) as m_listener, \
         keyboard.Listener(on_press=on_activity) as k_listener:
        m_listener.join()
        k_listener.join()
