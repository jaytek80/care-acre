from allauth.socialaccount.providers.discord.provider import DiscordProvider
from custom_discord_auth.provider import CustomDiscordProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns


#urlpatterns = default_urlpatterns(DiscordProvider)
urlpatterns = default_urlpatterns(CustomDiscordProvider)