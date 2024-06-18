import requests
import sys
import json

def call_create_user(token):
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/user",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": json.dumps({
			"username": "testi",
			"email": "linus@broms.fi",
			"password": "testi"
		})
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=request["body"], cookies=request["cookies"])
	print(response.text)

def call_login(token):
	client = requests.session()
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/login",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": {
			"username": "testi",
			"password": "testi"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]), cookies=request["cookies"])
	print(response.text)
	sessionId = client.get(request["url"]).cookies['sessionid']
	return sessionId

def purge_all_users(token, auth):
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/purgeallusers",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token,
			"Authorization": auth
		},
		"cookies": {
			"csrftoken": token
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], cookies=request["cookies"])
	print(response.text)

def delete_user(token):
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/user",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": {
			"username": "testi"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"], cookies=request["cookies"]))
	print(response.text)

def get_user(token):
	request = {
		"method": "GET",
		"url": "http://localhost:8000/api/user?username=testi",
		"cookies": {
			"csrftoken": token
		},
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], cookies=request["cookies"])
	print(response.text)
	return response.json()["avatar_url"]

def get_avatar(avatar_url):
	print("tryinf url: " + avatar_url)
	request = {
		"method": "GET",
		"url": "http://localhost:8000" + avatar_url,
		"cookies": {
			"csrftoken": token
		},
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], cookies=request["cookies"])
	with open("avatar.png", "wb") as f:
		f.write(response.content)
	print("avatar.png saved.")

def call_create_friend_user(token):
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/user",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": {
			"username": "testifriend",
			"email": "friend@gmail.com",
			"password": "testi"
			}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]), cookies=request["cookies"])
	print(response.text)

def add_friend(token):
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/friend",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": {
			"username": "testi",
			"friendUsername": "testifriend"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]), cookies=request["cookies"])
	print(response.text)

def delete_friend(token):
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/friend",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
		},
		"cookies": {
			"csrftoken": token
		},
		"body": {
			"username": "testi",
			"friendUsername": "testifriend"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]), cookies=request["cookies"])
	print(response.text)



client = requests.Session()

############# BASIC DEMONSTRATION OF API USAGE #############

## get index and csrf token will be set
response = client.get("http://localhost:8000")
print(response.text)

## Call create user to make first user
response = client.post("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "email": "linus@broms.fi", "password": "testi"}))
print(response.text)

## Call login to get session id
response = client.post("http://localhost:8000/api/login", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "password": "testi"}))
print(response.text)
print(client.cookies)

## Call get user to get user data
response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

## call create user to make a friend
response = client.post("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testifriend", "email": "firend@gmail.com", "password": "testi"}))
print(response.text)

## call add friend to add friend
response = client.post("http://localhost:8000/api/friend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testi", "friendUsername": "testifriend"}))
print(response.text)

## call get user to get user data

response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##call delete friend to delete friend
response = client.delete("http://localhost:8000/api/friend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testi", "friendUsername": "testifriend"}))
print(response.text)

## call get user to see that friend got deleted
response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

## call delete user to delete user
response = client.delete("http://localhost:8000/api/user?username=testifriend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testifriend"}))
print(response.text)

## call get user to see that user got deleted
response = client.get("http://localhost:8000/api/user?username=testifriend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##call logout to logout
response = client.post("http://localhost:8000/api/logout", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##print all cookies to see that session id got deleted and logout worked
print(client.cookies)

##call login again to get access to user
response = client.post("http://localhost:8000/api/login", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "password": "testi"}))
print(response.text)

## call get avatar to get users avatar
response = client.get("http://localhost:8000/api/avatar?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
with open("avatar.png", "wb") as f:
	f.write(response.content)
print("avatar.png saved.")

## Call purge to delete all users
response = client.delete("http://localhost:8000/api/purgeallusers", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)


