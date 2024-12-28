ملف README.md
markdown
نسخ الكود
# WhatsApp Number Checker  
> **A Python-based program to validate WhatsApp numbers via WhatsApp Web.**  
> **برنامج بايثون للتحقق من أرقام الواتساب باستخدام واتساب ويب.**

---

## **Table of Contents | جدول المحتويات**  
- [Introduction | مقدمة](#introduction--مقدمة)  
- [Features | الميزات](#features--الميزات)  
- [System Requirements | متطلبات النظام](#system-requirements--متطلبات-النظام)  
- [Installation | خطوات التثبيت](#installation--خطوات-التثبيت)  
- [Usage | كيفية الاستخدام](#usage--كيفية-الاستخدام)  
- [Troubleshooting | استكشاف الأخطاء](#troubleshooting--استكشاف-الأخطاء)  
- [License | الرخصة](#license--الرخصة)  

---

## **Introduction | مقدمة**  
**WhatsApp Number Checker** is a program that automates the process of validating WhatsApp numbers using Selenium WebDriver and Firefox browser.  

**برنامج "WhatsApp Number Checker"** هو برنامج يقوم بأتمتة عملية التحقق من أرقام الواتساب باستخدام Selenium WebDriver ومتصفح Firefox.  

---

## **Features | الميزات**  
- Validates WhatsApp numbers using **WhatsApp Web**.  
- Supports **batch processing** for large datasets.  
- Automatically installs required dependencies.  
- Supports **restarting from the last checked number** in case of interruptions.  

- يتحقق من أرقام الواتساب باستخدام **واتساب ويب**.  
- يدعم **معالجة الأرقام على دفعات** للملفات الكبيرة.  
- يقوم بتثبيت المتطلبات الضرورية تلقائيًا.  
- يدعم **استئناف التحقق من الرقم الأخير** في حالة حدوث انقطاع.  

---

## **System Requirements | متطلبات النظام**  
### **Operating System | نظام التشغيل**  
- **Windows**, **macOS**, or **Linux**  

### **Python Version | إصدار بايثون**  
- Python **3.8** or higher | إصدار بايثون 3.8 أو أعلى  

### **Browser | المتصفح**  
- Mozilla Firefox | متصفح Firefox  

### **Python Libraries | مكتبات بايثون**  
- `selenium`  
- `webdriver_manager`  
- `psutil`  
- `tkinter`  

---

## **Installation | خطوات التثبيت**  

### **1. Install Python | تثبيت بايثون**  
#### **Windows**  
Download Python from [python.org](https://www.python.org/) and select **Add Python to PATH** during installation.  

#### **Linux/macOS**  
Run the following command:  
```bash
sudo apt-get install python3 python3-pip  # Linux
brew install python  # macOS
2. Verify Python Installation | التحقق من تثبيت بايثون
Run the following command:

bash
نسخ الكود
python --version
3. Install Required Libraries | تثبيت مكتبات بايثون المطلوبة
Run this command:

bash
نسخ الكود
pip install selenium webdriver-manager psutil
4. Install Firefox | تثبيت متصفح فايرفوكس
Windows
Download Firefox from firefox.com.

Linux
bash
نسخ الكود
sudo apt-get install firefox
macOS
bash
نسخ الكود
brew install --cask firefox
5. Run the Program | تشغيل البرنامج
Run the program using this command:

bash
نسخ الكود
python whatsapp_check.py
Usage | كيفية الاستخدام
Prepare a text file (.txt) containing the phone numbers you wish to validate. Each number should be on a separate line.

Launch the program and log in to WhatsApp Web when prompted.

Select the file with numbers and choose an output directory to save the results.

The program will process the numbers and save the valid ones in the specified output file.

قم بتحضير ملف نصي (.txt) يحتوي على أرقام الهواتف التي تريد التحقق منها. يجب أن يكون كل رقم في سطر منفصل.

شغل البرنامج وقم بتسجيل الدخول إلى واتساب ويب عند طلب ذلك.

اختر ملف الأرقام وحدد مجلدًا لحفظ النتائج.

سيقوم البرنامج بمعالجة الأرقام وحفظ الأرقام الصالحة في الملف المحدد.

Troubleshooting | استكشاف الأخطاء
Error: Module Not Found
Run this command:

bash
نسخ الكود
pip install <missing_library>
Browser Not Found
Ensure that Firefox is installed and added to the system PATH.

Connection Timeout
Check your internet connection and restart the program.

License | الرخصة
This project is licensed under the MIT License.
هذا المشروع مرخص بموجب رخصة MIT.

yaml
