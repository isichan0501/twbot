# -*- coding: utf-8 -*-
"""最初に相互フォローでアカウントを育てる用


account.txtにID:PW:MAIL:MAILPWの形式でアカウントを入れる


"""

from TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow, check_shadowban


import pprint
from importlib import reload
import glob
import random
import os
import time
import pysnooper
from gimei import Gimei
import requests
from requests.exceptions import ReadTimeout, ProxyError,JSONDecodeError
from update_user_agents import get_latest_user_agents

import loguru
from loguru import logger
import pysnooper


import pandas as pd
import json
import ast
from line_notify import line_push
from dotenv import load_dotenv


# 環境変数を参照
load_dotenv()

# logger.add("logs/log.txt", rotation="3 MB", encoding="utf8", enqueue=True)

log_path = os.path.join(*[os.path.dirname(os.path.abspath(__file__)), 'logs', 'log.jsonl'])

logger.add(log_path, rotation="3 MB", encoding="utf8", serialize=True)




def modify_proxy(prox):
    prox = prox.strip()
    px = prox.split(':')
    prx  = "http://{}:{}@{}:{}".format(px[2],px[3],px[0],px[1])
    return prx


def get_proxy_list(file_path='proxy.txt'):
    with open(file_path, mode='r', encoding='utf-8') as f:
        proxys = [modify_proxy(prox) for prox in f.readlines()]
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
    proxys = get_proxy_list()
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


    
def modify_account(account):
    account = account.split(':')
    mydict = {
        'screen_name': account[0],
        'password': account[1],
        'email': account[2],
        'email_pw': account[3],
        }
    return mydict



def get_random_prof():

    name = Gimei(gender='female').name

    namae = name.kanji + '@相互フォロー'

    description="""相互フォロー"""

    location='jp'
    prof = dict()
    prof = {
            'birthdate_year': '{}'.format(random.randint(1990,2000)),
            'birthdate_month': '{}'.format(random.randint(1,12)),
            'birthdate_day': '{}'.format(random.randint(1,28)),
            'birthdate_visibility': 'self',
            'birthdate_year_visibility': 'self',
            'displayNameMaxLength': 50,
            'birthdate_year_visibility': 'self',
            'name': namae,
            'description': description,
            'location': location
            }
    return prof



def get_cursor(res):
    instruct = res['timeline']['instructions']
    get_cursor_value = lambda x: x['content']['operation']['cursor']['value']
    cursor= get_cursor_value(instruct[-1]['addEntries']['entries'][-1])
    return cursor



def recommend_user_ids(text='相互フォロー', max_num=15):
    friend_ids = flow.friends_ids(screen_name).content['ids']
    friend_ids = [str(i) for i in friend_ids]
    print('account {} friend len {}'.format(screen_name, len(friend_ids)))
    
    # res = flow.user_search("相互フォロー").content

    user_ids = []
    text = "相互フォロー"
    # import pdb;pdb.set_trace()
    res = flow.user_search(text).content
    cursor = ''
    while len(user_ids) < max_num:
        cursor = get_cursor(res)
        print('now list len{}'.format(len(user_ids)))
        user_ids.extend([u for u in res['globalObjects']['users'].keys() if u not in friend_ids])
        res = flow.user_search(text, count=20, cursor=cursor).content

    return user_ids



@pysnooper.snoop()
def mutual_follow(search_word='相互フォロー'):
    user_ids = recommend_user_ids(text=search_word, max_num=15)
    for user_id in user_ids:
        try:
            resp = flow.friendships_create(user_id).content
            if 'errors' in resp:
                print(resp['errors'])
                continue
            print('フォロー to {}'.format(resp['screen_name']))
            time.sleep(1)
        except Exception as e:
            print(e)
            return None


