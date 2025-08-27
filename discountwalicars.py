import aiohttp
import asyncio
import json
import websockets


async def send_ping(websocket, ping_message):
    await websocket.send(json.dumps(ping_message))
    print("Sent ping message")


async def connect_websocket(uri, ping_message):
    async with websockets.connect(uri) as websocket:
        await send_ping(websocket, ping_message)
        for x in range(2):
            message = await websocket.recv()
            print(f"Received message: {message}")
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            message_mode=json.loads(message)
            if 'data' in message_mode:
                mydata=json.loads(message_mode['data'])
                if 'search' in mydata:
                    if 'complete' in mydata['search']:
                        if mydata['search']['complete']:
                            break


async def make_http_request(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            resp=await response.json()
            return resp


async def main():
    headers = {
        'authority': 'hub.discountusacarrental.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en;q=0.5',
        'content-type': 'application/json; charset=utf-8',
        'origin': 'https://www.discounthawaiicarrental.com',
        'referer': 'https://www.discounthawaiicarrental.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-no-redirect': 'true',
    }

    params = {'site_id': '58'}

    init_url = 'https://hub.discountusacarrental.com/api/init/?site_id=58'
    response = await make_http_request(init_url, headers)
    pusher_channel = response['init']['pusher_channel']
    sinc=response['init']['sinc']
    ping_message = {"event": "pusher:subscribe",
                    "data": {"auth": "", "channel": pusher_channel}}

    ws_uri = 'wss://ws-mt1.pusher.com/app/071472a623a5da61a72d?protocol=7&client=js&version=8.0.1&flash=false'
    headers = {
        'authority': 'hub.discountusacarrental.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en;q=0.5',
        'content-type': 'application/json',
        'origin': 'https://www.discounthawaiicarrental.com',
        'referer': 'https://www.discounthawaiicarrental.com/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-no-redirect': 'true',
        'x-sinc': sinc,
    }
    await asyncio.gather(

        connect_websocket(ws_uri, ping_message),
        make_http_request('https://hub.discountusacarrental.com/api/search/?location=Honolulu%20International%20Airport%2C%20HI%20(HNL)&pickup_date_time=2024-09-22T09:00:00.000&return_date_time=2024-09-23T09:00:00.000&country_of_residence=IN&pickuplocation=Honolulu%20International%20Airport%2C%20HI%20(HNL)&country=IN', headers)
    )

if __name__ == "__main__":
    asyncio.run(main())

