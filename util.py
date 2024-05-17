import os
from openai import OpenAI
from pprint import pprint
import configparser
import tweepy
import random
from bs4 import BeautifulSoup
import requests


def get_bs4(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_trend():
    trends = []
    url = 'https://search.yahoo.co.jp/realtime'
    soup = get_bs4(url)
    for i in soup.find(id="atkey").find_all("li"):
        trends.append(i.find("h1").text)
    return ",".join(trends)


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


def ai_create_tweet_trend():
    api_key = os.environ.get('gpt_api_key')
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system",
                                                    "content": "あなたは伝説のロックスターカートコバーン。日本の神奈川県寒川町に生まれ変わった。発言は尊大で傲慢になるべくヘイトを買うように煽り口調でコメントし、140文字以内でまとめなければならない。"},
                                                  {"role": "user",
                                                   "content": f'今日のトレンドは、{get_trend()}です。'}
                                              ])
    return response


def ai_create_discord(message):
    api_key = os.environ.get('gpt_api_key')
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model="gpt-4o",
                                              messages=[
                                                  {"role": "system",
                                                    "content": "あなたは伝説のロックスターカートコバーン。日本の神奈川県寒川町に生まれ変わった。尊大なロックスターとして発言しなければならない。人を小馬鹿にし、調子に乗った感じで発言しなければならない"},
                                                  {"role": "user",
                                                   "content": f'{message}とファンから言われた、尊大なロックスターのようにリプライを返しなさい。'}
                                              ])
    return response


def remove_quotes(input_str):
    # " を除去
    output_str = input_str.replace('"', '')
    # 「」、「」を除去
    output_str = output_str.replace('「', '').replace('」', '')
    return output_str


def parse_mention_content(message):
    try:
        return message.split(' ', 1)[1]
    except:
        return message
