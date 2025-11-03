"""
Unit tests for Twitter utility functions
"""
import unittest
from datetime import datetime, timedelta
from twitter_utils import (
    check_bio_keywords,
    check_post_keywords,
    check_post_count_within_timeframe,
    filter_early_account
)


class TestBioKeywords(unittest.TestCase):
    """Test bio keyword filtering"""
    
    def test_bio_with_matching_keyword(self):
        """Test bio containing a matching keyword"""
        bio = "Building the next generation blockchain project"
        keywords = ["blockchain", "crypto", "web3"]
        self.assertTrue(check_bio_keywords(bio, keywords))
    
    def test_bio_without_matching_keyword(self):
        """Test bio without matching keywords"""
        bio = "Just a regular person tweeting about life"
        keywords = ["blockchain", "crypto", "web3"]
        self.assertFalse(check_bio_keywords(bio, keywords))
    
    def test_bio_case_insensitive(self):
        """Test case-insensitive matching"""
        bio = "CRYPTO enthusiast and BLOCKCHAIN developer"
        keywords = ["crypto", "blockchain"]
        self.assertTrue(check_bio_keywords(bio, keywords))
    
    def test_empty_bio(self):
        """Test with empty bio"""
        bio = ""
        keywords = ["crypto", "blockchain"]
        self.assertFalse(check_bio_keywords(bio, keywords))
    
    def test_none_bio(self):
        """Test with None bio"""
        bio = None
        keywords = ["crypto", "blockchain"]
        self.assertFalse(check_bio_keywords(bio, keywords))


class TestPostKeywords(unittest.TestCase):
    """Test post keyword filtering"""
    
    def test_posts_with_matching_keyword(self):
        """Test posts containing matching keywords"""
        tweets = [
            {'text': 'Just launched our new project!'},
            {'text': 'Building something amazing'}
        ]
        keywords = ["launch", "building", "project"]
        self.assertTrue(check_post_keywords(tweets, keywords))
    
    def test_posts_without_matching_keyword(self):
        """Test posts without matching keywords"""
        tweets = [
            {'text': 'Good morning everyone'},
            {'text': 'Having a great day'}
        ]
        keywords = ["launch", "building", "project"]
        self.assertFalse(check_post_keywords(tweets, keywords))
    
    def test_empty_tweets_list(self):
        """Test with empty tweets list"""
        tweets = []
        keywords = ["launch", "building"]
        self.assertFalse(check_post_keywords(tweets, keywords))
    
    def test_posts_case_insensitive(self):
        """Test case-insensitive matching"""
        tweets = [
            {'text': 'LAUNCHING our NEW project soon!'}
        ]
        keywords = ["launch", "project"]
        self.assertTrue(check_post_keywords(tweets, keywords))


class TestPostCountWithinTimeframe(unittest.TestCase):
    """Test post count filtering within timeframe"""
    
    def test_posts_within_limit(self):
        """Test with posts within the limit"""
        created_at = datetime(2024, 1, 1, 0, 0, 0)
        tweets = [
            {'created_at': datetime(2024, 1, 2, 0, 0, 0)},
            {'created_at': datetime(2024, 1, 3, 0, 0, 0)}
        ]
        self.assertTrue(check_post_count_within_timeframe(tweets, created_at, 2, 7))
    
    def test_posts_exceeding_limit(self):
        """Test with posts exceeding the limit"""
        created_at = datetime(2024, 1, 1, 0, 0, 0)
        tweets = [
            {'created_at': datetime(2024, 1, 2, 0, 0, 0)},
            {'created_at': datetime(2024, 1, 3, 0, 0, 0)},
            {'created_at': datetime(2024, 1, 4, 0, 0, 0)}
        ]
        self.assertFalse(check_post_count_within_timeframe(tweets, created_at, 2, 7))
    
    def test_posts_outside_timeframe(self):
        """Test with posts outside the timeframe"""
        created_at = datetime(2024, 1, 1, 0, 0, 0)
        tweets = [
            {'created_at': datetime(2024, 1, 10, 0, 0, 0)},
            {'created_at': datetime(2024, 1, 15, 0, 0, 0)},
            {'created_at': datetime(2024, 1, 20, 0, 0, 0)}
        ]
        # All posts are outside the 7-day window, so count is 0
        self.assertTrue(check_post_count_within_timeframe(tweets, created_at, 2, 7))
    
    def test_no_posts(self):
        """Test with no posts"""
        created_at = datetime(2024, 1, 1, 0, 0, 0)
        tweets = []
        self.assertTrue(check_post_count_within_timeframe(tweets, created_at, 2, 7))
    
    def test_mixed_posts_in_and_out_of_timeframe(self):
        """Test with some posts in and some out of timeframe"""
        created_at = datetime(2024, 1, 1, 0, 0, 0)
        tweets = [
            {'created_at': datetime(2024, 1, 2, 0, 0, 0)},  # Within
            {'created_at': datetime(2024, 1, 10, 0, 0, 0)},  # Outside
            {'created_at': datetime(2024, 1, 15, 0, 0, 0)}   # Outside
        ]
        # Only 1 post within timeframe, which is <= 2
        self.assertTrue(check_post_count_within_timeframe(tweets, created_at, 2, 7))


