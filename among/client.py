import discord
import asyncio
import redis
import logging
import vat.config as config
from vat.channel import VoiceAndTextChannel

logger = logging.getLogger(__name__)

def _is_mute_or_deafen_event(before_voice_state, after_voice_state):
    return before_voice_state.channel == after_voice_state.channel

def _is_leaving_voice_and_text_channel(before_voice_state):
    return not (before_voice_state.channel is None or before_voice_state.afk)

def _is_entering_voice_and_text_channel(after_voice_state):
    return not (after_voice_state.channel is None or after_voice_state.afk)

def _should_create_voice_and_text_channel(after_voice_state):
    if after_voice_state.channel is None or after_voice_state.afk:
        return False
    return len(after_voice_state.channel.members) == 1

def _should_delete_voice_and_text_channel(before_voice_state):
    if before_voice_state.channel is None or before_voice_state.afk:
        return False
    return not before_voice_state.channel.members

class VatClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._redis = redis.Redis(config.REDIS_SERVER, config.REDIS_PORT, encoding="utf-8", decode_responses=True)

    def _get_voice_and_text_channel(self, voice_channel):
        # Deserialize the voice and text channel from Redis database
        id_dict = self._redis.hgetall(voice_channel.id)
        role = voice_channel.guild.get_role(int(id_dict['role_id']))
        text_channel = self.get_channel(int(id_dict['text_channel_id']))
        logger.debug('Retrieved entry from Redis: key={}, values={}.'.format(voice_channel.id, id_dict))
        return VoiceAndTextChannel(voice_channel, role, text_channel)

    async def _add_voice_and_text_channel(self, voice_channel):
        voice_and_text_channel = await VoiceAndTextChannel.create(voice_channel)
        # Serialize the voice and text channel into Redis database for storage
        id_dict = {'text_channel_id': voice_and_text_channel.text_id, 'role_id': voice_and_text_channel.role_id}
        logger.debug('Attempting to add entry to Redis: key={}, values={}.'.format(voice_and_text_channel.voice_id, id_dict))
        self._redis.hmset(voice_and_text_channel.voice_id, id_dict)
        logger.info('Successfully added voice-n-text channel w/ name: {}, voice_id: {}'.format(voice_channel.name, voice_channel.id))
        return voice_and_text_channel

    async def _remove_voice_and_text_channel(self, voice_channel):
        voice_and_text_channel = self._get_voice_and_text_channel(voice_channel)
        logger.debug('Attempting to remove entry from Redis: key={}.'.format(voice_and_text_channel.voice_id))
        keys = ['role_id', 'text_channel_id']
        self._redis.hdel(voice_channel.id, *keys)
        await voice_and_text_channel.delete()
        logger.info('Successfully deleted voice-n-text channel w/ name: {}, voice_id: {}'.format(voice_channel.name, voice_channel.id))

    async def on_voice_state_update(self, member, before, after):
        # If mute/deafen event, we ignore
        if _is_mute_or_deafen_event(before, after):
            logger.info('Detected mute/deafen event - ignoring.')
            return

        # Destroy/leave voice and text channel
        if _should_delete_voice_and_text_channel(before):
            await self._remove_voice_and_text_channel(before.channel)

        elif _is_leaving_voice_and_text_channel(before):
            voice_and_text_channel = self._get_voice_and_text_channel(before.channel)
            await voice_and_text_channel.remove_member(member)

        # Create/enter voice and text channel
        if _should_create_voice_and_text_channel(after):
            voice_and_text_channel = await self._add_voice_and_text_channel(after.channel)
            await voice_and_text_channel.add_member(member)
        elif _is_entering_voice_and_text_channel(after):
            voice_and_text_channel = self._get_voice_and_text_channel(before.channel)
            await voice_and_text_channel.add_member(member)