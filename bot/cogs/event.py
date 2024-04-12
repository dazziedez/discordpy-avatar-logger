import discord
import time
from pathlib import Path
BASE_PATH = Path(__file__).resolve().parent.parent.parent

from discord.ext import commands
from datetime import datetime

class AvatarChange(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar == after.avatar or not after.avatar:
            return

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Saving {after.name}")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        random_string = self.bot.random_string(10)
        fname = f"{timestamp}.{random_string}.png"
        avatar_path = BASE_PATH / f'webui/static/avatars/{after.id}/'
        avatar_path.mkdir(parents=True, exist_ok=True)

        file = await self.bot.save_image(after.avatar.url)
        with open(f"{avatar_path}/{fname}", 'wb') as f:
            f.write(file.getbuffer())

        guild = self.bot.get_guild(self.bot.testing_guild_id) or await self.bot.fetch_guild(self.bot.testing_guild_id)

        for i in guild.channels:
            if i.name == "avatar-log":
                channel = guild.get_channel(i.id) or await guild.fetch_channel(i.id)
                await channel.send(f"{after.mention} | `{after.name}` | `{after.id}` | <t:{int(time.time())}:R>", file=discord.File(f"{avatar_path}{fname}", fname))
                break

async def setup(bot):
    await bot.add_cog(AvatarChange(bot))
