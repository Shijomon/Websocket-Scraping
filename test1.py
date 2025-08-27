# import requests

# headers = {
#     'Pragma': 'no-cache',
#     'Origin': 'https://www.autorentals.com',
#     'Accept-Language': 'en-GB,en;q=0.8',
#     'Sec-WebSocket-Key': 'qCSYofb+eKiD6ZDiHnTl8g==',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Upgrade': 'websocket',
#     'Cache-Control': 'no-cache',
#     'Sec-WebSocket-Protocol': 'v10.stomp, v11.stomp, v12.stomp',
#     'Connection': 'Upgrade',
#     'Sec-WebSocket-Version': '13',
#     'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
# }

# response = requests.get('wss://ws.autorentals.com/async_rates', headers=headers)

import asyncio
import websockets

async def connect_websocket():
    uri = 'wss://ws.autorentals.com/async_rates'
    
    # WebSocket headers
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.autorentals.com',
        'Accept-Language': 'en-GB,en;q=0.8',
        'Sec-WebSocket-Key': 'qCSYofb+eKiD6ZDiHnTl8g==',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Upgrade': 'websocket',
        'Cache-Control': 'no-cache',
        'Sec-WebSocket-Protocol': 'v10.stomp, v11.stomp, v12.stomp',
        'Connection': 'Upgrade',
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    }
    
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # Send a message or perform actions here
        await websocket.send('DISCONNECT receipt:close-2')
        
        # Receive a response
        response = await websocket.recv()
        print(response)

# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_websocket())
