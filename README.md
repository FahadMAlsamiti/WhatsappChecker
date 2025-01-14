# WhatsApp Number Checker

### Author: En.FahadMAlsamiti

---

## Overview
The **WhatsApp Number Checker** is a tool designed to verify the availability of WhatsApp accounts associated with phone numbers. This repository contains two versions of the tool:

1. **Command-Line Version (`whatsapp_check.py`)**: A script-based implementation for batch processing phone numbers.
2. **GUI Version (`whatsapp_checker_gui.py`)**: A user-friendly graphical interface with advanced configuration options.

---

## Features

### Command-Line Version (`whatsapp_check.py`):
- Reads phone numbers from a text file.
- Processes numbers in batches.
- Verifies WhatsApp availability via Firefox.
- Saves valid numbers to a text file.
- Allows resuming progress using a temporary file.

### GUI Version (`whatsapp_checker_gui.py`):
- Provides a graphical interface for easier use.
- Supports both Chrome and Firefox.
- Offers advanced configuration options:
  - Batch size.
  - Delay between requests.
  - Number of retry attempts.
- Dark mode support.
- Outputs results in multiple formats (TXT, CSV, XLSX).
- Displays progress and logs in real-time.

---

## Requirements

### Common Dependencies
- Python 3.7 or higher.
- Internet connection.
- WebDriver Manager (`webdriver_manager`).
- Selenium (`selenium`).

### Additional Dependencies for GUI Version
- `tkinter` (for GUI components).
- `openpyxl` (for XLSX output).
- `queue` and `threading` (for concurrency).

### Browser Support
- **Command-Line Version**: Requires Firefox.
- **GUI Version**: Supports both Chrome and Firefox.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install required Python libraries:
   ```bash
   pip install selenium webdriver_manager openpyxl
   ```

### Note:
The script will automatically install missing dependencies if not found.

---

## Usage

### Command-Line Version (`whatsapp_check.py`):
1. Run the script:
   ```bash
   python whatsapp_check.py
   ```
2. Follow the prompts to:
   - Select the file containing phone numbers.
   - Select an output directory.
   - Log in to WhatsApp Web manually in the Firefox browser.
3. The script will process phone numbers and save valid ones to the output file.

### GUI Version (`whatsapp_checker_gui.py`):
1. Run the script:
   ```bash
   python whatsapp_checker_gui.py
   ```
2. Configure the following settings in the GUI:
   - Batch size, delay, attempts, and rate limits.
   - Output format (TXT, CSV, or XLSX).
   - Browser (Chrome or Firefox).
   - Dark mode (optional).
3. Select the phone numbers file and output directory.
4. Click "Start" to begin the process.
5. Monitor the progress, logs, and results via the interface.

---

## Differences Between Versions

| Feature                   | Command-Line Version        | GUI Version                |
|---------------------------|-----------------------------|----------------------------|
| **Interface**            | Command-Line                | Graphical (GUI)            |
| **Browsers Supported**   | Firefox                     | Chrome, Firefox            |
| **Output Formats**       | TXT                         | TXT, CSV, XLSX             |
| **Customization Options**| Limited                     | Extensive                  |
| **Pause/Resume**         | Not Supported               | Supported                  |
| **Dark Mode**            | Not Available               | Available                  |

---

## Example Output

### Command-Line Version
```
Checking number: +1234567890
+1234567890: available (message box found)
+0987654321: not available (invalid number - no WhatsApp)
```
Output file: `whatsapp_numbers_1234.txt`

### GUI Version
- Progress bar indicates completion.
- Logs are displayed in the GUI.
- Valid numbers are saved in the chosen format (e.g., `valid_numbers_1.xlsx`).

---

## Troubleshooting

1. **WebDriver Errors**: Ensure the appropriate WebDriver is installed and up-to-date.
   - Chrome: `webdriver_manager.chrome`.
   - Firefox: `webdriver_manager.firefox`.

2. **Login Issues**: Log in to WhatsApp Web manually when prompted.

3. **Dependencies Not Found**: Run the following command:
   ```bash
   pip install selenium webdriver_manager openpyxl
   ```

---

## Contribution
Contributions are welcome! Please fork the repository and submit a pull request.

---

## License
This project is licensed under the MIT License.
