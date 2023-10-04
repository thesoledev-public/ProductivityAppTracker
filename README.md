# ProductivityAppTracker

## Author
**Julius Garcia**  
[Website](https://jubox.dev)

## Description
"ProductivityAppTracker" is a Python-based utility designed to aid users in tracking their application usage and managing screen time effectively. It logs the active application window on a user's computer, recording various usage data such as the application name, window title, start time, end time, and total usage duration. Moreover, it accounts for idle time, ensuring that periods of inactivity are logged accordingly.

### Purpose
The primary objective is to provide insights into the user's application usage, assisting in understanding and optimizing their screen time for enhanced productivity and digital well-being. Whether you aim to improve productivity, minimize screen time, or simply understand your computing habits, this tool offers a comprehensive and automated approach to gather this data. 

## Features
- **Application Tracking:** Monitors and logs the active application window.
- **Idle Time Tracking:** Records periods of inactivity as 'Idle' entries.
- **CSV Logging:** Stores the data in a CSV file, creating a new file for each day of tracking.
- **Human-Readable Format:** Presents total usage time in both `HH:MM:SS` and a human-readable format.

## Usage
Ensure the following Python libraries are installed:
- `pygetwindow`: For retrieving the current active window.
- `pandas`: For managing data and writing CSV files.
- `pynput`: For listening to mouse and keyboard events.

You can install the necessary libraries using pip:
```shell
pip install pygetwindow pandas pynput
```

To run the script:
```shell
python app_usage_tracker.py
```

## Data Output
The script outputs a CSV file named in the format `application_usage_YYYYMMDD.csv` containing the following columns:
- `Application`: The estimated name of the application.
- `Title`: The title of the window.
- `Start Time`: When the application/window became active.
- `End Time`: When the application/window ceased to be active.
- `Total Time`: The total time the application/window was active, in `HH:MM:SS`.
- `Readable Total Time`: The total time in a human-readable string format.

## Note
- The application name is estimated from the window title and may not be accurate for all applications.
- Ensure to handle the KeyboardInterrupt event (Ctrl + C in the console) to save the data when you wish to stop the script.

## License
This project is open source and available to anyone under the [MIT License](LICENSE).
