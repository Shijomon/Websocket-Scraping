import aiohttp
import asyncio
import json
import websockets
import requests
import re
import base64
import os


async def send_ping(websocket, ping_message):
    await websocket.send(ping_message)
    print("Sent ping message")


async def connect_websocket(uri, ping_message,headers_val):
    async with websockets.connect(uri,extra_headers=headers_val) as websocket:

        await send_ping(websocket, ping_message)
        for x in range(2):
            print(x)
            message = await websocket.recv()
            print(f"Received message: {message}")
      

async def make_http_request(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            resp=response.text
            return resp


async def main():
    ws_uri = 'wss://ws.autorentals.com/async_rates'
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
    mainurl='https://www.autorentals.com/cars/search?location=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&pickupLocation=New%20York%2C%20NY%20(JFK%20-%20New%20York%20City%20-%20John%20F%20Kennedy%20Intl)&dropoffLocation=&oneway=no&pickupDate=20240802&pickupTime=10%3A00&dropoffDate=20240805&dropoffTime=10%3A00&vid=93f42f27-a8a5-45d5-b215-b3046272af35&carGroup=&ar_search_source=1&plid=445&dlid=&pst=A&dst=&pstid=452&dstid='
    response = requests.get(
        mainurl,
        cookies=cookies,
        headers=headers,
    )
    print(response)
    open("myres.html","w").write(response.text)
    searchid=re.search('pageInfo["searchId"] = "(.*?)"',response.text)

    ping_message=f"""SEND
    destination:/app/search.{searchid}
    content-length:31

    start async search for{searchid}"""
#     ping_message="""CONNECT
# accept-version:1.0,1.1,1.2
# heart-beat:40000,40000"""
    headers_val = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.autorentals.com',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Sec-WebSocket-Key': base64.b64encode(os.urandom(16)).decode('utf-8'),
        # 'Sec-WebSocket-Protocol': 'v10.stomp, v11.stomp, v12.stomp',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
    await asyncio.gather(

        connect_websocket(ws_uri, ping_message,headers_val),make_http_request(mainurl,headers))

if __name__ == "__main__":
    asyncio.run(main())

