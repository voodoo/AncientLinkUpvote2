from datetime import datetime, timedelta
from math import log

def calculate_score(votes, item_hour_age, gravity=1.8):
    """Calculate the score of an item based on votes and time."""
    return (votes - 1) / pow((item_hour_age + 2), gravity)

def get_score(link):
    """Get the score for a link."""
    age = datetime.utcnow() - link.created_at
    item_hour_age = age.total_seconds() / 3600
    return calculate_score(link.score, item_hour_age)

def get_top_links(links, max_age=timedelta(days=7)):
    """Get the top links, excluding those older than max_age."""
    now = datetime.utcnow()
    return sorted(
        [link for link in links if now - link.created_at <= max_age],
        key=get_score,
        reverse=True
    )
