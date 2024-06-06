from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User
import requests
import json

#non functioning/test endpoints
def henriika(request):
	return HttpResponse('Hello, Henriika!')

def makesoc(request):
	if (request.method == 'GET'):
		matchmakingUrl = 'http://matcher:8001/matchmaking'
		matchmakerResponse = requests.post(matchmakingUrl + '/getready', data=request)
		if (matchmakerResponse.status_code == 200):
			return redirect(matchmakingUrl + '/connect')
		else:
			return HttpResponse('Matchmaker is not available', status=503)
	else:
		return HttpResponse('Method not allowed', status=405)
	








#Functioning endpoints

@csrf_exempt
def purgeallusers(request):
	if (request.method == 'DELETE'):
		try:
			User.objects.all().delete()
			return HttpResponse('All users purged', status=200)
		except:
			return HttpResponse('User purge failed', status=500)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def deleteuser(request):
	if (request.method == 'DELETE'):
		try:
			data = json.loads(request.body)
			deleteUsername = data.get('username')
			user = User.objects.get(username=deleteUsername)
			user.delete()
			return HttpResponse('User deleted', status=200)
		except:
			return HttpResponse('User not found', status=404)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def createuser(request):
	if (request.method == 'POST'):
		try:
			data = json.loads(request.body)
			if (data.get('avatar') == None):
				avatar = 'api/static/avatars/default.png'
			else:
				avatar = data.get('avatar')
			user = User(
				username= data.get('username'),
				email= data.get('email'),
				password= data.get('password'),
				avatar= avatar
			)
			user.save()
			return HttpResponse('User created', status=201)
		except Exception as e:
			print(e)
			return HttpResponse('User creation failed', status=500)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def login(request):
	if (request.method == 'POST'):
		try:
			data = json.loads(request.body)
			loginUsername = data.get('username')
			loginPassword = data.get('password')
			user = User.objects.get(username=loginUsername, password=loginPassword)
			#Generate access token. Will be used to access any other endpoints
			return HttpResponse('Login successful: this will be a token later xD', status=200)
		except:
			return HttpResponse('Login failed', status=401)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def avatar(request):
	if (request.method == 'GET'):
		try:
			getUsername = request.GET.get('username')
			user = User.objects.get(username=getUsername)
			usrAvatar = user.avatar
			return HttpResponse(usrAvatar, status=200)
		except Exception as e:
			print(e)
			return HttpResponse('Avatar not found', status=404)
	if (request.method == 'POST'): #change avatar. NOT WORKING YET
		try:
			data = request.body
			toChangeUsername = data.POST.get('username')
			user = User.objects.get(username=toChangeUsername)
			user.avatar = data.FILES['avatar']
			user.save()
			return HttpResponse('Avatar changed', status=200)
		except Exception as e:
			print(e)
			return HttpResponse('Avatar not changed', status=500)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def friend(request): #delete friend
	if (request.method == 'POST'):
		try:
			data = json.loads(request.body)
			toAddUsername = data.get('username')
			friendUsername = data.get('friendUsername')
			user = User.objects.get(username=toAddUsername)
			friend = User.objects.get(username=friendUsername)
			user.friendList.add(friend)
			return HttpResponse('Friend added', status=200)
		except Exception as e:
			print(e)
			return HttpResponse('Friend not added', status=500)
	if (request.method == 'DELETE'):
		try:
			data = json.loads(request.body)
			toDeleteUsername = data.get('username')
			friendUsername = data.get('friendUsername')
			user = User.objects.get(username=toDeleteUsername)
			friend = User.objects.get(username=friendUsername)
			user.friendList.remove(friend)
			return HttpResponse('Friend deleted', status=200)
		except Exception as e:
			print(e)
			return HttpResponse('Friend not deleted', status=500)
	else:
		return HttpResponse('Method not allowed', status=405)

@csrf_exempt
def getuser(request):
	if (request.method == 'GET'):
		try:
			getUsername = request.GET.get('username')
			user = User.objects.get(username=getUsername)
			allFriends = user.friendList.all()
			allFriendsUsernames = []
			for friend in allFriends:
				allFriendsUsernames.append(friend.username)
			userData = {
				'username': user.username,
				'email': user.email,
				'avatar_url': '/api/avatar?username=' + user.username,
				'friends': allFriendsUsernames,
			}
			return HttpResponse(json.dumps(userData), status=200)
		except Exception as e:
			print(e)
			return HttpResponse('User not found', status=404)
	else:
		return HttpResponse('Method not allowed', status=405)
