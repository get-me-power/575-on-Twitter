import twitter
import requests
from requests_oauthlib import OAuth1Session

def is575(text, amari=False, tarazu=False, partial=False):
    import MeCab
    import re
    mt = MeCab.Tagger()
    res = mt.parse(text)
    lensum = [0]
    pat = re.compile(r'[ゃゅょャュョ]')

    for s in res.splitlines():
        if s == 'EOS': continue
        surface, feature = s.split("\t")
        features = feature.split(",")
        if features[0] != '記号':
            if len(features) >= 8:
                lensum.append(lensum[-1] + len(pat.sub('', features[7])))
            else:
                lensum.append(lensum[-1] + len(pat.sub('', surface)))

    senryu = 5, 7, 5
    offset = 0
    start = 0
    end = 1

    while start < len(lensum) and offset < 3:
        if(any([
        lensum[end] - lensum[start] == senryu[offset],
        tarazu and lensum[end] - lensum[start] == senryu[offset]-1,
        amari and lensum[end] - lensum[start] == senryu[offset]+1])):
            offset += 1
            start = end
            end = start + 1
            if partial and offset == 3:
                return True
        else:
            end += 1
            if end == len(lensum):
                if partial:
                    offset = 0
                    start += 1
                    end = start + 1
                else:
                    break

    return offset == 3

    """ メイン関数 """
    
if __name__ == '__main__':
    api_key = "xxxx"
    api_secret = "xxxx"
    access_key = "xxxx"
    access_secret = "xxxx"


    auth = twitter.OAuth(consumer_key="xxxx",
    consumer_secret="xxxx",
    token="xxxx",
    token_secret="xxxx")

    auth2 = OAuth1Session(api_key, api_secret, access_key, access_secret)

    favo = "https://api.twitter.com/1.1/favorites/create.json"
    tweet = "https://api.twitter.com/1.1/statuses/update.json"

    #t = twitter.Twitter(auth=auth) いらない
    #Userstreamを用いる
    t_userstream = twitter.TwitterStream(auth=auth,domain='userstream.twitter.com')

    #自分のタイムラインのツイートおよびユーザーの情報が流れる
    for msg in t_userstream.user():
        if ('text' in msg.keys() and is575(msg['text'])==True):
            print(msg.keys())
            
            print(msg['text'])
            
            params={'id' : msg['id_str']}
            
            request = auth2.post(favo, params = params)
            
            print(msg['id_str'])
            
            params_tweet={'in_reply_to_status_id':msg['id_str'],'status':'@' + msg["user"]['screen_name'] + " 575"}
            
            request2 = auth2.post(tweet, params = params_tweet)
            

