import discord
import toml
from discord.ext import commands

class Food(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    with open('resources/ascended_food.toml', 'r') as f:
        mainTomlDict = toml.load(f)

    @staticmethod
    def embedMessage(string):
        if string.startswith('http'):
            embed = discord.Embed(color=0x01a8ef)
            embed.set_image(url=string)
        else:
            embed = discord.Embed(description=string, color=0x01a8ef)
        return embed

    @commands.command()
    async def food(self, ctx, profession, statType, *, role=None):
        try:
            profession = profession.lower()
            stat = statType.lower()
            if role is not None:
                if len(role.split()) == 1:
                    role = role.lower()
                else:
                    raise ValueError
        except:
            embed = Food.embedMessage('Invalid input. Please try again!')
            await ctx.send(embed=embed)
            return

        food1 = None
        food2 = None
        food3 = None
        food4 = None

        if profession in ['chrono', 'chronomancer']:
            chronoDict = Food.mainTomlDict['Mesmer']['Chronomancer']
            if stat in ['power']:
                chronoDict = chronoDict['Power']
                if role in ['dps']:
                    food1 = chronoDict['DPS']['Primary']
                    food2 = chronoDict['DPS']['Secondary']
                elif role in ['boon']:
                    # DPS
                    food1 = chronoDict['Boon']['Primary']
                    food2 = chronoDict['Boon']['Secondary']

                    # Boon Duration
                    food3 = chronoDict['Boon']['Tertiary']
                    food4 = chronoDict['Boon']['Quartiary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Power Chrono requires an additional "role" argument. Please try again! \n\n' \
                        'Example: !food chrono power boon , !food chrono power dps'
                        )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Invalid role for Power Chrono. Please try again!'
                    )
                    await ctx.send(embed=embed)
                    return
            elif stat in ['condi', 'condition']:
                chronoDict = chronoDict['Condition']
                if role in ['tank']:
                    food1 = chronoDict['Tank']['Primary']
                elif role in ['dps']:
                    food1 = chronoDict['DPS']['Primary']
                    food2 = chronoDict['DPS']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Condition Chrono requires an additional "role" argument. Please try again! \n\n' \
                        'Example: !food chrono condi dps , !food chrono condi tank'
                        )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Invalid role for COndition Chrono. Please try again!'
                    )
                    await ctx.send(embed=embed)
                    return
        elif profession in ['mirage']:
            mirageDict = Food.mainTomlDict['Mesmer']['Mirage']
            if stat in ['condi']:
                food1 = mirageDict['Condition']['Primary']
                food2 = mirageDict['Condition']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for Mirage. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['tempest']:
            tempestDict = Food.mainTomlDict['Elementalist']['Tempest']
            if stat in ['power']:
                food1 = tempestDict['Power']['Primary']
                food2 = tempestDict['Power']['Secondary']
            elif stat in ['condi', 'condition']:
                food1 = tempestDict['Condition']['Primary']
                food2 = tempestDict['Condition']['Secondary']
            elif stat in ['heal', 'healing', 'healer']:
                food1 = tempestDict['Heal']['Primary']
            else:     
                embed = Food.embedMessage(
                    'Invalid stat type for Tempest. Please try again!'
                )
                await ctx.send(embed=embed)
                return   
        elif profession in ['weaver']:
            foodDict = Food.mainTomlDict['Elementalist']['Weaver']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            elif stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['reaper']:
            foodDict = Food.mainTomlDict['Necromancer']['Reaper']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['scourge']:
            foodDict = Food.mainTomlDict['Necromancer']['Scourge']
            if stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            elif stat in ['heal', 'healing', 'healer']:
                food1 = foodDict['Heal']['Primary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['engineer', 'eng']:
            foodDict = Food.mainTomlDict['Engineer']['Engineer']
            if stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['holosmith', 'hs']:
            foodDict = Food.mainTomlDict['Engineer']['Holosmith']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['scrapper']:
            foodDict = Food.mainTomlDict['Engineer']['Scrapper']
            if stat in ['heal', 'healing', 'healer']:
                food1 = foodDict['Heal']['Primary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['druid']:
            foodDict = Food.mainTomlDict['Ranger']['Druid']
            if stat in ['heal', 'healer', 'healing']:
                food1 = foodDict['Heal']['Primary']
            elif stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['soulbeast', 'sb']:
            foodDict = Food.mainTomlDict['Ranger']['Soulbeast']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            elif stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            elif stat in ['handkite', 'handkiter', 'hk']:
                food1 = foodDict['Handkite']['Primary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['thief']:
            foodDict = Food.mainTomlDict['Thief']['Thief']
            if stat in ['power']:
                if role in ['boon']:
                    food1 = foodDict['Power']['Boon']['Primary']
                    food2 = foodDict['Power']['Boon']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for Thief. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for thief. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['daredevil', 'dd']:
            foodDict = Food.mainTomlDict['Thief']['Daredevil']
            if stat in ['power']:
                if role in ['dps']:
                    food1 = foodDict['Power']['DPS']['Primary']
                    food2 = foodDict['Power']['DPS']['Secondary']
                elif role in ['boon']:
                    food1 = foodDict['Power']['Boon']['Primary']
                    food2 = foodDict['Power']['Boon']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['deadeye', 'de']:
            foodDict = Food.mainTomlDict['Thief']['Deadeye']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['guardian', 'guard']:
            foodDict = Food.mainTomlDict['Guardian']['Guardian']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['dragonhunter', 'dh']:
            foodDict = Food.mainTomlDict['Guardian']['Dragonhunter']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['firebrand', 'fb']:
            foodDict = Food.mainTomlDict['Guardian']['Firebrand']
            if stat in ['condition', 'condi']:
                if role in ['quickness', 'quick', 'boon']:
                    food1 = foodDict['Condition']['Boon']['Primary']
                elif role in ['dps']:
                    food1 = foodDict['Condition']['DPS']['Primary']
                    food2 = foodDict['Condition']['DPS']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed =Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['herald']:
            foodDict = Food.mainTomlDict['Revenant']['Herald']
            if stat in ['power']:
                if role in ['boon']:
                    food1 = foodDict['Power']['Boon']['Primary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            elif stat in ['handkite', 'handkiter', 'hk']:
                food1 = foodDict['Handkite']['Primary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['renegade', 'ren']:
            foodDict = Food.mainTomlDict['Revenant']['Renegade']
            if stat in ['power']:
                if role in ['alac', 'alacrity', 'alacrigade', 'boon']:
                    food1 = foodDict['Power']['Boon']['Primary']
                    food2 = foodDict['Power']['Boon']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            elif stat in ['condi', 'condition']:
                food1 = foodDict['Condition']['Primary']
                food2 = foodDict['Condition']['Secondary']
            elif stat in ['healing', 'healer', 'heal']:
                food1 = foodDict['Heal']['Primary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['berserker', 'zerker', 'zerk']:
            foodDict = Food.mainTomlDict['Warrior']['Berserker']
            if stat in ['power']:
                if role in ['banners', 'boon', 'banner']:
                    food1 = foodDict['Power']['Boon']['Primary']
                    food2 = foodDict['Power']['Boon']['Secondary']
                elif role in ['dps']:
                    food1 = foodDict['Power']['DPS']['Primary']
                    food2 = foodDict['Power']['DPS']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            elif stat in ['condi', 'condition']:
                if role in ['banners', 'boon', 'banner']:
                    food1 = foodDict['Condition']['Boon']['Primary']
                    food2 = foodDict['Condition']['Boon']['Secondary']
                elif role in ['dps']:
                    food1 = foodDict['Condition']['DPS']['Primary']
                    food2 = foodDict['Condition']['DPS']['Secondary']
                elif role is None:
                    embed = Food.embedMessage(
                        'Invalid role for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = Food.embedMessage(
                        'Role required for this profession. Please try again.'
                    )
                    await ctx.send(embed=embed)
                    return
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        elif profession in ['spellbreaker']:
            foodDict = Food.mainTomlDict['Warrior']['Spellbreaker']
            if stat in ['power']:
                food1 = foodDict['Power']['Primary']
                food2 = foodDict['Power']['Secondary']
            else:
                embed = Food.embedMessage(
                    'Invalid stat type for this profession. Please try again!'
                )
                await ctx.send(embed=embed)
                return
        else:
            embed = Food.embedMessage(
                'Invalid profession. Please try again!'
            )
            await ctx.send(embed=embed)
            return

        foodEmbed = discord.Embed(
            title=f"Optimal Food"
        )
        foodEmbed.set_thumbnail(
            url='https://i.imgur.com/1BEj2FF.png'
        )
        foodEmbed.add_field(
            name = 'Primary Food',
            value = f"[{food1['name']}]({food1['link']})",
            inline=True
        )
        if food2 is not None:
            foodEmbed.add_field(
                name = 'Benching Food',
                value = f"[{food2['name']}]({food2['link']})",
                inline = True
            )
            if food3 is not None and food4 is not None:
                foodEmbed.add_field(
                name = 'Primary Boon Food',
                value = f"[{food3['name']}]({food3['link']})",
                inline = False
            )
                foodEmbed.add_field(
                name = 'Benching Boon Food',
                value = f"[{food4['name']}]({food4['link']})",
                inline = False
            )
        else:
            foodEmbed.add_field(
                name = 'Benching Food',
                value = 'N/A',
                inline = True
            )
        
        await ctx.send(embed=foodEmbed)
        return



def setup(bot):
    bot.add_cog(Food(bot))