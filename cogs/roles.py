import discord
from discord.ext import commands


class RoleAssigners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    emojiRoleDict = {
        '<:raid:737553929411493930>': 737555904760643698,
        '<:fractal:737553944410062898>': 737555903275859999,
        '<:dungeon:737552892226961509>': 737555953875943475,
        '<:strike:737553953583267880>': 737555901023518801,
    }

    @commands.command()
    @commands.is_owner()
    async def setRoleAssigner(self, ctx):
        """Initializes the initial role assigner."""
        channel = ctx.channel

        roleEmbed = discord.Embed(
            color=0x00ADEF,
            description="""
            React with the appropriate emojis to self-assign your roles.
            
            <:raid:737553929411493930>  :  @raids
            <:fractal:737553944410062898>  :  @fractals
            <:dungeon:737552892226961509>  :  @dungeons
            <:strike:737553953583267880>  :  @strikes
            """
        )
        await ctx.send(embed=roleEmbed)

    @commands.command()
    @commands.is_owner()
    async def setEmojis(self, ctx):
        roleChannel = await self.bot.fetch_channel(737551865717194783)
        mainRoleMessage = await roleChannel.fetch_message(737554270349426689)

        for emojiName in RoleAssigners.emojiRoleDict.keys():
            await mainRoleMessage.add_reaction(emojiName)

        return

    @commands.command()
    @commands.is_owner()
    async def updateText(self, ctx):
        roleChannel = await self.bot.fetch_channel(737551865717194783)
        mainRoleMessage = await roleChannel.fetch_message(737554270349426689)

        newEmbed = discord.Embed(
            title='PvE Roles',
            color=0x00ADEF,
            description="""
                   React with the appropriate emoji to self-assign your roles.

                   <:raid:737553929411493930>  :  @raids
                   <:fractal:737553944410062898>  :  @fractals
                   <:dungeon:737552892226961509>  :  @dungeons
                   <:strike:737553953583267880>  :  @strikes
                   """
        )
        await mainRoleMessage.edit(embed=newEmbed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        roleChannel = await self.bot.fetch_channel(737551865717194783)
        mainRoleMessage = await roleChannel.fetch_message(737554270349426689)
        mainRoleMessageID = mainRoleMessage.id
        mainGuild = mainRoleMessage.guild

        member = payload.member
        reaction = str(payload.emoji)

        if payload.message_id == mainRoleMessageID:
            if reaction in RoleAssigners.emojiRoleDict.keys():
                roleID = RoleAssigners.emojiRoleDict[reaction]
                newRole = mainGuild.get_role(roleID)
                if newRole not in member.roles:
                    await member.add_roles(newRole)
                else:
                    return
            else:
                return
        return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        roleChannel = await self.bot.fetch_channel(737551865717194783)
        mainRoleMessage = await roleChannel.fetch_message(737554270349426689)
        mainRoleMessageID = mainRoleMessage.id
        mainGuild = mainRoleMessage.guild

        member = await mainGuild.fetch_member(payload.user_id)
        reaction = str(payload.emoji)

        if payload.message_id == mainRoleMessageID:
            if reaction in RoleAssigners.emojiRoleDict.keys():
                roleID = RoleAssigners.emojiRoleDict[reaction]
                newRole = mainGuild.get_role(roleID)
                if newRole in member.roles:
                    await member.remove_roles(newRole)
                else:
                    return
            else:
                return
        return


def setup(bot):
    bot.add_cog(RoleAssigners(bot))
