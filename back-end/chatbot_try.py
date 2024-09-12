import asyncio
import websockets
import json

async def chatbot_client():
    uri = "ws://127.0.0.1:8000/ai/chatbot"  # Adjust the URL if your server is running on a different address or port
    session_id = None

    async with websockets.connect(uri) as websocket:
        print("Connected to the chatbot. Type your messages and press Enter. Type 'exit' to quit.")

        # Receive the initial session ID from the server
        response = await websocket.recv()
        if response.startswith("SESSION_ID:"):
            session_id = response.split(":", 1)[1]
            print(f"Received session ID: {session_id}")
        
        while True:
            message = input("You: ")
            
            if message.lower() == 'exit':
                print("Exiting the chatbot.")
                break
            
            if session_id:
                # If we have a session ID, send it with the message
                payload = {
                    "session_id": session_id,
                    "message": message,
                }
                await websocket.send(json.dumps(payload))
            
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(chatbot_client())