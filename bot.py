import discord
import os
import google.generativeai as genai

def split_text(text, chunk_size=1500):
    # テキスト文字列をchunk_sizeで指定した大きさに分割し、リストに格納する
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Google Generative AIの初期化
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model.start_chat(history=[])

# Discordクライアントの初期化
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    # 入力メッセージに対する応答を送信
    input_text = message.content
    try:
        answer = chat.send_message(input_text)
        splitted_text = split_text(answer.text)

        # 分割された応答を順次送信
        for chunk in splitted_text:
            await message.channel.send(chunk)
    except Exception as e:
        await message.channel.send(f"エラーが発生しました: {str(e)}")

# Discordボットを実行
client.run(os.environ['BOT_KEY'])