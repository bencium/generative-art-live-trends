# Netlify Deployment Guide - Search Currents

## ✅ Why Netlify Solves CORS Issues

**The Problem Locally:**
- Browser blocks Google Trends API calls from `file://` or `localhost` (CORS policy)
- Different origins = CORS errors

**The Solution on Netlify:**
- Frontend: `https://generative-art-live-trends.netlify.app`
- API: `https://generative-art-live-trends.netlify.app/api/trends`
- **Same origin** → No CORS issues!

Netlify serverless functions fetch Google Trends server-side, then your frontend fetches from same domain.

---

## 🚀 Quick Deploy (Recommended)

### Option 1: Deploy from GitHub

1. **Push code to GitHub** (already done!)

2. **Go to Netlify**
   - Visit: https://app.netlify.com
   - Click "Add new site" → "Import an existing project"

3. **Connect GitHub**
   - Choose: GitHub
   - Select repository: `generative-art-live-trends`
   - Click "Deploy"

4. **Done!**
   - Netlify auto-detects `netlify.toml`
   - Builds WASM automatically
   - Deploys serverless functions
   - Live in ~3 minutes

---

## ⚙️ Manual Netlify Settings

If Netlify doesn't auto-detect settings, configure manually:

### Build Settings

```
Build command:  cd trends-wasm && cargo install wasm-pack && wasm-pack build --target web --out-dir pkg
Publish directory:  .
Functions directory:  netlify/functions
```

### Environment Variables

**None required!** Google Trends API doesn't need API keys for basic trending searches.

(Optional: If you want to add custom settings later)
```
TRENDS_REGION=US
TRENDS_COUNT=12
```

### Python Runtime

```
Python version:  3.9
```

This is set in `netlify.toml` already.

---

## 📁 Files Created for Netlify

### netlify.toml
```toml
[build]
  command = "cd trends-wasm && cargo install wasm-pack && wasm-pack build --target web --out-dir pkg"
  publish = "."
  functions = "netlify/functions"

[functions]
  python_version = "3.9"
```

### netlify/functions/trends.py
Python serverless function that:
- Fetches real Google Trends data using `pytrends`
- Returns JSON response
- Handles errors gracefully

### netlify/functions/requirements.txt
```
pytrends==4.9.2
pandas>=1.5.0
```

---

## 🧪 Testing the Deployment

### 1. Test API Endpoint

After deployment, test the serverless function:

```bash
curl https://generative-art-live-trends.netlify.app/api/trends?region=US&count=5
```

Expected response:
```json
{
  "trends": [
    {
      "query": "some trending topic",
      "volume": 100,
      "velocity": 45,
      "category": "Technology",
      "rank": 1
    }
    ...
  ],
  "timestamp": "2025-10-18T12:00:00Z",
  "region": "US",
  "source": "google_trends_pytrends",
  "count": 5
}
```

### 2. Test Frontend

Visit: https://generative-art-live-trends.netlify.app

1. Click "🔄 Fetch Live Trends" button
2. Should see: "✅ Loaded X live trends from Google (US)"
3. Particles should flow based on real data

### 3. Check Function Logs

In Netlify dashboard:
- Go to "Functions" tab
- Click on `trends`
- View logs to see requests

---

## 🔧 Build Process

Netlify runs this sequence:

1. **Install Rust** (if not cached)
2. **Install wasm-pack**: `cargo install wasm-pack`
3. **Build WASM**: `wasm-pack build --target web --out-dir pkg`
4. **Install Python dependencies**: From `netlify/functions/requirements.txt`
5. **Deploy functions**: Upload to serverless runtime
6. **Publish site**: All HTML, JS, WASM files

**Build time:** ~5-7 minutes (first build), ~2 minutes (cached)

---

## 🌍 Supported Regions

Change the region parameter to fetch trends from different countries:

| Region Code | Country |
|------------|---------|
| `US` | United States |
| `GB` | United Kingdom |
| `CA` | Canada |
| `AU` | Australia |
| `DE` | Germany |
| `FR` | France |
| `JP` | Japan |
| `IN` | India |

