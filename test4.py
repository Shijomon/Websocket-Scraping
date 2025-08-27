import asyncio
import websockets
import base64
import os
import requests
import logging
import re

logging.basicConfig(level=logging.DEBUG)

async def connect_and_send_message():
    websocket_url = 'wss://ws.autorentals.com/async_rates'

    # Make an initial HTTP request to establish a session
    initial_url = 'https://www.autorentals.com'
    session = requests.Session()
    initial_response = session.get(initial_url)
    cookies = session.cookies.get_dict()

    logging.debug("Initial response cookies: %s", cookies)

    # Generate dynamic WebSocket key
    sec_websocket_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    sec_websocket_key='qCSYofb+eKiD6ZDiHnTl8g=='
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.autorentals.com',
        'Accept-Language': 'en-US,en;q=0.7',
        'Sec-WebSocket-Key': sec_websocket_key,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    }

    logging.debug("WebSocket headers: %s", headers)

    async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
        logging.debug("Opened connection")
        cookies = {
            'datadome': 'QazLVenCgeRCJTpQ4ogj6TKI1Bvzix~ACKAB5MARFmFw5hIe36gnEZgiKvlr5UTAeyZm1L6U3c9QxaHdF~hUCl1r9gLuwTjEjzQLfAFPrHxqIw8QKXvU412jopGgy9ZC',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-device-memory': '8',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.126", "Google Chrome";v="126.0.6478.126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        response = requests.get(
            'https://www.autorentals.com/cars/search?location=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&pickupLocation=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&dropoffLocation=&oneway=no&pickupDate=20240802&pickupTime=10%3A00&dropoffDate=20240805&dropoffTime=10%3A00&vid=93f42f27-a8a5-45d5-b215-b3046272af35&carGroup=&ar_search_source=1&plid=445&dlid=&pst=A&dst=&pstid=452&dstid=',
            cookies=cookies,
            headers=headers,
        )
        print(response)
        open("myres.html","w").write(response.text)
        searchid = re.search('pageInfo\["searchId"\] = "(.*?)"', response.text).group(1)
        print(searchid)
        message1  = (
            "CONNECT\n"
            "accept-version:1.0,1.1,1.2\n"
            "heart-beat:40000,40000\n"
            "\n"  
        )
        await websocket.send(message1)
        message2=()
        await websocket.send()
        logging.debug("Sent message: %s", message1)

        # Continuous loop to receive messages
        try:
            while True:
                response = await websocket.recv()
                logging.debug("Received response: %s", response)
        except websockets.ConnectionClosed:
            logging.debug("Connection closed")

asyncio.run(connect_and_send_message())
