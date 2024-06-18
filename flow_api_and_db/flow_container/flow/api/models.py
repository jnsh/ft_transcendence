from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='api/static/avatars/')
	friendList = models.ManyToManyField('self', blank=True)
	matches = models.ManyToManyField('Match', blank=True)

	def __str__(self):
		return self.user.username

class Match(models.Model):
	matchId = models.IntegerField()
	matchName = models.CharField(max_length=50)
	matchDate = models.DateTimeField()
	matchWinner = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=False, null=True, related_name='match_winner')
	matchLoser = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=False, null=True, related_name='match_loser')
	matchWinnerScore = models.IntegerField()
	matchLoserScore = models.IntegerField()

class Message(models.Model):
	messageId = models.IntegerField()
	messageContent = models.CharField(max_length=500)
	messageSender = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False, null=False, related_name='message_sender')
	messageReceiver = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False, null=False, related_name='message_receiver')
	messageDate = models.DateTimeField()


