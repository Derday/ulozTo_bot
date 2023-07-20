from discord.ext import commands
from pathlib import Path
import discord, os, yaml, asyncio


with open(Path(os.path.dirname(__file__)).joinpath('config.yaml'), 'r') as f:
    config = yaml.safe_load(f)
DEBUG: bool = config['debug']
TOKEN: str  = config['token']
PRFX:  str  = config['prfx']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix=PRFX, help_command=None)

async def load():
    for filename in os.listdir(Path(os.path.dirname(__file__)).joinpath('cogs')):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())