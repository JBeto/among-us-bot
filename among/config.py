import os

# Import environment variables
DISCORD_ACCESS_TOKEN = os.environ['DISCORD_ACCESS_TOKEN']

# Redis server FQDN - determined by Docker DNS within docker-compose.yml
REDIS_SERVER = os.environ['REDIS_SERVER']

# Redis server port
REDIS_PORT = int(os.environ['REDIS_PORT'])