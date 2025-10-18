# Pre-Deployment Checklist

Use this checklist before deploying to Netlify to ensure everything is ready.

## ✅ Code & Files

- [x] **WASM module builds successfully**
  ```bash
  cd trends-wasm && wasm-pack build --target web
  ```
  Should complete without errors.

- [x] **HTML file exists**: `search_currents_wasm.html`
  - Visualization canvas renders
  - Labels display on trends
  - Hover interactions work
  - Mock data loads (25 trends, no Sports/Entertainment)

- [x] **Index.html redirects correctly** to `search_currents_wasm.html`

- [x] **Netlify configuration** (`netlify.toml`):
  - Build command includes WASM compilation
  - Functions directory set to `netlify/functions`
  - Redirects point to correct files
  - CORS headers configured

- [x] **API function** (`netlify/functions/trends.js`):
  - Multi-region support (8 regions)
  - Deduplication logic
  - Sports/Entertainment filtering
  - Error handling and fallback to NewsAPI

- [x] **Dependencies listed**:
  - `netlify/functions/package.json` has `serpapi`
  - `netlify/functions/requirements.txt` has Python deps (if any)

## ✅ Environment Variables

- [ ] **Get API Keys**:
  - SerpApi key from https://serpapi.com
  - NewsAPI key from https://newsapi.org

- [ ] **Verify .env.example** exists with template

- [ ] **DO NOT commit** actual `.env` file (check `.gitignore`)

## ✅ Testing Locally

### 1. Test WASM Build
```bash
cd trends-wasm
wasm-pack build --target web
# Should see: ✨ Done in X.XXs
```

### 2. Test Local Server
```bash
python3 -m http.server 3000
# Open: http://localhost:3000/search_currents_wasm.html
```

### 3. Test Visualization
- Click "📊 Mock Data"
  - [ ] 25 trends load
  - [ ] No Sports or Entertainment topics
  - [ ] Labels visible on canvas
  - [ ] Hover shows detailed stats
  - [ ] Particles flow correctly

### 4. Test Regeneration
- Click "↻ Random" button
  - [ ] Labels reposition
  - [ ] Particle flow changes
  - [ ] New seed value shown

## ✅ Git & Version Control

- [ ] **Initialize git** (if not done):
  ```bash
  git init
  ```

- [ ] **Check .gitignore** includes:
  ```
  .env
  .env.local
  .DS_Store
  __pycache__/
  ```

- [ ] **Commit all changes**:
  ```bash
  git add .
  git commit -m "Prepare for Netlify deployment"
  ```

- [ ] **Push to remote** (GitHub/GitLab):
  ```bash
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

## ✅ Netlify Setup

- [ ] **Create Netlify account** at https://netlify.com

- [ ] **Connect repository**:
  - New site → Import from Git
  - Select your repo

- [ ] **Verify build settings auto-detected**:
  - Build command: Check from netlify.toml
  - Publish directory: `.`
  - Functions directory: `netlify/functions`

- [ ] **Add environment variables** in Netlify:
  - Site settings → Environment variables
  - Add `SERPAPI_API_KEY`
  - Add `NEWSAPI_KEY`

## ✅ Final Verification

### Before Deploying
- [ ] All code committed and pushed
- [ ] No secrets in repository
- [ ] Build command tested locally
- [ ] Environment variables documented

### After Deploying
- [ ] Visit site URL
- [ ] Test "Mock Data" button works
- [ ] Test "Live RSS" button (if API keys configured)
- [ ] Check Netlify function logs for errors
- [ ] Test API endpoint: `https://your-site.netlify.app/api/trends`

## 🚀 Deploy Commands

### Option 1: Via Netlify Dashboard
1. Click "Deploy site" button
2. Wait for build to complete
3. Check build logs for errors

### Option 2: Via Netlify CLI
```bash
# Install CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod

# Set environment variables
netlify env:set SERPAPI_API_KEY "your_key"
netlify env:set NEWSAPI_KEY "your_key"
```

## 📋 Post-Deployment

- [ ] Site accessible at deployed URL
- [ ] Mock data works
- [ ] API returns global trends
- [ ] No console errors
- [ ] Labels render correctly
- [ ] Hover interactions work

## 🐛 If Build Fails

### Check These Common Issues:

1. **WASM build fails**:
   - Verify Rust/wasm-pack installed in build environment
   - Check netlify.toml build command

2. **Function deployment fails**:
   - Check package.json syntax
   - Verify serpapi dependency listed

3. **Environment variables not working**:
   - Confirm variables added in Netlify dashboard
   - Redeploy site after adding variables

4. **API returns errors**:
   - Check function logs in Netlify dashboard
   - Verify API keys are correct
   - Test API keys independently

---

## ✨ Ready to Deploy!

If all checkboxes above are checked, you're ready to deploy to Netlify!

Follow the [DEPLOYMENT.md](./DEPLOYMENT.md) guide for detailed instructions.
