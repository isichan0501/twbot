import os, sys
import warnings
import time, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        InvalidArgumentException,
                                        JavascriptException,
                                        NoAlertPresentException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        UnexpectedAlertPresentException,
                                        TimeoutException,
                                        NoSuchElementException)
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service as ChromeService



    
import socket
import time
import random
import string
from colorama import Back, Fore
from os import path
import requests
from .add_proxy import get_proxy_extension
from fake_headers import Headers
import platform
import pysnooper
from contextlib import contextmanager
import shutil
import tempfile
import re
import emoji
import json
from pathlib import Path


from .util_sms import Sms, CountryExpress
from .line_notify import line_push

from dotenv import load_dotenv

# 環境変数を参照
load_dotenv()
apikey = os.getenv('SMSHUB_API_KEY')



def modify_proxy(prox):
    prox = prox.strip()
    px = prox.split(':')
    prx  = "http://{}:{}@{}:{}".format(px[2],px[3],px[0],px[1])
    return prx


def get_proxy_list(file_path='proxy.txt'):
    with open(file_path, mode='r', encoding='utf-8') as f:
        proxys = [prox.strip() for prox in f.readlines()]
    return proxys
    

def check_ip_with_requests():

    try:
        response = requests.get('http://jsonip.com', timeout=20)
        ip = response.json()['ip']
        print('Your public IP is:', ip)
        return True
    except Exception:
        print('proxy set error.return False')
        return False


def set_random_proxy():
    proxys = [modify_proxy(x) for x in get_proxy_list()]
    del_env = os.environ.pop('http_proxy', None)
    del_env = os.environ.pop('https_proxy', None)
    time.sleep(1)
    proxy = random.choice(proxys)

    #proxy用ー失敗するからコメントアウト
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy
    is_proxy = check_ip_with_requests()
    return proxy if is_proxy else is_proxy
    


# ID:PW:email:emailpwのアカウントリストを返す
def get_accounts(file_path='account.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [x.strip() for x in f.readlines()]

    return data

def write_accounts(accounts):
    file_path='account.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(accounts))

def modify_account(account):
    print(f'start @{account}')
    account = account.split(':')
    mydict = {
        'screen_name': account[0],
        'password': account[1],
        'email': account[2],
        'email_pw': account[3],
        'filepath': './db/{}.json'.format(account[0]),
        }

    if 4 < len(account):
        mydict['phone'] = account[4]
    if 5 < len(account):
        mydict['auth_token'] = account[5]
    return mydict

class ProxyExtension:
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
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
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
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, host, port, user, password):
        self._dir = os.path.normpath(tempfile.mkdtemp())

        manifest_file = os.path.join(self._dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(self.manifest_json)

        background_js = self.background_js % (host, port, user, password)
        background_file = os.path.join(self._dir, "background.js")
        with open(background_file, mode="w") as f:
            f.write(background_js)

    @property
    def directory(self):
        return self._dir

    def __del__(self):
        shutil.rmtree(self._dir)


def page_load(driver, myurl):
    waitTime = 5
    for ww in range(1, 4):
        mywait = waitTime * ww
        try:
            driver.get(myurl)
            WebDriverWait(driver, mywait).until(
                EC.presence_of_all_elements_located)
            break
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print(e)


def myClick(driver, by, desc):
    waitn = WebDriverWait(driver, 5)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.element_to_be_clickable((By.XPATH, desc))).click()
        if by == 'ID':
            waitn.until(EC.element_to_be_clickable((By.ID, desc))).click()
        if by == 'LINK_TEXT':
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).click()
        if by == "NAME":
            waitn.until(EC.element_to_be_clickable((By.NAME, desc))).click()
        if by == "CSS":
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).click()
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            desc.click()

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)



def mySendkey(driver, by, desc, my_word):
    waitn = WebDriverWait(driver, 10)
    time.sleep(1)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.element_to_be_clickable((By.XPATH, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.XPATH, desc))).send_keys(my_word)
        if by == 'ID':
            waitn.until(EC.element_to_be_clickable((By.ID, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.ID, desc))).send_keys(my_word)
        if by == 'LINK_TEXT':
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).send_keys(my_word)
        if by == "NAME":
            waitn.until(EC.element_to_be_clickable((By.NAME, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.NAME, desc))).send_keys(my_word)
        if by == "CSS":
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).clear()
            waitn.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).send_keys(my_word)
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            desc.clear()
            desc.send_keys(my_word)

        waitn.until(EC.presence_of_all_elements_located)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        raise


