import asyncio
import websockets
import json
import ssl
import certifi

async def chatbot_client(token):
    uri = f"wss://localhost:8000/ai/chatbot?token={token}"
    session_id = None

    # Create an SSL context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # If using a self-signed certificate for development, uncomment the following lines:
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
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
                
                payload = {
                    "session_id": session_id,
                    "message": message,
                }
                await websocket.send(json.dumps(payload))
                
                response = await websocket.recv()
                print(f"Chatbot: {response}")

    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 401:
            print("Authentication failed. Please check your token.")
        else:
            print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(chatbot_client("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNzI2MjU1NTc0fQ.3hl4q3suf6SubkqR5vLKsSP-9nEISzQCnk7JQwy-LhE"))