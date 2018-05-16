from django.db import models

# Create your models here.
class NickName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField("Nick Name", max_length=1024, blank=True, default='')

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.user.username


class Preferential(models.Model):
    position
    winners
    candidate[s]

class Candidate(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Ranking(models.Model):
    race
    candidate
    rank

class Ballot(models.Model):
    poll
    user
    ranking[s]

