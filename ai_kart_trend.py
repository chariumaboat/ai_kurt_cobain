from util import *
import sys

response = ai_create_tweet_trend()
# 発言だけ取り出す
content = remove_quotes(response.choices[0].message.content)
print(content)
client = auth_api_v2('ai_kart')
try:
    post_tweet = client.create_tweet(text=content[0:139])
except Exception as e:
    print(e)
else:
    print(post_tweet)
