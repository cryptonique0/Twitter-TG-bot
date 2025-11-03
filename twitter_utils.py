"""
Utility functions for Twitter account analysis
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import tweepy


def check_bio_keywords(bio: str, keywords: List[str]) -> bool:
    """
    Check if bio contains any of the specified keywords
    
    Args:
        bio: User's Twitter bio
        keywords: List of keywords to search for
        
    Returns:
        True if any keyword is found in bio (case-insensitive)
    """
    if not bio:
        return False
    
    bio_lower = bio.lower()
    return any(keyword.lower() in bio_lower for keyword in keywords)


def check_post_keywords(tweets: List[Dict], keywords: List[str]) -> bool:
    """
    Check if any tweets contain specified keywords
    
    Args:
        tweets: List of tweet objects
        keywords: List of keywords to search for
        
    Returns:
        True if any keyword is found in any tweet (case-insensitive)
    """
    if not tweets:
        return False
    
    for tweet in tweets:
        text = tweet.get('text', '').lower()
        if any(keyword.lower() in text for keyword in keywords):
            return True
    
    return False


def check_post_count_within_timeframe(
    tweets: List[Dict], 
    account_created_at: datetime, 
    max_posts: int, 
    days: int
) -> bool:
    """
    Check if account has posted maximum number of posts within specified days from creation
    
    Args:
        tweets: List of tweet objects with 'created_at' field
        account_created_at: Account creation date
        max_posts: Maximum allowed posts
        days: Number of days from account creation
        
    Returns:
        True if post count is within limit
    """
    if not tweets:
        return True  # No posts means within limit
    
    # Calculate the timeframe end date
    timeframe_end = account_created_at + timedelta(days=days)
    
    # Count posts within the timeframe
    posts_within_timeframe = 0
    for tweet in tweets:
        tweet_date = tweet.get('created_at')
        if isinstance(tweet_date, str):
            # Parse datetime if it's a string
            tweet_date = datetime.strptime(tweet_date, '%a %b %d %H:%M:%S %z %Y')
        
        if account_created_at <= tweet_date <= timeframe_end:
            posts_within_timeframe += 1
    
    return posts_within_timeframe <= max_posts


def filter_early_account(
    user_data: Dict,
    tweets: List[Dict],
    bio_keywords: List[str],
    post_keywords: List[str],
    max_posts: int,
    days: int
) -> Dict:
    """
    Filter Twitter account based on criteria for early accounts
    
    Args:
        user_data: User profile data
        tweets: List of user's tweets
        bio_keywords: Keywords to search in bio
        post_keywords: Keywords to search in posts
        max_posts: Maximum posts allowed within timeframe
        days: Number of days from account creation
        
    Returns:
        Dictionary with filter results
    """
    results = {
        'matches': False,
        'bio_match': False,
        'post_count_match': False,
        'post_keywords_match': False,
        'details': {}
    }
    
    # Extract user data
    bio = user_data.get('description', '')
    created_at = user_data.get('created_at')
    
    if isinstance(created_at, str):
        created_at = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    
    # Check bio keywords
    results['bio_match'] = check_bio_keywords(bio, bio_keywords)
    
    # Check post count within timeframe
    results['post_count_match'] = check_post_count_within_timeframe(
        tweets, created_at, max_posts, days
    )
    
    # Check post keywords
    results['post_keywords_match'] = check_post_keywords(tweets, post_keywords)
    
    # Account matches if all criteria are met
    results['matches'] = (
        results['bio_match'] and 
        results['post_count_match'] and 
        results['post_keywords_match']
    )
    
    # Add details
    results['details'] = {
        'username': user_data.get('username', user_data.get('screen_name', '')),
        'name': user_data.get('name', ''),
        'bio': bio,
        'created_at': created_at.strftime('%Y-%m-%d') if created_at else 'Unknown',
        'tweet_count': len(tweets),
        'followers': user_data.get('public_metrics', {}).get('followers_count', 
                                   user_data.get('followers_count', 0))
    }
    
    return results


def format_account_info(results: Dict) -> str:
    """
    Format account information for display
    
    Args:
        results: Filter results dictionary
        
    Returns:
        Formatted string for display
    """
    details = results['details']
    
    message = f"""
🔍 **Early Account Found!**

👤 **Name:** {details['name']}
🐦 **Username:** @{details['username']}
📅 **Created:** {details['created_at']}
👥 **Followers:** {details['followers']}
📝 **Tweets:** {details['tweet_count']}

💬 **Bio:**
{details['bio']}

✅ **Matches:**
- Bio keywords: {'✓' if results['bio_match'] else '✗'}
- Post count (within limit): {'✓' if results['post_count_match'] else '✗'}
- Post keywords: {'✓' if results['post_keywords_match'] else '✗'}
"""
    
    return message.strip()
