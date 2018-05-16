# We don't actually need any models, but this is a good place to put stuff that futzes with them
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount

from custom_discord_auth.swnroles import SWNRole

# This is a hack to get nice long ass nicknames from the discord channel to show up
class NickName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField("Nick Name", max_length=1024, blank=True, default='')

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        NickName.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #print("save_user_profile")
    try: 
        instance.nickname.save()
    except:
        NickName.objects.create(user=instance)


# This is a quick and dirty hack to keep usernames pure and have the nickname plug into the first_name field to be displayed
def get_nick_name(self):
    name = ""
    try:
        name = self.nickname.nick_name
    except:
        print ("creating nickname for", self.username)
        nickname = NickName.objects.create(user=self)
        nickname.save()
        name = self.username
    return name

User.add_to_class("__str__", get_nick_name)



# Spruce up the displayed name and also toss in some groups
@receiver(user_logged_in)
def add_discord_metadata(sender, **kwargs):
    user = kwargs['user']
    sociallogin = kwargs['sociallogin']
    uid = sociallogin.account.uid
    
    # Hook into external API to get roles goes here
    roles = SWNRole(uid)
    has_roles = roles.pull_data()
    if has_roles:
        roles.update_user(user)
