from django.db import models

# Create your models here.
class OngoingMatch(models.Model):
	roomId = models.CharField(max_length=200)
	playerCount = models.IntegerField(default=1)
	ready = models.BooleanField(default=False)

	player1 = models.CharField(max_length=200)
	player2 = models.CharField(max_length=200)

	player1Paddle_y = models.FloatField(default=0)
	player2Paddle_y = models.FloatField(default=0)

	goalsPlayer1 = models.IntegerField(default=0)
	goalsPlayer2 = models.IntegerField(default=0)

	ball_x = models.FloatField(default=0)
	ball_y = models.FloatField(default=0)