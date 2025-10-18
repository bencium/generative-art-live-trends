// Google Trends API for Netlify Functions (Node.js)
// Using dailyTrends() method for better reliability

const googleTrends = require('google-trends-api');

exports.handler = async function(event, context) {
  // Parse query parameters
  const params = event.queryStringParameters || {};
  const region = (params.region || 'US').toUpperCase();
  const count = Math.min(parseInt(params.count || 10), 20);

  try {
    // Try dailyTrends first (more reliable than realTimeTrends)
    const results = await googleTrends.dailyTrends({
      geo: region
    });

    const data = JSON.parse(results);

    // Extract trending searches from daily trends
    const trendingSearches = data.default?.trendingSearchesDays?.[0]?.trendingSearches || [];

    // Process into our format
    const trends = trendingSearches.slice(0, count).map((item, index) => {
      const title = item.title?.query || 'Unknown';
      const traffic = item.formattedTraffic || '0';

      // Parse traffic number (e.g., "50K+" -> 50000)
      const trafficNum = parseTrafficString(traffic);

      // Calculate volume (normalize traffic)
      const volume = Math.min(100, Math.max(20, 100 - (index * 5)));

      // Calculate velocity based on traffic
      const velocity = Math.floor((trafficNum / 50000) * 100) - 30;

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
      source: 'google_trends_daily',
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

  } catch (dailyError) {
    console.error('dailyTrends error:', dailyError);

    // Fallback to realTimeTrends if dailyTrends fails
    try {
      const results = await googleTrends.realTimeTrends({
        geo: region,
        category: 'all'
      });

      const data = JSON.parse(results);
      const trendingSearches = data.storySummaries || [];

      const trends = trendingSearches.slice(0, count).map((story, index) => {
        const title = story.title || 'Unknown';
        const traffic = story.traffic || 0;

        const volume = Math.min(100, Math.max(20, 100 - (index * 5)));
        const velocity = Math.floor((traffic / 50000) * 100) - 30;
        const category = categorizeQuery(title);

        return {
          query: title,
          volume: volume,
          velocity: Math.max(-100, Math.min(100, velocity)),
          category: category,
          rank: index + 1
        };
      });

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
        body: JSON.stringify({
          trends: trends,
          timestamp: new Date().toISOString(),
          region: region,
          source: 'google_trends_realtime',
          count: trends.length
        })
      };

    } catch (realTimeError) {
      console.error('realTimeTrends error:', realTimeError);

      // Return error response without mock data
      return {
        statusCode: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          error: realTimeError.message,
          dailyError: dailyError.message,
          message: 'Failed to fetch Google Trends data from both dailyTrends and realTimeTrends',
          timestamp: new Date().toISOString(),
          region: region
        })
      };
    }
  }
};

// Parse traffic string like "50K+", "2M+", "500+" to numbers
function parseTrafficString(traffic) {
  if (typeof traffic !== 'string') return 0;

  const cleanTraffic = traffic.replace(/[+,]/g, '').toUpperCase();

  if (cleanTraffic.includes('M')) {
    return parseFloat(cleanTraffic) * 1000000;
  } else if (cleanTraffic.includes('K')) {
    return parseFloat(cleanTraffic) * 1000;
  } else {
    return parseInt(cleanTraffic) || 0;
  }
}

// Categorize query based on keywords
function categorizeQuery(query) {
  const queryLower = query.toLowerCase();

  const techKeywords = ['ai', 'tech', 'apple', 'google', 'microsoft', 'iphone', 'android', 'app', 'chatgpt', 'tesla', 'meta'];
  const newsKeywords = ['election', 'president', 'government', 'war', 'protest', 'vote', 'climate', 'politics', 'policy'];
  const entertainmentKeywords = ['movie', 'film', 'actor', 'singer', 'music', 'netflix', 'spotify', 'game', 'concert', 'album', 'tv', 'show'];
  const sportsKeywords = ['nba', 'nfl', 'soccer', 'football', 'basketball', 'championship', 'olympics', 'world cup', 'league', 'match'];

  if (techKeywords.some(k => queryLower.includes(k))) return 'Technology';
  if (newsKeywords.some(k => queryLower.includes(k))) return 'News';
  if (entertainmentKeywords.some(k => queryLower.includes(k))) return 'Entertainment';
  if (sportsKeywords.some(k => queryLower.includes(k))) return 'Sports';

  return 'General';
}
