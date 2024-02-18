# インストールした discord.py を読み込む
import discord
from util import ai_create_discord, parse_mention_content
import os


TOKEN = os.environ.get('discord_api_key')

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # 起動時に動作する処理
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


async def reply(message):
    # 発言とメンションを分離して発言だけ取得
    content = parse_mention_content(message.content)
    # カートが発言するから発言だけ分離する
    kurt_message = ai_create_discord(content).choices[0].message.content
    reply = f'{message.author.mention} {kurt_message}'
    await message.channel.send(reply)  # 返信メッセージを送信


@client.event
# 発言時に実行されるイベントハンドラを定義
async def on_message(message):
    if client.user in message.mentions:  # 話しかけられたかの判定
        await reply(message)  # 返信する非同期関数を実行

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
