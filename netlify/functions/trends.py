#!/usr/bin/env python3
"""
Netlify Serverless Function - Google Trends API
Fetches real-time and daily trending searches from Google Trends
"""

import json
from pytrends.request import TrendReq
from datetime import datetime
import random


def handler(event, context):
    """
    Netlify serverless function handler

    Query params:
        - region: Country code (US, GB, etc.) - default: US
        - count: Number of trends to return (1-20) - default: 10
    """

    # Parse query parameters
    params = event.get('queryStringParameters', {}) or {}
    region = params.get('region', 'US').upper()
    count = min(int(params.get('count', 10)), 20)

    try:
        # Initialize pytrends
        pytrends = TrendReq(hl='en-US', tz=360)

        # Fetch trending searches
        trending_searches_df = pytrends.trending_searches(pn=region.lower())

        # Convert to list
        trending_list = trending_searches_df[0].tolist()[:count]

        # Process trends into our format
        trends = []
        for i, query in enumerate(trending_list):
            # Calculate mock volume and velocity for now
            # (Google Trends API doesn't provide these directly for trending searches)
            volume = 100 - (i * 5)  # Decreasing volume by rank
            velocity = random.randint(-30, 80)  # Simulated velocity

            # Try to categorize based on query content (simple heuristic)
            category = categorize_query(query)

            trends.append({
                'query': query,
                'volume': max(20, volume),
                'velocity': velocity,
                'category': category,
                'rank': i + 1
            })

        # Build response
        response_data = {
            'trends': trends,
            'timestamp': datetime.now().isoformat(),
            'region': region,
            'source': 'google_trends_pytrends',
            'count': len(trends)
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps(response_data)
        }

    except Exception as e:
        # Error response
        error_data = {
            'error': str(e),
            'message': 'Failed to fetch Google Trends data',
            'timestamp': datetime.now().isoformat()
        }

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(error_data)
        }


def categorize_query(query):
    """
    Simple categorization based on keywords
    """
    query_lower = query.lower()

    tech_keywords = ['ai', 'tech', 'apple', 'google', 'microsoft', 'iphone', 'android', 'app']
    news_keywords = ['election', 'president', 'government', 'war', 'protest', 'vote']
    entertainment_keywords = ['movie', 'film', 'actor', 'singer', 'music', 'netflix', 'spotify', 'game']
    sports_keywords = ['nba', 'nfl', 'soccer', 'football', 'basketball', 'championship', 'olympics']

    if any(keyword in query_lower for keyword in tech_keywords):
        return 'Technology'
    elif any(keyword in query_lower for keyword in news_keywords):
        return 'News'
    elif any(keyword in query_lower for keyword in entertainment_keywords):
        return 'Entertainment'
    elif any(keyword in query_lower for keyword in sports_keywords):
        return 'Sports'
    else:
        return 'General'
