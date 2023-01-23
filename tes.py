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

import loguru
from loguru import logger
import pysnooper
from utils import get_accounts, get_random_prof, check_log, set_random_proxy, modify_account

import pandas as pd
import json
import ast
from BotHelper.line_notify import line_push
from dotenv import load_dotenv


# 環境変数を参照
load_dotenv()

# logger.add("logs/log.txt", rotation="3 MB", encoding="utf8", enqueue=True)

log_path = os.path.join(*[os.path.dirname(os.path.abspath(__file__)), 'logs', 'log.jsonl'])

logger.add(log_path, rotation="3 MB", encoding="utf8", serialize=True)






def get_cursor(res):
    instruct = res['timeline']['instructions']
    get_cursor_value = lambda x: x['content']['operation']['cursor']['value']
    cursor= get_cursor_value(instruct[-1]['addEntries']['entries'][-1])
    return cursor



def recommend_user_ids(text='相互フォロー', max_num=10):
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
    user_ids = recommend_user_ids(text=search_word, max_num=10)
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
                # os.remove(filepath)
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


@pysnooper.snoop()
def check_login(account):
    #account: dict(screen_name, password, email, emailpw, filepath)
    try:
        flow = TwitterFrontendFlow()
        if os.path.exists(account['filepath']):
            flow.LoadCookies(account['filepath'])
            #---------------プロフィール-----------------
            # user_info = flow.user_info(screen_name=screen_name).content
            return flow
    
        
        flow.login_flow()
        flow.LoginJsInstrumentationSubtask()
        print(flow.get_subtask_ids())
        if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
            print("Telephone number / Email address / User name")
            flow.LoginEnterUserIdentifierSSO(account['screen_name'])
            print(flow.get_subtask_ids())
        if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
            flow.LoginEnterAlternateIdentifierSubtask(account['email'])
            print(flow.get_subtask_ids())
        if "LoginEnterPassword" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
            flow.LoginEnterPassword(account['password'])
            print(flow.get_subtask_ids())
        if "AccountDuplicationCheck" in flow.get_subtask_ids():
            flow.AccountDuplicationCheck()
            print(flow.get_subtask_ids())
        if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
            print(flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"])
            flow.LoginTwoFactorAuthChallenge(input())
            print(flow.get_subtask_ids())
        if "LoginAcid" in flow.get_subtask_ids():
            verify_text = flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"]["text"]
            print(verify_text)
            if ('phone' in verify_text) and ('phone' in account):
                flow.LoginAcid(account['phone'])
            else:
                flow.LoginAcid(account['email'])
            print(flow.get_subtask_ids())
        if "LoginSuccessSubtask" in flow.get_subtask_ids():
            print("===========Success===========")
            print(flow.get_subtask_ids())
        if "SuccessExit" not in flow.get_subtask_ids():
            print("Error")
            exit()

        flow.SaveCookies(account['filepath'])
        # user_info = flow.user_info(screen_name=screen_name).content
        return flow

    except (ReadTimeout, ProxyError, Exception) as e:
        print(e)
        return None




def check_account_status(flow, account):
    #flow.contentに最終リクエストのレスポンスが入ってるからエラー出てるかチェック

    try:
        user_info = flow.user_info(screen_name=account['screen_name']).content
        #エラー文を表示して再ログイン
        if 'errors' in user_info:
            print(user_info)
            # os.remove(filepath)
            time.sleep(3)
            if user_info["errors"][0]["code"] == 326:
                msg = user_info["errors"][0]["message"] + '\n' + ':'.join(account)
                line_push(msg)
                return None
        else:
            return flow
            
    except (ReadTimeout, ProxyError, Exception) as e:
        print(e)
        return None
    
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
    # proxys = get_proxy_list(file_path='proxy.txt')
    for account in accounts:
        #proxy
        prox = set_random_proxy()
        if not prox:
            continue
        
        #アカウント情報
        account = modify_account(account)
        vals = [x for x in account.values()]
        if len(vals) == 6:
            screen_name, password, email, email_pw, filepath, phone = vals
        else:
            screen_name, password, email, email_pw, filepath = vals
        
        #ログインできるかチェック
        flow = check_login(account)

        
        if not flow:
            print('login error')
            import pdb;pdb.set_trace()
            continue
        
        user_info = flow.user_info(screen_name=screen_name).content
        #エラー文を表示して再ログイン
        if 'errors' in user_info:
            print(user_info);time.sleep(3)
            msg = user_info["errors"][0]["message"] + '\n' + ':'.join(account)
            line_push(msg)
            #エラーコードごとに対応を分ける
            error_code = user_info["errors"][0]["code"]
            #アカウントロックの場合
            if error_code == 326:
                print('er')


            # import pdb;pdb.set_trace()
            # os.remove(filepath)
                

        # import pdb;pdb.set_trace()
        
        # flow = TwitterFrontendFlow()
        try:

            res = check_shadowban(screen_name=screen_name)
            logger.debug(res)
            if ('相互フォロー' not in user_info['name']) and (user_info['followers_count'] < 100):
                first_prof_set(flow, account["password"])
            # import pdb;pdb.set_trace()
            # flow = TwitterFrontendFlow()
            # flow.LoadCookies(filepath)
            #------プロフィール設定用------------
            mutual_follow()
            flow.SaveCookies(account["filepath"])
            # import pdb;pdb.set_trace()
        except (KeyError,JSONDecodeError) as e:
            print(e)
            # continue

        # import pdb;pdb.set_trace()
        