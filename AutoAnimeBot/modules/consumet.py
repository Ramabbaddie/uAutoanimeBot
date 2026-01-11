import aiohttp
import logging
from config import CONSUMET_API

logger = logging.getLogger("Consumet")

class ConsumetClient:
    def __init__(self):
        self.base_url = CONSUMET_API.rstrip("/")
    
    async def get_recent_episodes(self):
        url = f"{self.base_url}/anime/gogoanime/recent-episodes?page=1&type=1"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        logger.error(f"Consumet API error: {resp.status}")
                        return []
                    data = await resp.json()
                    # Map to format expected by parser.py (list of dicts with 'id')
                    # Consumet returns { results: [ { id: '...', ... } ] }
                    return data.get("results", [])
            except Exception as e:
                logger.error(f"Failed to fetch recent episodes: {e}")
                return []

    async def get_episode_links(self, episode_id):
        url = f"{self.base_url}/anime/gogoanime/watch/{episode_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        logger.error(f"Consumet API error for {episode_id}: {resp.status}")
                        return {"dlinks": {}}
                    data = await resp.json()
                    # Map Consumet sources to 'dlinks' format: {'quality': 'url'}
                    # Consumet sources: [ { url: '...', quality: '1080p', ... } ]
                    dlinks = {}
                    sources = data.get("sources", [])
                    for source in sources:
                        quality = source.get("quality")
                        link = source.get("url")
                        if quality and link:
                            # Normalize quality names if needed (e.g. 'default', 'backup')
                            dlinks[quality] = link
                    
                    return {"dlinks": dlinks}
            except Exception as e:
                logger.error(f"Failed to fetch episode links for {episode_id}: {e}")
                return {"dlinks": {}}
