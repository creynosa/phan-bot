import discord
from discord.ext import commands

class RoleAssignment(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # Emoji ID to role
    emojiDict = {
        '<:dungeon:737552892226961509>': 737555953875943475, #dungeons
        '<:fractalx:742424888190566570>': 737555903275859999, #fractals
        '<:raid:737553929411493930>': 737555904760643698, #raids
        '<:strike:737553953583267880>': 737555901023518801, #strikes
        '<:among_us:749727834527891476>': 749723933200220272, #among us
    }

    @commands.command()
    @commands.has_role('Phan')
    async def initiate(self, ctx):

        embed = discord.Embed(
            color=0x01a8ef,
            description='test',
        )

        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_role('Phan')
    async def updateEmbed(self, ctx):

        roleAssignChannelID = 737551865717194783
        roleAssignChannel = await self.bot.fetch_channel(roleAssignChannelID)

        roleMsgID = 749726421546434641
        roleMsg = await roleAssignChannel.fetch_message(roleMsgID)


        roleText = "React with the following emojis to assing yourself a GW2 role. \n \n" \
            "<:dungeon:737552892226961509> : @dungeons \n" \
            "<:fractalx:742424888190566570> : @fractals \n" \
            "<:raid:737553929411493930> : @raids \n" \
            "<:strike:737553953583267880> : @strikes \n\n" \
            "__**Other Roles**__ \n\n" \
            "<:among_us:749727834527891476> : @among us \n" 

        newEmbed = discord.Embed(
            color=0x01a8ef,
            description=roleText,
        )

        await roleMsg.edit(embed=newEmbed)

        for emojiID in RoleAssignment.emojiDict:
            emoji = self.bot.get_emoji(emojiID)
            await roleMsg.add_reaction(emoji)
        
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guildID = payload.guild_id
        guild = self.bot.get_guild(guildID)
        member = payload.member
        emoji = payload.emoji
        messageID = 749726421546434641

        # Ignores bot's own reactions
        if payload.user_id == self.bot.user.id:
            return

        # Ignore any non-relevant reactions
        if payload.message_id != messageID:
            return

        emojiRoleID = RoleAssignment.emojiDict[str(emoji)]
        emojiRole = guild.get_role(emojiRoleID)

        if emojiRole not in member.roles:
            await member.add_roles(emojiRole)
        else:
            return
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guildID = payload.guild_id
        guild = self.bot.get_guild(guildID)
        userID = payload.user_id
        emoji = payload.emoji
        messageID = 749726421546434641

        # Ignores bot's own reactions
        if payload.user_id == self.bot.user.id:
            return

        # Ignore any non-relevant reactions
        if payload.message_id != messageID:
            return
        
        try:
            member = guild.get_member(userID)
        except:
            return

        emojiRoleID = RoleAssignment.emojiDict[str(emoji)]
        emojiRole = guild.get_role(emojiRoleID)

        if emojiRole in member.roles:
            await member.remove_roles(emojiRole)
        else:
            return

def setup(bot):
    bot.add_cog(RoleAssignment(bot))