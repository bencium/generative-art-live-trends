// Google Trends API for Netlify Functions (Node.js)
// Uses google-trends-api npm package

const googleTrends = require('google-trends-api');

exports.handler = async function(event, context) {
  // Parse query parameters
  const params = event.queryStringParameters || {};
  const region = (params.region || 'US').toUpperCase();
  const count = Math.min(parseInt(params.count || 10), 20);

  try {
    // Fetch real-time trending searches from Google Trends
    const results = await googleTrends.realTimeTrends({
      geo: region,
      category: 'all'
    });

    const data = JSON.parse(results);

    // Extract trending searches
    const trendingSearches = data.storySummaries || [];

    // Process into our format
    const trends = trendingSearches.slice(0, count).map((story, index) => {
      const title = story.title || 'Unknown';
      const traffic = story.traffic || 0;

      // Calculate volume (normalize traffic)
      const volume = Math.min(100, Math.max(20, 100 - (index * 5)));

      // Simulate velocity based on traffic
      const velocity = Math.floor((traffic / 50000) * 100) - 30;

      // Simple categorization
      const category = categorizeQuery(title);

      return {
        query: title,
        volume: volume,
        velocity: Math.max(-100, Math.min(100, velocity)),
        category: category,
        rank: index + 1
      };
    });

    // Build response
    const response = {
      trends: trends,
      timestamp: new Date().toISOString(),
      region: region,
      source: 'google_trends_realtime',
      count: trends.length
    };

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
      },
      body: JSON.stringify(response)
    };

  } catch (error) {
    console.error('Google Trends fetch error:', error);

    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        error: error.message,
        message: 'Failed to fetch Google Trends data',
        timestamp: new Date().toISOString()
      })
    };
  }
};

function categorizeQuery(query) {
  const queryLower = query.toLowerCase();

  const techKeywords = ['ai', 'tech', 'apple', 'google', 'microsoft', 'iphone', 'android', 'app'];
  const newsKeywords = ['election', 'president', 'government', 'war', 'protest', 'vote'];
  const entertainmentKeywords = ['movie', 'film', 'actor', 'singer', 'music', 'netflix', 'spotify', 'game'];
  const sportsKeywords = ['nba', 'nfl', 'soccer', 'football', 'basketball', 'championship', 'olympics'];

  if (techKeywords.some(k => queryLower.includes(k))) return 'Technology';
  if (newsKeywords.some(k => queryLower.includes(k))) return 'News';
  if (entertainmentKeywords.some(k => queryLower.includes(k))) return 'Entertainment';
  if (sportsKeywords.some(k => queryLower.includes(k))) return 'Sports';

  return 'General';
}
