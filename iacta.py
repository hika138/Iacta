import discord
from discord.ext import commands
import os
from os.path import join, dirname
import dotenv

dotenv_path = join(dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

server_id:int = int(str(os.getenv("SERVER_ID")))
token:str = str(os.getenv("TOKEN"))

class IactaBot(commands.Bot):
    def __init__(self, server_id: int):
        intent = discord.Intents.default()
        intent.message_content = True
        super().__init__(command_prefix="!", intents=intent)
        self.server_id = server_id

    async def setup_hook(self):
        await self.load_extension("cogs.roll")
        await self.tree.sync(guild=discord.Object(id=self.server_id))

    async def on_ready(self):
        print("get on ready!")

bot = IactaBot(server_id)
bot.run(token)