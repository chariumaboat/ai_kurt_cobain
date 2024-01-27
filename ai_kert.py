import os
from openai import OpenAI
from pprint import pprint
import configparser
import tweepy
import random
import sys


def auth_api_v2(envName):
    config = configparser.ConfigParser(interpolation=None)
    config.read('ai_kart.ini')
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    bearer_token = config.get(envName, 'bearer_token')
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_key,
                           access_token_secret=access_secret)
    return client


def auth_api_v1(envName):
    config = configparser.ConfigParser()
    config.read('ai_kart.ini')
    consumer_key = config.get(envName, 'consumer_key')
    consumer_secret = config.get(envName, 'consumer_secret')
    access_key = config.get(envName, 'access_key')
    access_secret = config.get(envName, 'access_secret')
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def randam_text():
    text_list = ["ロックスターとして政治的発言を140文字でしてください",
                 "新譜「nevermind part3」について一言コメントをください。140文字以下にまとめてください",
                 "炎上しそうなツイートを140文字でしてください",
                 "カートコバーンの生まれ変わりとしてオリジナルのカートコバーンについて非常に厳しく140文字で批評してください",
                 "カートコバーンの生まれ変わりとしてオリジナルのカートコバーンについて非常に厳しく140文字でdisってください",
                 "ファンに向けて一言、調子に乗ってる感じで、140文字で",
                 "ファンに向けて一言、馬鹿にした感じで、140文字で",
                 "人を馬鹿にしてください、140文字で",
                 "オーディエンスを煽ってください、140文字で"
                 ]
    return random.choice(text_list)


def ai_create_tweet():
    api_key = os.environ.get('gpt_api_key')
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system",
                                                    "content": "あなたは伝説のロックスターカートコバーン。日本の神奈川県寒川町に生まれ変わった。尊大なロックスターとして発言しなければならない。"},
                                                  {"role": "user",
                                                   "content": randam_text()}
                                              ])
    return response


def remove_quotes(input_str):
    # " を除去
    output_str = input_str.replace('"', '')
    # 「」、「」を除去
    output_str = output_str.replace('「', '').replace('」', '')
    return output_str


response = ai_create_tweet()
print(response)

# 発言だけ取り出す
content = remove_quotes(response.choices[0].message.content)
print(content)

# 画像アップロード


if random.randint(1, 5) == 1:
    directory_path = './jpg/ai_kart/'
    image_files = [f for f in os.listdir(directory_path) if f.endswith(
        ('.jpg', '.jpeg', '.png', '.gif'))]
    if image_files:
        random_image = random.choice(image_files)
        image_path = os.path.join(directory_path, random_image)
        print("ランダムに選択された画像パス:", image_path)
    else:
        print("ディレクトリ内に画像が見つかりませんでした。")
        sys.exit(1)
    api = auth_api_v1('ai_kart')
    media_id = api.media_upload(image_path).media_id_string
    print(media_id)
    client = auth_api_v2('ai_kart')
    post_tweet = client.create_tweet(text=content, media_ids=[media_id])
    print(post_tweet)
else:
    client = auth_api_v2('ai_kart')
    post_tweet = client.create_tweet(text=content)
    print(post_tweet)