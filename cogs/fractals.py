import discord
import toml
from discord.ext import commands

class Fractals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    configs = toml.load("configurations/configurations.toml")
    channelID = configs['Signups']['fractalChannelID']
    guildID = 733944519640350771
    roleID = 737555903275859999

    guildFractalRoleIDs = {
        'Free Users' : 737547101877305374,
        'Only Phans' : 734152243972014120,
        'Phancy Phans' : 737603553480278068,
        'Top Phans' : 742630788750901279,
        'Premium Phans' : 743410326996779089,
        'Omega Phans' : 743410705264410694,
    }

    @commands.command()
    async def fractal(self, ctx, level=None):
        await ctx.message.delete()

        guild = ctx.guild
        fractalRole = guild.get_role(Fractals.roleID)

        errorInLevelString = 'Incorrect syntax. Please try again and use one of the four ' \
            'options: \n\n"beginner", "intermediate", "advanced", or leave blank for public.'

        if level is None:
            level = 'public'
        else:
            level = level.lower()

        if level not in ['public', 'beginner', 'intermediate', 'advanced']:
            await Fractals.sendMessage(
                ctx,
                string = errorInLevelString,
                level=level,
                footer=False
            )
            return
        
        # Determining if the user is able to make the fractal
        if level == 'intermediate':
            allowedRoles = [
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'advanced':
            allowedRoles = [
                'Top Phans',
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'beginner':
            allowedRoles = [
                'Only Phans',
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'public':
            allowedRoles = [
                'Free Users',
                'Only Phans',
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]

        # Determing the embed colors
        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F


        allowedRoleObjects = []
        for roleName in allowedRoles:
            roleID = Fractals.guildFractalRoleIDs[roleName]
            roleObject = guild.get_role(roleID)
            allowedRoleObjects.append(roleObject)

        canMake = False
        memberRoles = ctx.author.roles 
        for role in memberRoles:
            if role in allowedRoleObjects:
                canMake = True
                break
        
        if not canMake:
            embed = discord.Embed(
                color = embedColor,
                description = 'Sorry, you need a higher role in order to '\
                    'create this kind of run.'
            )
            await ctx.channel.send(embed=embed)
            return


        try:
            def checkAuthor(message):
                return ctx.author == message.author

            botMessage = await Fractals.sendMessage(
                ctx,
                'Please enter a description for the fractal run.\n\n' \
                'Example: CMs + T4s',
                level=level
                )

            response1 = await self.bot.wait_for(
                'message', 
                check=checkAuthor,
                timeout=30
                )
            
            embedDescription = response1.content

            await response1.delete()
            await botMessage.delete()

            if response1.content.lower() == 'cancel':
                raise AssertionError

            botMessage = await Fractals.sendMessage(
                ctx,
                'Please enter a time and a time zone for the fractal run.\n\n' \
                'Example: Today at 7:00 PM CST',
                level=level
                )

            response2 = await self.bot.wait_for(
                'message', 
                check=checkAuthor,
                timeout=30
                )
            
            embedTime = response2.content

            await response2.delete()
            await botMessage.delete()

            if response2.content.lower() == 'cancel':
                raise AssertionError
            
            if level != 'public' and level != 'beginner':
                blankRoster = {
                    'Healbrand': False, 
                    'Alacrigade': False, 
                    'BS': False, 
                    'DPS1': False, 
                    'DPS2': False
                }
            else:
                blankRoster = {
                    'Healbrand': False, 
                    'Alacrigade': False, 
                    'DPS1': False, 
                    'DPS2': False, 
                    'DPS3': False
                }

            blankSpecs = blankRoster

            channel = self.bot.get_channel(Fractals.channelID)
            await channel.send(f'{fractalRole.mention}')
            finalMessage = await channel.send(
                embed= await Fractals.createFractalEmbed(
                    embedDescription,
                    embedTime,
                    ctx.author,
                    self.bot,
                    blankRoster,
                    blankSpecs,
                    level=level
                )
            )

            if level != 'public' and level != 'beginner':
                initialRosterDict = {
                    str(finalMessage.id): {
                        'Healbrand': False, 
                        'Alacrigade': False, 
                        'BS': False, 
                        'DPS1': False, 
                        'DPS2': False
                        }
                    }
            else:
                initialRosterDict = {
                str(finalMessage.id): {
                    'Healbrand': False, 
                    'Alacrigade': False, 
                    'DPS1': False, 
                    'DPS2': False, 
                    'DPS3': False
                    }
                }
            
            fractalEmbedDict = {
                str(finalMessage.id) : {
                    'Description': embedDescription,
                    'Time' : embedTime,
                    'Author ID' : ctx.author.id,
                    'Level' : level
                }
            }

            if level != 'public' and level != 'beginner':
                specsDict = {
                    str(finalMessage.id): {
                        'Healbrand': False,
                        'Alacrigade': False,
                        'BS': False,
                        'DPS1': False,
                        'DPS2' : False
                    }
                }
            else:
                specsDict = {
                    str(finalMessage.id): {
                        'Healbrand': False,
                        'Alacrigade': False,
                        'DPS1': False,
                        'DPS2': False,
                        'DPS3' : False
                    }
                }

            # Writing intial configuration to temporary files.
            with open('temporary/fractalteams.toml', 'a') as f:
                toml.dump(initialRosterDict, f)
                f.write('\n')
            with open ('temporary/fractalembeds.toml', 'a') as g:
                toml.dump(fractalEmbedDict, g)
                g.write('\n')        
            with open('temporary/fractalteamspecs.toml', 'a') as h:
                toml.dump(specsDict, h)
                h.write('\n')

            await Fractals.reactWithEmojis(self.bot, finalMessage, 'Core')

            return

        except AssertionError:
            await Fractals.sendCancelMessage(
                ctx,
                'Cancelled. Take care!',
                level = level
            )
        except TimeoutError:
            await botMessage.delete(delay=3)
            await Fractals.sendCancelMessage(
                ctx,
                'Sorry, you took too long. Please try again!',
                level=level
            )

    @staticmethod
    async def sendMessage(ctx, string, level='public', footer=True):

        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F
        else:
            embedColor = 0x99AAB5

        embed = discord.Embed(
            color = embedColor,
            description = f"{string}"
        )
        embed.set_thumbnail(
            url='https://i.imgur.com/Dkc5BjH.png'
        )
        embed.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        )
        if footer:
            embed.set_footer(text="Type 'cancel' to cancel at anytime.")
        msg = await ctx.send(embed=embed)
        return msg

    @staticmethod
    async def sendCancelMessage(ctx, string, level='public'):

        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F

        embed = discord.Embed(
            color = embedColor,
            description = f"{string}"
        )
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=3)
        return

    @staticmethod
    async def createFractalEmbed(description, time, author, bot, roster, specs, level ='public', footer=True):
        guild = bot.get_guild(Fractals.guildID)

        with open('resources/emojisets.toml', 'r') as f:
            professionEmojiDict = toml.load(f)['Professions']

        emojis = []
        for spec in list(specs.values()):
            if spec is False:
                emoji = 'N'
                emojis.append(emoji)
            else:
                emojiID = int(professionEmojiDict[spec])
                emoji = bot.get_emoji(emojiID)
                emojis.append(emoji)

        membersMention = []
        for memberID in list(roster.values()):
            if memberID is False:
                memberMention = '/A'
                membersMention.append(memberMention)
            else:
                memberID = int(memberID)
                member = await guild.fetch_member(memberID)
                membersMention.append(member.mention)

        if level == 'public':
            embedColor = 0x99AAB5
            prefix = 'Public'
        elif level == 'beginner':
            embedColor = 0x01a8ef
            prefix = 'Beginner'
        elif level == 'intermediate':
            embedColor = 0x2ECC71
            prefix = 'Intermediate'
        elif level == 'advanced':
            embedColor = 0xF1C40F
            prefix = 'Advanced'

        embed = discord.Embed(
            color = embedColor,
            title = f'{prefix} Fractal Signup: {description}',
            description=f'`Time:` {time}'
        )
        embed.set_thumbnail(
            url='https://i.imgur.com/Dkc5BjH.png'
        )
        embed.set_author(
            name=f'{author}',
            icon_url=f'{author.avatar_url}'
        )
        if level != 'public' and level != 'beginner':
            embed.add_field(
            name='Roster',
            value=f'`[Healbrand]` {emojis[0]}{membersMention[0]} \n'\
                    f'`[Alacrigade]` {emojis[1]}{membersMention[1]} \n'\
                    f'`[BS]` {emojis[2]}{membersMention[2]} \n' \
                    f'`[DPS 1]` {emojis[3]}{membersMention[3]} \n' \
                    f'`[DPS 2]` {emojis[4]}{membersMention[4]} '  
            )   
        else:
            embed.add_field(
                name='Roster',
                value=f'`[Healbrand]` {emojis[0]}{membersMention[0]} \n'\
                        f'`[Alacrigade]` {emojis[1]}{membersMention[1]} \n'\
                        f'`[DPS 1]` {emojis[2]}{membersMention[2]} \n' \
                        f'`[DPS 2]` {emojis[3]}{membersMention[3]} \n' \
                        f'`[DPS 3]` {emojis[4]}{membersMention[4]} '  
            )
        if footer:     
            embed.set_footer(
                text='React with the "🗑️" emoji to cancel this posting.' \
                    ' React with the red "X" emoji to remove yourself.'
            )
        return embed

    @staticmethod
    async def reactWithEmojis(bot, message, group):
        with open('resources/emojisets.toml', 'r') as f:
            emojiDict = toml.load(f)[group]
        with open('resources/emojisets.toml', 'r') as f:    
            cancelEmojiID = toml.load(f)['Extras']['X']

        emojis = []
        for key in emojiDict.keys():
            emoji = bot.get_emoji(int(emojiDict[key]))
            emojis.append(emoji)

        cancelEmoji = bot.get_emoji(int(cancelEmojiID))
        emojis.append(cancelEmoji)
        
        # Adding wastebasket emoji for closing down a post.
        emojis.append('🗑️')

        for emoji in emojis:
            await message.add_reaction(emoji)
        
        return

    @staticmethod
    def getSpecs(className):
        if className == 'Guardian':
            spec1 = 'Guardian'
            spec2 = 'Dragonhunter'
            spec3 = 'Firebrand'
        if className == 'Warrior':
            spec1 = 'Warrior'
            spec2 = 'Berserker'
            spec3 = 'Spellbreaker'
        if className == 'Thief':
            spec1 = 'Thief'
            spec2 = 'Daredevil'
            spec3 = 'Deadeye'
        if className == 'Elementalist':
            spec1 = 'Elementalist'
            spec2 = 'Tempest'
            spec3 = 'Weaver'
        if className == 'Ranger':
            spec1 = 'Ranger'
            spec2 = 'Druid'
            spec3 = 'Soulbeast'
        if className == 'Engineer':
            spec1 = 'Engineer'
            spec2 = 'Holosmith'
            spec3 = 'Scrapper'
        if className == 'Necromancer':
            spec1 = 'Necromancer'
            spec2 = 'Reaper'
            spec3 = 'Scourge'
        if className == 'Revenant':
            spec1 = 'Revenant'
            spec2 = 'Herald'
            spec3 = 'Renegade'
        if className == 'Mesmer':
            spec1 = 'Mesmer'
            spec2 = 'Chronomancer'
            spec3 = 'Mirage'
        
        return [spec1, spec2, spec3]
        
    @staticmethod
    def makeSpecEmbed(bot, specs, level='public'):
        with open('resources/emojisets.toml', 'r') as f:
            professionEmojiDict = toml.load(f)['Professions']

        spec1, spec2, spec3 = specs
        emojis = []
        for spec in specs:
            emojiID = int(professionEmojiDict[spec])
            emoji = bot.get_emoji(emojiID)
            emojis.append(emoji)
  
        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F

        embed = discord.Embed(
            color = embedColor,
            title = 'Elite Specialization',
            description = 'Please type the number of the specialization that '\
                'you will be using. \n\n' \
                f'\t `1` {emojis[0]} {spec1} \n'
                f'\t `2` {emojis[1]} {spec2} \n'
                f'\t `3` {emojis[2]} {spec3} \n \n'
                'You may also type "*cancel*" to exit at anytime.'
        )

        return embed

    @staticmethod
    def makeRoleSelectionEmbed(bot, spec, team, level='public'):

        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F

        if level != 'public' and level != 'beginner':
            if spec == 'Firebrand' and bool(team['Healbrand']) is False:
                options = ['Healbrand', 'DPS']
            elif spec == 'Renegade' and bool(team['Alacrigade']) is False:
                options = ['Alacrigade', 'DPS']
            elif spec == 'Berserker' and bool(team['BS']) is False:
                options = ['BS', 'DPS']
            else:
                options = ['DPS']
        else:
            if spec == 'Firebrand' and bool(team['Healbrand']) is False:
                options = ['Healbrand', 'DPS']
            elif spec == 'Renegade' and bool(team['Alacrigade']) is False:
                options = ['Alacrigade', 'DPS']
            else:
                options = ['DPS']

        if len(options) > 1:
            embed = discord.Embed(
                color = embedColor,
                description = "What role will you be playing? \n\n" \
                f"`1` {options[0]} \n" \
                f"`2` {options[1]}"
            )
            return embed
        else:
            return None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guildID = payload.guild_id
        guild = self.bot.get_guild(guildID)
        fullTeam = False
        closePost = False
        member = payload.member
        emoji = payload.emoji
        messageID = payload.message_id

        # Ignores bot's own reactions
        if payload.user_id == self.bot.user.id:
            return

        # Retrieves the entire Fractal Teams rosters, specs, embeds, and emojis.
        with open('temporary/fractalteams.toml', 'r') as f:
            teamsToml = toml.load(f)
        with open('resources/emojisets.toml', 'r') as g:
            emojiToml = toml.load(g)
        with open('temporary/fractalteamspecs.toml', 'r') as h:
            specsToml = toml.load(h)
        with open('temporary/fractalembeds.toml', 'r') as g:
            fractalEmbedsToml = toml.load(g)
        
        # Retrieving information from the original embed.
        fractalEmbedDict = fractalEmbedsToml[str(messageID)]
        level = fractalEmbedDict['Level']
        oldDescription = fractalEmbedDict['Description']
        oldTime = fractalEmbedDict['Time']
        oldAuthorID = fractalEmbedDict['Author ID']
        oldMember = await guild.fetch_member(oldAuthorID)

        # Setting the color for embeds created within this section of code.
        # Will also be utilized for role checking.   

        if level == 'public':
            embedColor = 0x99AAB5
        elif level == 'beginner':
            embedColor = 0x01a8ef
        elif level == 'intermediate':
            embedColor = 0x2ECC71
        elif level == 'advanced':
            embedColor = 0xF1C40F


        # Intiating process of obtaining the team information for a
        # given message.
        fractalMessageIDs = teamsToml.keys()

        # Ignore any non-relevant reactions
        if str(payload.message_id) not in fractalMessageIDs:
            return
        
        # Removes the reaction immediately.
        channel = self.bot.get_channel(Fractals.channelID)
        ogMessage = await channel.fetch_message(messageID)
        await ogMessage.remove_reaction(emoji, member)

        teamDict = teamsToml[str(payload.message_id)]
        specsDict = specsToml[str(payload.message_id)]

        # Sets a DM channel with the user, if one doesn't exist.
        if member.dm_channel is None:
            await member.create_dm()
        dmChannel = member.dm_channel 

        # Determines if the user is able to react to the post given
        # their role and experience.

        if level == 'intermediate':
            allowedRoles = [
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'advanced':
            allowedRoles = [
                'Top Phans',
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'beginner':
            allowedRoles = [
                'Only Phans',
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]
        elif level == 'public':
            allowedRoles = [
                'Free Users',
                'Only Phans',
                'Phancy Phans', 
                'Top Phans', 
                'Premium Phans',
                'Omega Phans'
            ]

        allowedRoleObjects = []
        for roleName in allowedRoles:
            roleID = Fractals.guildFractalRoleIDs[roleName]
            roleObject = guild.get_role(roleID)
            allowedRoleObjects.append(roleObject)

        canReact = False
        memberRoles = member.roles 
        for role in memberRoles:
            if role in allowedRoleObjects:
                canReact = True
                break
        
        if not canReact:
            embed = discord.Embed(
                color = embedColor,
                description = 'Sorry, you need a higher role to sign up for this run.'
            )
            await dmChannel.send(embed=embed)
            return

        # If the user reacted with a core class, initiate the selection process.
        # The user can also react with an "X" icon to remove themselves from the
        # roster, or a wastebasket to scrap the whole post itself.
        if emoji.name in emojiToml['Core'].keys():

            # If the user is already on the roster, send the user an error.
            if payload.user_id in list(teamDict.values()):
                embed = discord.Embed(
                    color=embedColor,
                    description='You are already on the roster. Please remove ' \
                        'yourself from the roster and try again.'
                )
                await dmChannel.send(embed=embed)
                return

            # Send a user a message asking them to pick a specialization.
            specsList = Fractals.getSpecs(emoji.name)
            specEmbed = Fractals.makeSpecEmbed(self.bot, specsList, level=level)

            await dmChannel.send(embed=specEmbed)
            try:
                response1 = await self.bot.wait_for(
                    'message',
                    timeout=60,
                    check = lambda message: payload.user_id == message.author.id
                )
            except:
                embed = discord.Embed(
                color = embedColor,
                description = "Sorry, you took too long. Please react again!"
                )
                await dmChannel.send(embed=embed)
                return

            if response1.content.lower() == 'cancel':
                await Fractals.sendCancelMessage(dmChannel, 'Cancelled!', level=level)
                return
            elif response1.content.lower() == '1':
                spec = specsList[0]
            elif response1.content.lower() == '2':
                spec = specsList[1]
            elif response1.content.lower() == '3':
                spec = specsList[2]

            # Depending on the specialization, asks the user to pick a role.
            # Default is DPS.
            roleEmbed = Fractals.makeRoleSelectionEmbed(self.bot, spec, teamDict, level=level)
            if roleEmbed is not None:
                await dmChannel.send(embed=roleEmbed)
                try:
                    response2 = await self.bot.wait_for(
                        'message',
                        timeout=60,
                        check = lambda message: payload.user_id == message.author.id
                    )
                except:
                    embed = discord.Embed(
                    color = embedColor,
                    description = "Sorry, you took too long. Please react again!"
                    )
                    await channel.send(embed=embed)
                    return
                
                if level != 'public' and level != 'beginner':
                    if response2.content.lower() == 'cancel':
                        await Fractals.sendCancelMessage(channel, 'Cancelled!')
                    elif response2.content.lower() == '1' and spec == 'Firebrand':
                        role = 'Healbrand'
                        specsDict['Healbrand'] = 'Firebrand'
                    elif response2.content.lower() == '1' and spec == 'Renegade':
                        role = 'Alacrigade'
                        specsDict['Alacrigade'] = 'Renegade'
                    elif response2.content.lower() == '1' and spec == 'Berserker':
                        role = 'BS'
                        specsDict['BS'] = 'Berserker'
                    else:
                        role = 'DPS'
                else:
                    if response2.content.lower() == 'cancel':
                        await Fractals.sendCancelMessage(channel, 'Cancelled!')
                    elif response2.content.lower() == '1' and spec == 'Firebrand':
                        role = 'Healbrand'
                        specsDict['Healbrand'] = 'Firebrand'
                    elif response2.content.lower() == '1' and spec == 'Renegade':
                        role = 'Alacrigade'
                        specsDict['Alacrigade'] = 'Renegade'
                    else:
                        role = 'DPS'
            else:
                role = 'DPS'

            # Determines if there are enough DPS players.
            if role == 'DPS':
                if level != 'public' and level != 'beginner':
                    if teamDict['DPS1'] is False:
                        role = 'DPS1'
                        teamDict['DPS1'] = payload.user_id
                        specsDict['DPS1'] = spec
                        successEmbed = discord.Embed(
                            color = embedColor,
                            description = "Sucessfully signed up!"
                        )
                        await dmChannel.send(embed=successEmbed)
                    elif teamDict['DPS2'] is False:
                        role = 'DPS2'
                        teamDict['DPS2'] = payload.user_id
                        specsDict['DPS2'] = spec
                        successEmbed = discord.Embed(
                            color = embedColor,
                            description = "Sucessfully signed up!"
                        )
                        await dmChannel.send(embed=successEmbed)
                    else:
                        embed = discord.Embed(
                            color = embedColor,
                            description='There are already enough DPS players. ' \
                                'Please pick a new role or try again later.'
                        )
                        await dmChannel.send(embed=embed)
                        return
                else:
                    if teamDict['DPS1'] is False:
                        role = 'DPS1'
                        teamDict['DPS1'] = payload.user_id
                        specsDict['DPS1'] = spec
                        successEmbed = discord.Embed(
                            color = embedColor,
                            description = "Sucessfully signed up!"
                        )
                        await dmChannel.send(embed=successEmbed)
                    elif teamDict['DPS2'] is False:
                        role = 'DPS2'
                        teamDict['DPS2'] = payload.user_id
                        specsDict['DPS2'] = spec
                        successEmbed = discord.Embed(
                            color = embedColor,
                            description = "Sucessfully signed up!"
                        )
                        await dmChannel.send(embed=successEmbed)
                    elif teamDict['DPS3'] is False:
                        role = 'DPS3'
                        teamDict['DPS3'] = payload.user_id
                        specsDict['DPS3'] = spec
                        successEmbed = discord.Embed(
                            color = embedColor,
                            description = "Sucessfully signed up!"
                        )
                        await dmChannel.send(embed=successEmbed)
                    else:
                        embed = discord.Embed(
                            color = embedColor,
                            description='There are already enough DPS players. ' \
                                'Please pick a new role or try again later.'
                        )
                        await dmChannel.send(embed=embed)
                        return
            
            # Changes the team dictionary roster accordingly.
            else:
                teamDict[role] = payload.user_id
                successEmbed = discord.Embed(
                    color = embedColor,
                    description = "Sucessfully signed up!"
                )
                await dmChannel.send(embed=successEmbed)
            
            # Edits the embed to include the newly changed Roster.
            updatedEmbed = await Fractals.createFractalEmbed(
                description = oldDescription,
                time = oldTime,
                author = oldMember,
                bot = self.bot,
                roster = teamDict,
                specs = specsDict,
                level=level
            )

            await ogMessage.edit(embed=updatedEmbed)
            
            # Starts the process of checking if a full team is made.
            fullTeam = True
            for role in teamDict.keys():
                if bool(teamDict[role]) is False:
                    fullTeam = False
                    break

        elif payload.emoji.name == 'X_':
            for key, value in teamDict.items():
                if payload.user_id == int(value):
                    dictKey = key
                    break
                else:
                    dictKey = None
            if dictKey is not None:
                teamDict[dictKey] = False
                specsDict[dictKey] = False

            updatedEmbed = await Fractals.createFractalEmbed(
                description = oldDescription,
                time = oldTime,
                author = oldMember,
                bot = self.bot,
                roster = teamDict,
                specs = specsDict,
                level=level
            )

            await ogMessage.edit(embed=updatedEmbed)
        elif payload.emoji.name == '🗑️' and member == oldMember:
            closePost = True

        # Once the roster is made, it is removed from the .toml dictionary.
        # Also executes if the user decides to scrap their post.
        if fullTeam or closePost:
            if fullTeam:
                completeRoster = teamDict.copy()

                playerIDs = list(completeRoster.values())
                playerMentions = []
                for playerID in playerIDs:
                    player = await guild.fetch_member(playerID)
                    playerMentions.append(player.mention)
                
                updatedEmbed = await Fractals.createFractalEmbed(
                    description = oldDescription,
                    time = oldTime,
                    author = oldMember,
                    bot = self.bot,
                    roster = teamDict,
                    specs = specsDict,
                    level = level,
                    footer=False
                )

                await channel.send(
                    f'Your team has been made! ' \
                    f'{playerMentions[0]} '\
                    f'{playerMentions[1]} '\
                    f'{playerMentions[2]} '\
                    f'{playerMentions[3]} '\
                    f'{playerMentions[4]}',
                    embed=updatedEmbed
                )

                embed = discord.Embed(
                    color = embedColor,
                    description = '[Completed]'
                    )
                await ogMessage.edit(embed=embed)
                await ogMessage.clear_reactions()
            else:
                embed = discord.Embed(
                    color = embedColor,
                    description = '[Cancelled]'
                    )
                await ogMessage.edit(embed=embed)
                await ogMessage.clear_reactions()

            teamsToml.pop(str(payload.message_id))
            specsToml.pop(str(payload.message_id))
            fractalEmbedsToml.pop(str(payload.message_id))
        
        # Rewrites the .toml files to finalize any updates.
        with open('temporary/fractalteams.toml', 'w') as f:
            toml.dump(teamsToml, f)
        with open('temporary/fractalteamspecs.toml', 'w') as g:
            toml.dump(specsToml, g)
        with open('temporary/fractalembeds.toml', 'w') as h:
            toml.dump(fractalEmbedsToml, h)       
        
        return

def setup(bot):
    bot.add_cog(Fractals(bot))