def exe_click(driver, by, desc):
    waitn = WebDriverWait(driver, 10)
    try:
        by = by.upper()
        if by == 'XPATH':
            waitn.until(EC.presence_of_element_located((By.XPATH, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.XPATH, desc))
        if by == 'ID':
            waitn.until(EC.presence_of_element_located((By.ID, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.ID, desc))
        if by == 'LINK_TEXT':
            waitn.until(EC.presence_of_element_located((By.LINK_TEXT, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.LINK_TEXT, desc))
        if by == "NAME":
            waitn.until(EC.presence_of_element_located((By.NAME, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.NAME, desc))
        if by == "CSS":
            waitn.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, desc)))
            driver.execute_script(
                "arguments[0].click();", driver.find_element(By.CSS_SELECTOR, desc))
        if by == "OK":
            waitn.until(EC.presence_of_all_elements_located)
            driver.execute_script("arguments[0].click();", desc)
        waitn.until(EC.presence_of_all_elements_located)

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)
        raise

def emoji_convert(texts):
    mytxt = texts
    for _ in range(20):
        if re.search(r':[a-z]+[^:]+[a-z]:', mytxt):
            emj = re.search(r':[a-z]+[^:]+[a-z]:', mytxt)
            if emj:
                myemj = emj.group()
                mytxt = mytxt.replace(
                    emj, emoji.emojize(myemj, use_aliases=True))
            continue
        else:
            return mytxt


def my_emojiSend(driver, by, desc, my_word):
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    INPUT_EMOJI = """
    arguments[0].value += arguments[1];
    arguments[0].dispatchEvent(new Event('change'));
    """

    try:
        by = by.upper()
        if by == 'XPATH':
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, desc))).clear()
            element = driver.find_element(By.XPATH, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")

        if by == 'ID':
            wait.until(EC.element_to_be_clickable((By.ID, desc))).clear()
            element = driver.find_element(By.ID, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == 'LINK_TEXT':
            wait.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, desc))).clear()
            element = driver.find_element(By.LINK_TEXT, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == "NAME":
            wait.until(EC.element_to_be_clickable((By.NAME, desc))).clear()
            element = driver.find_element(By.NAME,  desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == "TAG_NAME":
            wait.until(EC.element_to_be_clickable(
                (By.TAG_NAME, desc))).clear()
            element = driver.find_element(By.NAME, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == "CSS_SELECTOR":
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, desc))).clear()
            element = driver.find_element(By.CSS_SELECTOR, desc)
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")
        if by == 'OK':
            element = desc
            element.clear()
            mytext = emoji_convert(my_word)
            driver.execute_script(INPUT_EMOJI, element, mytext)
            element.send_keys(" ")

    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)


def check_if_not(driver, by, desc):
    driver.implicitly_wait(2)
    try:
        by = by.upper()
        if by == 'XPATH':
            elem = driver.find_element(By.XPATH, desc)
            if not elem.is_selected():
                elem.click()
        if by == 'ID':
            elem = driver.find_element(By.ID, desc)
            if not elem.is_selected():
                elem.click()
        if by == 'LINK_TEXT':
            elem = driver.find_element(By.LINK_TEXT, desc)
            if not elem.is_selected():
                elem.click()
        if by == "NAME":
            elem = driver.find_element(By.NAME, desc)
            if not elem.is_selected():
                elem.click()
        if by == "TAG_NAME":
            elem = driver.find_element(By.TAG_NAME, desc)
            if not elem.is_selected():
                elem.click()
        if by == "CSS_SELECTOR":
            elem = driver.find_element(By.CSS_SELECTOR, desc)
            if not elem.is_selected():
                elem.click()
        if by == "OK":
            if not desc.is_selected():
                desc.click()
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception, ElementNotInteractableException) as ex:
        print(ex)

    finally:
        driver.implicitly_wait(5)


