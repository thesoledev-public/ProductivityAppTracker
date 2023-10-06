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
import logging  # Import the logging module
import os  # Import the os module to handle file paths


# Creating directories if they don't exist
os.makedirs('report', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Configuring logging to write logs to the 'logs' folder
logging.basicConfig(filename='logs/app_time_tracker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        # Check if the file already exists
        if os.path.exists(filename):
            # If it does, read the existing data
            existing_data = pd.read_csv(filename)
            # Convert the existing data to a DataFrame
            df_existing = pd.DataFrame(existing_data)
            # Convert the new data to a DataFrame
            df_new = pd.DataFrame(data)
            # Concatenate the existing and new data
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            # If the file doesn't exist, simply convert the new data to a DataFrame
            df = pd.DataFrame(data)
        
        # Save (or overwrite) the CSV file
        df.to_csv(filename, index=False)
    except Exception as e:
        # Log any error encountered during the saving process
        logging.error(f"Failed to save data to CSV. Error: {str(e)}")


def get_csv_filename():
    """
    Generate a string for the CSV filename based on the current date.

    :return: String, formatted filename.
    """
    # Generating a filename using the current date
    date_str = datetime.now().strftime("%Y%m%d")
    # Returning the filename with path to 'report' folder
    return f'report/application_usage_{date_str}.csv'


def extract_app_name(title):
    """
    Extract an estimated application name from the window title.

    :param title: String, the window title.
    :return: String, estimated application name.
    """
    # Define browser tags and corresponding application names
    browser_tags = {
        " - Google Chrome": "Google Chrome", 
        " - Mozilla Firefox": "Mozilla Firefox", 
        " - Microsoft Edge": "Microsoft Edge"
    }
    
    # Check for browser tags and return the corresponding application name if found
    for tag, app_name in browser_tags.items():
        if tag in title:
            return app_name
    
    # Special handling for specific applications
    if "Excel" in title:
        return "Microsoft Excel"
    elif "Word" in title:
        return "Microsoft Word"
    # Add more special cases as needed
    
    # General handling for other titles
    parts = title.split(' - ')
    if len(parts) > 1:
        # Check if the last part is empty and return the second-last if it is
        return parts[-1] if parts[-1].strip() != "" else parts[-2]  
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
        # Continuous loop to keep the tracking active at all times
        while True:
            # Get the currently active window's title
            active_window = gw.getActiveWindow()
            # Check if we got a window title, else assign "Unknown"
            new_window_name = active_window.title if active_window is not None else "Unknown"
            
            # Check for inactivity (considered idle if no activity for 5 minutes)
            if datetime.now() - last_activity_time > timedelta(minutes=5):
                new_window_name = "Idle"
                
            # Check if the active window has changed
            if active_window_name != new_window_name:
                # Record the end time of the previous activity
                end_time = datetime.now()
                
                # If the active window name is not an empty string, log the data
                if active_window_name:  
                    # Calculate and format the total time spent on the activity
                    total_time = end_time - start_time
                    formatted_total_time = format_timedelta(total_time)
                    readable_total_time = format_readable_timedelta(total_time)
                    
                    # Append the data to the global data list and save it to CSV, then clear the list
                    data.append({
                        "Application": extract_app_name(active_window_name),
                        "Title": active_window_name,
                        "Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "End Time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Total Time": formatted_total_time,
                        "Readable Total Time": readable_total_time
                    })
                    
                    save_to_csv(data, get_csv_filename())
                    data.clear()
                    
                    # Update the start time for the next activity
                    start_time = end_time
                
                # Update the active window name
                active_window_name = new_window_name
            
            # Pause the loop for 1 second before checking the active window again
            time.sleep(1)
            
    # Handle manual interruption gracefully and log the last activity
    except KeyboardInterrupt:
        end_time = datetime.now()
        if active_window_name:
            total_time = end_time - start_time
            formatted_total_time = format_timedelta(total_time)
            readable_total_time = format_readable_timedelta(total_time)
            
            data.append({
                "Application": extract_app_name(active_window_name),
                "Title": active_window_name,
                "Start Time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "End Time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Total Time": formatted_total_time,
                "Readable Total Time": readable_total_time
            })
            
        save_to_csv(data, get_csv_filename())
        
    # Log unexpected errors
    except Exception as e:
        logging.error(f"Unexpected error in track_active_window. Error: {str(e)}")


def on_activity(*args):
    """
    Update the last activity time whenever mouse or keyboard activity is detected.
    """
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
