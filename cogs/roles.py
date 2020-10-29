import discord
from discord.ext import commands


class RoleAssignment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guildID = 733944519640350771
    newRoleID = 771400729075515443

    roles = {
        "strikes": 737555901023518801,
        "fractals": 737555903275859999,
        "raids": 737555904760643698,
        "dungeons": 737555953875943475,
        "among-us": 749723933200220272,
        "phasmophobia": 764391990178611230,
        "raft": 768513337444139008,
        "minecraft": 768751825405870150,
    }

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith("!"):
            return

        channel = message.channel
        member = message.author
        splitMessage = message.content.split()
        command = splitMessage[0]

        if command == "!role":
            try:
                roleName = splitMessage[1]
                if RoleAssignment.validRole(roleName):
                    role = RoleAssignment.getRole(self, roleName)
                    if RoleAssignment.hasRole(self, roleName, member):
                        await member.remove_roles(role)
                        await RoleAssignment.sendConfirmation(
                            self, channel, added=False
                        )
                    else:
                        await member.add_roles(role)
                        await RoleAssignment.sendConfirmation(self, channel)
                else:
                    await RoleAssignment.sendInvalidRole(self, channel)
            except IndexError:
                await RoleAssignment.sendMissingRole(self, channel)
        elif command == "!roles":
            await RoleAssignment.sendRoles(self, channel)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Member successfully joined!")
        guild = self.bot.get_guild(RoleAssignment.guildID)
        newRole = guild.get_role(RoleAssignment.newRoleID)

        await member.add_roles(newRole)

    @staticmethod
    def validRole(roleName):
        return True if roleName in RoleAssignment.roles else False

    def getRole(self, roleName):
        roleID = RoleAssignment.roles[roleName]
        guild = self.bot.get_guild(RoleAssignment.guildID)
        role = guild.get_role(roleID)
        return role

    def hasRole(self, roleName, member):
        role = RoleAssignment.getRole(self, roleName)
        return True if role in member.roles else False

    async def sendConfirmation(self, channel, added=True):
        keyword = "added" if added else "removed"
        embed = discord.Embed(
            description=f"Role successfully {keyword}!",
            color=0xFFFFFF,
        )
        await channel.send(embed=embed)

    async def sendInvalidRole(self, channel):
        embed = discord.Embed(
            description="Not a valid role. Please try again!",
            color=0xFFFFFF,
        )
        await channel.send(embed=embed)

    async def sendRoles(self, channel):
        rolesString = ""
        for role in RoleAssignment.roles:
            rolesString += f"{role} \n"
        embed = discord.Embed(
            title="Available Roles",
            description=rolesString,
            color=0xFFFFFF,
        )
        await channel.send(embed=embed)

    async def sendMissingRole(self, channel):
        embed = discord.Embed(
            description='"!role" requires a role to be assigned or removed.'
            "\n\nExample: !role phasmophobia",
            color=0xFFFFFF,
        )
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(RoleAssignment(bot))