def action_click(driver, elem):
    # elemは(By.XPATH, 'xpath')のようなタプル
    waitn = WebDriverWait(driver, 5)
    try:
        elem = waitn.until(EC.element_to_be_clickable(elem))
        webdriver.ActionChains(driver).move_to_element(elem).click().perform()
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as ex:
        print(ex)


def wifi_reboot(driver, passwd='admin'):
    try:
        page_load(driver,"http://web.setting/html/home.html")
        myClick(driver, "id", "settings")
        time.sleep(2)
        # import pdb; pdb.set_trace()
        myClick(driver, "id", "password")
        time.sleep(1)
        mySendkey(driver,"id","password",passwd)
        time.sleep(1)
        exe_click(driver, "link_text", "ログイン")
        time.sleep(2)
        if driver.current_url != "http://web.setting/html/quicksetup.html":
            exe_click(driver, "link_text", "ログイン")
            time.sleep(2)
        driver.refresh()
        time.sleep(3)
        myClick(driver, "id", "system")
        myClick(driver, "link_text", "再起動")
        time.sleep(2)
        exe_click(driver, "id", "button_reboot")
        # myClick(driver, "css", ".button_center")
        time.sleep(2)
        exe_click(driver, "link_text", "はい")
        time.sleep(3)
        wait_str = driver.find_element(By.ID, "wait_table").text
        print(wait_str)
        time.sleep(5)
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)


@pysnooper.snoop()
def check_ip(driver):
    for i in range(5):
        try:
            driver.get('http://ip.smartproxy.com/')
            time.sleep(4)
            body_text = driver.find_element_by_tag_name('body').text
            print('myip is {}'.format(body_text))
            return body_text
        except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
            print(e)
    return False


@pysnooper.snoop()
def start_driver(prox=None):
    OSNAME = platform.system()
    if OSNAME == 'Linux':
        OSNAME = 'lin'
    elif OSNAME == 'Darwin':
        OSNAME = 'mac'
    elif OSNAME == 'Windows':
        OSNAME = 'win'

    header = Headers(
        browser="chrome",
        os=OSNAME,
        headers=False
    ).generate()
    agent = header['User-Agent']
    print(agent)
    option = uc.ChromeOptions()
    # option = webdriver.ChromeOptions()
    
    # setting profile
    # option.user_data_dir = "C:\\temp\\profile"
    option.add_argument('--user-data-dir=C:\\temp\\profile1')
    # option.add_argument("--enable-javascript")
    # option.add_argument('--profile-directory=Profile1')

    # option.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    # option.add_argument("--proxy-bypass-list:localhost,127.0.0.1")
    # option.add_argument('--no-default-browser-check')
    option.add_argument("--mute-audio")
    option.add_argument('--allow-file-access-from-files')
    # option.add_argument('--disable-web-security')
    # option.add_experimental_option("excludeSwitches", ['enable-automation'])
    # option.add_argument('--disable-blink-features=AutomationControlled')
    # co.add_argument('--disable-gpu')
    
    option.add_argument('--start-maximized')
    # option.add_argument('--disable-popup-blocking')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-web-security')
    option.add_argument('--no-sandbox')
    option.add_argument('--log-level=3')
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors=yes')
    #画像消す
    # option.add_argument('--blink-settings=imagesEnabled=false')
    # option.page_load_strategy = 'eager'
    # option.add_argument('--allow-running-insecure-content')

    
    option.add_argument("--disable-site-isolation-trials")
    option.add_experimental_option('prefs', {'enable_do_not_track': True})
    #言語設定
    # option.add_argument('--lang=ja-JP')
    option.add_argument('--lang=en-US')
    # option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # option.add_experimental_option('useAutomationExtension', False)
    option.add_argument(f'--user-agent={agent}')
    # option.add_argument(f'--proxy-server=http://{proxy}')
    # option.add_extension('./nopecha.crx')

    
    ch_r = [os.path.join(os.path.abspath(os.path.dirname(__file__))), 'ifibfemgeogfhoebkmokieepdoobkbpo', '3.3.0_0']
    crxpath = os.path.join(*ch_r)
    # option.add_argument('--load-extension={}'.format(crxpath))
    # option.add_argument('--load-extension=C:\\Users\\sibuy\\anaconda3\\envs\\py39\Scripts\\\TwitterFrontendFlow\\ifibfemgeogfhoebkmokieepdoobkbpo\\3.3.0_0')
    
    if prox:
        PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = prox.split(':')
        proxy = (PROXY_HOST, int(PROXY_PORT), PROXY_USER, PROXY_PASS)  # your proxy with auth, this one is obviously fake
        proxy_extension = ProxyExtension(*proxy)
        option.add_argument(f"--load-extension={proxy_extension.directory},{crxpath}")
        # pluginfile = get_proxy_extension(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        # # option.add_extension(pluginfile)
        # option.add_argument('--load-extension={}'.format(pluginfile))
        # option.add_argument('--proxy-server=http://{}:{}'.format(PROXY_HOST,PROXY_PORT))
        # option.add_argument('--proxy-auth={}:{}'.format(PROXY_USER, PROXY_PASS))
    
    # option.add_extension(os.getcwd() + '\solver.crx') # gets the directory of the hCap solver.
    # option.add_experimental_option("excludeSwitches", ["enable-logging"])

    #option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1")
    driver = uc.Chrome(options=option)
    # service = ChromeService(executable_path=ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=option)
    # driver.delete_all_cookies()
    driver.implicitly_wait(20)
    driver.set_page_load_timeout(130)
    return driver


