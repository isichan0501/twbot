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
from update_user_agents import get_latest_user_agents

import loguru
from loguru import logger
import pysnooper


import pandas as pd
import json
import ast
from line_notify import line_push


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
    except Exception:
        print('error')


def set_random_proxy():
    proxys = get_proxy_list()
    del_env = os.environ.pop('http_proxy', None)
    del_env = os.environ.pop('https_proxy', None)
    time.sleep(1)
    proxy = random.choice(proxys)

    #proxy用ー失敗するからコメントアウト
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy
    check_ip_with_requests()
    return proxy



def login_set(flow,screen_name,password,email,email_pw):
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



# @pysnooper.snoop()
def mutual_follow(search_word='相互フォロー'):
    user_ids = recommend_user_ids(text=search_word, max_num=15)
    for user_id in user_ids:
        try:
            resp = flow.friendships_create(user_id).content
            print('フォロー to {}'.format(resp['screen_name']))
            time.sleep(1)
        except Exception as e:
            print(e)
            return None


def first_prof_set(flow, password):
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

    df = df[(now - max_time) > df['time']]
    return df
    # if len(df[df['screen_name'] == screen_name]) == 0:
    #     print('{} is within {} seconds'.format(screen_name, max_time))
    #     return True



def extract_log(df):
    df_last = df.groupby(by='screen_name').last()
    return df_last
    
if __name__ == "__main__":
    


    #アカウント情報のリスト
    accounts = get_accounts()

    #時間経過してないアカウントは除外
    df = check_log(log_path, max_time=7200)
    active_accounts = list(set(df['screen_name'].to_list()))
    # accounts = list(set([x.split(':')[0] for x in accounts]) & set(active_accounts))
    
    for account in accounts:


        #アカウント情報
        account = account.split(':')
        screen_name,password,email,email_pw = account[0],account[1],account[2],account[3]
        filepath = f'./db/{screen_name}.json'
        print(f'start @{account}')

        if screen_name not in active_accounts:
            print(f'{screen_name} is within time limit. pass')
            continue
        #proxy
        prox = set_random_proxy()
        

        try:
            flow = TwitterFrontendFlow()
            #クッキーがなければログイン
            if not os.path.exists(filepath):
                login_set(flow, screen_name,password,email,email_pw)

            print("ファイル名")
            flow.LoadCookies(filepath)

            #---------------プロフィール-----------------
            # user_id = flow.user_info(screen_name="Flower_kyujin")
            user_info = flow.user_info(screen_name=screen_name).content
            user_id = user_info['id_str']
        
            res = check_shadowban(screen_name=screen_name)
            logger.debug(res)
            if '相互フォロー' not in user_info['name']:
                first_prof_set(flow, password)


            # import pdb;pdb.set_trace()

            #------プロフィール設定用------------
            mutual_follow()
        except Exception as e:
            print('error')
            continue

            
            # import pdb;pdb.set_trace()