@pysnooper.snoop()
def first_prof_set(flow, password):
    try:
        print('start profile setting')
        #アカウント設定用---
        res = flow.verify_password(password)
        mydata = flow.account_data(password=password).content
        res = flow.change_country()
        flow.dm_filter()
        flow.display_sensitive_media()
        flow.gender()
        flow.allow_dm()

        #アカウント設定用---
        #------プロフィール設定用------------
        # pprint.pprint(mydata)
        # pprint.pprint(user_info)
        prof = get_random_prof()
        res = flow.update_profile(data=prof)
        imgs = glob.glob('./img/*')
        img_path = random.choice(imgs)
        res_img = flow.update_profile_image(img_path).content
        os.remove(img_path)
    except (ReadTimeout, ProxyError) as e:
        print(e)

#指定時間内のログのデータフレームを返す
def check_log(log_path, max_time=3600):

    now = time.time()

    df = pd.read_json(log_path, orient='records', lines=True)
    df = df.tail(1000)
    #ログのメッセージの辞書
    df['log'] = df['record'].apply(lambda x: ast.literal_eval(x['message']))
    #名前
    df['screen_name'] = df['log'].apply(lambda x: x['user']['screen_name'])
    #ログ時間
    df['time'] = df['record'].apply(lambda x: x['time']['timestamp']).astype('int')

    df = df[(now - max_time) < df['time']]
    return df
    # if len(df[df['screen_name'] == screen_name]) == 0:
    #     print('{} is within {} seconds'.format(screen_name, max_time))
    #     return True



@pysnooper.snoop()
def login_set(account):
    try:
        #アカウント情報
        account = account.split(':')
        screen_name,password,email,email_pw = account[0],account[1],account[2],account[3]
        filepath = f'./db/{screen_name}.json'
        print(f'start @{account}')

        flow = TwitterFrontendFlow()

        if os.path.exists(filepath):
            flow.LoadCookies(filepath)

            #---------------プロフィール-----------------
            user_info = flow.user_info(screen_name=screen_name).content
            #エラー文を表示して再ログイン
            if 'errors' in user_info:
                print(user_info)
                os.remove(filepath)
                time.sleep(3)
                if user_info["errors"][0]["code"] == 326:
                    msg = user_info["errors"][0]["message"] + '\n' + ':'.join(account)
                    line_push(msg)
                    return None
            else:
                return flow

            
        flow.login_flow()
        flow.LoginJsInstrumentationSubtask()
        print(flow.get_subtask_ids())
        if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
            print("Telephone number / Email address / User name")
            flow.LoginEnterUserIdentifierSSO(screen_name)
            print(flow.get_subtask_ids())
        if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
            flow.LoginEnterAlternateIdentifierSubtask(email)
            print(flow.get_subtask_ids())
        if "LoginEnterPassword" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
            flow.LoginEnterPassword(password)
            print(flow.get_subtask_ids())
        if "AccountDuplicationCheck" in flow.get_subtask_ids():
            flow.AccountDuplicationCheck()
            print(flow.get_subtask_ids())
        if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"])
            flow.LoginTwoFactorAuthChallenge(input())
            print(flow.get_subtask_ids())
        if "LoginAcid" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"]["text"])
            flow.LoginAcid(email)
            print(flow.get_subtask_ids())
        if "LoginSuccessSubtask" in flow.get_subtask_ids():
            print("===========Success===========")
            print(flow.get_subtask_ids())
        if "SuccessExit" not in flow.get_subtask_ids():
            print("Error")
            exit()

        flow.SaveCookies(filepath)
        user_info = flow.user_info(screen_name=screen_name).content
        return flow

    except (ReadTimeout, ProxyError, Exception) as e:
        print(e)
        return None


