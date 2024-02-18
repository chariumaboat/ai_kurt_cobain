from util import *


response = ai_create_tweet()

# 発言だけ取り出す
content = remove_quotes(response.choices[0].message.content)[0:139]

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
