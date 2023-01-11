# -*- coding: utf-8 -*-
"""TwitterBot用

１、ログインする（クッキーがなければ）
２，クッキーをファイルに保存

# flow.change_country_flow(country_code="jp")
# flow.change_country_subtask()
# flow.change_country_end()

# print(flow.display_sensitive_media())
# print(flow.gender())
# print(flow.allow_dm())
Todo:
    *ログイン情報（screen_name,password,mail,passwordmail,phone_number)


"""



from TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow, check_shadowban


import pprint
from importlib import reload
import glob
import random
import os
from dotenv import load_dotenv
import requests
import pysnooper
import time




screen_name = input('screen_name:')
password=input('password:')
target_user = input('screen_name to sent dm with follower:')

filepath = f'./db/{screen_name}.json'



#ログインフロー

flow = TwitterFrontendFlow()

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

    flow.SaveCookies(filepath)


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
    flow.LoadCookies(filepath)

    
# flow.LoadCookies(filepath)


#---proxy

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
        return ip
    except Exception:
        print('error')
        return None



#使えるプロキシを得るまでループ


def set_proxy():
    proxys = get_proxy_list()
    for i in range(100):
        prox = random.choice(proxys)
        print(f'check ip {prox}')

        del_env = os.environ.pop('http_proxy', None)
        del_env = os.environ.pop('https_proxy', None)
        time.sleep(1)

        #シートからproxy情報取得
        os.environ['http_proxy'] = prox
        os.environ['https_proxy'] = prox
        myip = check_ip_with_requests()
        if not myip:
            continue
        return prox
    
    




#------DM用----------------

# @pysnooper.snoop()
def create_conversation_id(user_id, you_id):
    if int(user_id) < int(you_id):
        return '{}-{}'.format(user_id, you_id)
    else:
        return '{}-{}'.format(you_id, user_id)
    

#送信歴なしなら相手のuserid, ありならNoneを返す
# @pysnooper.snoop()
def get_unsent_userid(flow, user_id, conversation_id):
    #送信履歴があるかチェックする
    #まずはDM履歴一覧を取得
    res = flow.get_conversation(conversation_id=conversation_id)
    #会話履歴
    convs = res.content['conversation_timeline']['entries']
    #会話相手のuserid
    msg = convs[0]['message']['message_data']
    you_id = msg['recipient_id'] if user_id == msg['sender_id'] else msg['sender_id']
    #送信ユーザのIDのリスト
    sender_ids = [cn['message']['message_data']['sender_id'] for cn in convs]
    #あとで２通目のDMなど作る場合用
    send_count = sender_ids.count(user_id)
    print('send dm count {}'.format(send_count))
    if user_id not in sender_ids:
        print(f'you_id:{you_id}はまだ送信してないユーザー')
        return you_id
    else:
        print(f'you_id:{you_id}は送信済み')
        return None



#最新20人のDM履歴から送信履歴ないやつに送信.さらに過去履歴もやるためにmin_entry_idを返す
def send_dm_for_unsent(flow, user_id, send_msg, max_id=''):
    res = flow.get_dm(max_id=max_id)
    dms = res.content['user_inbox']


    #さらに過去のＤＭを取得する場合
    # min_entry_id=dms['min_entry_id']
    # res = flow.get_dm_more(max_id=min_entry_id)
    # dms = res.content['user_inbox']

    #会話一覧
    conversation_ids = list(dms['conversations'].keys())
    for conversation_id in conversation_ids:
        you_id = get_unsent_userid(flow, user_id, conversation_id)
        if you_id:
            flow.send_dm(send_msg, user_id=you_id)
            print(f'send dm to {you_id}')

    return dms['min_entry_id']



from get_mamadm import get_mamadm


if __name__ == "__main__":


    #proxy
    myproxy = set_proxy()

    #ターゲットのフォロワーID一覧
    res = flow.followers_ids(target_user)
    userid_list = [str(u) for u in res.content['ids']]
    print('{} follower is {}'.format(target_user, len(userid_list)))

    #自分のID
    user_id = flow.user_info(screen_name=screen_name).content["id_str"]

    send_count = 0
    for you_id in userid_list:
        conversation_id = create_conversation_id(user_id, you_id)
        # import pdb;pdb.set_trace()
        #会話履歴を確認

        
        res = flow.get_conversation(conversation_id=conversation_id)
        #履歴がないとres.content['conversation_timeline']のキーがstatus１つのみ
        if len(res.content['conversation_timeline'].keys()) == 1:
            res = flow.friendships_show_with_id(user_id, you_id)
            if res.content['relationship']['source']['can_dm'] == True:
                send_msg = get_mamadm()
                res = flow.send_dm(send_msg, user_id=you_id)
                print(f'send dm to {you_id}')
                send_count+=1
                print('now sent {} user'.format(send_count))
            else:
                print(f'{you_id} is not can_dm. pass')
        else:
            print(f'{you_id} is send in past! pass')

        # import pdb;pdb.set_trace()
        time.sleep(2)





    import pdb;pdb.set_trace()


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