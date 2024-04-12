import discord

from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", description="Get a permanent url of someone's avatar", aliases=["av", "a", "pfp"])
    async def avatar(self, ctx, user: discord.Member | discord.User = None): # type: ignore
        await ctx.defer()
        user = user or ctx.author

        embed = discord.Embed(title=f"{user.name}'s avatar")

        file = None
        if user.avatar:
            file = await self.bot.save_image(user.avatar.url)
            file = discord.File(file, filename="avatar.png")
            embed.set_image(url="attachment://avatar.png")
        else:
            root = "https://cdn.discordapp.com/embed/avatars/"
            img = user.default_avatar.url.split("/")[-1]
            embed.set_image(url=root+img)

        await ctx.reply(file=file, embed=embed)

    @commands.command(name="banner", description="Get a permanent url of someone's banner", aliases=["bn", "b"])
    async def banner(self, ctx, user: discord.Member | discord.User = None): # type: ignore
        await ctx.defer()
        user = user or ctx.author
        user = await self.bot.fetch_user(user.id)
        embed = discord.Embed(title=f"{user.name}'s banner")

        file = None
        if user.banner:
            file = await self.bot.save_image(user.banner.url)
            file = discord.File(file, filename="banner.png")
            embed.set_image(url="attachment://banner.png")
        else:
            embed.description = "The user does not seem to have a banner."

        await ctx.reply(file=file, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Commands(bot))
