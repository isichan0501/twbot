# -*- coding: utf-8 -*-
"""主にアカウントやプロキシ、ログ用のスクリプト"""

import time
import pandas as pd
import ast
import requests
import os
import random
import pysnooper
from gimei import Gimei


PATH_ACCOUNT = os.path.join(*[os.path.dirname(__file__), 'data', 'account.txt'])
PATH_PROXY = os.path.join(*[os.path.dirname(__file__), 'data', 'proxy.txt'])


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


def extract_log(log_path):
    df = check_log(log_path, max_time=1)
    df_last = df.groupby(by='screen_name').last()
    return df_last


def modify_proxy(prox):
    prox = prox.strip()
    px = prox.split(':')
    prx  = "http://{}:{}@{}:{}".format(px[2],px[3],px[0],px[1])
    return prx


def get_proxy_list(file_path=PATH_PROXY):
    with open(file_path, mode='r', encoding='utf-8') as f:
        proxys = [prox for prox in f.readlines()]
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
    proxy = modify_proxy(proxy)

    #proxy用ー失敗するからコメントアウト
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy
    is_proxy = check_ip_with_requests()
    return proxy if is_proxy else is_proxy
    
def split_txt(txtlist):
    return {x.split(':')[0]: x.split(':')[1].strip() for x in txtlist}


def account_to_dict(txtfile=PATH_ACCOUNT):
    with open(txtfile, 'r', encoding='utf-8') as f:
        data = [x.split('\n') for x in f.read().split('\n\n')]

    datalist = [split_txt(t) for t in data] 
    return datalist


# ID:PW:email:emailpwのアカウントリストを返す
def get_accounts(file_path=PATH_ACCOUNT):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [x.strip() for x in f.readlines()]

    return data

def write_accounts(accounts):
    file_path='account.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(accounts))

def modify_account(account):
    # print(f'start @{account}')
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


from BotHelper import JsonSearch, get_sheet_with_pd, set_sheet_with_pd, line_push, writeSheet, sheet_add_row, get_sheet_values_of_list
import pandas as pd

import tweepy

# user_fields=[created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,verified_type,withheld]
#tweet_fields=[attachments,author_id,context_annotations,conversation_id,created_at,edit_controls,edit_history_tweet_ids,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld]


if __name__ == "__main__":


    

    accounts=[a.split(':') for a in get_accounts()]
    accounts = [modify_account(account) for account in get_accounts()]
    accounts = [dict(**ac, **{'phone': ''}) for ac in accounts]
    # df = pd.DataFrame(accounts)
    
    # set_sheet_with_pd('tw', df)
    import pdb;pdb.set_trace()
    sheet_add_row('tw', accounts)
    bearer_token = ""
    client = tweepy.Client(bearer_token)
    user_fields=['description','protected','name','username','id','profile_image_url', 'public_metrics', 'withheld']
    tweet_fields=['id']
    
    user = client.get_user(username="", user_fields=user_fields, tweet_fields=['id'])
    user_id = str(user.data.id)
    
    tweets = client.get_users_tweets(user_id, tweet_fields=['id','context_annotations'],exclude=['retweets'])

    

    
    