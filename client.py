import aiohttp
import asyncio

async def crawl_url(url):
    async with aiohttp.ClientSession() as session:
        params = {'url': url}
        async with session.get('http://localhost:8080/crawl', params=params) as response:
            if response.status == 200:
                sitemap = await response.text()
                print(sitemap.strip())  # Remove any leading/trailing whitespace
            else:
                print(f"Error: {response.status}")
                print(await response.text())

async def main():
    url = input("Enter the URL to crawl: ")
    await crawl_url(url)

if __name__ == '__main__':
    asyncio.run(main())