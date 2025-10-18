# Search Currents - Deployment Guide

## Prerequisites

Before deploying to Netlify, ensure you have:

1. **Netlify Account**: Sign up at [netlify.com](https://netlify.com)
2. **API Keys** (for live data):
   - SerpApi key from [serpapi.com](https://serpapi.com) (250 searches/month free)
   - NewsAPI key from [newsapi.org](https://newsapi.org) (100 requests/day free)

## Quick Deploy to Netlify

### Option 1: Deploy from Git (Recommended)

1. **Push to GitHub/GitLab**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Search Currents visualization"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Netlify**:
   - Go to [Netlify Dashboard](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your Git provider
   - Select your repository

3. **Build Settings** (auto-detected from `netlify.toml`):
   - Build command: `curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh && cd trends-wasm && wasm-pack build --target web`
   - Publish directory: `.`
   - Functions directory: `netlify/functions`

4. **Add Environment Variables**:
   - Go to Site settings → Environment variables
   - Add the following variables:
     ```
     SERPAPI_API_KEY=your_serpapi_key_here
     NEWSAPI_KEY=your_newsapi_key_here
     ```

5. **Deploy**:
   - Click "Deploy site"
   - Wait for build to complete (2-3 minutes)

### Option 2: Netlify CLI

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**:
   ```bash
   netlify login
   ```

3. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

4. **Set Environment Variables**:
   ```bash
   netlify env:set SERPAPI_API_KEY "your_key_here"
   netlify env:set NEWSAPI_KEY "your_key_here"
   ```

## Build Process

The deployment automatically:

1. **Installs Rust and wasm-pack** on Netlify build server
2. **Compiles WASM module** from Rust code (`trends-wasm/`)
3. **Installs Node.js dependencies** for serverless functions (`serpapi` package)
4. **Deploys serverless functions** to `/.netlify/functions/`
5. **Publishes static files** (HTML, CSS, JS, WASM)

## What Gets Deployed

```
/
├── index.html                     → Redirects to main app
├── search_currents_wasm.html      → Main application
├── trends-wasm/
│   └── pkg/                       → WASM module (built during deployment)
│       ├── trends_wasm.js
│       ├── trends_wasm_bg.wasm
│       └── trends_wasm_bg.wasm.d.ts
└── .netlify/functions/
    └── trends                     → API endpoint at /api/trends
```

## URLs After Deployment

- **Homepage**: `https://your-site.netlify.app/`
- **Visualization**: `https://your-site.netlify.app/search_currents_wasm.html`
- **API Endpoint**: `https://your-site.netlify.app/api/trends`

## Testing the Deployment

### 1. Test the Visualization

Visit `https://your-site.netlify.app/` and:
- Click "📊 Mock Data" - should load 25 trends instantly
- Click "🌐 Live RSS" - should fetch global trends from API
- Hover over particles to see trend labels

### 2. Test the API Directly

```bash
curl https://your-site.netlify.app/api/trends
```

Expected response:
```json
{
  "trends": [...],
  "timestamp": "2025-01-18T...",
  "region": "GLOBAL",
  "source": "serpapi_google_trends_multi_region",
  "count": 20,
  "regions_fetched": ["US", "GB", "CA", "AU", "DE", "FR", "JP", "IN"]
}
```

## Troubleshooting

### Build Fails

**Error**: `wasm-pack not found`
- **Solution**: Build command should install wasm-pack automatically. Check `netlify.toml` build command.

**Error**: `Cargo.toml not found`
- **Solution**: Ensure `trends-wasm/` directory exists with `Cargo.toml`

### API Returns Errors

**Error**: `Missing SERPAPI_API_KEY environment variable`
- **Solution**: Add API keys in Netlify dashboard → Site settings → Environment variables

**Error**: API returns 500
- **Solution**: Check Netlify function logs in dashboard → Functions tab

### WASM Module Not Loading

**Error**: `Failed to load WASM module`
- **Solution**:
  1. Check browser console for errors
  2. Verify WASM files exist in `trends-wasm/pkg/`
  3. Check CORS headers in `netlify.toml`

### No Trends Displayed

**Issue**: Visualization shows but no trends appear
- **Solution**:
  1. Click "📊 Mock Data" to test WASM module
  2. Check browser console for errors
  3. Verify API endpoint is accessible: `/api/trends`

## Performance Optimization

### Caching Strategy (configured in `netlify.toml`)

- **HTML files**: No cache (always fresh)
- **WASM files**: 1 year cache (immutable)
- **API responses**: No cache (always live data)

### API Rate Limits

- **SerpApi**: 250 searches/month (free tier)
  - Each visualization load = 8 API calls (one per region)
  - ~31 visualization loads per month with free tier
- **NewsAPI** (fallback): 100 requests/day

### Recommended: Use Mock Data for Development

To preserve API quota:
1. Use "📊 Mock Data" button during development
2. Only use "🌐 Live RSS" for production testing

## Monitoring

### Check Function Logs

```bash
netlify functions:log trends
```

### View Build Logs

- Netlify Dashboard → Deploys → Build log

### Analytics

- Netlify Dashboard → Analytics (traffic, bandwidth, function invocations)

## Cost Considerations

### Free Tier Limits

- **Netlify**:
  - 100GB bandwidth/month
  - 125,000 serverless function requests/month
  - Unlimited builds

- **SerpApi**: 250 searches/month
- **NewsAPI**: 100 requests/day

### Expected Usage

- Each page load: ~100KB (including WASM)
- Each API call: ~5KB response
- Typical monthly usage: Well within free tier for moderate traffic

## Security

### Environment Variables

- **Never commit** `.env` files
- Store all secrets in Netlify environment variables
- Use `.env.example` as reference only

### API Keys

- SerpApi and NewsAPI keys are server-side only
- Never exposed to client-side code
- Requests proxied through Netlify functions

## Updates & Redeployment

### Automatic Deployment

When connected to Git:
- Every push to main branch triggers automatic build
- No manual deployment needed

### Manual Deployment

```bash
netlify deploy --prod
```

## Support

### Resources

- [Netlify Docs](https://docs.netlify.com)
- [wasm-pack Guide](https://rustwasm.github.io/wasm-pack/)
- [SerpApi Docs](https://serpapi.com/google-trends-api)

### Common Issues

Check the [Troubleshooting](#troubleshooting) section above.

---

**Ready to Deploy?** Follow the [Quick Deploy](#quick-deploy-to-netlify) steps above!
