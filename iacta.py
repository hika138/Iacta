import discord
from discord import app_commands
import random
import re
import os
from os.path import join, dirname
import dotenv

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
    formula = formula.replace(' ', '')
    expression_1 = formula.split('+')
    expression_2 = []
    #それぞれの項を-で分割
    for i in range(len(expression_1)):
        temp = expression_1[i].split('-')
        for j in range(len(temp)):
            if j != 0:
                temp[j] = '-'+temp[j]
                print(temp[j])
            expression_2.append(temp[j])
    terms = []
    #全ての項をDで分割する
    for i in range(len(expression_2)):
        terms.append(re.split('[Dd]', expression_2[i]))

    terms_num = []
    for i in range(len(terms)):
        terms_num.append([])
        for j in range(len(terms[i])):
            try:
                terms_num[i].append(int(terms[i][j]))
            except ValueError:
                await ctx.response.send_message("[!式を解釈できません!]")
                return

    #それぞれのランダムを計算
    RandomValues = []
    values = []
    for i in range(len(terms_num)):
        RandomValues.append([])
        values.append(0)
        #ランダムの有無
        if len(terms_num[i])==2:
            for j in range(abs(terms_num[i][0])):
                RandomValues[i].append([])
                RandomValues[i][j] = random.randrange(1, terms_num[i][1]+1)
                if terms_num[i][0] > 0:
                    values[i]=values[i]+RandomValues[i][j] 
                else:
                    values[i]=values[i]-RandomValues[i][j] 
        else:
            #ランダムがない場合はその項の値をそのまま代入
            RandomValues[i]=terms_num[i][0]
            values[i]=terms_num[i][0]

    #それぞれの項を足し算
    result = 0
    for i in range(len(values)):
        result = result + values[i]

    #結果を表示する
    msg = str(ctx.user.display_name)+"::["+formula+"] > "+str(RandomValues)+" > "+str(result)
    await ctx.response.send_message(msg)

client.run(token)