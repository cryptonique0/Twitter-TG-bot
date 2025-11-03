"""
Twitter API wrapper for fetching user data and tweets
"""
import os
from typing import List, Dict, Optional
import tweepy
from datetime import datetime


class TwitterAPI:
    """Wrapper for Twitter API operations"""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize Twitter API client
        
        Args:
            bearer_token: Twitter API Bearer Token
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        
        if not self.bearer_token:
            raise ValueError("Twitter Bearer Token is required")
        
        self.client = tweepy.Client(bearer_token=self.bearer_token)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Get user data by username
        
        Args:
            username: Twitter username (without @)
            
        Returns:
            User data dictionary or None
        """
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            response = self.client.get_user(
                username=username,
                user_fields=['created_at', 'description', 'public_metrics', 'profile_image_url']
            )
            
            if response.data:
                user = response.data
                return {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'description': user.description,
                    'created_at': user.created_at,
                    'public_metrics': user.public_metrics,
                    'profile_image_url': getattr(user, 'profile_image_url', None)
                }
            
            return None
            
        except tweepy.TweepyException as e:
            print(f"Error fetching user {username}: {e}")
            return None
    
    def get_user_tweets(self, user_id: int, max_results: int = 100) -> List[Dict]:
        """
        Get tweets from a user
        
        Args:
            user_id: Twitter user ID
            max_results: Maximum number of tweets to fetch (5-100)
            
        Returns:
            List of tweet dictionaries
        """
        try:
            # Ensure max_results is within valid range
            max_results = max(5, min(100, max_results))
            
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'text']
            )
            
            if response.data:
                tweets = []
                for tweet in response.data:
                    tweets.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'public_metrics': tweet.public_metrics
                    })
                return tweets
            
            return []
            
        except tweepy.TweepyException as e:
            print(f"Error fetching tweets for user {user_id}: {e}")
            return []
    
    def search_recent_users(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for users based on a query
        Note: This is a simplified version. Twitter API v2 doesn't have direct user search.
        This searches tweets and extracts unique users.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of user data dictionaries
        """
        try:
            # Search for tweets; we'll get up to max_results * 2 to account for duplicate users
            # Twitter API requires min 10 and max 100 for search_recent_tweets
            tweet_max = min(100, max(10, max_results * 5))
            
            response = self.client.search_recent_tweets(
                query=query,
                max_results=tweet_max,
                tweet_fields=['author_id'],
                expansions=['author_id'],
                user_fields=['created_at', 'description', 'public_metrics', 'username', 'name']
            )
            
            if response.includes and 'users' in response.includes:
                users = []
                for user in response.includes['users']:
                    users.append({
                        'id': user.id,
                        'username': user.username,
                        'name': user.name,
                        'description': user.description,
                        'created_at': user.created_at,
                        'public_metrics': user.public_metrics
                    })
                    # Limit to max_results users
                    if len(users) >= max_results:
                        break
                return users
            
            return []
            
        except tweepy.TweepyException as e:
            print(f"Error searching users with query '{query}': {e}")
            return []
    
    def get_user_profile_and_tweets(self, username: str, max_tweets: int = 100) -> Optional[tuple]:
        """
        Get both user profile and their tweets
        
        Args:
            username: Twitter username
            max_tweets: Maximum number of tweets to fetch
            
        Returns:
            Tuple of (user_data, tweets) or None
        """
        user_data = self.get_user_by_username(username)
        if not user_data:
            return None
        
        tweets = self.get_user_tweets(user_data['id'], max_tweets)
        
        return user_data, tweets
