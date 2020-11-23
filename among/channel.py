import discord
import asyncio
import logging

logger = logging.getLogger(__name__)

async def _create_basic_text_role(name, guild):
    # Set discord permissions explictly instead of using bitmask directly
    permissions = discord.Permissions(
        read_messages=True,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        mention_everyone=True,
        external_emojis=True,
        add_reactions=True
    )
    return await guild.create_role(name=name, permissions=permissions)

async def _create_private_text_channel(name, guild, allowed_role, category):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        allowed_role: discord.PermissionOverwrite(read_messages=True)
    }
    return await guild.create_text_channel(name=name, overwrites=overwrites, category=category)

class VoiceAndTextChannel:
    def __init__(self, voice_channel, role, text_channel):
        self._voice_channel = voice_channel
        self._role = role
        self._text_channel = text_channel

    @classmethod
    async def create(cls, voice_channel):
        # Construct associated private text channel
        voice_channel = voice_channel
        role = await _create_basic_text_role(name='Vat-role-{}'.format(voice_channel.name), guild=voice_channel.guild)
        text_channel = await _create_private_text_channel(name=voice_channel.name,
            guild=voice_channel.guild, allowed_role=role, category=voice_channel.category)

        # Send friendly reminder of temporary channel
        message = await text_channel.send('**Reminder:** This chat is temporary and will be deleted once the last person leaves!')
        await message.pin()

        # Return constructed voice and text channel
        logger.info('Created voice-n-text channel w/ voice_id: {}, role_id: {}, text_id: {}.'
            .format(voice_channel.id, role.id, text_channel.id))
        return VoiceAndTextChannel(voice_channel, role, text_channel)

    async def add_member(self, member):
        logger.info('Adding member (id: {}) to voice-n-text channel w/ voice_id: {}.'.format(member.id, self.voice_id))
        await member.add_roles(self._role)

    async def remove_member(self, member):
        logger.info('Removing member (id: {}) to voice-n-text channel w/ voice_id: {}.'.format(member.id, self.voice_id))
        await member.remove_roles(self._role)

    async def delete(self):
        logger.info('Deleting voice-n-text channel w/ voice_id: {}.'.format(self.voice_id))
        await self._role.delete()
        await self._text_channel.delete()

    @property
    def voice_id(self):
        return self._voice_channel.id

    @property
    def role_id(self):
        return self._role.id

    @property
    def text_id(self):
        return self._text_channel.id