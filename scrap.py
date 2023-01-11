# 必要なライブラリをインポート
import snscrape.modules.twitter as sntwitter
import pandas as pd








if __name__ == '__main__':


    import collections

    
    max_result = 300
    search_word = 'paypay配布'
    hashtags = []
    for i, x in enumerate(sntwitter.TwitterHashtagScraper(search_word).get_items()):

        print('now {}'.format(i))
        # import pdb;pdb.set_trace()
        hashtags.extend(x.hashtags)
    
        if max_result < i:
            break

    counter = collections.Counter(hashtags)
    import pdb;pdb.set_trace()
    

    
    # ツイートの個数設定
    maxTweets = 1000
    # ツイート検索するキーワード
    keyword = '新年'

    df=[]
    cols=pd.DataFrame([['id','date','tweet','likeCount']])
    cols.to_csv('tweet.csv',index=False,header=False)

    # 2022年1月1日の「新年」を含むツイート
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' since:2022-01-01 until:2022-01-02 lang:ja -filter:links -filter:replies').get_items()):
            # いいね数20以上、文字数20以上のツイートを取得
            if tweet.likeCount >= 20 and len(tweet.content) >= 20:
                # 改行を削除 
                t = tweet.content
                text = t.replace('\n', '')

                df.append([tweet.id, tweet.date, text, tweet.likeCount])
                df1=pd.DataFrame([[tweet.id, tweet.date, text, tweet.likeCount]])
                # csvファイルとして保存
                df1.to_csv('tweet.csv',index=False,mode='a+',header=False)
            elif len(df) == maxTweets:
                break