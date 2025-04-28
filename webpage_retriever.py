import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
visited = set()

async def extract_links(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return [urljoin(url, a.get('href')) for a in soup.find_all('a') if a.get('href')]
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return []

async def recursive_crawl(url, delay=1):  # Be nice to the server
    if url in visited:
        return
    
    if 'dfrobot' not in url:
        logging.info(f"Skipping URL without keyword: {url}")
        return
    
    visited.add(url)
    logging.info(f"Processing: {url}")
    links = await extract_links(url)
    for link in links:
        await asyncio.sleep(delay)  # Be nice to the server
        await recursive_crawl(link)

if __name__ == "__main__":
    start_url = "https://www.dfrobot.com.cn/"
    logging.info(f"Starting crawl at {start_url}")
    asyncio.run(recursive_crawl(start_url))
    
    # Save links to a file
    with open('links.txt', 'w') as f:
        for link in visited:
            f.write(link + '\n')
    
    logging.info(f"Crawl completed. {len(visited)} links found.")
