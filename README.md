# WhatsappChecker
A powerful and efficient tool designed to validate WhatsApp numbers in bulk. This program leverages Selenium and browser automation to identify active WhatsApp accounts quickly and accurately.

### Features:  
- **Bulk Number Validation**: Process thousands of numbers in a single run.  
- **Error Handling**: Automatically saves progress and handles interruptions like internet disconnections or browser crashes.  
- **User-Friendly**: Supports file-based input/output for seamless user interaction.  
- **Smart Retry Mechanism**: Automatically retries numbers that fail to load due to network or temporary errors.  
- **Multi-Platform Support**: Compatible with Windows, macOS, and Linux systems.  
- **Firefox Integration**: Automates WhatsApp Web using Firefox for reliable performance.  

### Use Cases:  
- Verify customer contact lists for businesses.  
- Identify inactive or invalid WhatsApp numbers.  
- Streamline bulk messaging campaigns by focusing only on active users.  

### How to Use:  
1. Install Python and required libraries.  
2. Run the script and log in to WhatsApp Web.  
3. Provide a file with phone numbers and specify an output directory.  
4. Let the tool validate numbers automatically and save the results.

5. ### System Requirements:
1. Operating System
   Windows , Linux , MacOS
2. Python V 3.8 or higher
3. Browser ( Mozilla Firefox )

### Required Python Libraries
1. selenium
2. webdriver_manager
3. psutil
4. tkinter (Included in Python by default on Windows, but you may need to install it on Linux.)

### Installation Instructions
1. install Python
   Windows ( Download Python from python.org and choose "Add Python to PATH" during installation. )
   Linux , MacOS
   Use the package manager to install Python:
# For Linux ( sudo apt-get install python3 python3-pip )
# For macOS ( brew install python )
2. Verify Python Installation
   Open a command line and make sure Python is installed correctly: ( python --version )
3. Install Required Libraries
   To install all required libraries, run the following command: ( pip install selenium webdriver-manager psutil )
4. Install Firefox
   Windows : Download Firefox from firefox.com
   Linux : ( sudo apt-get install firefox )
   MacOS : ( brew install --cask firefox )
5. (Optional) Install Geckodriver Manually
   If Geckodriver is not installed automatically, you can download it manually: Visit Geckodriver Releases.
   Place the executable file in the system path.
6. Run the Program
   Run the program using the following command: ( python whatsapp_check.py )
   

