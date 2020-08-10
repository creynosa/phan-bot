import discord
import datetime
import random

from discord.ext import commands, tasks


class Fractals(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fractalMessage.start()
        self.makeGroup.start()

    channelID = 738992913127833621
    guildID = 733944519640350771
    role = 737555903275859999
    reactions = [
        '<:firebrand:739020215236427776>',
        '<:renegade:739020214938632253>',
        '⚔️',
    ]

    with open('fractalmessageid.txt', 'r') as f:
        try:
            messageID = [int(f.readlines()[0])]
        except:
            messageID = [None]

    @tasks.loop(minutes=1.0)
    async def fractalMessage(self):

        channel = self.bot.get_channel(Fractals.channelID)
        guild = await self.bot.fetch_guild(Fractals.guildID)
        fractalRole = guild.get_role(Fractals.role)

        dtNow = datetime.datetime.utcnow()
        if dtNow.minute == 17 and Fractals.messageID[0] is None:

            embed = discord.Embed(
                color=0x01A8EF,
                title='Fractal Sign-up!',
                description="""
                React with the role you want to play today down below!
                Teams will be made and posted 30 minutes before reset.
                
                <:firebrand:739020215236427776> Healbrand
                <:renegade:739020214938632253> Alacrigade
                :crossed_swords:  DPS
                """
            )
            msg = await channel.send(f'{fractalRole.mention}', embed=embed)

            for reaction in Fractals.reactions:
                await msg.add_reaction(reaction)

            with open('fractalmessageid.txt', 'w') as f:
                f.write(str(msg.id))

            Fractals.messageID[0] = msg.id

        else:
            return

    @fractalMessage.before_loop
    async def before_fractalMessage(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if payload.message_id == Fractals.messageID[0]:
                memberID = str(payload.member.id)
                emoji = str(payload.emoji)
                if emoji == '<:firebrand:739020215236427776>':
                    with open('healbrands.txt', 'a') as f:
                        f.write(f'{memberID} \n')
                elif emoji == '<:renegade:739020214938632253>':
                    with open('alacrigades.txt', 'a') as f:
                        f.write(f'{memberID} \n')
                elif emoji == '⚔️':
                    with open('dps.txt', 'a') as f:
                        f.write(f'{memberID} \n')
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.bot.user.id:
            if payload.message_id == Fractals.messageID[0]:

                guildID = payload.guild_id
                guild = await self.bot.fetch_guild(guildID)
                member = await guild.fetch_member(payload.user_id)
                memberID = str(member.id)
                emoji = payload.emoji

                if str(emoji) == '<:firebrand:739020215236427776>':
                    with open('healbrands.txt', 'r') as f:
                        lines = f.readlines()
                    with open('healbrands.txt', 'w') as f:
                        for line in lines:
                            if memberID not in line:
                                f.write(line)
                elif str(emoji) == '<:renegade:739020214938632253>':
                    with open('alacrigades.txt', 'r') as f:
                        lines = f.readlines()
                    with open('alacrigades.txt', 'w') as f:
                        for line in lines:
                            if memberID not in line:
                                f.write(line)
                elif str(emoji) == '⚔️':
                    with open('dps.txt', 'r') as f:
                        lines = f.readlines()
                    with open('dps.txt', 'w') as f:
                        for line in lines:
                            if memberID not in line:
                                f.write(line)
            else:
                return
        else:
            return

    @tasks.loop(minutes=1.0)
    async def makeGroup(self):
        dtNow = datetime.datetime.utcnow()
        if dtNow.minute == 30 and Fractals.messageID[0] is not None:
            with open('fractalmessageid.txt', 'r+') as f:
                f.truncate(0)

            healbrands = []
            alacrigades = []
            dps = []

            with open('healbrands.txt', 'r+') as f:
                lines = f.readlines()
                for line in lines:
                    healbrands.append(line.rstrip())
                f.truncate(0)

            with open('alacrigades.txt', 'r+') as f:
                lines = f.readlines()
                for line in lines:
                    alacrigades.append(line.rstrip())
                f.truncate(0)

            with open('dps.txt', 'r+') as f:
                lines = f.readlines()
                for line in lines:
                    dps.append(line.rstrip())
                f.truncate(0)

            random.shuffle(healbrands)
            random.shuffle(alacrigades)
            random.shuffle(dps)

            print(f'Healbrand List: {healbrands}')
            print(f'Alacrigade List: {alacrigades}')
            print(f'DPS List: {dps}')

            teams = Fractals.makeTeam(healbrands, alacrigades, dps)
            print(f'Teams Made: {teams}')

            channel = self.bot.get_channel(Fractals.channelID)
            guild = await self.bot.fetch_guild(733944519640350771)
            i = 0
            if teams:
                for team in teams:
                    i += 1

                    players = []
                    for playerID in team:
                        playerID = int(playerID)
                        playerMember = await guild.fetch_member(playerID)
                        players.append(playerMember)

                    await channel.send(f'\
                    __**Team {i}**__\n\n\
                    Healbrand: {players[0].mention}\n\
                    Alacrigade: {players[1].mention}\n\
                    DPS: {players[2].mention}\n\
                    DPS: {players[3].mention}\n\
                    DPS: {players[4].mention}\n\
                    ')
            else:
                embed = discord.Embed(
                    color=0x01A8EF,
                    description='Not enough people signed '
                                'up. Try again tomorrow!')
                await channel.send(embed=embed)

        return

    @makeGroup.before_loop
    async def before_makeGroup(self):
        await self.bot.wait_until_ready()

    @staticmethod
    def makeTeam(healbrands, alacrigades, dps):
        print('Making teams...')
        roles = [healbrands, alacrigades, dps]
        teams = []

        while True:
            try:
                print('Selecting player 1...')
                player1 = random.choice(healbrands)
                Fractals.removePlayer(player1, roles)
                print(f'Player 1: {player1}')

                player2 = random.choice(alacrigades)
                Fractals.removePlayer(player2, roles)

                player3 = random.choice(dps)
                Fractals.removePlayer(player3, roles)

                player4 = random.choice(dps)
                Fractals.removePlayer(player4, roles)

                player5 = random.choice(dps)
                Fractals.removePlayer(player5, roles)

                team = [player1, player2, player3, player4, player5]
                teams.append(team)

            except IndexError:
                print('No more teams can be made!')
                return teams

    @staticmethod
    def removePlayer(player, lists):
        for list in lists:
            try:
                list.remove(player)
            except ValueError:
                pass
        return


def setup(bot):
    bot.add_cog(Fractals(bot))