def check_login(account):
    flow = TwitterFrontendFlow()
    #アカウント情報
    account = account.split(':')
    screen_name,password,email,email_pw = account[0],account[1],account[2],account[3]
    filepath = f'./db/{screen_name}.json'
    print(f'start @{account}')
    #クッキーがなければログイン
    if not os.path.exists(filepath):
        login_set(account)


        #------------ログイン------------------
        #flow = login_set(flow, screen_name,password,email,email_pw, filepath)

    flow.LoadCookies(filepath)

    #---------------プロフィール-----------------
    user_info = flow.user_info(screen_name=screen_name).content
    #エラー文を表示して再ログイン
    if 'errors' in user_info:
        print(user_info)
        os.remove(filepath)
        time.sleep(3)
        #------------ログイン------------------
        print('start login')
        flow.login_flow()
        flow.LoginJsInstrumentationSubtask()
        print(flow.get_subtask_ids())
        if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
            print("Telephone number / Email address / User name")
            flow.LoginEnterUserIdentifierSSO(screen_name)
            print(flow.get_subtask_ids())
        if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
            flow.LoginEnterAlternateIdentifierSubtask(email)
            print(flow.get_subtask_ids())
        if "LoginEnterPassword" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
            flow.LoginEnterPassword(password)
            print(flow.get_subtask_ids())
        if "AccountDuplicationCheck" in flow.get_subtask_ids():
            flow.AccountDuplicationCheck()
            print(flow.get_subtask_ids())
        if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"])
            flow.LoginTwoFactorAuthChallenge(input())
            print(flow.get_subtask_ids())
        if "LoginAcid" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"]["text"])
            flow.LoginAcid(email)
            print(flow.get_subtask_ids())
        if "LoginSuccessSubtask" in flow.get_subtask_ids():
            print("===========Success===========")
            print(flow.get_subtask_ids())
        if "SuccessExit" not in flow.get_subtask_ids():
            print("Error")
            exit()

        flow.SaveCookies(filepath)
        
        # flow = login_set(flow, screen_name,password,email,email_pw, filepath)
        # flow.LoadCookies(filepath)

        # continue

    # import pdb;pdb.set_trace()
    user_info = flow.user_info(screen_name=screen_name).content
    user_id = user_info['id_str']


    res = check_shadowban(screen_name=screen_name)
    logger.debug(res)
    if '相互フォロー' not in user_info['name']:
        first_prof_set(flow, password)




def extract_log(log_path):
    df = check_log(log_path, max_time=1)
    df_last = df.groupby(by='screen_name').last()
    return df_last

    
if __name__ == "__main__":

    
    # dfl = [json.dumps(x, indent=2) for x in df.to_dict(orient='records')]
    # msg = df['log'].to_string()
    # line_push(msg)
    # import pdb;pdb.set_trace()
    #アカウント情報のリスト
    accounts = get_accounts()
    # import pdb;pdb.set_trace()
    
    #時間内のアカウント（除外リスト）のログを返す
    df = check_log(log_path, max_time=7200)
    active_accounts = list(set(df['screen_name'].to_list()))
    accounts = [x for x in accounts if x.split(':')[0] not in active_accounts]
    print('accounts len = {}. start loop!'.format(len(accounts)))
    # import pdb;pdb.set_trace()
    for account in accounts:
        #proxy
        prox = set_random_proxy()
        if not prox:
            continue
        #ログインできなければ飛ばす
        flow = login_set(account)
        if not flow:
            continue
        account = account.split(':')
        screen_name,password,email,email_pw = account[0],account[1],account[2],account[3]
        filepath = f'./db/{screen_name}.json'
        # flow = TwitterFrontendFlow()
        try:
            user_info = flow.user_info(screen_name=screen_name).content
            if 'errors' in user_info:
                msg = '{screen_name} login error{user_info}'
                line_push(msg)
                print(msg)
                import pdb;pdb.set_trace()

            # import pdb;pdb.set_trace()

            # import pdb;pdb.set_trace()
            # res = flow.verify_password(password)

            res = check_shadowban(screen_name=screen_name)
            logger.debug(res)
            if ('相互フォロー' not in user_info['name']) and (user_info['followers_count'] < 100):
                first_prof_set(flow, password)
            # import pdb;pdb.set_trace()
            # flow = TwitterFrontendFlow()
            # flow.LoadCookies(filepath)
            #------プロフィール設定用------------
            mutual_follow()
            flow.SaveCookies(filepath)
            import pdb;pdb.set_trace()
        except (KeyError,JSONDecodeError) as e:
            print(e)
            # continue

        # import pdb;pdb.set_trace()
        