@contextmanager
def driver_set(prox):

    driver = start_driver(prox=prox)
    try:
        yield driver
    finally:
        driver.quit()

def captcha_setting(driver):
    try:
        driver.get('https://www.cman.jp/network/support/go_access.cgi')
        time.sleep(2)
        driver.get('chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html')
        time.sleep(1)
        driver.find_element(By.ID, "connect").click()
        time.sleep(8)
        Alert(driver).accept()
        return True
    except (UnexpectedAlertPresentException, NoSuchElementException, TimeoutException, NoAlertPresentException) as e:
        print(e)
        return False
        
def driver_quit(driver):
    driver.delete_all_cookies()
    driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
        "origin": '*',
        "storageTypes": 'all',
    })
    time.sleep(3)
    driver.quit()
    time.sleep(1)


def unlock_outlook(prox, email, email_pw, country_exp="ロシア"):
    #sms-activate
    service = 'mm'
    sms = Sms(apikey)
    #----outlook login----

    try:
        driver = start_driver(prox=prox)
        driver.get('https://outlook.live.com/owa/logoff.owa')
        driver.get('https://login.live.com/login.srf')
        # import pdb;pdb.set_trace()
        print('a')
        mySendkey(driver, "xpath", "//input[@id='i0116']", email)
        myClick(driver, "id", "idSIButton9")
        time.sleep(3)
        driver.execute_script("document.getElementById('i0118').setAttribute('class', 'form-control')")
        mySendkey(driver, "xpath", "//input[@id='i0118']", email_pw)
        driver.execute_script("document.getElementById('idSIButton9').disabled=false")
        myClick(driver, "id", "idSIButton9")
        time.sleep(3)
        #ロックされてるかチェック-'Your account has been temporarily suspended'
        
        if 'suspended' in driver.title:
            country_id = CountryExpress.smshub_id(country_exp)
            country_code = CountryExpress.code(country_exp)
            res = sms._get(service, operator='any', country=country_id)
            activate_id, country_code, sms_number_not_country = sms._get_id_number(res)
            print(activate_id, country_code, sms_number_not_country)
            myClick(driver, 'id', 'StartAction')
            select = Select(driver.find_element(By.TAG_NAME, "select"))
            select.select_by_value(country_code)
            #番号入力
            elem = driver.find_element(By.XPATH, "//*[@id=\"wlspispHipChallengeContainer\"]//input[@autocomplete=\"off\"]")
            mySendkey(driver, "ok", elem, sms_number_not_country)
            time.sleep(2)
            # exe_click(driver, "LINK_TEXT", "Send code")
            #send code
            myClick(driver, "LINK_TEXT", "Send code")
            pin_code = sms.wait_for_pin_activate(activate_id)
            mySendkey(driver, "xpath", "//input[@aria-label=\"Enter the access code\"]", pin_code)
            time.sleep(2)
            myClick(driver, "id", "ProofAction")
            time.sleep(3)
            myClick(driver, "id", "FinishAction")
            time.sleep(3)
            myClick(driver, "id", "idSIButton9")
            time.sleep(2)

        else:
            myClick(driver, "id", "idBtn_Back")
            driver.get(r'https://outlook.live.com/mail/0/')
            
        return True
    
    except (socket.timeout, NoSuchElementException, TimeoutException, Exception) as e:
        print(e)
        return False



