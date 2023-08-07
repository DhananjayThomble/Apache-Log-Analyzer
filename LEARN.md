# Apache Log Analyzer - LEARN.md

## Introduction

Welcome to the Apache Log Analyzer tutorial! In this guide, I will walk you through the process of creating the **Apache Log Analyzer** script, which helps analyze Apache access log files to gain insights into API response times and hit counts.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Choosing the Log File](#choosing-the-log-file)
4. [Selecting Time Range](#selecting-time-range)
5. [Extracting Data from Log Lines](#extracting-data-from-log-lines)
6. [Filtering Invalid Log Lines](#filtering-invalid-log-lines)
7. [Analyzing API Data](#analyzing-api-data)
8. [Saving Analysis Results](#saving-analysis-results)
9. [Customization](#customization)
10. [Conclusion](#conclusion)

## 1. Prerequisites

Before you begin, make sure you have the following:

- Python 3.x installed on your system.
- The required packages mentioned in `requirements.txt`.
- Access to Apache access log files to analyze. (You can also use the sample log file provided in the repository.)

## 2. Project Structure

Let's start by understanding the project structure:

```
Apache-Log-Analyzer/
|-- api_log_analysis.py
|-- requirements.txt
|-- debug.txt (optional)
|-- api_names_with_response_times.txt (optional)
|-- log (sample apache access log file)
```

The `api_log_analysis.py` file contains the main script that performs the log analysis. The `requirements.txt` file lists the dependencies needed to run the script. The `debug.txt` and `api_names_with_response_times.txt` files store debugging information and analysis results, respectively.

## 3. Choosing the Log File

The script begins by prompting the user to choose a valid Apache access log file from their local storage. We use the `easygui` package to create a simple GUI for file selection. The chosen file's path is stored in the `log_file_path` variable.

## 4. Selecting Time Range

The script then prompts the user to choose a time range for the analysis. They can either select a custom range, analyze logs from yesterday, or logs between 5 AM to 12 AM yesterday.

## 5. Extracting Data from Log Lines

The `extract_timestamp`, `extract_route`, and `extract_response_time` functions help extract important data from each log line. They retrieve the timestamp, API route, and response time from the log lines, respectively.

## 6. Filtering Invalid Log Lines

The script filters out invalid log lines that do not contain necessary information, such as timestamps or response times. These lines are skipped and logged in the `debug.txt` file for reference.

## 7. Analyzing API Data

The script calculates the response times and hit counts for each API route that falls within the specified time range. The `api_response_times` and `api_hit_count` dictionaries store this data.

## 8. Saving Analysis Results

The script writes the analysis results into the `api_names_with_response_times.txt` file. This file contains API response times and hit counts, sorted by response times in descending order.

## 9. Customization

The script is highly customizable using constant variables. You can modify the `RESPONSE_TIME_THRESHOLD`, `TIME_ZONE_OFFSET`, and `TIME_FORMAT` to fit your specific requirements.

## 10. Conclusion

Congratulations! You have successfully created the **Apache Log Analyzer** script that provides valuable insights into API response times and hit counts. With this script, you can efficiently analyze Apache access log files and gain valuable information about your API performance.

Feel free to explore the code and experiment with different log files and time ranges. If you encounter any issues or have suggestions for improvement, please feel free to contribute to the project.

Happy analyzing! 🚀
