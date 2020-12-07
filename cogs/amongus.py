from discord.ext import commands
from discord.ext.commands import BucketType
import json, random, discord, asyncio, config

# conversation data
with open("./data/possibilities.json", "r") as f:
    possibilities = json.load(f)
    player_red = possibilities['Red']
    player_orange = possibilities['Orange']
    player_yellow = possibilities['Yellow']
    player_java = possibilities['Green']
    player_html = possibilities['Blue']

def get_message(player: str):
    if player == 'Red':
        msg = random.choice(player_red)
    elif player == 'Orange':
        msg = random.choice(player_orange)
    elif player == 'Yellow':
        msg = random.choice(player_yellow)
    elif player == 'Green':
        msg = random.choice(player_java)
    elif player == 'Blue':
        msg = random.choice(player_html)
    else:
        msg = "player not found"
        print(msg)
    return msg


# emoji data
emojis = {
    "Red": "🔴",
    "Orange": "🟠",
    "Yellow": "🟡",
    "Green": "🟢",
    "Blue": "🔵"
}

#configuration
server_id = config.server_id


# getting a quick embed!
def get_embed(_title, _description, _color):
    return discord.Embed(title=_title, description=_description, color=_color)

# getting random colors for embeds, pretty cool
def RandomColour():
    return random.randint(1048576, 0xFFFFFF)


class AmongUs(commands.Cog):
    """
    - Reactions based 'Among US'(an online multiplayer social deduction by American game studio Innersloth) game with programming languages as imposters and crewmates.
    """
    def __init__(self, bot):
        self.bot = bot
        self.home_server = server_id

    @commands.command(name="AmongUs", aliases=['Among_Us', 'among_us', 'amongus', 'Amongus'])
    @commands.cooldown(rate=1, per=120, type=BucketType.user)
    async def among_us(self, ctx):
        """
        - Reactions based 'Among US' game with programming languages as imposters and crewmates.
        The main point is to find the imposter.
        Impostors can sabotage the reactor, 
        which gives Crew mates 30–45 seconds to resolve the sabotage.
        If it is not resolved in the allotted time, The Impostor will win.
        """
        # message management
        cached_messages = []

        await ctx.trigger_typing()
        guild = discord.utils.get(self.bot.guilds, id=self.home_server)

        async def _send(e: discord.Embed):
            # sending the message
            return await ctx.send(embed=e)

        # Welcome
        embed1 = get_embed("Welcome to Among Us!", "Find out who the imposter is, before the reactor melts down!", _color=RandomColour())
        embed1.set_image(url="https://i.ibb.co/3y0rNFC/welcome-screen.png")
        _msg = await _send(embed1)

        # for cleaning purposes
        cached_messages.append(_msg)

        # conversation. color=randint(0, 0xFFFFFF)
        for item, value in emojis.items():
            await ctx.trigger_typing()
            await asyncio.sleep(random.randrange(1, 5))
            embed = get_embed('{0} {1}'.format(await guild.fetch_emoji(value), item), get_message(item), _color=RandomColour())
            _msg = await _send(embed)

            # for cleaning purposes
            cached_messages.append(_msg)
        
        # question.
        await asyncio.sleep(1)
        embed = get_embed('Who might be the imposter? ', "**vote below**", discord.Color.blue())
        embed.set_image(url="https://i.ibb.co/2SZ67mW/amongus.jpg")
        msg = await _send(embed)

        # for cleaning purposes
        cached_messages.append(msg)


        # who is the real imposter?
        imposter = random.choice(list(emojis.items()))
        # accessing the name.
        imposter = imposter[0]

        # to see the id use: imp_id = imposter[1]
        # print the imposter name to console, for test purposes.
        print(imposter)

        # adding choices
        try:
            # this will be successfull if your server has these emojis
            for emoji in emojis.values():
                await msg.add_reaction(await guild.fetch_emoji(emoji))
        except:
            # you need to assign emoji IDs in ./data/emojis.json
            ctx.send("I think i'm missing `external emojis` permissions")
            return
        
        # a simple check, whether reacted emoji is in given choices.
        def check(reaction, user):
            self.reacted = reaction.emoji.id
            return user == ctx.author and str(reaction.emoji.id) in emojis.values()

        # waiting for the reaction to proceed
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

        except asyncio.TimeoutError:
            # reactor meltdown - defeat
            description = "Reactor Meltdown. \n**{0}** was the imposter...".format(imposter)
            embed = get_embed("Defeat", description, discord.Color.red())
            embed.set_image(url="https://i.ibb.co/tY6HTR8/image.png")
            
            await ctx.send(embed=embed)
        else:
            # victory
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = get_embed("Victory", description, discord.Color.blue())
                embed.set_image(url="https://i.ibb.co/S5XpXkb/image.png")
                
                await ctx.send(embed=embed)

            # defeat
            else:
                for key, value in emojis.items():
                    if value == str(self.reacted):
                        description = "It wasn't poor **{0}**...\nThe Imposter was **{1}**".format(key, imposter)
                        embed = get_embed("Defeat", description, discord.Color.red())
                        embed.set_image(url="https://i.ibb.co/tY6HTR8/image.png")
                        
                        await ctx.send(embed=embed)
                        break
        
        # cleaning up trash
        for m in cached_messages:
            await m.delete()
    @among_us.error
    async def among_us_error(self, ctx, error):
        


def setup(bot):
    bot.add_cog(AmongUs(bot))
