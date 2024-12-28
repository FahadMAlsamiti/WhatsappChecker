import os
import platform
import subprocess
import sys
import importlib
import random
import urllib.request
from pathlib import Path
from tkinter import Tk, filedialog
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import psutil
import time
import json

# قائمة المكتبات المطلوبة
REQUIRED_LIBRARIES = ['selenium', 'webdriver_manager', 'psutil', 'tkinter']

# التحقق من وجود Python
def check_python_installed():
    try:
        subprocess.run(["python", "--version"], check=True)
        print("Python is installed.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Python is not installed.")
        return False

# تثبيت المكتبات المطلوبة
def install_required_libraries():
    for lib in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(f"{lib} not found. Installing it now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# تشغيل جلسة Firefox
def start_or_connect_to_firefox():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--disable-logging")
    print("Starting a new Firefox session.")
    return webdriver.Firefox(options=firefox_options, service=FirefoxService(GeckoDriverManager().install()))

# فتح ملف الأرقام دفعة دفعة
def read_numbers_in_batches(file_path, batch_size):
    with open(file_path, 'r') as file:
        batch = []
        for line in file:
            batch.append(line.strip())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

# اختيار ملف الأرقام
def select_phone_numbers_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Phone Numbers File",
        filetypes=[("Text Files", "*.txt")]
    )
    return file_path

# اختيار مكان حفظ النتائج
def select_output_directory():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Output Directory")
    return folder_path

# التحقق من وجود رقم واتساب بناءً على العناصر المرئية في الصفحة
def check_whatsapp_number(driver, phone_number, max_attempts=3, delay=10):
    url = f"https://web.whatsapp.com/send?phone={phone_number}"
    driver.get(url)
    time.sleep(delay)  # الانتظار الأولي لتحميل الصفحة
    
    attempt = 0
    while attempt < max_attempts:
        try:
            # التحقق من رسالة الخطأ الخاصة بالرقم غير الموجود
            error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'غير صحيح')]")
            if error_elements:
                print(f"{phone_number}: not available (invalid number - no WhatsApp)")
                return False

            # التحقق من وجود مربع الرسائل
            message_box = driver.find_elements(By.XPATH, "//div[contains(@class, 'selectable-text copyable-text')]")
            if message_box:
                print(f"{phone_number}: available (message box found)")
                return True

            # التحقق من الصورة الشخصية أو اسم المستخدم كعلامة على وجود المحادثة
            user_name_element = driver.find_elements(By.XPATH, "//span[@title]")
            if user_name_element:
                print(f"{phone_number}: available (user found)")
                return True

            # زيادة المهلة وإعادة المحاولة
            attempt += 1
            print(f"Attempt {attempt} for {phone_number} failed. Retrying...")
            time.sleep(delay)

        except Exception as e:
            print(f"Error checking {phone_number}: {e}")
            return False

    print(f"{phone_number}: not available (no message box or user found after {max_attempts} attempts)")
    return False

# حفظ الأرقام الصحيحة
def save_numbers_to_file(numbers, file_path):
    with open(file_path, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

# حفظ حالة التقدم إلى ملف مؤقت
def save_progress(temp_file_path, checked_numbers):
    with open(temp_file_path, 'w') as temp_file:
        json.dump(checked_numbers, temp_file)

# تحميل حالة التقدم من ملف مؤقت
def load_progress(temp_file_path):
    if os.path.exists(temp_file_path):
        with open(temp_file_path, 'r') as temp_file:
            return set(json.load(temp_file))
    return set()

# العملية الرئيسية
def main():
    print("Checking system and installing required tools...")
    install_required_libraries()

    driver = start_or_connect_to_firefox()
    driver.get("https://web.whatsapp.com")
    print("Please log in to WhatsApp Web in the browser.")
    input("Press Enter after you have logged in to WhatsApp Web...")

    phone_numbers_file = select_phone_numbers_file()
    output_directory = select_output_directory()

    if not os.path.isfile(phone_numbers_file):
        print("Invalid phone numbers file path.")
        return

    if not os.path.isdir(output_directory):
        print("Invalid output directory.")
        return

    output_file = os.path.join(output_directory, f"whatsapp_numbers_{random.randint(1000, 9999)}.txt")
    temp_file = os.path.join(output_directory, "progress_temp.json")

    # تحميل الأرقام التي تم التحقق منها مسبقًا
    checked_numbers = load_progress(temp_file)
    valid_numbers = []

    # معالجة الأرقام على دفعات
    for phone_batch in read_numbers_in_batches(phone_numbers_file, 100):  # 100 رقم في كل دفعة
        for number in phone_batch:
            if number in checked_numbers:
                print(f"Skipping {number}, already checked.")
                continue

            if check_whatsapp_number(driver, number):
                valid_numbers.append(number)

            # تحديث قائمة الأرقام التي تم التحقق منها وحفظ التقدم
            checked_numbers.add(number)
            save_progress(temp_file, list(checked_numbers))

    # حفظ الأرقام الصحيحة
    save_numbers_to_file(valid_numbers, output_file)
    print(f"Process completed. Valid numbers saved in {output_file}.")

if __name__ == "__main__":
    main()
