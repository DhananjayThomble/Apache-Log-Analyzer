# Apache Log Analyzer

![GitHub last commit](https://img.shields.io/github/last-commit/DhananjayThomble/Apache-Log-Analyzer)
![GitHub](https://img.shields.io/github/license/DhananjayThomble/Apache-Log-Analyzer)

Apache Log Analyzer is a Python script that analyzes Apache access log files and provides insights into API response times and hit counts for different routes. It extracts relevant information from the log file and calculates response times and hit counts for each API route within a specified time range.
It helps you gain insights into your web server's performance and identify potential issues.

## Features

- Choose the log file from your local storage using a user-friendly interface.
- Customize the time range for API analysis based on specific dates or predefined options (Yesterday's All Logs, Custom, Yesterday 5AM to 12AM).
- Set your desired threshold for API response times (in milliseconds) using a constant variable.
- Extract and analyze timestamps, API routes, and response times from the log file.
- Calculate API hit counts and identify routes with higher response times.
- Save the analysis results in a separate output file.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

```bash
git clone https://github.com/DhananjayThomble/Apache-Log-Analyzer.git
cd Apache-Log-Analyzer
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

1. Run the script:

```bash
python api_log_analysis.py
```

2. Select the Apache access log file you want to analyze using the file dialog.
3. Choose the time range for the analysis based on your preference or select a predefined option.
4. View the analysis results in the `api_names_with_response_times.txt` file.

## Configuration

You can customize the following settings in the script:

- `RESPONSE_TIME_THRESHOLD`: Set your desired threshold for API response times (in milliseconds).
- `TIME_ZONE_OFFSET`: Set your desired timezone offset.
- `TIME_FORMAT`: Set your desired time format for timestamp extraction.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
