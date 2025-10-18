#!/usr/bin/env python3
"""
Social Media Data Fetcher
Fetches trending content from Reddit and Hacker News to visualize in Chromatic Archaeology
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time

class SocialDataFetcher:
    """Fetches and processes social media trending data"""

    def __init__(self):
        self.reddit_base_url = "https://www.reddit.com/r/all/top.json"
        self.hn_base_url = "https://hacker-news.firebaseio.com/v0"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ChromaticArchaeology/1.0 (Educational Data Visualization)'
        })

    def fetch_reddit_trends(self, limit=50, timeframe='day'):
        """
        Fetch top posts from Reddit

        Args:
            limit: Number of posts to fetch (max 100)
            timeframe: 'hour', 'day', 'week', 'month', 'year', 'all'

        Returns:
            List of trending events
        """
        print(f"Fetching Reddit trends (top {limit} from past {timeframe})...")

        params = {
            'limit': min(limit, 100),
            't': timeframe
        }

        try:
            response = self.session.get(self.reddit_base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            events = []
            for post in data['data']['children']:
                post_data = post['data']

                # Calculate significance score
                score = self._calculate_reddit_score(post_data)

                # Simple sentiment based on subreddit and score
                sentiment = self._estimate_sentiment_reddit(post_data)

                events.append({
                    'platform': 'reddit',
                    'title': post_data.get('title', 'Untitled'),
                    'subreddit': post_data.get('subreddit', 'unknown'),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': post_data.get('created_utc', 0),
                    'url': post_data.get('url', ''),
                    'significance': score,
                    'sentiment': sentiment,
                    'category': self._categorize_subreddit(post_data.get('subreddit', ''))
                })

            print(f"✓ Fetched {len(events)} Reddit posts")
            return events

        except Exception as e:
            print(f"✗ Error fetching Reddit data: {e}")
            return []

    def fetch_hackernews_trends(self, limit=30):
        """
        Fetch top stories from Hacker News

        Args:
            limit: Number of stories to fetch

        Returns:
            List of trending events
        """
        print(f"Fetching Hacker News trends (top {limit} stories)...")

        try:
            # Get top story IDs
            response = self.session.get(f"{self.hn_base_url}/topstories.json", timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit]

            events = []
            for story_id in story_ids:
                try:
                    # Fetch individual story details
                    story_response = self.session.get(f"{self.hn_base_url}/item/{story_id}.json", timeout=5)
                    story_response.raise_for_status()
                    story = story_response.json()

                    if not story or story.get('type') != 'story':
                        continue

                    # Calculate significance
                    score = self._calculate_hn_score(story)
                    sentiment = self._estimate_sentiment_hn(story)

                    events.append({
                        'platform': 'hackernews',
                        'title': story.get('title', 'Untitled'),
                        'score': story.get('score', 0),
                        'num_comments': len(story.get('kids', [])),
                        'created_utc': story.get('time', 0),
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'significance': score,
                        'sentiment': sentiment,
                        'category': 'technology'
                    })

                    # Small delay to avoid rate limiting
                    time.sleep(0.05)

                except Exception as e:
                    print(f"  Warning: Could not fetch story {story_id}: {e}")
                    continue

            print(f"✓ Fetched {len(events)} Hacker News stories")
            return events

        except Exception as e:
            print(f"✗ Error fetching Hacker News data: {e}")
            return []

    def _calculate_reddit_score(self, post_data):
        """Calculate significance score for Reddit post"""
        score = post_data.get('score', 0)
        comments = post_data.get('num_comments', 0)

        # Engagement-based scoring
        engagement_score = score + (comments * 2)  # Comments worth more

        # Recency bonus (posts from last 6 hours get boost)
        now = time.time()
        created = post_data.get('created_utc', now)
        age_hours = (now - created) / 3600

        recency_multiplier = 1.5 if age_hours < 6 else 1.0

        return engagement_score * recency_multiplier

    def _calculate_hn_score(self, story):
        """Calculate significance score for HN story"""
        score = story.get('score', 0)
        comments = len(story.get('kids', []))

        # Engagement-based scoring
        engagement_score = score + (comments * 3)  # HN comments highly valued

        # Recency bonus
        now = time.time()
        created = story.get('time', now)
        age_hours = (now - created) / 3600

        recency_multiplier = 1.5 if age_hours < 6 else 1.0

        return engagement_score * recency_multiplier

    def _estimate_sentiment_reddit(self, post_data):
        """
        Estimate sentiment based on subreddit and engagement patterns
        Returns value between -1 (negative) and 1 (positive)
        """
        subreddit = post_data.get('subreddit', '').lower()
        score_ratio = post_data.get('upvote_ratio', 0.5)

        # Subreddit-based sentiment hints
        positive_subs = ['upliftingnews', 'mademesmile', 'happy', 'wholesome', 'aww']
        negative_subs = ['tifu', 'wellthatsucks', 'mildlyinfuriating']
        controversial_subs = ['politics', 'worldnews', 'news']

        if any(sub in subreddit for sub in positive_subs):
            base_sentiment = 0.6
        elif any(sub in subreddit for sub in negative_subs):
            base_sentiment = -0.4
        elif any(sub in subreddit for sub in controversial_subs):
            base_sentiment = 0.0
        else:
            base_sentiment = 0.2

        # Adjust based on upvote ratio (high ratio = more positive reception)
        sentiment = base_sentiment + ((score_ratio - 0.5) * 0.8)

        return max(-1.0, min(1.0, sentiment))

    def _estimate_sentiment_hn(self, story):
        """
        Estimate sentiment for HN story
        Tech news tends neutral to positive
        """
        score = story.get('score', 0)
        comments = len(story.get('kids', []))

        # More comments relative to score = more controversy
        if comments > 0 and score > 0:
            comment_ratio = comments / score
            if comment_ratio > 0.5:  # High discussion relative to upvotes
                return -0.2  # Slightly controversial

        # Generally positive for highly upvoted content
        if score > 500:
            return 0.7
        elif score > 200:
            return 0.4
        else:
            return 0.1

    def _categorize_subreddit(self, subreddit):
        """Categorize subreddit into broad categories"""
        subreddit = subreddit.lower()

        tech_subs = ['technology', 'programming', 'coding', 'science', 'gadgets']
        news_subs = ['news', 'worldnews', 'politics', 'economics']
        entertainment_subs = ['movies', 'television', 'music', 'gaming', 'videos']
        lifestyle_subs = ['fitness', 'food', 'travel', 'fashion', 'art']

        if any(sub in subreddit for sub in tech_subs):
            return 'technology'
        elif any(sub in subreddit for sub in news_subs):
            return 'news'
        elif any(sub in subreddit for sub in entertainment_subs):
            return 'entertainment'
        elif any(sub in subreddit for sub in lifestyle_subs):
            return 'lifestyle'
        else:
            return 'general'

    def get_all_trends(self, reddit_limit=50, hn_limit=30):
        """
        Fetch trends from all sources and combine

        Returns:
            Dict with timestamp and sorted events by significance
        """
        print("\n" + "="*60)
        print("FETCHING SOCIAL MEDIA TRENDS")
        print("="*60 + "\n")

        all_events = []

        # Fetch from both sources
        reddit_events = self.fetch_reddit_trends(limit=reddit_limit)
        hn_events = self.fetch_hackernews_trends(limit=hn_limit)

        all_events.extend(reddit_events)
        all_events.extend(hn_events)

        # Sort by significance
        all_events.sort(key=lambda x: x['significance'], reverse=True)

        # Prepare result
        result = {
            'timestamp': datetime.now().isoformat(),
            'total_events': len(all_events),
            'reddit_count': len(reddit_events),
            'hackernews_count': len(hn_events),
            'events': all_events[:100]  # Top 100 most significant
        }

        print(f"\n" + "="*60)
        print(f"SUMMARY: Captured {result['total_events']} total events")
        print(f"  • Reddit: {result['reddit_count']} posts")
        print(f"  • Hacker News: {result['hackernews_count']} stories")
        print("="*60 + "\n")

        return result

    def save_to_cache(self, data, filename='social_trends_cache.json'):
        """Save fetched data to cache file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Data cached to {filename}")

    @staticmethod
    def load_from_cache(filename='social_trends_cache.json'):
        """Load data from cache file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"✓ Loaded cached data from {filename}")
            return data
        except FileNotFoundError:
            print(f"✗ Cache file {filename} not found")
            return None


def main():
    """Test the data fetcher"""
    fetcher = SocialDataFetcher()

    # Fetch all trends
    trends = fetcher.get_all_trends(reddit_limit=30, hn_limit=20)

    # Show top 10
    print("\nTop 10 Most Significant Events:")
    print("-" * 80)
    for i, event in enumerate(trends['events'][:10], 1):
        sentiment_emoji = "🟢" if event['sentiment'] > 0.3 else "🔴" if event['sentiment'] < -0.3 else "🟡"
        print(f"{i}. [{event['platform'].upper()}] {sentiment_emoji}")
        print(f"   {event['title'][:70]}...")
        print(f"   Score: {event['score']}, Comments: {event['num_comments']}, Significance: {event['significance']:.0f}")
        print()

    # Save to cache
    fetcher.save_to_cache(trends)

    return trends


if __name__ == '__main__':
    main()
