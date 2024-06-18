import requests
import sys
import json

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


