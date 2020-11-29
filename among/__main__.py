import discord
from discord.ext import commands
import among.config as config

# Setup intents
intents = discord.Intents.none()
intents.voice_states = True
intents.guilds = True
intents.messages = True

# Display help menu
HELP_DESCRIPTION = """
```
Among Us Discord bot to automate muting/unmuting and showing game maps.

Commands:
  - !among mute    # Mute everyone in same voice channel
  - !among meet    # Unmute everyone in same voice channel
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

@among.command(name='mute')
async def _mute(ctx):
    """Mute everyone in corresponding voice channel."""
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if voice_channel is None:
        print('No voice channel to mute')
        await ctx.send("Dunno which channel to mute. Make sure you're in a voice channel.")
    else:
        print('Muting everyone in voice channel: {}'.format(voice_channel))
        for m in voice_channel.members:
            await m.edit(reason="Managing Among Us - muting", mute=True)
        await ctx.send("Muting everyone in the voice channel. Run `!among meet` to un-mute.")

@among.command(name='meet')
async def _meet(ctx):
    """Unmute everyone in corresponding voice channel."""
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None
    if voice_channel is None:
        print('No voice channel to un-mute')
        await ctx.send("Dunno which channel to un-mute. Make sure you're in a voice channel.")
    else:
        print('Un-muting everyone in voice channel: {}'.format(voice_channel))
        for m in voice_channel.members:
            await m.edit(reason="Managing Among Us - unmuting", mute=False)
        await ctx.send("Talking is allowed again.")

async def _show_map(ctx, name):
    print('Showing map: {}'.format(name))
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