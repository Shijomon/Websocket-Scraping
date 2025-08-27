import aiohttp
import asyncio
import json
import websockets
import logging
# from car_support import supply
import os
import re
import base64

logging.basicConfig(level=logging.DEBUG)

class hawai():
    def __init__(self):
        print("working")
        # super().__init__()

    async def send_ping(self, websocket, ping_message):
        await websocket.send(ping_message)
        logging.debug("Sent message: %s", ping_message)

    async def connect_websocket(self, uri, ping_message):
        sec_websocket_key = 'PvBzJK4Ald1pu7n9/358aA=='
        headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://www.autorentals.com',
            'Accept-Language': 'en-US,en;q=0.7',
            'Sec-WebSocket-Key': sec_websocket_key,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Cookie': 'datadome=QazLVenCgeRCJTpQ4ogj6TKI1Bvzix~ACKAB5MARFmFw5hIe36gnEZgiKvlr5UTAeyZm1L6U3c9QxaHdF~hUCl1r9gLuwTjEjzQLfAFPrHxqIw8QKXvU412jopGgy9ZC'
        }

        async with websockets.connect(uri, extra_headers=headers) as websocket:
            await self.send_ping(websocket, ping_message)
            messages = []
            # try:
            while True:
                message = await websocket.recv()
                logging.debug("Received message: %s", message)
                messages.append(message)
            # except websockets.exceptions.ConnectionClosed:
            #     logging.debug("WebSocket connection closed")
            # return messages

    async def make_http_request(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()

    async def load(self, search_url):
        ws_uri = 'wss://ws.autorentals.com/async_rates'
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
        response = await self.make_http_request(search_url, headers)
        # logging.debug("HTTP response: %s", response)
        
        searchid_match = re.search(r'pageInfo\["searchId"\] = "(.*?)"', response)
        if not searchid_match:
            logging.error("Search ID not found in response")
            return
        
        searchid = searchid_match.group(1)
        logging.debug("Search ID: %s", searchid)
        
        message=f"""SEND
destination:/app/search.{searchid}
content-length:31

start async search for{searchid}"""
        
        resps = await asyncio.gather(
            self.connect_websocket(ws_uri, message),
            self.make_http_request(search_url, headers),
        )
        return resps[0]

    def main(self):
        search_url = "https://www.autorentals.com/cars/search?location=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&pickupLocation=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&dropoffLocation=&oneway=no&pickupDate=20240802&pickupTime=10%3A00&dropoffDate=20240805&dropoffTime=10%3A00&vid=93f42f27-a8a5-45d5-b215-b3046272af35&carGroup=&ar_search_source=1&plid=445&dlid=&pst=A&dst=&pstid=452&dstid="
        resps = asyncio.run(self.load(search_url))
        print(json.dumps(resps, indent=4))


if __name__ == "__main__":
    obj = hawai()
    obj.main()

