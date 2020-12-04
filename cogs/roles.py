import discord
import toml
import asyncio
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class CancelledError(commands.CommandError):
        pass

    embedLogoURL = r"https://raw.githubusercontent.com/creynosa/phan-bot/main/resources/images/Phan%20Logo%20-%20135.png"

    @staticmethod
    def createGameRolesEmbed():
        """Creates and returns a custom embed for the role embed command."""

        initialEmbed = discord.Embed(
            title="Game Roles",
            description="""**React to sign up for the following roles**:

            <:choyayaya:761762764271124491> @guildwars2
            <:ghostblob:781714216058355722> @phasmophobia
            <:among_us:781714930604310528> @among-us
            <:minecraft:781715314668077077> @minecraft""",
            color=0xFFFFFF,
        )
        initialEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )

        return initialEmbed

    @staticmethod
    def createGW2Embed():
        """Creates and returns a custom embed for the role embed command."""

        initialEmbed = discord.Embed(
            title="GW2 Roles",
            description="""**React to sign up for the following roles**:

            <:fractals:784312868987338782> @fractals
            <:raids:784312867720921108> @raids
            <:strikes:784314456901550110> @strikes
            <:dungeons:784314457186631680> @dungeons""",
            color=0xFFFFFF,
        )
        initialEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )

        return initialEmbed

    @staticmethod
    def createInitialEmbed():
        """Creates and returns the initial embed for the role embed commands."""

        initialEmbed = discord.Embed(
            title="Role Embed Options",
            color=0xFFFFFF,
        )
        initialEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        initialEmbed.add_field(
            name="Please enter the number of one of the following:",
            value="""`1` Update an existing role embed
            `2` Delete an existing role embed""",
        )
        initialEmbed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return initialEmbed

    @staticmethod
    def createTimeoutEmbed():
        """Creates and returns an embed used in response to a timeout error."""

        timeoutEmbed = discord.Embed(
            title="You have been timed out!",
            color=0xFFFFFF,
            description="You took more than 30 seconds to respond. Please try again.",
        )
        timeoutEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )

        return timeoutEmbed

    @staticmethod
    def createCancelledEmbed():
        """Creates and returns an embed used in response to a cancellation."""

        cancelledEmbed = discord.Embed(
            title="Cancelled.",
            color=0xFFFFFF,
        )
        cancelledEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )

        return cancelledEmbed

    @staticmethod
    def createIncorrectResponseEmbed():
        """Creates and returns an incorrect response embed for the role embed command."""

        incorrectEmbed = discord.Embed(
            title="Invalid Response. Please try again.",
            color=0xFFFFFF,
        )
        incorrectEmbed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        incorrectEmbed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return incorrectEmbed

    @staticmethod
    def createEmbed_1A():
        """Creates and returns an embed used for the role embed commands."""

        embed = discord.Embed(
            title="Role Embed Options",
            color=0xFFFFFF,
        )
        embed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        embed.add_field(
            name="Please enter one of the following:",
            value="""A) The target channel for the embed (Example: `#role-assignments`)
            OR
            B) The target channel's ID (Example: `781351551540920391`)""",
        )
        embed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return embed

    @staticmethod
    def createEmbed_2A():
        """Creates and returns an embed used for the role embed commands."""

        embed = discord.Embed(
            title="Message Url Required",
            color=0xFFFFFF,
            description="Please enter the message url for the chosen embed.",
        )
        embed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        embed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return embed

    @staticmethod
    def createEmbed_2B():
        """Creates and returns an embed used for the role embed commands."""

        embed = discord.Embed(
            title="Emoji Required",
            color=0xFFFFFF,
            description="Please enter the emoji used for role assignment.",
        )
        embed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        embed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return embed

    @staticmethod
    def createEmbed_2C():
        """Creates and returns an embed used for the role embed commands."""

        embed = discord.Embed(
            title="Role Required",
            color=0xFFFFFF,
            description="Please enter the role to be used for the role assignment.",
        )
        embed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        embed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return embed

    @staticmethod
    def createEmbed_2D():
        """Creates and returns an embed used for the role embed commands."""

        embed = discord.Embed(
            title="Continue?",
            color=0xFFFFFF,
            description="Added. Would you like to add another?",
        )
        embed.set_author(
            name="Phan Bot",
            icon_url=Roles.embedLogoURL,
        )
        embed.set_footer(
            text='Type "cancel" to quit and exit at anytime. You have 30 seconds to respond.',
        )

        return embed

    async def checkResponse(self, ctx, vCheck):
        def userCheck(message):
            return message.author == ctx.author

        async def checkCancelled(message):
            response = message.content.lower()
            if response in ("cancel", "quit", "exit", "q"):
                raise Roles.CancelledError

        response = None
        while True:
            response = await self.bot.wait_for("message", check=userCheck, timeout=30)
            await checkCancelled(response)
            if await vCheck(ctx, response):
                break
            else:
                incorrectEmbed = Roles.createIncorrectResponseEmbed()
                await ctx.send(embed=incorrectEmbed)

        return response.content

    @commands.command()
    @commands.is_owner()
    async def createEmbed(self, ctx):
        """Starts the process of creating a role-assignment embed."""

        async def check_1A(ctx, m):
            response = m.content.lower()
            try:
                await commands.TextChannelConverter().convert(ctx, response)
                return True
            except commands.ChannelNotFound:
                return False

        nextEmbed = Roles.createEmbed_1A()
        await ctx.send(embed=nextEmbed)
        response = await Roles.checkResponse(self, ctx, vCheck=check_1A)

        channel = await commands.TextChannelConverter().convert(ctx, response)
        roleEmbed = Roles.createGW2Embed()

        await channel.send(embed=roleEmbed)

    @commands.command()
    @commands.is_owner()
    async def updateEmbed(self, ctx):
        """Starts the process of updating or deleting a role embed."""

        async def check_1(ctx, m):
            response = m.content.lower()
            if response in ("1", "2"):
                return True
            else:
                return False

        async def ynCheck(ctx, m):
            response = m.content.lower()
            if response in ["yes", "no", "y", "n"]:
                return True
            else:
                return False

        async def validMsg(ctx, m):
            response = m.content
            try:
                await commands.MessageConverter().convert(ctx, response)
                return True
            except commands.MessageNotFound:
                return False

        async def validRole(ctx, m):
            response = m.content
            try:
                await commands.RoleConverter().convert(ctx, response)
                return True
            except commands.RoleNotFound:
                return False

        async def validPEmoji(ctx, m):
            response = m.content
            try:
                await commands.PartialEmojiConverter().convert(ctx, response)
                return True
            except commands.PartialEmojiConversionFailure:
                return False

        # Have the user select a valid option for the initial part of the
        # role embed creation process.
        initialEmbed = Roles.createInitialEmbed()
        msg = await ctx.send(embed=initialEmbed)
        response = await Roles.checkResponse(self, ctx, vCheck=check_1)
        await msg.delete()

        # Have the bot update an existing role-assigment embed.
        if response == "1":
            # Asking for embed ID
            nextEmbed = Roles.createEmbed_2A()
            msg = await ctx.send(embed=nextEmbed)
            response = await Roles.checkResponse(self, ctx, vCheck=validMsg)
            await msg.delete()
            embedMessage = await commands.MessageConverter().convert(ctx, response)

            # Updating role emojis
            config = toml.load("configurations/role_assignments.toml")
            while True:
                # Asking for an Emoji.
                nextEmbed = Roles.createEmbed_2B()
                msg = await ctx.send(embed=nextEmbed)
                response = await Roles.checkResponse(self, ctx, vCheck=validPEmoji)
                await msg.delete()
                emoji = await commands.PartialEmojiConverter().convert(ctx, response)

                # Asking for a Role.
                nextEmbed = Roles.createEmbed_2C()
                msg = await ctx.send(embed=nextEmbed)
                response = await Roles.checkResponse(self, ctx, vCheck=validRole)
                await msg.delete()
                role = await commands.RoleConverter().convert(ctx, response)

                # Updating the embed with the reaction.
                await embedMessage.add_reaction(emoji)

                # Updating the configuration file.
                config["Roles"][str(emoji)] = role.id

                # Asking if they want to continue adding more assignments.
                nextEmbed = Roles.createEmbed_2D()
                msg = await ctx.send(embed=nextEmbed)
                response = await Roles.checkResponse(self, ctx, vCheck=ynCheck)
                await msg.delete()

                if response in ["yes", "y"]:
                    continue
                else:
                    with open(
                        "configurations/role_assignments.toml", "w"
                    ) as configfile:
                        toml.dump(config, configfile)
                    break

        # Have the bot completely delete an existing role-assignment embed.
        elif response == "2":
            pass
            # TODO

    @updateEmbed.error
    async def updateEmbed_error(self, ctx, error):
        errorEmbed = None

        if isinstance(error, commands.CommandInvokeError):
            errorEmbed = Roles.createTimeoutEmbed()
        elif isinstance(error, Roles.CancelledError):
            errorEmbed = Roles.createCancelledEmbed()

        await ctx.send(embed=errorEmbed)

    @createEmbed.error
    async def createEmbed_error(self, ctx, error):
        errorEmbed = None

        if isinstance(error, commands.CommandInvokeError):
            errorEmbed = Roles.createTimeoutEmbed()
        elif isinstance(error, Roles.CancelledError):
            errorEmbed = Roles.createCancelledEmbed()

        await ctx.send(embed=errorEmbed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        config = toml.load("configurations/role_assignments.toml")

        if payload.message_id in list(config["EmbeddedMessagesIDs"].values()):
            if str(payload.emoji) in config["Roles"]:
                guildID = config["GuildID"]["onlyphans"]
                guild = self.bot.get_guild(guildID)
                roleID = config["Roles"][str(payload.emoji)]
                role = guild.get_role(roleID)
                member = payload.member
                if role not in member.roles:
                    await member.add_roles(role)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        config = toml.load("configurations/role_assignments.toml")

        if payload.message_id in list(config["EmbeddedMessagesIDs"].values()):
            if str(payload.emoji) in config["Roles"]:
                guildID = config["GuildID"]["onlyphans"]
                guild = self.bot.get_guild(guildID)
                roleID = config["Roles"][str(payload.emoji)]
                role = guild.get_role(roleID)
                userID = payload.user_id
                member = guild.get_member(userID)
                if role in member.roles:
                    await member.remove_roles(role)
            else:
                return
        else:
            return


def setup(bot):
    bot.add_cog(Roles(bot))