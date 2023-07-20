from speedtest import Speedtest
from colorama import Back, Fore, Style
from discord import app_commands
from pathlib import Path
from discord.ext import commands
import discord, os, json, yaml, time, asyncio

class Common(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        try:
            with open(Path(os.path.dirname(__file__)).joinpath('onStart.json'), 'r', encoding='utf-8') as f:
                self.onStart = json.loads(f.read())
        except Exception as e:
            print(e)
            self.newJson(False, 1)
        
        with open(Path(os.path.dirname(__name__)).joinpath('config.yaml'), 'r') as f:
            config = yaml.safe_load(f)
        self.DEBUG: bool = config['debug']
        self.TOKEN: str  = config['token']
        self.PRFX:  str  = config['prfx']
    
    def newJson(self, reboot, id):
        self.onStart = {
            'reboot':reboot,
            'id':id
        }
        with open(Path(os.path.dirname(__file__)).joinpath('onStart.json'), 'w', encoding='utf-8') as f:
            json.dump(self.onStart, f)
    
    def _print(self, msg: str, value: str = None):
        if not msg.endswith(' '):
            msg+=' '
        prfx = (Back.BLACK + Fore.GREEN + time.strftime('[%H:%M:%S UTC]', time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        if value:
            print(prfx + msg + Fore.YELLOW + value)
        else:
            print(prfx + msg)

    @commands.Cog.listener()    
    async def on_ready(self):
        self._print('Logged in as', self.bot.user.name)
        self._print('Bot id', str(self.bot.user.id))
        self._print('API version', discord.__version__)
        self._print('Initializing commands')
        await self.bot.change_presence(status=discord.Status.idle)
        synced = await self.bot.tree.sync()
        self._print('Commands synced', str(len(synced)))
        ac = discord.Game(name='/help')
        await self.bot.change_presence(status=discord.Status.online, activity=ac)
        if self.onStart['reboot']:
            await self.bot.get_channel(self.onStart['id']).send('Sucesfully rebooted')
        self.newJson(False, 1)
        self._print('Bot is online')


async def setup(bot):
    await bot.add_cog(Common(bot))