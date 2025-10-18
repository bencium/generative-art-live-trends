// Google Trends via SerpApi with NewsAPI fallback
// Primary: SerpApi (250 searches/month free)
// Fallback: NewsAPI (100 requests/day free)

const { getJson } = require('serpapi');
const https = require('https');

exports.handler = async function(event, context) {
  // Parse query parameters
  const params = event.queryStringParameters || {};
  const region = (params.region || 'US').toUpperCase();
  const count = Math.min(parseInt(params.count || 10), 20);

  // API keys from environment variables only
  const serpApiKey = process.env.SERPAPI_API_KEY;
  const newsApiKey = process.env.NEWSAPI_KEY;

  // Validate API keys exist
  if (!serpApiKey) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        error: 'Missing SERPAPI_API_KEY environment variable',
        message: 'Please configure API keys in Netlify environment variables',
        timestamp: new Date().toISOString()
      })
    };
  }

  try {
    // PRIMARY: Try SerpApi first
    const response = await getJson({
      engine: "google_trends_trending_now",
      geo: region,
      hours: 24,
      api_key: serpApiKey
    });

    const trendingSearches = response.trending_searches || [];

    const trends = trendingSearches.slice(0, count).map((item, index) => {
      const query = item.query || 'Unknown';
      const searchVolume = item.search_volume || 0;
      const increasePercentage = item.increase_percentage || 0;

      const volume = Math.min(100, Math.max(20, Math.floor((searchVolume / 10000) * 20) + 80 - (index * 3)));
      const velocity = Math.min(100, Math.max(-100, Math.floor((increasePercentage / 10)) - 50));

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
        source: 'serpapi_google_trends',
        count: trends.length,
        quota_info: {
          provider: 'SerpApi',
          tier: 'free_tier_250_monthly'
        }
      })
    };

  } catch (serpError) {
    console.error('SerpApi error, trying NewsAPI fallback:', serpError.message);

    // FALLBACK: Use NewsAPI if SerpApi fails
    try {
      const newsData = await fetchNewsAPI(region, count, newsApiKey);
      const articles = newsData.articles || [];

      const trends = articles.slice(0, count).map((article, index) => {
        const query = article.title.split(' - ')[0]; // Remove source from title
        const volume = Math.min(100, Math.max(20, 100 - (index * 5)));
        const velocity = Math.floor(Math.random() * 80) - 20; // -20 to 60 for news

        return {
          query: query,
          volume: volume,
          velocity: velocity,
          category: categorizeQuery(query),
          rank: index + 1,
          source: article.source.name,
          publishedAt: article.publishedAt
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
          source: 'newsapi_fallback',
          count: trends.length,
          quota_info: {
            provider: 'NewsAPI',
            tier: 'free_tier_100_daily',
            note: 'Using news headlines as SerpApi unavailable'
          }
        })
      };

    } catch (newsError) {
      console.error('NewsAPI fallback also failed:', newsError.message);

      return {
        statusCode: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          error: newsError.message,
          serpApiError: serpError.message,
          message: 'Failed to fetch data from both SerpApi and NewsAPI',
          timestamp: new Date().toISOString(),
          region: region
        })
      };
    }
  }
};

// Fetch from NewsAPI using native https module
function fetchNewsAPI(region, count, apiKey) {
  return new Promise((resolve, reject) => {
    const countryCode = mapRegionToCountry(region);
    const url = `https://newsapi.org/v2/top-headlines?country=${countryCode}&pageSize=${count}&apiKey=${apiKey}`;

    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.status === 'ok') {
            resolve(parsed);
          } else {
            reject(new Error(parsed.message || 'NewsAPI error'));
          }
        } catch (e) {
          reject(new Error('Failed to parse NewsAPI response'));
        }
      });

    }).on('error', (err) => {
      reject(err);
    });
  });
}

// Map region code to NewsAPI country code
function mapRegionToCountry(region) {
  const mapping = {
    'US': 'us',
    'GB': 'gb',
    'CA': 'ca',
    'AU': 'au',
    'DE': 'de',
    'FR': 'fr',
    'JP': 'jp',
    'IN': 'in',
    'IT': 'it',
    'ES': 'es',
    'BR': 'br',
    'MX': 'mx',
    'RU': 'ru',
    'CN': 'cn',
    'KR': 'kr'
  };
  return mapping[region] || 'us';
}

// Categorize based on keywords
function categorizeQuery(query) {
  const queryLower = query.toLowerCase();

  const techKeywords = ['ai', 'tech', 'apple', 'google', 'microsoft', 'iphone', 'android', 'app', 'chatgpt', 'tesla', 'meta', 'crypto', 'bitcoin'];
  const newsKeywords = ['election', 'president', 'government', 'war', 'protest', 'vote', 'climate', 'politics', 'policy', 'senate', 'congress'];
  const entertainmentKeywords = ['movie', 'film', 'actor', 'singer', 'music', 'netflix', 'spotify', 'game', 'concert', 'album', 'tv', 'show', 'celebrity'];
  const sportsKeywords = ['nba', 'nfl', 'soccer', 'football', 'basketball', 'championship', 'olympics', 'world cup', 'league', 'match', 'vs', 'game'];

  if (techKeywords.some(k => queryLower.includes(k))) return 'Technology';
  if (newsKeywords.some(k => queryLower.includes(k))) return 'News';
  if (entertainmentKeywords.some(k => queryLower.includes(k))) return 'Entertainment';
  if (sportsKeywords.some(k => queryLower.includes(k))) return 'Sports';

  return 'General';
}
