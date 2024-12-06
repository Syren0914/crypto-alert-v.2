import json
import websocket

# WebSocket API Testnet endpoint
socket = "wss://testnet.binance.vision/ws-api/v3"

# Callback for incoming messages
def on_message(ws, message):
    message = json.loads(message)
    print("Received:", message)

# Callback for when the connection is opened
def on_open(ws):
    # Correct format for the 'ticker.price' method
    request = {
        "id": 1,  # Unique identifier for this request
        "method": "ticker.price",
        "params": {"symbol": "BTCUSDT"}  # Use a dictionary here
    }
    ws.send(json.dumps(request))
    print("Request sent:", request)


# Callback for errors
def on_error(ws, error):
    print("Error:", error)

# Initialize and run WebSocket connection
ws = websocket.WebSocketApp(
    socket,
    on_message=on_message,
    on_open=on_open,
    on_error=on_error
)
ws.run_forever()
