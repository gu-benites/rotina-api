import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import json

timeout = ClientTimeout(total=30)

async def crawl(url, session):
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a')
            absolute_links = []
            for link in links:
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    if '#' not in absolute_url:
                        absolute_links.append(absolute_url)
            return absolute_links
    except asyncio.TimeoutError:
        print(f"Request timed out for URL: {url}. Discarding and continuing...")
        return []

# Additional functions...
