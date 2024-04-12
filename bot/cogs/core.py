from __future__ import annotations

import pathlib

import discord
from discord.ext import commands, tasks


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.tree = bot.tree
		self.cogs_path = pathlib.Path("cogs")
		self.extensions = [self.format_cog(str(item)) for item in self.cogs_path.glob(
			'**/*.py')]

	def format_cog(self, string: str):
		return string.replace("\\", ".")[:-3]

	async def setup_hook(self):
		await self.tree.sync(guild=discord.Object(id=self.bot.testing_guild_id))

	@commands.Cog.listener()
	async def on_ready(self):

		await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(
			type=discord.ActivityType.watching, name='for avatars'))

		for extension in self.extensions:
			try:
				await self.bot.load_extension(extension)
				print(f'   {extension} was loaded')
			except Exception as e:
				if not isinstance(e, commands.errors.ExtensionAlreadyLoaded):
					print(f'🟥 {extension} was not loaded: {e}')

		print(
			f"🆗 Logged in as {self.bot.user} with a {round(self.bot.latency * 1000)}ms delay")


async def setup(ce):
	await ce.add_cog(Events(ce))
