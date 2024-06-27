import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from .models import OngoingMatch
from asgiref.sync import sync_to_async
from time import sleep
import asyncio
channel_layer = get_channel_layer()

class MatchConsumer(AsyncWebsocketConsumer):

	role = 0

#### CONNECT AND DISCONNECT WEBSOCKETS ####

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['game_room']
		self.room_group_name = 'match_%s' % self.room_name
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()
		theMatchObject = await sync_to_async(OngoingMatch.objects.get)(roomId=self.room_name)
		if (theMatchObject.ready == True):
			await self.initiate_start_match()
		self.role = theMatchObject.playerCount
		theMatchObject.playerCount += 1
		await sync_to_async(theMatchObject.save)()
		self.current_match = theMatchObject
		self.game_loop_task = asyncio.create_task(self.listen_data())

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		self.game_loop_task.cancel()


#### RECEIVE KEY PRESSES ####

	async def receive(self, text_data): # handle key presses up and down
		data = json.loads(text_data)
		if (data['key'] == 'up' or data['key'] == 'down'):
			theMatchObject = self.current_match
			if (self.role == 1):
				if (data['key'] == 'up'):
					theMatchObject.player1Paddle_y -= 0.1
				else:
					theMatchObject.player1Paddle_y += 0.1
			else:
				if (data['key'] == 'up'):
					theMatchObject.player2Paddle_y -= 0.1
				else:
					theMatchObject.player2Paddle_y += 0.1
			await sync_to_async(theMatchObject.save)()


#### RADIO ELEMENT POSITIONS TO CLIENTS ####

	async def listen_data(self):
		while True:
			theMatchObject = self.current_match
			await self.send(json.dumps({
				'player1Paddle_y': theMatchObject.player1Paddle_y,
				'player2Paddle_y': theMatchObject.player2Paddle_y,
				'ball_x': theMatchObject.ball_x,
				'ball_y': theMatchObject.ball_y,
				'goalsPlayer1': theMatchObject.goalsPlayer1,
				'goalsPlayer2': theMatchObject.goalsPlayer2
			}))
			await sleep(0.1)


#### INITIATE GAME SESSION ####

	async def initiate_start_match(self): ## this calls the start_match function below in all client instances
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'start_match'
			}
		)

	async def start_match(self, event):
		await self.send(json.dumps({
			'start': True
		}))
