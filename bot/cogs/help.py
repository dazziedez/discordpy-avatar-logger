from typing import Any
from discord.ext import commands
from discord.ui import Select, View
import discord


class HelpSelect(Select):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = commands
        self.placeholder = 'Choose a command...'
        for command in commands:
            self.add_option(label=command.name,
                            description=command.short_doc or 'No description')

    async def callback(self, interaction: discord.Interaction):
        command = discord.utils.get(self.commands, name=self.values[0])
        description = command.description or "No description available."
        usage = " ".join(
            [f"<{param.name}>" if param.default is param.empty else f"[{param.name}]" for param in command.clean_params.values()])
        embed = discord.Embed(
            title=f"Help for `{command}`", description=description)
        embed.add_field(
            name="Usage", value=f"```{command.qualified_name} {usage}```", inline=False)
        if command.aliases:
            embed.set_footer(text=f"Aliases: {' | '.join(command.aliases)}")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpView(View):
    def __init__(self, commands, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(HelpSelect(commands))


class Help(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Select a command for help",
                              description="Choose from the dropdown to see more details.")
        command_list = [command for cog in mapping.values()
                        for command in cog if command.cog_name != "Help" and not command.hidden]
        view = HelpView(command_list)
        await self.get_destination().send(embed=embed, view=view)

    async def send_command_help(self, command):
        if command.hidden:
            return

        description = command.description or "No description available."
        usage = " ".join(
            [f"<{param.name}>" if param.default is param.empty else f"[{param.name}]" for param in command.clean_params.values()])
        embed = discord.Embed(
            title=f"Help for `{command}`", description=description)
        embed.add_field(
            name="Usage", value=f"```{command.qualified_name} {usage}```", inline=False)

        if command.aliases:
            embed.set_footer(text=f"Aliases: {' | '.join(command.aliases)}")
        await self.get_destination().send(embed=embed)

async def setup(_):
    return