class TestFilterEarlyAccount(unittest.TestCase):
    """Test complete account filtering"""
    
    def test_account_matches_all_criteria(self):
        """Test account that matches all criteria"""
        user_data = {
            'username': 'testuser',
            'name': 'Test User',
            'description': 'Building a new blockchain project',
            'created_at': datetime(2024, 1, 1, 0, 0, 0),
            'public_metrics': {'followers_count': 100}
        }
        tweets = [
            {
                'text': 'Launching our project soon!',
                'created_at': datetime(2024, 1, 2, 0, 0, 0)
            }
        ]
        
        results = filter_early_account(
            user_data=user_data,
            tweets=tweets,
            bio_keywords=['blockchain', 'crypto'],
            post_keywords=['launch', 'project'],
            max_posts=2,
            days=7
        )
        
        self.assertTrue(results['matches'])
        self.assertTrue(results['bio_match'])
        self.assertTrue(results['post_count_match'])
        self.assertTrue(results['post_keywords_match'])
    
    def test_account_fails_bio_criteria(self):
        """Test account that fails bio criteria"""
        user_data = {
            'username': 'testuser',
            'name': 'Test User',
            'description': 'Just a regular person',
            'created_at': datetime(2024, 1, 1, 0, 0, 0),
            'public_metrics': {'followers_count': 100}
        }
        tweets = [
            {
                'text': 'Launching our project soon!',
                'created_at': datetime(2024, 1, 2, 0, 0, 0)
            }
        ]
        
        results = filter_early_account(
            user_data=user_data,
            tweets=tweets,
            bio_keywords=['blockchain', 'crypto'],
            post_keywords=['launch', 'project'],
            max_posts=2,
            days=7
        )
        
        self.assertFalse(results['matches'])
        self.assertFalse(results['bio_match'])
    
    def test_account_fails_post_count_criteria(self):
        """Test account that exceeds post count limit"""
        user_data = {
            'username': 'testuser',
            'name': 'Test User',
            'description': 'Building a blockchain project',
            'created_at': datetime(2024, 1, 1, 0, 0, 0),
            'public_metrics': {'followers_count': 100}
        }
        tweets = [
            {'text': 'Launch post 1', 'created_at': datetime(2024, 1, 2, 0, 0, 0)},
            {'text': 'Launch post 2', 'created_at': datetime(2024, 1, 3, 0, 0, 0)},
            {'text': 'Launch post 3', 'created_at': datetime(2024, 1, 4, 0, 0, 0)}
        ]
        
        results = filter_early_account(
            user_data=user_data,
            tweets=tweets,
            bio_keywords=['blockchain'],
            post_keywords=['launch'],
            max_posts=2,
            days=7
        )
        
        self.assertFalse(results['matches'])
        self.assertFalse(results['post_count_match'])
    
    def test_account_fails_post_keywords_criteria(self):
        """Test account that fails post keywords criteria"""
        user_data = {
            'username': 'testuser',
            'name': 'Test User',
            'description': 'Building a blockchain project',
            'created_at': datetime(2024, 1, 1, 0, 0, 0),
            'public_metrics': {'followers_count': 100}
        }
        tweets = [
            {
                'text': 'Just a regular tweet',
                'created_at': datetime(2024, 1, 2, 0, 0, 0)
            }
        ]
        
        results = filter_early_account(
            user_data=user_data,
            tweets=tweets,
            bio_keywords=['blockchain'],
            post_keywords=['launch', 'project', 'announcement'],
            max_posts=2,
            days=7
        )
        
        self.assertFalse(results['matches'])
        self.assertFalse(results['post_keywords_match'])


if __name__ == '__main__':
    unittest.main()