**Usage:**
```javascript
fetch('/api/trends?region=JP&count=10')
```

---

## 📊 API Endpoints

### GET /api/trends

Fetches trending searches from Google Trends.

**Query Parameters:**
- `region` (optional): Country code (default: `US`)
- `count` (optional): Number of trends (1-20, default: `10`)

**Example:**
```
GET /api/trends?region=GB&count=15
```

**Response:**
```json
{
  "trends": [...],
  "timestamp": "ISO-8601",
  "region": "GB",
  "source": "google_trends_pytrends",
  "count": 15
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "message": "Failed to fetch Google Trends data",
  "timestamp": "ISO-8601"
}
```

---

## 🐛 Troubleshooting

### Build Fails: "cargo: command not found"

**Fix:** Add buildpack for Rust

In Netlify dashboard:
1. Site settings → Build & deploy → Build settings
2. Add build plugin: `@netlify/plugin-rust`

Or add to `netlify.toml`:
```toml
[[plugins]]
  package = "@netlify/plugin-rust"
```

### Function Timeout

**Issue:** `pytrends` takes >10 seconds

**Fix:** Increase function timeout (Pro plan only)

Or optimize the Python function:
```python
# Add timeout parameter
pytrends = TrendReq(hl='en-US', tz=360, timeout=(5, 10))
```

### Empty Trends Array

**Possible causes:**
1. Google Trends rate limiting
2. Invalid region code
3. pytrends API change

**Check logs:**
- Netlify dashboard → Functions → trends → Logs

### CORS Still Happening

**If you still see CORS errors:**

1. Check you're calling `/api/trends` (not full URL)
   - ✅ `fetch('/api/trends')`
   - ❌ `fetch('https://trends.google.com/...')`

2. Verify redirect works:
   ```bash
   curl -I https://your-site.netlify.app/api/trends
   ```
   Should return `200 OK`

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

1. **Already set up!** Netlify watches your GitHub repo
2. Every push to `main` branch triggers new build
3. Changes live in ~2-5 minutes

### Manual Deploy

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

---

## 💰 Cost

**Netlify Free Tier includes:**
- ✅ 100GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ 125,000 serverless function requests/month
- ✅ Custom domain
- ✅ HTTPS

**This project usage:**
- Build: ~5 min/deploy
- Functions: ~1-10 requests/minute (normal usage)
- Bandwidth: ~2MB per user session

**Estimate:** Free tier handles **thousands of visitors/month**

---

## 🎯 Post-Deployment Checklist

- [ ] Visit site URL
- [ ] Click "Fetch Live Trends" button
- [ ] Verify real Google data loads
- [ ] Test different regions (optional)
- [ ] Check function logs in dashboard
- [ ] Update `README.md` with live URL ✅ (already done!)
- [ ] Share on social media 🎉

---

## 🔗 Useful Links

- **Live Site:** https://generative-art-live-trends.netlify.app
- **Netlify Dashboard:** https://app.netlify.com
- **Netlify Docs:** https://docs.netlify.com
- **pytrends Docs:** https://pypi.org/project/pytrends/

---

## 🚨 Security Notes

**API Rate Limiting:**
- Google Trends has informal rate limits
- pytrends handles this automatically
- If you get errors, wait ~1 minute

**No API Keys Required:**
- Google Trends RSS/API is public
- No authentication needed
- Data is publicly available search trends

**Function Security:**
- Netlify auto-handles CORS
- No sensitive data exposed
- All responses are public trending data

---

## 📝 Summary

**What changed from local:**
1. ❌ Mock data → ✅ Real Google Trends
2. ❌ CORS errors → ✅ Same-origin requests
3. ❌ Local server → ✅ Global CDN
4. ❌ Manual WASM builds → ✅ Auto-builds

**What stayed the same:**
- ✅ All visualizations work
- ✅ Seed-based reproducibility
- ✅ Parameter controls
- ✅ PNG export

---

**Need help?** Open an issue on GitHub!
**Everything working?** Share your creations! 🎨
