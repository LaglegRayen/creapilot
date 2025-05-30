import os
import requests

__all__ = ['fetch_instagram_data']

def fetch_instagram_data(topic):
    """
    Executes two requests against the Instagram scraper API:
    1) search_ig.php for keyword suggestions
    2) search_hashtag.php for details on the top suggestion or the topic itself.

    Args:
        topic (str): The search query or hashtag topic.

    Returns:
        tuple: (suggestions: List[str], hashtag_details: dict)

    Raises:
        RuntimeError: If the RAPIDAPI_KEY environment variable is not set.
        requests.HTTPError: If any request returns a non-200 response.
    """
    rapidapi_host = 'instagram-scraper-stable-api.p.rapidapi.com'
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if not rapidapi_key:
        raise RuntimeError("RAPIDAPI_KEY not set in environment")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-rapidapi-host': rapidapi_host,
        'x-rapidapi-key': rapidapi_key
    }

    # First request: get keyword suggestions
    resp1 = requests.post(
        f'https://{rapidapi_host}/search_ig.php',
        headers=headers,
        data={'search_query': topic}
    )
    resp1.raise_for_status()
    data1 = resp1.json()
    suggestions = [item['keyword']['name'] for item in data1.get('see_more', {}).get('list', [])]

    # Determine which hashtag to fetch details for
    hashtag_to_search = suggestions[0] if suggestions else topic

    # Second request: get hashtag details
    resp2 = requests.get(
        f'https://{rapidapi_host}/search_hashtag.php',
        headers={'x-rapidapi-host': rapidapi_host, 'x-rapidapi-key': rapidapi_key},
        params={'hashtag': hashtag_to_search}
    )
    resp2.raise_for_status()
    data2 = resp2.json()

    # Extract ideas from top posts & reels
    ideas = []
    top_sections = data2.get('data', {}).get('top', {}).get('sections', [])
    for section in top_sections:
        layout_content = section.get('layout_content', {})
        for block in layout_content.values():
            # Reels
            if 'clips' in block:
                for item in block['clips'].get('items', []):
                    media = item.get('media', {})
                    caption = media.get('caption', {}).get('text', '')
                    engagement = {}
                    if 'play_count' in media:
                        engagement['views'] = media.get('play_count')
                    if 'like_count' in media:
                        engagement['likes'] = media.get('like_count')
                    ideas.append({'caption': caption, 'type': 'reel', 'engagement': engagement})
            # Carousel posts
            elif 'carousel_media' in block:
                for media_item in block['carousel_media'].get('items', []):
                    caption = media_item.get('caption', {}).get('text', '')
                    engagement = {'likes': media_item.get('like_count')}
                    ideas.append({'caption': caption, 'type': 'carousel', 'engagement': engagement})
            # Single posts
            elif 'media' in block:
                media_item = block.get('media', {})
                caption = media_item.get('caption', {}).get('text', '')
                mtype = 'video' if media_item.get('media_type') == 2 else 'image'
                engagement = {}
                if 'play_count' in media_item:
                    engagement['views'] = media_item.get('play_count')
                if 'like_count' in media_item:
                    engagement['likes'] = media_item.get('like_count')
                ideas.append({'caption': caption, 'type': mtype, 'engagement': engagement})

    return suggestions, data2, ideas



fetch_instagram_data('fitness')