import asyncio
import websockets
from time import sleep

async def connect_and_send(uri):
    async with websockets.connect(uri) as websocket:
        # Get user input
        while True:
            key_press = input("Enter 'up' or 'down': ")
            if key_press not in ("up", "down"):
                print("Invalid key. Please enter 'up' or 'down'.")
                continue  # Skip sending if invalid input

            # Send the key press to the server
            await websocket.send(f'{{"key": "{key_press}"}}')

            # Receive a response (optional)
            response = await websocket.recv()
            print(f"Received from server: {response}")

# Replace with your actual WebSocket server URL
uri = "ws://localhost:8000/match/connect/" + "1719341143-458415-628681"
asyncio.run(connect_and_send(uri))