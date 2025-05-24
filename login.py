
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Open credentials
f = open("cred.txt",'r',encoding = 'utf-8')
line = f.read()
f.close()

# Check if user is new or OLD
if line == "#":
    print("Hello New user! Please provide us your RPH Wifi username and password to auto login on your next start")
    print("Make sure you enter details correctly with Caps")
    usr = str(input("Username:"))
    psw = str(input("Password:"))
    flush = psw + "#" + usr
    f = open("cred.txt",'w',encoding = 'utf-8')
    f.write(flush)
    f.close()
    close = input("We have updated our records. Please reopen the program for updates to apply..\n Press any key to terminate")
    exit()
else:
    cred = line.split("#")
    print("Using saved details>>> Username: {} Password: {}".format(cred[1], cred[0]))
    passwordStr = cred[0]
    usernameStr = cred[1]
    
    # Setup Chrome options to ignore SSL errors
    options = Options()
    options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
    browser = webdriver.Chrome(options=options)
    browser.get('http://172.16.2.1:1000/login?150f9d65e4cc02f5')

    # Wait for the username field and fill it in
    username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    username.send_keys(usernameStr)
    
    # Wait for the password field and fill it in
    password = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password.send_keys(passwordStr)
    
    # Submit the form using JavaScript (auto-submit)
    browser.execute_script("document.querySelector('form').submit()")

    # Wait for a specific element that indicates a successful login (adjust selector as needed)
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Authentication Keepalive")]'))  # Adjust this as needed
        )
        print("Login successful!")
    except:
        print("Login failed or timed out!")

import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import simpledialog

# Global variables for UID and password
user_uid = "23bcs10303"
user_password = "Mayank@2"

# Function to start the browser and perform the login action
def run_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in the background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Set up the Chrome WebDriver with the appropriate driver
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)
    # Use ChromeDriverManager to install the correct driver
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get('http://127.0.0.1:5500/')  # Replace with the actual URL
    
    try:
        # Wait for the page to load
        time.sleep(2)

        # Find the username, password fields, and login button
        username_field = browser.find_element(By.NAME, 'username')
        password_field = browser.find_element(By.NAME, 'password')
        signInButton = browser.find_element(By.NAME, 'login')
        
        # Autofill the fields
        username_field.send_keys(user_uid)
        password_field.send_keys(user_password)
        
        # Submit the form automatically
        signInButton.click()

        print("Logged in successfully!")

    except Exception as e:
        print(f"Error occurred during login: {str(e)}")

    # Close the browser after 5 seconds
    time.sleep(5)
    browser.quit()

# Function to run the browser login process in a separate thread
def start_browser_thread():
    login_thread = threading.Thread(target=run_browser)
    login_thread.start()

# Function to update UID and Password
def update_credentials():
    global user_uid, user_password

    # Ask user for new UID and Password via GUI
    user_uid = simpledialog.askstring("Input", "Enter new UID:", parent=root)
    user_password = simpledialog.askstring("Input", "Enter new Password:", parent=root)

    print(f"Updated UID: {user_uid}")
    print(f"Updated Password: {user_password}")

# Function to create the GUI app
def create_gui():
    global root

    root = tk.Tk()
    root.title("WiFi Auth - Auto Login App")
    
    # Add a label
    label = tk.Label(root, text="WiFi Authentication Auto-Login", font=("Arial", 16))
    label.pack(pady=20)

    # Add a button to start the login process
    login_button = tk.Button(root, text="Start Login", command=start_browser_thread)
    login_button.pack(pady=10)

    # Add a button to update credentials
    update_button = tk.Button(root, text="Update Credentials", command=update_credentials)
    update_button.pack(pady=10)

    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    create_gui()
