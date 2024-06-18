from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
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

##### ADMIN PURGE OF USERS. NOT IN PRODUCTION #####

def purgeallusers_view(request):
	if request.user.is_authenticated:
		if (request.method == 'DELETE'):
			try:
				User.objects.all().delete()
				return HttpResponse('All users purged', status=200)
			except:
				return HttpResponse('User purge failed', status=500)
		else:
			return HttpResponse('Method not allowed', status=405)
	else:
		return HttpResponse('Unauthorized', status=401)



##### LOGIN AND LOGOUT ENDPOINTS #####

@csrf_exempt
def login_view(request):
	if (request.method == 'POST'):
		try:
			data = json.loads(request.body)
			loginUsername = data.get('username')
			loginPassword = data.get('password')
			user = authenticate(request, username=loginUsername, password=loginPassword)
			if user is not None:
				login(request, user)
				request.session['username'] = loginUsername
				request.session.save()
				return HttpResponse('Login successful', status=200)
			else:
				return HttpResponse('Login failed', status=401)
		except:
			return HttpResponse('Internal Server Error', status=500)
	else:
		return HttpResponse('Method not allowed', status=405)


def logout_view(request):
	try:
		logout(request)
		Session.objects.filter(session_key=request.session.session_key).delete()
		return HttpResponse('Logout successful', status=200)
	except: 
		return HttpResponse('Logout failed', status=500)


##### AVATAR ENDPOINT #####

def avatar_view(request):
	if request.user.is_authenticated:
		if (request.method == 'GET'): ##get avatar
			try:
				getUsername = request.GET.get('username')
				user = Account.objects.get(user__username=getUsername)
				usrAvatar = user.avatar
				return HttpResponse(usrAvatar, status=200)
			except Exception as e:
				return HttpResponse(e, status=404)
		if (request.method == 'POST'): #change avatar. NOT WORKING YET
			try:
				data = request.body
				toChangeUsername = data.POST.get('username')
				user = Account.objects.get(user__username=toChangeUsername)
				user.avatar = data.FILES['avatar']
				user.save()
				return HttpResponse('Avatar changed', status=200)
			except Exception as e:
				return HttpResponse(e, status=500)
		else:
			return HttpResponse('Method not allowed', status=405)
	else:
		return HttpResponse('Unauthorized', status=401)



##### FRIEND ENDPOINT #####

def friend_view(request):
	if request.user.is_authenticated:
		if (request.method == 'POST'): ##add friend
			try:
				data = json.loads(request.body)
				toAddUsername = data.get('username')
				friendUsername = data.get('friendUsername')
				user = Account.objects.get(user__username=toAddUsername)
				friend = Account.objects.get(user__username=friendUsername)
				user.friendList.add(friend)
				return HttpResponse('Friend added', status=200)
			except Exception as e:
				return HttpResponse(e, status=500)
		if (request.method == 'DELETE'): ##delete friend from list
			try:
				data = json.loads(request.body)
				toDeleteUsername = data.get('username')
				friendUsername = data.get('friendUsername')
				user = Account.objects.get(user__username=toDeleteUsername)
				friend = Account.objects.get(user__username=friendUsername)
				user.friendList.remove(friend)
				return HttpResponse('Friend deleted', status=200)
			except Exception as e:
				return HttpResponse(e, status=500)
		else:
			return HttpResponse('Method not allowed', status=405)
	else:
		return HttpResponse('Unauthorized', status=401)


##### USER ENDPOINT #####

def user_view(request):
	if (request.method == 'POST'): ##create user
		try:
			data = json.loads(request.body)
			avatar = 'api/static/avatars/default.png'
			toSetUsername = data.get('username')
			toSetEmail = data.get('email')
			toSetPassword = data.get('password')
			newUser = User.objects.create_user(toSetUsername, toSetEmail, toSetPassword)
			newUser.save()
			newAccount = Account(
				user= newUser,
				avatar= avatar
			)
			newAccount.save()
			return HttpResponse('User created', status=201)
		except Exception as e:
			print(e)
			return HttpResponse(e, status=500)
	if request.user.is_authenticated:
		if (request.method == 'GET'): ##get user data
			try:
				getUsername = request.GET.get('username')
				currentAccount = Account.objects.get(user__username=getUsername)
				try:
					allFriends = user.friendList.all()
				except:
					allFriends = []
				allFriendsUsernames = []
				for friend in allFriends:
					allFriendsUsernames.append(friend.user.username)
				userData = {
					'username': currentAccount.user.username,
					'email': currentAccount.user.email,
					'avatar_url': '/api/avatar?username=' + currentAccount.user.username,
					'friends': allFriendsUsernames,
				}
				return HttpResponse(json.dumps(userData), status=200)
			except Exception as e:
				print(e)
				return HttpResponse('User not found', status=404)
		if (request.method == 'DELETE'): ##delete user
			try:
				data = json.loads(request.body)
				deleteUsername = data.get('username')
				user = User.objects.get(user__username=deleteUsername)
				user.delete()
				return HttpResponse('User deleted', status=200)
			except:
				return HttpResponse('User not found', status=404)
		if (request.method == 'PUT'): ##change user password
			try:
				data = json.loads(request.body)
				toChangeUsername = data.get('username')
				account = User.objects.get(username=toChangeUsername)
				if (data.get('password') != None):
					account.user.set_password(data.get('password'))
					account.user.save()
				return HttpResponse('User updated', status=200)
			except Exception as e:
				return HttpResponse(e, status=500)
		else:
			return HttpResponse('Method not allowed', status=405)
	else:
		return HttpResponse('Unauthorized', status=401)
