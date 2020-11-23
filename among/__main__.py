import discord
import logging
from vat.client import VatClient
import vat.config as config

# Set up logging as part of module
FORMAT = '%(asctime)-s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Setup Intents to only listen to voice events
    intents = discord.Intents.none()
    intents.guilds = True
    intents.voice_states = True

    # Run the client
    print('VatClient is starting.')
    client = VatClient(intents=intents)
    client.run(config.DISCORD_ACCESS_TOKEN)

if __name__ == '__main__':
    main()