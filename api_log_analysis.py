# Sample log line: 106.216.255.173 - - [30/Jul/2023:12:02:03 +0530] "POST /api/v1/admin/get_order_items_by_order_id HTTP/1.0" 200 1055 "-" "okhttp/4.7.2"

import easygui  # for importing choice dialog
from datetime import datetime, timedelta
from tkinter import simpledialog  # for importing date time picker
from tqdm import tqdm

# Constant variables
RESPONSE_TIME_THRESHOLD = 10  # Set your desired threshold in milliseconds
TIME_ZONE_OFFSET = "+0530"  # Set your desired timezone offset, e.g., +0530
TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"  # Set your desired time format


# Function to choose the log file from local storage
def choose_log_file():
    log_file_path = easygui.fileopenbox(
        title="Select Log File",
        msg="Please select a valid Apache access log file",
    )
    return log_file_path


def extract_timestamp(log_line):
    try:
        timestamp_str = log_line.split("[")[1].split("]")[0]
        return datetime.strptime(timestamp_str, TIME_FORMAT)
    except IndexError:
        return None
    except ValueError:
        return None


def extract_response_time(log_line):
    try:
        fields = log_line.split()
        response_time_str = fields[9]
        if response_time_str != '"-"':
            return float(response_time_str)
        return None
    except IndexError:
        return None
    except ValueError:
        return None


log_file_path = choose_log_file()  # Choose the log file from local storage
if not log_file_path:
    exit(0)

output_file_path = "./api_names_with_response_times.txt"
debug_file_path = "./debug.txt"


# Function to get the time range from the user using choice dialog
def get_time_range():
    msg = "Choose the time range for API analysis"
    title = "API Analysis Time Range"
    choices = ["Yesterday's All Logs", "Custom", "Yesterday 5AM to 12AM"]
    choice = easygui.choicebox(msg, title, choices)

    if choice == "Custom":
        start_time_str = easygui.enterbox(
            "Enter the start time (e.g., 26/Jul/2023:12:00:00):",
            default="03/Aug/2023:12:00:00",
        )
        # start_time_str += " +0530"  # Add the timezone offset
        start_time_str = f"{start_time_str} {TIME_ZONE_OFFSET}"

        end_time_str = easygui.enterbox(
            "Enter the end time (e.g., 26/Jul/2023:13:00:00):",
            default="03/Aug/2023:14:00:00",
        )
        end_time_str = f"{end_time_str} {TIME_ZONE_OFFSET}"

    elif choice == "Yesterday's All Logs":
        # set the start date to yesterday 00:00:00, end date to yesterday 23:59:59
        yesterday = datetime.now() - timedelta(days=1)
        start_time_str = f"{yesterday.strftime('%d/%b/%Y:00:00:00')} {TIME_ZONE_OFFSET}"
        end_time_str = f"{yesterday.strftime('%d/%b/%Y:23:59:59')} {TIME_ZONE_OFFSET}"
    elif choice == "Yesterday 5AM to 12AM":
        yesterday = datetime.now() - timedelta(days=1)
        start_time_str = f"{yesterday.strftime('%d/%b/%Y:05:00:00')} {TIME_ZONE_OFFSET}"
        end_time_str = f"{yesterday.strftime('%d/%b/%Y:23:59:59')} {TIME_ZONE_OFFSET}"

    return start_time_str, end_time_str


start_time_str, end_time_str = get_time_range()

api_response_times = {}
api_hit_count = {}

with open(log_file_path, "r") as log_file, open(debug_file_path, "w") as debug_file:
    lines = log_file.readlines()
    total_lines = len(lines)

    for line in tqdm(lines, total=total_lines, desc="Processing Log"):
        fields = line.split()
        # Check if the log line has enough fields to extract the response time
        if len(fields) >= 12:
            response_time = extract_response_time(line)
            if response_time is None:
                debug_file.write(f" - Invalid response time or missing value\n")
                continue

            timestamp = extract_timestamp(line)
            if timestamp is None:
                debug_file.write(f" - Invalid timestamp format , line: {timestamp} \n")
                continue

            start_time = datetime.strptime(start_time_str, TIME_FORMAT)
            end_time = datetime.strptime(end_time_str, TIME_FORMAT)

            if start_time <= timestamp <= end_time:
                route = fields[6]
                api_response_times.setdefault(route, []).append(
                    (timestamp, response_time)
                )

                # Increment the hit count for the route
                api_hit_count[route] = (
                    api_hit_count.get(route, 0) + 1
                )  # get(route, 0): This method is used to retrieve the value associated with the key route from the api_hit_count dictionary. If the key is not present in the dictionary, then the default value 0 is returned.

            else:
                debug_file.write(
                    f" - Timestamp {timestamp} is not in the given time range\n"
                )
        else:
            debug_file.write(f"\nInvalid log line: {line.strip()}\n")

# Filter routes with higher response times
routes_with_high_response_times = {
    route: max(response_times, key=lambda x: x[1])
    for route, response_times in api_response_times.items()
    if max(response_times, key=lambda x: x[1])[1] > RESPONSE_TIME_THRESHOLD
}

# Sort routes by response time in descending order
sorted_routes = sorted(
    routes_with_high_response_times.items(), key=lambda x: x[1][1], reverse=True
)

print(f"Saving the results in {output_file_path} ...")

# Display or save the results in a separate file
with open(output_file_path, "a") as output_file:
    output_file.write(
        f"\n\n-------------------Analysis started at: {datetime.now()}-------------------\n"
    )
    output_file.write(f"Time Range: {start_time_str} to {end_time_str}\n")
    output_file.write(f"Response Time Threshold: {RESPONSE_TIME_THRESHOLD} ms\n")
    output_file.write("\n\n-------------------API Response Times-------------------\n")
    for route, (timestamp, max_response_time) in sorted_routes:
        output_file.write(
            f"API Route: {route}, Timestamp: {timestamp}, Response Time: {max_response_time} ms\n"
        )

    output_file.write("\n\n-------------------API Hit Count-------------------\n")
    for route, hit_count in sorted(
        api_hit_count.items(), key=lambda x: x[1], reverse=True
    ):
        output_file.write(f"API Route: {route}, Hit Count: {hit_count}\n")

print("Done!")
