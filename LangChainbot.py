import discord
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# ChatGoogleGenerativeAIインスタンスの作成
# ここでGoogle Gemini 1.5モデルを使って、AIの応答を得る設定を行う
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # 使用するAIモデル
    temperature=0,  # 応答のランダム性を0に設定（確定的な応答）
    max_tokens=None,  # トークン数に制限を設けない
    timeout=None,  # タイムアウトなし
    max_retries=2,  # 最大2回の再試行
    # 他のパラメータ...
)

# Discordクライアントの初期化
# Discord APIとの接続に必要な設定を行う
intents = discord.Intents.default()  # 標準のインテントを使用
intents.message_content = True  # メッセージの内容を取得できるように設定
client = discord.Client(intents=intents)  # クライアントオブジェクトの作成

# ボットがログインしたときに実行されるイベント
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')  # ボットがログインしたことを確認

# メッセージが送信されたときに実行されるイベント
@client.event
async def on_message(message):
    # ボット自身のメッセージや他のボットのメッセージには反応しない
    if message.author == client.user:
        return
    if message.author.bot:
        return

    # ユーザーからのメッセージを取得
    input_text = message.content

    # メッセージをAIに送信するための形式に変換
    messages = [
        ("system", "default"),  # システムからのメッセージ
        ("human", input_text),  # ユーザーからのメッセージ
    ]
    
    # AIからの応答を取得
    ai_msg = llm.invoke(messages)
    
    # AIの応答をDiscordのチャンネルに送信
    await message.channel.send(ai_msg.content)

# Discordボットを実行
# ボットの認証トークンを使ってDiscordサーバーに接続
client.run(os.environ['BOT_KEY'])  # 環境変数からボットのキーを取得して実行