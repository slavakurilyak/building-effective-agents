import time
from typing import List, Dict, Optional

# Placeholder Twitter tool implementations.
# In a real environment, you'd integrate with Twitter's API (via Tweepy or similar).
# For demonstration, we assume we have a local mock or partial stubs.

def search_prospects_twitter(icp_filters: Dict[str, str], max_results: int = 5) -> List[Dict]:
    """
    Search for prospects on Twitter based on ICP filters.
    icp_filters may include role, region, or other keywords.
    Returns a list of dictionaries, each with keys like 'twitter_handle', 'bio', 'followers'.
    """
    # Placeholder logic:
    # In real code, you'd call the Twitter API, parse results, etc.
    # Here we mock a few prospects:
    time.sleep(1)  # simulate network delay
    results = []
    for i in range(max_results):
        results.append({
            'twitter_handle': f'prospect_{i}',
            'bio': 'Bio text for prospect',
            'followers': 100 + i,
            'icp_match': True  # simplified assumption
        })
    return results

def send_dm_twitter(twitter_handle: str, message: str) -> bool:
    """
    Sends a DM to the specified Twitter handle.
    Returns True if successful, False otherwise.
    """
    time.sleep(0.5)  # simulate network delay
    print(f"[Mock] Sent DM to {twitter_handle}: {message}")
    return True

def check_inbox_twitter(since_id: Optional[str] = None) -> List[Dict]:
    """
    Checks the inbox for new messages/responses.
    since_id can help us fetch only messages after a certain ID or timestamp.
    Returns a list of message dicts, e.g.:
    [
      {
        'id': 'message123',
        'sender_handle': 'prospect_1',
        'text': 'Sure, let me know more!',
        'timestamp': 1698771123
      },
      ...
    ]
    """
    time.sleep(0.5)  # simulate network delay
    return [
        {
            'id': 'msg_1',
            'sender_handle': 'prospect_1',
            'text': 'Thanks for reaching out!',
            'timestamp': int(time.time())
        }
    ]