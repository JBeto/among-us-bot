import discord
from discord.ext import commands
import among.config as config

# Setup intents
intents = discord.Intents.none()
intents.guilds = True
intents.messages = True

# Display help menu
HELP_DESCRIPTION = """
```
Among Us Discord bot to automate muting/unmuting and showing game maps.

Commands:
  - !among mute    # Mute everyone in voice channel w/ same name & category
  - !among meet    # Unmute everyone in voice channel w/ same name & category
  - !among skeld   # Show Skeld game map and connected vents/paths
  - !among mira    # Show Mira HQ game map and connected vents/paths
  - !among polus   # Show Polus game map and connected vents/paths
```
"""

# Setup bot
bot = commands.Bot(command_prefix='!', description=HELP_DESCRIPTION, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {} w/ ID: {}'.format(bot.user.name, bot.user.id))

@bot.group()
async def among(ctx):
    """Among Us Discord bot base command."""
    if ctx.invoked_subcommand is None:
        # By default, display help menu if command is invalid
        await ctx.send(HELP_DESCRIPTION)

def _get_corresponding_voice_channel(ctx):
    name = ctx.channel.name
    category = ctx.channel.category
    if category is None: # Search in guild for voice_channel
        return next((x for x in ctx.guild.voice_channels if x.name == name), None)
    else: # Search in respective category
        return next((x for x in category.voice_channels if x.name == name), None)

@among.command(name='mute')
async def _mute(ctx):
    """Mute everyone in corresponding voice channel."""
    voice_channel = _get_corresponding_voice_channel(ctx)
    if voice_channel is None:
        await ctx.send("Dunno which channel to mute! Make sure there's a voice channel w/ the same name and category as this text channel.")
    else:
        for m in voice_channel.members:
            await m.edit(reason="Managing Among Us - muting", mute=True)

@among.command(name='meet')
async def _meet(ctx):
    """Unmute everyone in corresponding voice channel."""
    voice_channel = _get_corresponding_voice_channel(ctx)
    if voice_channel is None:
        await ctx.send("Dunno which channel to unmute! Make sure there's a voice channel w/ the same name and category as this text channel.")
    else:
        for m in voice_channel.members:
            await m.edit(reason="Managing Among Us - unmuting", mute=False)

async def _show_map(ctx, name):
    with open(name, 'rb') as fp:
        async with ctx.typing():
            await ctx.send(file=discord.File(fp))

@among.command(name='skeld')
async def _skeld(ctx):
    """Show Skeld game map."""
    await _show_map(ctx, 'assets/skeld.jpg')

@among.command(name='mira')
async def _mira(ctx):
    """Show Mira HQ game map."""
    await _show_map(ctx, 'assets/mira-hq.jpg')

@among.command(name='polus')
async def _polus(ctx):
    """Show Polus game map."""
    await _show_map(ctx, 'assets/polus.jpg')

bot.run(config.DISCORD_ACCESS_TOKEN)