import discord
from discord import app_commands
import os
from os.path import join, dirname
import dotenv
import myast

dotenv_path = join(dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

server_id:int = int(str(os.getenv("SERVER_ID")))
token:str = str(os.getenv("TOKEN"))

#botのintentの取得
intent = discord.Intents.default()
intent.message_content = True
client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print("get on ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(
        name="roll", 
        description="Throw Dice Command"
        )
@discord.app_commands.rename(
    formula="式"
)
@discord.app_commands.guilds(server_id)
async def roll(ctx: discord.Interaction, formula:str):
    #トークナイズ
    tokenizer = myast.Tokenizer(formula)
    try:
        tokens = tokenizer.tokenize()
    except RuntimeError as e:
        await ctx.response.send_message(f"{str(e)}")
        return

    #構文解析
    try:
        parser = myast.Parser(tokens)
        tree = parser.parse()
    except ValueError as e:
        await ctx.response.send_message(f"{str(e)}")
        return

    #評価
    try:
        result = tree.eval()
    except Exception as e:
        await ctx.response.send_message(f"{str(e)}")
        return

    #結果を表示する
    msg = f"{str(ctx.user.display_name)}::`{formula}` > `{str(tree)}` > `{str(result)}`"
    await ctx.response.send_message(msg)

client.run(token)