def twitter_login(prox, screen_name, password):
    try:
        driver = start_driver(prox=prox)
        page_load(driver, 'https://twitter.com')
        time.sleep(2)
        # login button
        login_bt = driver.find_element(
            By.XPATH, '//a[@href="/login"]')
        webdriver.ActionChains(driver).move_to_element(login_bt).click().perform()
        time.sleep(2)
        element = driver.find_element(By.CSS_SELECTOR,'#react-root input')
        action = webdriver.ActionChains(driver)
        action.send_keys_to_element(element, screen_name).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
        time.sleep(2)
        # password input
        element = driver.find_elements(By.CSS_SELECTOR,'#layers > div:nth-child(2) input')[1]
        action = webdriver.ActionChains(driver)
        action.send_keys_to_element(element, password).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
        time.sleep(2)
        
        # submit_check = [(By.XPATH, '//a[@href="/compose/tweet"]'), None]
        # passed = recaptcha_solver_api(driver, submit_check_element=submit_check)

        # recaptcha check:
        # driver.get('https://www.google.com/recaptcha/api2/demo')
        # submit_check = [(By.CSS_SELECTOR, 'div.recaptcha-success'), 'Проверка прошла успешно… Ура!']
        # submit = None
        # passed = recaptcha_solver_api(driver, submit=submit,
        #                               submit_check_element=submit_check)
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()


@pysnooper.snoop()
def submit_login_button(driver):
    try:
        # login-button
        login_bt = driver.find_element(By.XPATH, '//a[@href="/login"]')
        webdriver.ActionChains(driver).move_to_element(login_bt).click().perform()
        time.sleep(6)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def send_screen_name(driver, screen_name):
    try:
        #username input
        element = driver.find_element(By.CSS_SELECTOR,'#react-root input')
        action = webdriver.ActionChains(driver)
        action.send_keys_to_element(element, screen_name).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
        time.sleep(6)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def send_password(driver, password):
    try:
        # password input
        element = driver.find_elements(By.CSS_SELECTOR,'#layers > div:nth-child(2) input')[1]
        action = webdriver.ActionChains(driver)
        action.send_keys_to_element(element, password).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
        time.sleep(6)
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def input_email(driver, email):
    try:
        #email input
        elements = driver.find_elements(By.XPATH,'//input[@type=\"email\"]')
        if len(elements) != 0:
            element = elements[0]
            action = webdriver.ActionChains(driver)
            action.send_keys_to_element(element, email).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
        time.sleep(6)
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def is_login_success(driver):
    try:
        if 'https://twitter.com/home' in driver.current_url:
            #要素があれば正常にログイン完了した
            tweet_elem = driver.find_elements(By.XPATH, '//a[@href="/compose/tweet"]')
            if len(tweet_elem) != 0:
                return True
            # continue
        return False
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def wait_solve_captcha(driver):
    try:
        
        if 'https://twitter.com/account/access' not in driver.current_url:
            return True
        page_title = driver.find_element(By.XPATH, "//div[@class=\"PageHeader Edge\"]").text
        #ロック解除
        if page_title == 'Your account has been locked.':
            element = driver.find_element(By.XPATH, "//input[@value=\"Start\"]")
            webdriver.ActionChains(driver).move_to_element(element).click().perform()
            time.sleep(3)
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        time.sleep(5)
        element = WebDriverWait(driver, 180).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id=\"arkose_form\"]")))
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

