import aiohttp
import asyncio


async def fetch_character(session, url):
    async with session.get(url) as response:
        return await response.json()
    


async def fetch_all_characters():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1,100): #We suggest that there are nor more than 100 personages
            url = f'https://swapi.dev/api/people/{i}/'
            tasks.append(fetch_character(session, url))
        return await asyncio.gather(*tasks)
