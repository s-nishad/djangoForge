import asyncio
import websockets
import json

# Replace with your server URL and JWT token
other_user_id = "9ecb9f7f762a473a9e21b9084d936fba"
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyNjY5MzM0LCJpYXQiOjE3NjI2NjU3MzUsImp0aSI6Ijk1NWY1OGMxYTAyMDQwNWZhMWNiOGJjMzAzN2YzYjM2IiwidXNlcl9pZCI6IjllY2I5ZjdmNzYyYTQ3M2E5ZTIxYjkwODRkOTM2ZmJhIn0.RN0Chs4470ON1CYZR8YEx8iQELnWmr07kjIYeTgmOT8"

# WS URL with token as query param
ws_url = f"ws://localhost:8000/ws/chat/{other_user_id}/?token={jwt_token}"

async def test_chat():
    try:
        async with websockets.connect(ws_url) as ws:
            print("✅ Connected to WebSocket!")

            # Send a test message
            await ws.send(json.dumps({"message": "Hello from Python test!"}))
            print("Message sent!")

            # Wait to receive messages
            while True:
                response = await ws.recv()
                data = json.loads(response)
                print("Received:", data)

    except Exception as e:
        print("❌ Error:", e)

asyncio.run(test_chat())
