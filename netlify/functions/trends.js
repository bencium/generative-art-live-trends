// Google Trends via SerpApi
// Reliable, production-ready Google Trends data
// Free tier: 250 searches/month

const { getJson } = require('serpapi');

exports.handler = async function(event, context) {
  // Parse query parameters
  const params = event.queryStringParameters || {};
  const region = (params.region || 'US').toUpperCase();
  const count = Math.min(parseInt(params.count || 10), 20);

  // Get API key from environment variable
  const apiKey = process.env.SERPAPI_API_KEY || '616a4be4884aa2982e781d7f37a6e0e6d32643f09dcbbdf5f4de2adc9b18d392';

  try {
    // Fetch trending searches from SerpApi
    const response = await getJson({
      engine: "google_trends_trending_now",
      geo: region,
      hours: 24, // Last 24 hours
      api_key: apiKey
    });

    // Extract trending searches
    const trendingSearches = response.trending_searches || [];

    // Process into our format
    const trends = trendingSearches.slice(0, count).map((item, index) => {
      const query = item.query || 'Unknown';
      const searchVolume = item.search_volume || 0;
      const increasePercentage = item.increase_percentage || 0;

      // Calculate volume (0-100 scale based on search volume)
      const volume = Math.min(100, Math.max(20, Math.floor((searchVolume / 10000) * 20) + 80 - (index * 3)));

      // Calculate velocity based on increase percentage
      const velocity = Math.min(100, Math.max(-100, Math.floor((increasePercentage / 10)) - 50));

      // Get category from SerpApi data
      const category = item.categories && item.categories.length > 0
        ? item.categories[0].name
        : categorizeQuery(query);

      return {
        query: query,
        volume: volume,
        velocity: velocity,
        category: category,
        rank: index + 1,
        searchVolume: searchVolume,
        increasePercentage: increasePercentage,
        active: item.active || false
      };
    });

    // Build response
    const response_data = {
      trends: trends,
      timestamp: new Date().toISOString(),
      region: region,
      source: 'serpapi_google_trends',
      count: trends.length,
      quota_info: {
        provider: 'SerpApi',
        tier: 'free_tier_250_monthly'
      }
    };

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
      },
      body: JSON.stringify(response_data)
    };

  } catch (error) {
    console.error('SerpApi error:', error);

    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        error: error.message,
        message: 'Failed to fetch Google Trends data from SerpApi',
        timestamp: new Date().toISOString(),
        region: region
      })
    };
  }
};

// Fallback categorization (if SerpApi doesn't provide category)
function categorizeQuery(query) {
  const queryLower = query.toLowerCase();

  const techKeywords = ['ai', 'tech', 'apple', 'google', 'microsoft', 'iphone', 'android', 'app', 'chatgpt', 'tesla', 'meta'];
  const newsKeywords = ['election', 'president', 'government', 'war', 'protest', 'vote', 'climate', 'politics', 'policy'];
  const entertainmentKeywords = ['movie', 'film', 'actor', 'singer', 'music', 'netflix', 'spotify', 'game', 'concert', 'album', 'tv', 'show'];
  const sportsKeywords = ['nba', 'nfl', 'soccer', 'football', 'basketball', 'championship', 'olympics', 'world cup', 'league', 'match', 'vs'];

  if (techKeywords.some(k => queryLower.includes(k))) return 'Technology';
  if (newsKeywords.some(k => queryLower.includes(k))) return 'News';
  if (entertainmentKeywords.some(k => queryLower.includes(k))) return 'Entertainment';
  if (sportsKeywords.some(k => queryLower.includes(k))) return 'Sports';

  return 'General';
}
