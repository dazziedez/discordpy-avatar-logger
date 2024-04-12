import discord

import asyncio
import string
import random
import logging
import io, os, json

from typing import List, Optional

from discord.ext import commands
from aiohttp import ClientSession

from cogs.help import Help

class Client(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        web_client: ClientSession,
        testing_guild_id: Optional[int],
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self):

        for extension in self.initial_extensions:
            await self.load_extension(extension)
            print("🌸", extension, "loaded")

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = discord.utils.utcnow()

    async def save_image(self, url):
        async with self.web_client.get(url) as resp:
            avatar_data = await resp.read()
            return io.BytesIO(avatar_data)

    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


async def main():

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('discord.log', encoding='utf-8')
    handler.setLevel(logging.INFO)

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as web_client:

        intents = discord.Intents.all()
        prefix = "="
        mentions = discord.AllowedMentions(
            roles=False, users=True, everyone=False)
        extensions = ["jishaku", "cogs.core"]
        async with Client(
            testing_guild_id=904460336118267954,
            web_client=web_client,
            initial_extensions=extensions,
            allowed_mentions=mentions,
            intents=intents,
            command_prefix=prefix,
            help_command=Help()
        ) as bot:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            with open(config_path, 'r') as file:
                config = json.load(file)
            await bot.start(config["bot_token"])

asyncio.run(main())
