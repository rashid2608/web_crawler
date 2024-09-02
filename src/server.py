import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from aiohttp import web, ClientConnectorError, TooManyRedirects, ClientResponseError
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self):
        self.visited = set()

    async def crawl(self, url):
        logger.info(f"Starting crawl of {url}")
        domain = urlparse(url).netloc
        sitemap = await self._crawl(url, domain)
        return self._format_sitemap(sitemap, domain)

    async def _crawl(self, url, domain, depth=0, max_retries=3):
        if url in self.visited or urlparse(url).netloc != domain:
            return {}

        logger.debug(f"Crawling {url} at depth {depth}")
        self.visited.add(url)
        sitemap = {url: {}}

        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            logger.debug(f"Successfully fetched {url}")
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            links = soup.find_all('a', href=True)
                            logger.debug(f"Found {len(links)} links on {url}")
                            tasks = []
                            for link in links:
                                href = urljoin(url, link['href'])
                                if href.startswith('http') and urlparse(href).netloc == domain:
                                    logger.debug(f"Queueing {href} for crawling")
                                    tasks.append(self._crawl(href, domain, depth + 1))
                            results = await asyncio.gather(*tasks, return_exceptions=True)
                            for result in results:
                                if isinstance(result, dict):
                                    sitemap[url].update(result)
                            return sitemap
                        else:
                            logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
            except (ClientConnectorError, TooManyRedirects, ClientResponseError, asyncio.TimeoutError) as e:
                logger.error(f"Error crawling {url}: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying in {wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Max retries reached for {url}")
            except Exception as e:
                logger.error(f"Unexpected error crawling {url}: {str(e)}")
                break

            await asyncio.sleep(1)  # Add a small delay between requests

        return sitemap

    def _format_sitemap(self, sitemap, domain):
        def _format_recursive(url, subpages, indent=""):
            path = urlparse(url).path
            if path == "":
                path = "/"
            result = f"{indent}- {path}\n"
            for sub_url, sub_subpages in subpages.items():
                result += _format_recursive(sub_url, sub_subpages, indent + "  ")
            return result

        result = f"{domain}\n"
        for url, subpages in sitemap.items():
            result += _format_recursive(url, subpages)
        return result

async def handle_crawl(request):
    url = request.query.get('url')
    if not url:
        return web.Response(text="Please provide a URL to crawl", status=400)
    
    logger.info(f"Received crawl request for {url}")
    crawler = Crawler()
    sitemap = await crawler.crawl(url)
    logger.info("Crawl completed")
    return web.Response(text=sitemap)

async def health_check(request):
    return web.Response(text="Healthy")

async def ready_check(request):
    # Add any additional readiness checks here
    return web.Response(text="Ready")

app = web.Application()
app.router.add_get('/crawl', handle_crawl)
app.router.add_get('/health', health_check)
app.router.add_get('/ready', ready_check)

if __name__ == '__main__':
    web.run_app(app, port=8080)