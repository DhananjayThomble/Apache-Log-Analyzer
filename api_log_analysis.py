# Sample log line: 106.216.255.173 - - [30/Jul/2023:12:02:03 +0530] "POST /api/v1/admin/get_order_items_by_order_id HTTP/1.0" 200 1055 "-" "okhttp/4.7.2"

import easygui # for importing choice dialog
from datetime import datetime, timedelta
from tkinter import simpledialog # for importing date time picker 

# Function to choose the log file from local storage
def choose_log_file():
    log_file_path = easygui.fileopenbox(
        title="Select Log File",
        msg="Please select a valid apache access log file",

        # ensure that the file has at least some extension
    )
    return log_file_path

log_file_path = choose_log_file() # Choose the log file from local storage
if not log_file_path:
    exit(0)


response_time_threshold = 2000  # Set your desired threshold in milliseconds
output_file_path = "./api_names_with_response_times.txt"


# Function to extract the timestamp from the log line
def extract_timestamp(log_line):
    timestamp_str = log_line.split("[")[1].split("]")[0]    # [30/Jul/2023:12:02:03 +0530]
    return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")   # 2023-07-30 12:02:03+05:30


api_response_times = {} # stores the response times for each API route
api_hit_count = {}  # stores the hit count for each API route

# Get the time range from the user using choice dialog
msg = "Choose the time range for API analysis"
title = "API Analysis Time Range"
choices = ["Yesterday's All Logs", "Custom", "Yesterday 5AM to 12AM"]
choice = easygui.choicebox(msg, title, choices)

if choice == "Custom":
    start_time_str = easygui.enterbox(
        "Enter the start time (e.g., 26/Jul/2023:12:00:00 +0530):"
    )
    start_time_str += " +0530"  # Add the timezone offset
    end_time_str = easygui.enterbox(
        "Enter the end time (e.g., 26/Jul/2023:13:00:00 +0530):"
    )
    end_time_str += " +0530"
elif choice == "Yesterday's All Logs":
    # set the start date to yesterday 00:00:00, end date to yesterday 23:59:59
    start_time_str = (datetime.now() - timedelta(days=1)).strftime("%d/%b/%Y:00:00:00 +0530")   
    # datetime.now() - timedelta(days=1) returns yesterday's date
    # strftime() converts the date to the specified format
    end_time_str = (datetime.now() - timedelta(days=1)).strftime("%d/%b/%Y:23:59:59 +0530")
elif choice == "Yesterday 5AM to 12AM":
    start_time_str = (datetime.now() - timedelta(days=1)).strftime("%d/%b/%Y:05:00:00 +0530")
    end_time_str = (datetime.now() - timedelta(days=1)).strftime("%d/%b/%Y:00:00:00 +0530")

with open(log_file_path, "r") as log_file:
    for line in log_file:
        fields = line.split()
        if len(fields) >= 10:
            response_time_str = fields[-3]
            if response_time_str != '"-"':
                try:
                    response_time = float(response_time_str)
                except ValueError:
                    continue

                timestamp = extract_timestamp(line) # extract the timestamp from the log line
                start_time = datetime.strptime(start_time_str, "%d/%b/%Y:%H:%M:%S %z")
                # strptime() converts the string to datetime object
                end_time = datetime.strptime(end_time_str, "%d/%b/%Y:%H:%M:%S %z")

                if start_time <= timestamp <= end_time:
                    request_line = " ".join(fields[5:8])
                    # Extract the route from the request line
                    route = request_line.split()[1]

                    if route in api_response_times:
                        api_response_times[route].append((timestamp, response_time))
                    else:
                        api_response_times[route] = [(timestamp, response_time)]

                    # Update API hit count
                    if route in api_hit_count:
                        api_hit_count[route] += 1
                    else:
                        api_hit_count[route] = 1

# Filter routes with higher response times
routes_with_high_response_times = {
    route: max(response_times, key=lambda x: x[1])
    for route, response_times in api_response_times.items()
    if max(response_times, key=lambda x: x[1])[1] > response_time_threshold
}

# Sort routes by response time in descending order
sorted_routes = sorted(
    routes_with_high_response_times.items(), key=lambda x: x[1][1], reverse=True
)

# Display or save the results in a separate file
with open(output_file_path, "a") as output_file:
    # give today's date and time
    output_file.write(f"\n\n-------------------{datetime.now()}-------------------\n")
    output_file.write( "\n\n-------------------API Response Times-------------------\n")
    for route, (timestamp, max_response_time) in sorted_routes:
        output_file.write(
            f"API Route: {route}, Timestamp: {timestamp}, Response Time: {max_response_time} ms\n"
        )
    # print(
    #     f"API Route: {route}, Timestamp: {timestamp}, Max Response Time: {max_response_time} ms"
    # )

    # Display the API hit count
    output_file.write("\n\n-------------------API Hit Count-------------------\n")
    for route, hit_count in sorted(
        api_hit_count.items(), key=lambda x: x[1], reverse=True
    ):
        output_file.write(f"API Route: {route}, Hit Count: {hit_count}\n")
        # print(f"API Route: {route}, Hit Count: {hit_count}")