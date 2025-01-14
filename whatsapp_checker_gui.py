import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import threading
import queue
import time
import os
import csv
import openpyxl
import subprocess
import sys
import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import platform

# List of required libraries
REQUIRED_LIBRARIES = ['selenium', 'webdriver_manager', 'openpyxl']

# Custom logging handler
class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        log_message = self.format(record)
        self.log_queue.put(log_message)

# Function to check and install missing dependencies
def install_dependencies():
    for lib in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"{lib} not found. Installing it now...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {lib}: {e}")

# Main GUI class
class WhatsAppCheckerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhatsApp Number Checker")
        self.geometry("800x600")

        # Variables
        self.batch_size_var = tk.StringVar(value="10")
        self.delay_var = tk.StringVar(value="10")
        self.attempts_var = tk.StringVar(value="3")
        self.rate_limit_var = tk.StringVar(value="5")
        self.headless_var = tk.IntVar(value=0)
        self.phone_file_path = tk.StringVar()
        self.output_dir_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Idle")
        self.total_numbers_var = tk.StringVar(value="Total: 0")
        self.valid_numbers_var = tk.StringVar(value="Valid: 0")
        self.failed_numbers_var = tk.StringVar(value="Failed: 0")
        self.dark_mode_var = tk.IntVar(value=0)
        self.output_format_var = tk.StringVar(value="txt")  # Default output format
        self.browser_var = tk.StringVar(value="Chrome")  # Default browser

        # Threading events
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.worker_done_event = threading.Event()

        # Logging queue
        self.log_queue = queue.Queue()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('app.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Install missing dependencies
        install_dependencies()

        # Create GUI components
        self.create_widgets()

        # Configure logging
        self.configure_logging()

    def create_widgets(self):
        # Menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Settings", command=self.open_settings)
        settings_menu.add_checkbutton(label="Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode)
        menubar.add_cascade(label="Options", menu=settings_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.open_help)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Batch size
        tk.Label(self, text="Batch Size:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self, textvariable=self.batch_size_var).grid(row=0, column=1, padx=10, pady=5)

        # Delay
        tk.Label(self, text="Delay (s):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self, textvariable=self.delay_var).grid(row=1, column=1, padx=10, pady=5)

        # Attempts
        tk.Label(self, text="Attempts:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self, textvariable=self.attempts_var).grid(row=2, column=1, padx=10, pady=5)

        # Rate Limit
        tk.Label(self, text="Rate Limit (s):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(self, textvariable=self.rate_limit_var).grid(row=3, column=1, padx=10, pady=5)

        # Headless mode
        tk.Checkbutton(self, text="Headless Mode", variable=self.headless_var).grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Browser selection
        tk.Label(self, text="Browser:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.browser_menu = ttk.Combobox(self, textvariable=self.browser_var, values=["Chrome", "Firefox"])
        self.browser_menu.grid(row=4, column=1, padx=10, pady=5)

        # Phone numbers file selection
        tk.Button(self, text="Select Phone Numbers File", command=self.select_phone_file).grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, textvariable=self.phone_file_path).grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Output directory selection
        tk.Button(self, text="Select Output Directory", command=self.select_output_dir).grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, textvariable=self.output_dir_path).grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Output format selection
        tk.Label(self, text="Output Format:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.output_format_menu = ttk.Combobox(self, textvariable=self.output_format_var, values=["txt", "csv", "xlsx"])
        self.output_format_menu.grid(row=7, column=1, padx=10, pady=5)

        # Start, Stop, Pause/Resume buttons
        self.start_button = tk.Button(self, text="Start", command=self.start_process)
        self.start_button.grid(row=8, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_process, state=tk.DISABLED)
        self.stop_button.grid(row=8, column=1, padx=10, pady=10)

        self.pause_button = tk.Button(self, text="Pause", command=self.pause_process, state=tk.DISABLED)
        self.pause_button.grid(row=8, column=2, padx=10, pady=10)

        # Log text widget
        self.log_text = tk.Text(self, wrap="word", state="disabled")
        self.log_text.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.scrollbar = tk.Scrollbar(self, command=self.log_text.yview)
        self.scrollbar.grid(row=10, column=3, padx=0, pady=10, sticky="nsew")
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=11, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Status bar
        tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).grid(row=12, column=0, columnspan=3, sticky="ew")

        # Statistics
        tk.Label(self, textvariable=self.total_numbers_var).grid(row=13, column=0, padx=10, pady=5)
        tk.Label(self, textvariable=self.valid_numbers_var).grid(row=13, column=1, padx=10, pady=5)
        tk.Label(self, textvariable=self.failed_numbers_var).grid(row=13, column=2, padx=10, pady=5)

        # Clear and Save Logs buttons
        tk.Button(self, text="Clear Logs", command=self.clear_logs).grid(row=14, column=0, padx=10, pady=10)
        tk.Button(self, text="Save Logs", command=self.save_logs).grid(row=14, column=1, padx=10, pady=10)

        # Apply dark mode if enabled
        self.toggle_dark_mode()

    def configure_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        queue_handler.setFormatter(formatter)
        self.logger.addHandler(queue_handler)
        self.logger.info("GUI initialized.")

    def select_phone_file(self):
        file_path = filedialog.askopenfilename(title="Select Phone Numbers File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.phone_file_path.set(file_path)

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir_path.set(dir_path)

    def start_process(self):
        # Validate inputs
        if not self.phone_file_path.get() or not self.output_dir_path.get():
            self.logger.error("Please select phone numbers file and output directory.")
            return

        try:
            batch_size = int(self.batch_size_var.get())
            delay = int(self.delay_var.get())
            attempts = int(self.attempts_var.get())
            rate_limit = int(self.rate_limit_var.get())
        except ValueError:
            self.logger.error("Please enter valid integer values for batch size, delay, attempts, and rate limit.")
            return

        # Reset events and enable/disable buttons
        self.stop_event.clear()
        self.pause_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL)

        # Start worker thread
        self.worker_thread = threading.Thread(
            target=self.worker_function,
            args=(batch_size, delay, attempts, rate_limit, self.headless_var.get(), self.phone_file_path.get(), self.output_dir_path.get(), self.browser_var.get())
        )
        self.worker_thread.start()

        # Start queue listener
        self.after(100, self.update_log_from_queue)

    def stop_process(self):
        self.stop_event.set()
        self.status_var.set("Stopped")
        self.logger.info("Process stopped by user.")

    def pause_process(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_button.config(text="Pause")
            self.status_var.set("Running")
            self.logger.info("Process resumed.")
        else:
            self.pause_event.set()
            self.pause_button.config(text="Resume")
            self.status_var.set("Paused")
            self.logger.info("Process paused.")

    def worker_function(self, batch_size, delay, attempts, rate_limit, headless, phone_file, output_dir, browser):
        try:
            if not os.path.isfile(phone_file):
                self.logger.error(f"Phone numbers file not found: {phone_file}")
                return

            if not os.path.isdir(output_dir):
                self.logger.error(f"Output directory not found: {output_dir}")
                return

            self.status_var.set("Running")
            self.logger.info("Starting the process.")

            # Set up WebDriver
            if browser == "Chrome":
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument('--headless')
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            else:
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument('--headless')
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)

            # Open WhatsApp Web
            driver.get("https://web.whatsapp.com")
            self.logger.info("Please log in to WhatsApp Web in the browser.")
            input("Press Enter after you have logged in to WhatsApp Web...")

            # Read phone numbers from file
            with open(phone_file, 'r') as f:
                phone_numbers = [line.strip() for line in f if line.strip()]

            total_numbers = len(phone_numbers)
            valid_numbers = 0
            failed_numbers = 0
            self.total_numbers_var.set(f"Total: {total_numbers}")
            self.valid_numbers_var.set(f"Valid: {valid_numbers}")
            self.failed_numbers_var.set(f"Failed: {failed_numbers}")

            # Process numbers one by one
            for i, number in enumerate(phone_numbers):
                if self.stop_event.is_set():
                    break

                while self.pause_event.is_set():
                    time.sleep(1)

                self.logger.info(f"Checking number: {number}")
                if self.check_whatsapp_number(driver, number, delay, attempts):
                    valid_numbers += 1
                else:
                    failed_numbers += 1

                # Update progress and statistics
                progress = ((i + 1) / total_numbers) * 100
                self.progress_var.set(progress)
                self.total_numbers_var.set(f"Total: {total_numbers}")
                self.valid_numbers_var.set(f"Valid: {valid_numbers}")
                self.failed_numbers_var.set(f"Failed: {failed_numbers}")

                time.sleep(rate_limit)  # Rate limiting

            # Save valid numbers to file
            output_file = self.get_unique_output_file(output_dir, self.output_format_var.get())
            self.save_valid_numbers(output_file, phone_numbers)

            # Close the WebDriver
            driver.quit()

            self.status_var.set("Completed")
            self.logger.info(f"Process completed. Valid numbers saved in {output_file}.")
            self.progress_var.set(100)

            # Signal worker done
            self.log_queue.put(('worker_done',))

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def check_whatsapp_number(self, driver, phone_number, delay, attempts):
        url = f"https://web.whatsapp.com/send?phone={phone_number}"
        driver.get(url)
        time.sleep(delay)  # Wait for the page to load

        for attempt in range(attempts):
            try:
                # Check for error message (invalid number)
                error_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'غير صحيح')]")
                if error_elements:
                    self.logger.info(f"{phone_number}: not available (invalid number - no WhatsApp)")
                    return False

                # Check for message box (valid number)
                message_box = driver.find_elements(By.XPATH, "//div[@role='textbox']")
                if message_box:
                    self.logger.info(f"{phone_number}: available (message box found)")
                    return True

            except Exception as e:
                self.logger.error(f"Error checking {phone_number}: {e}")

            time.sleep(delay)  # Wait before retrying

        self.logger.info(f"{phone_number}: not available (no message box or user found after {attempts} attempts)")
        return False

    def get_unique_output_file(self, output_dir, file_format):
        base_name = "valid_numbers"
        counter = 1
        while True:
            file_name = f"{base_name}_{counter}.{file_format}"
            file_path = os.path.join(output_dir, file_name)
            if not os.path.exists(file_path):
                return file_path
            counter += 1

    def save_valid_numbers(self, output_file, phone_numbers):
        file_format = self.output_format_var.get()
        if file_format == "txt":
            with open(output_file, 'w') as f:
                for number in phone_numbers:
                    f.write(f"{number}\n")
        elif file_format == "csv":
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Phone Numbers"])
                for number in phone_numbers:
                    writer.writerow([number])
        elif file_format == "xlsx":
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Valid Numbers"
            sheet.append(["Phone Numbers"])
            for number in phone_numbers:
                sheet.append([number])
            workbook.save(output_file)

    def update_log_from_queue(self):
        try:
            while True:
                message = self.log_queue.get(block=False)
                if isinstance(message, str):
                    self.log_text.configure(state="normal")
                    self.log_text.insert(tk.END, message + "\n")
                    self.log_text.configure(state="disabled")
                    self.log_text.see(tk.END)
                elif isinstance(message, tuple) and message[0] == 'worker_done':
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.pause_button.config(state=tk.DISABLED)
                    self.status_var.set("Idle")
                elif isinstance(message, tuple) and message[0] == 'progress':
                    self.progress_var.set(message[1])
        except queue.Empty:
            pass
        self.after(100, self.update_log_from_queue)

    def clear_logs(self):
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

    def save_logs(self):
        log_file = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])
        if log_file:
            with open(log_file, "w") as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.logger.info(f"Logs saved to {log_file}")

    def open_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")

        # Add input fields for default values
        tk.Label(settings_window, text="Default Batch Size:").grid(row=0, column=0, padx=10, pady=5)
        batch_size_entry = tk.Entry(settings_window)
        batch_size_entry.grid(row=0, column=1, padx=10, pady=5)
        batch_size_entry.insert(0, self.batch_size_var.get())

        tk.Label(settings_window, text="Default Delay (s):").grid(row=1, column=0, padx=10, pady=5)
        delay_entry = tk.Entry(settings_window)
        delay_entry.grid(row=1, column=1, padx=10, pady=5)
        delay_entry.insert(0, self.delay_var.get())

        # Save settings button
        def save_settings():
            self.batch_size_var.set(batch_size_entry.get())
            self.delay_var.set(delay_entry.get())
            settings_window.destroy()

        tk.Button(settings_window, text="Save", command=save_settings).grid(row=2, column=0, columnspan=2, pady=10)

    def toggle_dark_mode(self):
        if self.dark_mode_var.get():
            # Dark mode colors
            self.configure(background="black")
            self.log_text.configure(background="black", foreground="white")
            # Configure ttk styles for dark mode
            style = ttk.Style()
            style.configure("TButton", background="grey10", foreground="white")
            style.configure("TLabel", background="black", foreground="white")
            style.configure("TEntry", fieldbackground="grey10", foreground="white")
            style.configure("TCombobox", fieldbackground="grey10", foreground="white")
            style.configure("TProgressbar", background="green", troughcolor="black")
            # Configure tkinter widgets
            for widget in self.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(background="black", foreground="white")
                elif isinstance(widget, tk.Button):
                    widget.configure(background="grey10", foreground="white")
                elif isinstance(widget, tk.Entry):
                    widget.configure(background="grey10", foreground="white")
                elif isinstance(widget, tk.Checkbutton):
                    widget.configure(background="black", foreground="white")
        else:
            # Light mode colors
            self.configure(background="white")
            self.log_text.configure(background="white", foreground="black")
            # Configure ttk styles for light mode
            style = ttk.Style()
            style.configure("TButton", background="SystemButtonFace", foreground="black")
            style.configure("TLabel", background="white", foreground="black")
            style.configure("TEntry", fieldbackground="white", foreground="black")
            style.configure("TCombobox", fieldbackground="white", foreground="black")
            style.configure("TProgressbar", background="green", troughcolor="white")
            # Configure tkinter widgets
            for widget in self.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, tk.Button):
                    widget.configure(background="SystemButtonFace", foreground="black")
                elif isinstance(widget, tk.Entry):
                    widget.configure(background="white", foreground="black")
                elif isinstance(widget, tk.Checkbutton):
                    widget.configure(background="white", foreground="black")

    def open_help(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        tk.Label(help_window, text="Instructions:\n1. Select a phone numbers file.\n2. Select an output directory.\n3. Configure settings and click Start.").pack(padx=10, pady=10)

    def preview_numbers(self):
        if not self.phone_file_path.get():
            self.logger.error("No phone numbers file selected.")
            return

        try:
            with open(self.phone_file_path.get(), "r") as f:
                numbers = [line.strip() for line in f.readlines()[:10]]
            preview_window = tk.Toplevel(self)
            preview_window.title("Preview")
            tk.Label(preview_window, text="First 10 numbers:").pack(padx=10, pady=10)
            for number in numbers:
                tk.Label(preview_window, text=number).pack()
        except Exception as e:
            self.logger.error(f"Error previewing numbers: {e}")

    def retry_failed_numbers(self):
        failed_numbers_file = os.path.join(self.output_dir_path.get(), "failed_numbers.txt")
        if not os.path.exists(failed_numbers_file):
            self.logger.error("No failed numbers found.")
            return

        self.phone_file_path.set(failed_numbers_file)
        self.start_process()

# Run the GUI
if __name__ == "__main__":
    app = WhatsAppCheckerGUI()
    app.mainloop()