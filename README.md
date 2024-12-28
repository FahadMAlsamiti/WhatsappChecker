# WhatsApp Number Checker
> **A Python-based program to validate WhatsApp numbers via WhatsApp Web.**

---

## **Table of Contents**
- [Introduction](#introduction)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## **Introduction**
**WhatsApp Number Checker** is a program that automates the process of validating WhatsApp numbers using Selenium WebDriver and Firefox browser. It is designed to process large datasets efficiently and supports batch processing and resumption after interruptions.

---

## **Features**
- Validates WhatsApp numbers using **WhatsApp Web**.
- Supports **batch processing** for large datasets.
- Automatically installs required dependencies.
- Supports **resumption** from the last checked number in case of interruptions.

---

## **System Requirements**
### **Operating System**
- **Windows**, **macOS**, or **Linux**

### **Python Version**
- Python **3.8** or higher

### **Browser**
- Mozilla Firefox

### **Python Libraries**
- `selenium`
- `webdriver_manager`
- `psutil`
- `tkinter`

---

## **Installation**

### **1. Install Python**
#### **Windows**
Download Python from [python.org](https://www.python.org/) and select **Add Python to PATH** during installation.

#### **Linux/macOS**
Run the following command:
```bash
sudo apt-get install python3 python3-pip  # Linux
brew install python  # macOS
```

---

### **2. Verify Python Installation**
Run the following command:
```bash
python --version
```

---

### **3. Install Required Libraries**
Run this command:
```bash
pip install selenium webdriver-manager psutil
```

---

### **4. Install Firefox**
#### **Windows**
Download Firefox from [firefox.com](https://www.mozilla.org/firefox/new/).

#### **Linux**
```bash
sudo apt-get install firefox
```

#### **macOS**
```bash
brew install --cask firefox
```

---

### **5. Run the Program**
Run the program using this command:
```bash
python whatsapp_check.py
```

---

## **Usage**
1. Prepare a text file (`.txt`) containing the phone numbers you wish to validate. Each number should be on a separate line.
2. Launch the program and log in to WhatsApp Web when prompted.
3. Select the file with numbers and choose an output directory to save the results.
4. The program will process the numbers and save the valid ones in the specified output file.

---

## **Troubleshooting**
- **Error: Module Not Found**
  Run this command:
  ```bash
  pip install <missing_library>
  ```

- **Browser Not Found**
  Ensure that Firefox is installed and added to the system PATH.

- **Connection Timeout**
  Check your internet connection and restart the program.

---

## **License**
This project is licensed under the MIT License.
