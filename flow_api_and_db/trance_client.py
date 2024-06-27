import requests
import sys
import json

client = requests.Session()

############# BASIC DEMONSTRATION OF API USAGE #############

## get index and csrf token will be set
print("\n\n #### GET INDEX ####")
response = client.get("http://localhost:8000")
print(response.text)

## Call create user to make first user
print("\n\n #### CREATE USER ####")
response = client.post("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "email": "linus@broms.fi", "password": "testi"}))
print(response.text)

## Call login to get session id
print("\n\n #### LOGIN ####")
response = client.post("http://localhost:8000/api/login", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "password": "testi"}))
print(response.text)
print(client.cookies)

## Call get user to get user data
print("\n\n #### GET USER ####")
response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

## call create user to make a friend
print("\n\n #### CREATE FRIEND ####")
response = client.post("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testifriend", "email": "firend@gmail.com", "password": "testi"}))
print(response.text)

## call add friend to add friend
print("\n\n #### ADD FRIEND ####")
response = client.post("http://localhost:8000/api/friend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testi", "friendUsername": "testifriend"}))
print(response.text)

## call get user to get user data
print("\n\n #### GET USER ####")
response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##call delete friend to delete friend
print("\n\n #### DELETE FRIEND ####")
response = client.delete("http://localhost:8000/api/friend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testi", "friendUsername": "testifriend"}))
print(response.text)

## call get user to see that friend got deleted
print("\n\n #### GET USER ####")
response = client.get("http://localhost:8000/api/user?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

## call delete user to delete user
print("\n\n #### DELETE USER ####")
response = client.delete("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"username": "testifriend"}))
print(response.text)

## call get user to see that user got deleted
print("\n\n #### GET USER ####")
response = client.get("http://localhost:8000/api/user?username=testifriend", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##call logout to logout
print("\n\n #### LOGOUT ####")
response = client.post("http://localhost:8000/api/logout", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

##print all cookies to see that session id got deleted and logout worked
print("#### COOKIES ####")
print(client.cookies)

##call login again to get access to user
print("\n\n #### LOGIN ####")
response = client.post("http://localhost:8000/api/login", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testi", "password": "testi"}))
print(response.text)

## call get avatar to get users avatar
print("\n\n #### GET AVATAR ####")
response = client.get("http://localhost:8000/api/avatar?username=testi", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
with open("avatar.png", "wb") as f:
	f.write(response.content)
print("avatar.png saved.")

## call create user to make user to send message to
print("\n\n #### CREATE RECEIVER ####")
response = client.post("http://localhost:8000/api/user", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"]}, data=json.dumps({"username": "testreceiver", "email": "receiver@gmail.com", "password": "testi"}))
print(response.text)

## call send message to send message to user
print("\n\n #### SEND MESSAGE ####")
response = client.post("http://localhost:8000/api/send/message", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]}, data=json.dumps({"sender": "testi", "receiver": "testreceiver" , "content": "Hello"}))
print(response.text)

## call get messages to get messages send by this user
print("\n\n #### GET MESSAGES ####")
response = client.get("http://localhost:8000/api/send/message?username=testi&receiver=testreceiver", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)

## Call purge to delete all users
print("\n\n #### PURGE ALL USERS ####")
response = client.delete("http://localhost:8000/api/purgeallusers", headers={"Content-Type": "application/json", "X-CSRFToken": client.cookies["csrftoken"], "session-id": client.cookies["sessionid"]})
print(response.text)






print("\n\n")
