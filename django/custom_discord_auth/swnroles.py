import requests

try:
    from django.conf import settings
    from django.contrib.auth.models import User, Group
except: #Running as a script... so gross
    import sys, os, django
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, '..')
    if path not in sys.path:
        sys.path.append(path)    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acre.settings")
    django.setup()
    from django.conf import settings
    from django.contrib.auth.models import User, Group

# Setting up as a class so I can do things later like error handling
# and automatic recovery in the background... but for now super simple
class SWNRole(object):
    base_url = "https://swnbot.itmebot.com/api/user/"
    timeout = 10.0  # Timeout time in seconds

    def __init__(self, uid, user=None):
        self.uid = uid
        self.user = user
        self.role_data = None

        self.headers = {
            'Authorization': settings.SWN_BOT_API,
        }
        
        self.url = self.base_url + uid

    def handle_error(self, r):
        print ("SWNRole error: ", r.status_code)
        print (r.headers)
        print (r.text)
        
        """
        returns 403 if theres and auth failure,
        returns 500 if theres an internal issue with the API,
        returns 404 if nothing is found,
        """


    def pull_data(self):
        
        try:
            r = requests.get(self.url, timeout=self.timeout, headers= self.headers)
        except requests.exeptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        
        status = r.status_code
        
        if status == 200:
            pass
        else:
            self.handle_error(r)
            return None

        self.role_data = r.json()
        return r.json()
        
    def update_user(self, user=None):
        if user:
            self.user = user
            
        if not self.user:
            import pprint
            pprint.pprint(self.role_data)
            return False
 
        if self.role_data:
            self.user.nickname.nick_name = self.role_data['userNick']
            #user.username = extra_data.json()['username']+"#"+extra_data.json()['discriminator'] # No idea why this changes....
            
            # First we wipe it clean
            self.user.groups.clear()
            # And then add the groups back in
            for role in self.role_data['userRoles']:
                group, created = Group.objects.get_or_create(name=role['roleName'])
                self.user.groups.add(group)
            self.user.save()
            
            return True


if __name__ == "__main__":
    # Grab all the stuff that comes default normally
    
    print ("swnroles")
    test = SWNRole("84403892799930368")
    print (test.pull_data())
    