import tweepy

import pandas as pd
import os
from dotenv import load_dotenv
from line_notify import line_push
load_dotenv()



#使い捨て用のAPIキー
CONSUMER_KEY = os.getenv('CONSUMER_KEY_SUB')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET_SUB')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN_SUB')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET_SUB')



#Id ... ユーザidでもスクリーンネームでもok
#@pysnooper.snoop()
def api_from_keys(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit = True)
        return api
    except tweepy.Forbidden as e:
        # lg.exception(e)
        message = "ACCESS_TOKEN:{0}, TwitterAccount locked.".format(ACCESS_TOKEN)
        line_push(message, img_path=None)




def get_woeid():
    with open('woeid.txt', 'r', encoding='utf-8') as f:
        data = [{x.split(',')[0]: int(x.split(',')[1].strip())} for x in f.readlines()[1:]]

    return data


if __name__ == '__main__':

    import pandas as pd

    filepath = "paypay配布.jsonl"
    df = pd.read_json(filepath, orient='records', lines=True, encoding='utf-8')

    import pdb;pdb.set_trace()
    
    api = api_from_keys(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    trend_list = []
    woeids = get_woeid()
    
    for woeid in woeids:

        whi = list(woeid.values())[0]
        #トレンド一覧取得
        
        trends = api.get_place_trends(whi)
        
        trend_list.extend(trends[0]["trends"])
        print(trends[0]["trends"])
        # import pdb;pdb.set_trace()
    print(trends)
    df = pd.DataFrame(trend_list)
    import pdb;pdb.set_trace()
    print(df)