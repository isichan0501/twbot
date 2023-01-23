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
from fake_headers import Headers
import platform
import pysnooper
from contextlib import contextmanager
import shutil
import tempfile
import json
from pathlib import Path


from BotHelper.util_sms import Sms, CountryExpress
from BotHelper.line_notify import line_push
from BotHelper.util_driver import ProxyExtension, page_load, myClick, mySendkey, exe_click,check_ip,start_driver,captcha_setting,driver_quit
from BotHelper.util_driver import unlock_outlook,get_proxy_list,get_accounts, write_accounts, modify_account,modify_proxy
from dotenv import load_dotenv

# 環境変数を参照
load_dotenv()
SMSHUB_API_KEY = os.getenv('SMSHUB_API_KEY')
IPROYAL_API_TOKEN = os.getenv('IPROYAL_API_TOKEN')





@contextmanager
def driver_set(prox):

    driver = start_driver(prox=prox)
    try:
        yield driver
    finally:
        driver.quit()



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
def start_captcha(driver):
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
    sms = Sms(SMSHUB_API_KEY)
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
            elem = driver.find_element(By.XPATH, "//input[@type=\"submit\"]")
            webdriver.ActionChains(driver).move_to_element(elem).click().perform()
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


@pysnooper.snoop()
def wait_solve_captcha(driver):
    try:
        page_title = driver.find_elements(By.XPATH, "//div[@class=\"PageHeader Edge\"]")
        if len(page_title) != 0:
            return False
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        
    for _ in range(5):
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#arkose_iframe')))
        except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
                JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
            print(e)

    for _ in range(10):
        try:
            #iframeを３回移動して内側に
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            if (iframe.get_attribute('id') == "arkose_iframe") or (iframe.get_attribute('title') == "Verification challenge"):
                driver.switch_to.frame(iframe)
                continue
            if iframe.get_attribute('id') == "fc-iframe-wrap":
                print('solving...')
                is_solve = driver.find_element(By.CSS_SELECTOR, "#challenge > div.captcha-solver").get_attribute('data-state')
                if is_solve == 'error':
                    driver.refresh();time.sleep(5)
                    continue
                else:
                    element = WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id=\"arkose_form\"]")))
                return True
        
        except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
                JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
            print(e)
    return False



def click_submit_btn(driver):
    try:
        elem = driver.find_element(By.XPATH, "//input[@type=\"submit\"]")
        webdriver.ActionChains(driver).move_to_element(elem).click().perform()
        time.sleep(6)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False

def load_twitter_cookies(driver, filepath):
    try:
        page_load(driver, 'https://twitter.com');time.sleep(6)
        # retrieve cookies from a json file
        for cookie in json.loads(Path(filepath).read_text()):
            driver.add_cookie(cookie)

        time.sleep(5)
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        driver.refresh();time.sleep(5)
        WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located)
        return True
    except (socket.timeout, NoSuchElementException, TimeoutException, ElementClickInterceptedException,ElementNotInteractableException,InvalidArgumentException,
            JavascriptException,NoAlertPresentException,StaleElementReferenceException,UnexpectedAlertPresentException,NoSuchElementException,Exception) as e:
        print(e)
        return False


def split_txt(txtlist):
    return {x.split(':')[0]: x.split(':')[1].strip() for x in txtlist}


def account_to_dict(txtfile='ac.txt'):
    with open(txtfile, 'r', encoding='utf-8') as f:
        data = [x.split('\n') for x in f.read().split('\n\n')]

    datalist = [split_txt(t) for t in data] 
    return datalist


def modify_account_to_file(result_file='ac.txt'):
    ac = account_to_dict()
    aaa = [x.pop('auth_token') for x in ac]
    acl = [':'.join([b for b in a.values()]) for a in ac]
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(acl))

    
if __name__ == "__main__":

    # ac = account_to_dict()
    modify_account_to_file()
    import pdb;pdb.set_trace()
    country_exp="カザフスタン"
    
    kz_proxy = "kz.smartproxy.com:{}:username:pass".format(random.randrange(40001, 40100))

    proxys = get_proxy_list()
    accounts = get_accounts()
    
    for account in accounts:
        account = modify_account(account)
        vals = [x for x in account.values()]
        if len(vals) == 6:
            screen_name, password, email, email_pw, filepath, phone = vals
        else:
            screen_name, password, email, email_pw, filepath = vals
        prox = random.choice(proxys)

        #----ここからロック解除---
        #メインフロー(username, pass, email, phone, pincode, continue, tweet-compaseで確認)
        driver = start_driver(prox=kz_proxy)
        # driver_quit(driver)
        # import pdb;pdb.set_trace()
        is_setting = captcha_setting(driver)
        if not is_setting:
            driver_quit(driver)
            continue


        is_ok = load_twitter_cookies(driver, account['filepath'])

        for i in range(10):
            #check page status
            if 'https://twitter.com/account/access' in driver.current_url:
                title_elem = driver.find_elements(By.XPATH, "//div[@class=\"PageHeader Edge\"]")
                if 0 < len(title_elem):
                    page_title = title_elem[0].text
                    if page_title == 'Your account has been locked.':
                        is_ok = start_captcha(driver)
                        is_ok = wait_solve_captcha(driver)
                    elif page_title == 'Enter your phone number':
                        is_ok = input_phone(driver, country_exp)
                    elif page_title == 'Account unlocked.':
                        is_ok = click_submit_btn(driver)
                    elif page_title == "We've temporarily limited some of your account features.":
                        is_ok = click_submit_btn(driver)
                    else:
                        is_ok = click_submit_btn(driver)
                        
                else:
                    is_ok = wait_solve_captcha(driver)
            else:
                #ログイン成功したら終了
                is_login = is_login_success(driver)
                if is_login:
                    filepath = account.pop('filepath')
                    line_push('twitter. {} is unlock success!'.format(account))
                    #アカウントリストから削除
                    ac = ":".join([x for x in account.values()])
                    accounts.remove(ac)
                    write_accounts(accounts)
            time.sleep(5)

        
        import pdb;pdb.set_trace()
        driver_quit(driver)
        
        
        # is_ok = submit_login_button(driver)
        # is_ok = send_screen_name(driver, account['screen_name'])
        # is_ok = send_password(driver, account['password'])
        
        # is_ok = input_email(driver, account['email'])
        # if 'https://twitter.com/account/access' in driver.current_url:
        #     is_ok = wait_solve_captcha(driver)
        #     # import pdb;pdb.set_trace()
        #     is_ok = input_phone(driver, country_exp)

        # is_ok = is_login_success(driver)
        # if is_ok:
        #     filepath = account.pop('filepath')
        #     line_push('twitter. {} is unlock success!'.format(account))
        #     #アカウントリストから削除
        #     ac = ":".join([x for x in account.values()])
        #     accounts.remove(ac)
        #     write_accounts(accounts)
        
        # # import pdb;pdb.set_trace()
        # driver_quit(driver)


        

        # import pdb;pdb.set_trace()
        
        # print('a')