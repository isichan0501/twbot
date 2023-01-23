from TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow

def modify_proxy(prox):
    prox = prox.strip()
    px = prox.split(':')
    prx  = "http://{}:{}@{}:{}".format(px[2],px[3],px[0],px[1])
    
    return {
        "http": prx,
        "https": prx,
            }


# prox = "http://isichan51:takt7777_country-jp_session-rnm7194m_lifetime-30mm@geo.iproyal.com:12321/"

# prox = "geo.iproyal.com:12321:isichan51:takt7777_country-jp_session-abbno31p_lifetime-30m"


# proxies = {
#     "http": modify_proxy(prox),
#     "https": modify_proxy(prox),
# }

def get_proxy_list(file_path='proxy.txt'):
    with open(file_path, mode='r', encoding='utf-8') as f:
        proxys = [modify_proxy(prox) for prox in f.readlines()]
    return proxys


import json
import requests
from concurrent.futures import ThreadPoolExecutor


def check_ip_with_requests(proxies):
    
    try:
        response = requests.get('http://jsonip.com', proxies=proxies, timeout=20)
        ip = response.json()['ip']
        print('Your public IP is:', ip)
        return True
    except Exception:
        print('proxy set error.return False')
        return False


proxys = get_proxy_list(file_path='data/proxy.txt')

#マルチスレッド
# with ThreadPoolExecutor(9) as executor:
#     results = list(executor.map(check_ip_with_requests, proxys))



# import pdb;pdb.set_trace()
proxies = proxys[0]
myip = check_ip_with_requests(proxies)
flow = TwitterFrontendFlow(proxies=proxies)

print(
"""login: ログイン
password_reset: パスワードリセット
load: cookieのロード""")

action = input()

if action == "login":
    flow.login_flow()
    flow.LoginJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
        print("Telephone number / Email address / User name")
        flow.LoginEnterUserIdentifierSSO(input())
        print(flow.get_subtask_ids())
    if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
        flow.LoginEnterAlternateIdentifierSubtask(input())
        print(flow.get_subtask_ids())
    if "LoginEnterPassword" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
        flow.LoginEnterPassword(input())
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
        flow.LoginAcid(input())
        print(flow.get_subtask_ids())
    if "LoginSuccessSubtask" in flow.get_subtask_ids():
        print("===========Success===========")
        print(flow.get_subtask_ids())
    if "SuccessExit" not in flow.get_subtask_ids():
        print("Error")
        exit()

elif action == "password_reset":
    flow.password_reset_flow()
    flow.PwrJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "PasswordResetBegin"in flow.get_subtask_ids():
        print("電話番号/メールアドレス/ユーザー名")
        flow.PasswordResetBegin(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetChooseChallenge"in flow.get_subtask_ids():
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetChooseChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetConfirmChallenge"in flow.get_subtask_ids():
        print("コードを入力")
        flow.PasswordResetConfirmChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetNewPassword"in flow.get_subtask_ids():
        print("新しいパスワードを入力")
        flow.PasswordResetNewPassword(input())
        print(flow.get_subtask_ids())
    if "PasswordResetSurvey"in flow.get_subtask_ids():
        print("パスワードを変更した理由を教えてください")
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetSurvey(input())
        print(flow.get_subtask_ids())
    exit()

elif action == "load":
    print("ファイル名")
    flow.LoadCookies(input())

while True:
    print(
"""tweet: ツイート
fav: いいね
unfav: いいね取り消し
rt: リツイート
unrt: リツイート取り消し
follow: フォロー
unfollow: フォロー取り消し
save: cookieの出力
end: 終了""")

    action = input()

    if action == "tweet":
        print("ツイート内容")
        flow.CreateTweet(input())
    elif action == "fav":
        print("ツイートid")
        flow.FavoriteTweet(input())
    elif action == "unfav":
        print("ツイートid")
        flow.UnfavoriteTweet(input())
    elif action == "rt":
        print("ツイートid")
        flow.CreateRetweet(input())
    elif action == "unrt":
        print("ツイートid")
        flow.DeleteRetweet(input())
    elif action == "follow":
        print("ユーザー内部id")
        flow.friendships_create(input())
    elif action == "unfollow":
        print("ユーザー内部id")
        flow.friendships_destroy(input())
    elif action == "save":
        print("ファイル名")
        flow.SaveCookies(input())
    elif action == "end":
        break



#----json to s3---
import json
import boto3


def twitter_cookies_to_s3(screen_name):
    bucket_name = "nanae0914-data"
    json_key = f"twitter_accounts/{screen_name}.json"
    filepath = f"db/{screen_name}.json"

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name,json_key)

    with open(filepath, 'r', encoding='utf-8') as f:
        json_obj = json.load(f)
        
    res = obj.put(Body = json.dumps(json_obj))

from botocore.errorfactory import NoSuchKey


def twitter_cookies_from_s3(screen_name):
    bucket_name = "nanae0914-data"
    json_key = f"twitter_accounts/{screen_name}.json"
    filepath = f"db/{screen_name}.json"

    try:
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket_name,json_key)
        json_obj = json.loads(obj.get()['Body'].read())
        return json_obj
    except NoSuchKey as e:
        print(e)
        return None
    
    

import pdb;pdb.set_trace()
screen_name = "AlexaIngram14"
json_obj = twitter_cookies_from_s3(screen_name)

