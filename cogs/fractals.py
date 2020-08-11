import discord
import toml
from discord.ext import commands

class Fractals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    configs = toml.load("configurations/configurations.toml")
    channelID = configs['Signups']['fractalChannelID']
    roleID = 737555903275859999

    @commands.command()
    @commands.has_role('Only Phans')
    async def fractal(self, ctx):
        guild = ctx.guild
        role = guild.get_role(Fractals.roleID)

        try:
            def checkAuthor(message):
                return ctx.author == message.author

            await ctx.message.delete()

            botMessage = await Fractals.sendMessage(
                ctx,
                'Please enter a description for the fractal run.\n\n' \
                'Example: CMs + T4s'
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
                'Example: Today at 7:00 PM CST'
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

            blankRoster = {
                'Healbrand': False, 
                'Alacrigade': False, 
                'DPS1': False, 
                'DPS2': False, 
                'DPS3': False
            }

            blankSpecs = blankRoster

            channel = self.bot.get_channel(Fractals.channelID)
            await channel.send(f'{role.mention}')
            finalMessage = await channel.send(
                embed= await Fractals.createFractalEmbed(
                    embedDescription,
                    embedTime,
                    ctx.author,
                    self.bot,
                    blankRoster,
                    blankSpecs
                )
            )

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
                    'Author ID' : ctx.author.id
                }
            }

            specsDict = {
                str(finalMessage.id): {
                    'Healbrand': False,
                    'Alacrigade': False,
                    'DPS1': False,
                    'DPS2': False,
                    'DPS3' : False
                }
            }

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
                'Cancelled. Take care!'
            )
        except TimeoutError:
            await botMessage.delete(delay=3)
            await Fractals.sendCancelMessage(
                ctx,
                'Sorry, you took too long. Please try again!'
            )

    @staticmethod
    async def sendMessage(ctx, string):
        embed = discord.Embed(
            color = 0x01a8ef,
            description = f"{string}"
        )
        embed.set_thumbnail(
            url='https://i.imgur.com/Dkc5BjH.png'
        )
        embed.set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        )
        embed.set_footer(text="Type 'cancel' to cancel at anytime.")
        msg = await ctx.send(embed=embed)
        return msg

    @staticmethod
    async def sendCancelMessage(ctx, string):
        embed = discord.Embed(
            color = 0x01a8ef,
            description = f"{string}"
        )
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=3)
        return

    @staticmethod
    async def createFractalEmbed(description, time, author, bot, roster, specs, footer=True):
        guild = bot.get_guild(733944519640350771)

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

        embed = discord.Embed(
            color = 0x01a8ef,
            title = f'Fractal Signup: {description}',
            description=f'When: {time}'
        )
        embed.set_thumbnail(
            url='https://i.imgur.com/Dkc5BjH.png'
        )
        embed.set_author(
            name=f'{author}',
            icon_url=f'{author.avatar_url}'
        )
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
    def makeSpecEmbed(bot, specs):
        with open('resources/emojisets.toml', 'r') as f:
            professionEmojiDict = toml.load(f)['Professions']

        spec1, spec2, spec3 = specs

        emojis = []

        for spec in specs:
            emojiID = int(professionEmojiDict[spec])
            emoji = bot.get_emoji(emojiID)
            emojis.append(emoji)

        embed = discord.Embed(
            color = 0x01a8ef,
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
    def makeRoleSelectionEmbed(bot, spec, team):
        if spec == 'Firebrand' and bool(team['Healbrand']) is False:
            options = ['Healbrand', 'DPS']
        elif spec == 'Renegade' and bool(team['Alacrigade']) is False:
            options = ['Alacrigade', 'DPS']
        else:
            options = ['DPS']

        if len(options) > 1:
            embed = discord.Embed(
                color = 0x01a8ef,
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
            tomlDict = toml.load(f)
        with open('resources/emojisets.toml', 'r') as g:
            emojiDict = toml.load(g)
        with open('temporary/fractalteamspecs.toml', 'r') as h:
            specsToml = toml.load(h)
        with open('temporary/fractalembeds.toml', 'r') as g:
            fractalEmbedsDict = toml.load(g)
        
        oldDescription = fractalEmbedsDict[str(messageID)]['Description']
        oldTime = fractalEmbedsDict[str(messageID)]['Time']
        oldMemberID = fractalEmbedsDict[str(messageID)]['Author ID']
        oldMember = await guild.fetch_member(oldMemberID)

        # Retrieves the roster and specs for the given message
        fractalMessageIDs = tomlDict.keys()

        # Ignore any non-relevant reactions
        if str(payload.message_id) not in fractalMessageIDs:
            return
        
        # Removes the reaction immediately.
        channel = self.bot.get_channel(Fractals.channelID)
        message = await channel.fetch_message(messageID)
        await message.remove_reaction(emoji, member)

        teamDict = tomlDict[str(payload.message_id)]
        specsDict = specsToml[str(payload.message_id)]

        # Sets a DM channel with the user, if one doesn't exist.
        if payload.member.dm_channel is None:
            await payload.member.create_dm()
        dmChannel = payload.member.dm_channel 

        # If the user reacted with a core class, initiate the selection process.
        # The user can also react with an "X" icon to remove themselves from the
        # roster, or a wastebasket to scrap the whole post itself.
        if payload.emoji.name in emojiDict['Core'].keys():

            # If the user is already on the roster, ignore it.
            if payload.user_id in list(teamDict.values()):
                embed = discord.Embed(
                    color=0x01a8ef,
                    description='You are already on the roster. Please remove ' \
                        'yourself from the roster and try again.'
                )
                await dmChannel.send(embed=embed)
                return

            # Send a user a message asking them to pick a specialization.
            specsList = Fractals.getSpecs(payload.emoji.name)
            specEmbed = Fractals.makeSpecEmbed(self.bot, specsList)

            await dmChannel.send(embed=specEmbed)
            try:
                response1 = await self.bot.wait_for(
                    'message',
                    timeout=60,
                    check = lambda message: payload.user_id == message.author.id
                )
            except:
                embed = discord.Embed(
                color = 0x01a8ef,
                description = "Sorry, you took too long. Please react again!"
                )
                await dmChannel.send(embed=embed)
                return

            if response1.content.lower() == 'cancel':
                await Fractals.sendCancelMessage(dmChannel, 'Cancelled!')
                return
            elif response1.content.lower() == '1':
                spec = specsList[0]
            elif response1.content.lower() == '2':
                spec = specsList[1]
            elif response1.content.lower() == '3':
                spec = specsList[2]

            # Depending on the specialization, asks the user to pick a role.
            # Default is DPS.
            roleEmbed = Fractals.makeRoleSelectionEmbed(self.bot, spec, teamDict)
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
                    color = 0x01a8ef,
                    description = "Sorry, you took too long. Please react again!"
                    )
                    await channel.send(embed=embed)
                    return
                
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

            # Assigns the user to a role.
            if role == 'DPS':
                if teamDict['DPS1'] is False:
                    role = 'DPS1'
                    teamDict['DPS1'] = payload.user_id
                    specsDict['DPS1'] = spec
                    successEmbed = discord.Embed(
                        color = 0x01a8ef,
                        description = "Sucessfully signed up!"
                    )
                    await dmChannel.send(embed=successEmbed)
                elif teamDict['DPS2'] is False:
                    role = 'DPS2'
                    teamDict['DPS2'] = payload.user_id
                    specsDict['DPS2'] = spec
                    successEmbed = discord.Embed(
                        color = 0x01a8ef,
                        description = "Sucessfully signed up!"
                    )
                    await dmChannel.send(embed=successEmbed)
                elif teamDict['DPS3'] is False:
                    role = 'DPS3'
                    teamDict['DPS3'] = payload.user_id
                    specsDict['DPS3'] = spec
                    successEmbed = discord.Embed(
                        color = 0x01a8ef,
                        description = "Sucessfully signed up!"
                    )
                    await dmChannel.send(embed=successEmbed)
                else:
                    embed = discord.Embed(
                        color = 0x01a8ef,
                        description='There are already enough DPS players. ' \
                            'Please pick a new role or try again later.'
                    )
                    await dmChannel.send(embed=embed)
                    return
            else:
                teamDict[role] = payload.user_id
                successEmbed = discord.Embed(
                    color = 0x01a8ef,
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
                specs = specsDict
            )

            await message.edit(embed=updatedEmbed)
            
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
            
            oldDescription = fractalEmbedsDict[str(messageID)]['Description']
            oldTime = fractalEmbedsDict[str(messageID)]['Time']
            oldMemberID = fractalEmbedsDict[str(messageID)]['Author ID']
            oldMember = await guild.fetch_member(oldMemberID)

            updatedEmbed = await Fractals.createFractalEmbed(
                description = oldDescription,
                time = oldTime,
                author = oldMember,
                bot = self.bot,
                roster = teamDict,
                specs = specsDict
            )

            await message.edit(embed=updatedEmbed)
        elif payload.emoji.name == '🗑️' and payload.member == oldMember:
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
                    color = 0x01a8ef,
                    description = '[Completed]'
                    )
                await message.edit(embed=embed)
                await message.clear_reactions()
            else:
                embed = discord.Embed(
                    color = 0x01a8ef,
                    description = '[Cancelled]'
                    )
                await message.edit(embed=embed)
                await message.clear_reactions()

            tomlDict.pop(str(payload.message_id))
            specsToml.pop(str(payload.message_id))
            fractalEmbedsDict.pop(str(payload.message_id))
        
        # Rewrites the .toml files to finalize any updates.
        with open('temporary/fractalteams.toml', 'w') as f:
            toml.dump(tomlDict, f)
        with open('temporary/fractalteamspecs.toml', 'w') as g:
            toml.dump(specsToml, g)
        with open('temporary/fractalembeds.toml', 'w') as h:
            toml.dump(fractalEmbedsDict, h)       
        
        return

def setup(bot):
    bot.add_cog(Fractals(bot))