@pysnooper.snoop()
def input_phone(driver, country_exp):
    sms = Sms(apikey)
    service = 'tw'

    try:
        if 'https://twitter.com/account/access' not in driver.current_url:
            return True
        page_title = driver.find_element(By.XPATH, "//div[@class=\"PageHeader Edge\"]").text
        if page_title == 'Enter your phone number':
            discover_phone = driver.find_element(By.XPATH, "//input[@name=\"discoverable_by_mobile_phone\"]")
            if discover_phone.get_attribute('checked') == 'true':
                myClick(driver, "xpath", "//input[@name=\"discoverable_by_mobile_phone\"]")
            #sms-activate--
            res = sms._get(service, operator='any', country=country_exp)
            #smshubの国ID #BR #国番号 +55
            country_id, country_code, tel_code = sms.country_id, sms.country_code, str(sms.tel_code)
            activate_id, sms_number_not_country = sms._get_id_number(res)
            print(activate_id, sms_number_not_country)
            #input sms-activate
            select = Select(driver.find_element(By.XPATH, "//*[@id=\"country_code\"]"))
            if select.first_selected_option.get_attribute('value') != tel_code:
                select.select_by_value("{}".format(tel_code))
            element = driver.find_element(By.XPATH,"//input[@id=\"phone_number\"]")
            action = webdriver.ActionChains(driver)
            action.send_keys_to_element(element, sms_number_not_country).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
            #pincode
            pin_code = sms.wait_for_pin_activate_next(activate_id)
            time.sleep(2)
            element = driver.find_element(By.XPATH,"//input[@id=\"code\"]")
            action = webdriver.ActionChains(driver)
            action.send_keys_to_element(element, pin_code).pause(random.uniform(.1, .5)).send_keys_to_element(element, Keys.ENTER).perform()
            time.sleep(6)
            elem = driver.find_elements(By.XPATH, "//input[@type=\"submit\"]")
            if 0 < len(elem):
                elem[0].submit()
            time.sleep(6)
            WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
            page_title = driver.find_element(By.XPATH, "//div[@class=\"PageHeader Edge\"]").text
            print(page_title)
            elem = driver.find_element(By.XPATH, "//input[@type=\"submit\"]")
            webdriver.ActionChains(driver).move_to_element(elem).click().perform()
            time.sleep(4)
            driver.refresh()
            time.sleep(4)
            return True

        return False
                
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False



if __name__ == "__main__":
    
    country_exp="カザフスタン"

    proxys = get_proxy_list()
    accounts = get_accounts()
    
    for account in accounts:
        account = account.split(':')
        screen_name,password,email,email_pw = account[0],account[1],account[2],account[3]
        prox = random.choice(proxys)
        #メインフロー(username, pass, email, phone, pincode, continue, tweet-compaseで確認)
        driver = start_driver(prox=prox)
        # driver_quit(driver)
        # import pdb;pdb.set_trace()
        is_setting = captcha_setting(driver)
        if not is_setting:
            driver_quit(driver)
            continue
        page_load(driver, 'https://twitter.com');time.sleep(16)

        import pdb;pdb.set_trace()
        dbpath = 'db/' + screen_name + '.json'
        # retrieve cookies from a json file
        for cookie in json.loads(Path(dbpath).read_text()):
            driver.add_cookie(cookie)

        import pdb;pdb.set_trace()
        
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        
        is_ok = submit_login_button(driver)
        is_ok = send_screen_name(driver, screen_name)
        is_ok = send_password(driver, password)
        
        is_ok = input_email(driver, email)
        if 'https://twitter.com/account/access' in driver.current_url:
            is_ok = wait_solve_captcha(driver)
            # import pdb;pdb.set_trace()
            is_ok = input_phone(driver, country_exp)

        is_ok = is_login_success(driver)
        if is_ok:
            line_push('twitter. {} is unlock success!'.format(":".join(account)))
            #アカウントリストから削除
            ac = ":".join(account)
            accounts.remove(ac)
            write_accounts(accounts)
        
        # import pdb;pdb.set_trace()
        driver_quit(driver)


        

        # import pdb;pdb.set_trace()
        
        # print('a')