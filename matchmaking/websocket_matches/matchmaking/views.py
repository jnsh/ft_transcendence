from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import OngoingMatch
from datetime import datetime
import random
import os
import json

# Create your views here.

def generateId():
	print("Generating ID")
	time = datetime.now().timestamp()
	ret = str(time).replace(".", "-") + '-' + str(random.randint(0, 1000)) + str(random.randint(0, 1000))
	return ret

@csrf_exempt
def initiatematch_view(request):
	try:
		if (request.method == 'POST'):
			data = json.loads(request.body)
			if (data["secret"] == os.environ.get("MATCHMAKING_SECRET", "default_secret")):
				# check if there is a match to connect to
				toConnectTo = OngoingMatch.objects.filter(ready=False)
				if (len(toConnectTo) > 0):
					match = toConnectTo[0]
					match.player2 = data["username"]
					match.ready = True
					match.save()
					return HttpResponse(json.dumps({"status": "success", "game_room": match.roomId, "ready": True}), status=200)
				else:
					generatedId = generateId()
					newMatch = OngoingMatch(player1=data["username"])
					newMatch.roomId = generatedId
					newMatch.save()
					return HttpResponse(json.dumps({"status": "success", "game_room": newMatch.roomId, "ready": False}), status=200)
			else:
				return HttpResponse("Unauthorized", status=401)
		else:
			return HttpResponse('Method not allowed', status=405)
	except Exception as e:
		return HttpResponse("error: " + str(e), status=500)
