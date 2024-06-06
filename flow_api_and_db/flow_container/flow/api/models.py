from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	email = models.EmailField()
	password = models.CharField(max_length=50)
	avatar = models.ImageField(upload_to='api/static/avatars/')
	friendList = models.ManyToManyField('self', blank=True)
	matches = models.ManyToManyField('Match', blank=True)

class Match(models.Model):
	matchId = models.IntegerField()
	matchName = models.CharField(max_length=50)
	matchDate = models.DateTimeField()
	matchWinner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='match_winner')
	matchLoser = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True, related_name='match_loser')
	matchWinnerScore = models.IntegerField()
	matchLoserScore = models.IntegerField()
