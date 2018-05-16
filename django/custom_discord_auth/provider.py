import requests

from allauth.socialaccount.providers.discord.provider import DiscordProvider
from django.contrib.auth.models import Group
from django.conf import settings

# Takes in less oath data than normal and also hits an api hook to grab group/role information
class CustomDiscordProvider(DiscordProvider):
    id = "custom_discord"
    name = 'Custom Discord'

    def extract_common_fields(self, data):
        return dict(
            #email=data.get('email'),
            username=data.get('username')+"#"+data.get('discriminator'),
            name=data.get('username'),
        )

    def get_default_scope(self):
        return ['identify']


provider_classes = [CustomDiscordProvider]
