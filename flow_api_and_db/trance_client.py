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

def purge_all_users(token):
	request = {
		"method": "DELETE",
		"url": "http://localhost:8000/api/purgeallusers",
		"headers": {
			"Content-Type": "application/json",
			"X-CSRFToken": token
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

def test_create_login_purge(token):
	call_create_user(token)
	call_login(token)
	purge_all_users(token)

def test_create_get_delete(token):
	call_create_user(token)
	avatar_url = get_user(token)
	get_avatar(avatar_url, token)
	delete_user(token)

def test_create_addFriend_getUser(token):
	call_create_user(token)
	call_create_friend_user(token)
	add_friend(token)
	get_user(token)
	delete_friend(token)
	get_user(token)
	purge_all_users(token)

def get_csrftoken():
	client = requests.session()
	request = {
		"method": "GET",
		"url": "http://localhost:8000/",
	}
	token = client.get(request["url"]).cookies['csrftoken']
	print(token)
	return token

token = get_csrftoken()

test_create_login_purge(token)
test_create_get_delete(token)
test_create_addFriend_getUser(token)

