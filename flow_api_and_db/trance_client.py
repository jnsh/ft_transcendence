import requests
import json

def call_create_user():
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/createuser",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": json.dumps({
			"username": "testi",
			"email": "linus@broms.fi",
			"password": "testi"
		})
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=request["body"])
	print(response.text)

def call_login():
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/login",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": {
			"username": "testi",
			"password": "testi"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]))
	print(response.text)

def purge_all_users():
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/purgeallusers",
		"headers": {
			"Content-Type": "application/json"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"])
	print(response.text)

def delete_user():
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/deleteuser",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": {
			"username": "testi"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]))
	print(response.text)

def get_user():
	request = {
		"method": "GET",
		"url": "http://localhost:8000/api/getuser?username=testi",
		"headers": {
			"Content-Type": "application/json"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"])
	print(response.text)
	return response.json()["avatar_url"]

def get_avatar(avatar_url):
	print("tryinf url: " + avatar_url)
	request = {
		"method": "GET",
		"url": "http://localhost:8000" + avatar_url,
		"headers": {
			"Content-Type": "application/json"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"])
	with open("avatar.png", "wb") as f:
		f.write(response.content)
	print("avatar.png saved.")

def call_create_friend_user():
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/createuser",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": {
			"username": "testifriend",
			"email": "friend@gmail.com",
			"password": "testi"
			}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]))
	print(response.text)

def add_friend():
	request = {
		"method": "POST",
		"url": "http://localhost:8000/api/friend",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": {
			"username": "testi",
			"friendUsername": "testifriend"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]))
	print(response.text)

def delete_friend():
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/friend",
		"headers": {
			"Content-Type": "application/json"
		},
		"body": {
			"username": "testi",
			"friendUsername": "testifriend"
		}
	}
	response = requests.request(request["method"], request["url"], headers=request["headers"], data=json.dumps(request["body"]))
	print(response.text)

def test_create_login_purge():
	call_create_user()
	call_login()
	purge_all_users()

def test_create_get_delete():
	call_create_user()
	avatar_url = get_user()
	get_avatar(avatar_url)
	delete_user()

def test_create_addFriend_getUser():
	call_create_user()
	call_create_friend_user()
	add_friend()
	get_user()
	delete_friend()
	get_user()
	purge_all_users()

test_create_login_purge()
test_create_get_delete()
test_create_addFriend_getUser()

