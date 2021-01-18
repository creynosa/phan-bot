# A module containing various commands and listeners for use with
# role-assignment embedded messages.

import discord
import toml
import asyncio
from discord.ext import commands


class RoleAssignment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Executes select code blocks when a reaction is added."""
        # Loading a fresh instance on the toml configuration file.
        # A fresh instance will allow for newly added configurations
        # without having to restart the bot.
        config = toml.load("configurations/role_assignments.toml")

        # First, determine that the message that the reaction was added to
        # is one of the self-role-assignment messages.
        if payload.message_id in list(config["EmbeddedMessagesIDs"].values()):
            # Determine if there is any role associated with the emote reaction
            # that was added.
            if str(payload.emoji) in config["Roles"]:
                # Get the Role object for the corresponding role
                guildID = config["GuildID"]["onlyphans"]
                guild = self.bot.get_guild(guildID)
                roleID = config["Roles"][str(payload.emoji)]
                role = guild.get_role(roleID)

                # Get the Member object for the user who added their reaction.
                member = payload.member

                # Add the role to the member.
                if role not in member.roles:
                    await member.add_roles(role)
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Executes select code blocks when a reaction is removed."""
        # Loading a fresh instance on the toml configuration file.
        # A fresh instance will allow for newly added configurations
        # without having to restart the bot.
        config = toml.load("configurations/role_assignments.toml")

        # First, determine that the message that the reaction was removed from
        # is one of the self-role-assignment messages.
        if payload.message_id in list(config["EmbeddedMessagesIDs"].values()):
            # Determine if there is any role associated with the emote reaction
            # that was removed.
            if str(payload.emoji) in config["Roles"]:
                # Get the Role object for the corresponding role.
                guildID = config["GuildID"]["onlyphans"]
                guild = self.bot.get_guild(guildID)
                roleID = config["Roles"][str(payload.emoji)]
                role = guild.get_role(roleID)

                # Get the Member object for the user who removed their
                # reaction.
                userID = payload.user_id
                member = guild.get_member(userID)

                # Remove the role from the member.
                if role in member.roles:
                    await member.remove_roles(role)
            else:
                return
        else:
            return


def setup(bot):
    bot.add_cog(RoleAssignment(bot))