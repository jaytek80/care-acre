import requests

from custom_discord_auth.provider import CustomDiscordProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from django.conf import settings

class DiscordOAuth2Adapter(OAuth2Adapter):
    provider_id = CustomDiscordProvider.id
    access_token_url = 'https://discordapp.com/api/oauth2/token'
    authorize_url = 'https://discordapp.com/api/oauth2/authorize'
    profile_url = 'https://discordapp.com/api/users/@me'

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            'Authorization': 'Bearer {0}'.format(token.token),
            'Content-Type': 'application/json',
        }
        extra_data = requests.get(self.profile_url, headers=headers)

        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )


oauth2_login = OAuth2LoginView.adapter_view(DiscordOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DiscordOAuth2Adapter)
