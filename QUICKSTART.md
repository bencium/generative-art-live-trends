# Search Currents - Quick Start Guide

## Test the Visualization in 2 Minutes

### Step 1: Start a Local Server

Choose one method:

```bash
# Option A: Python (if installed)
python3 -m http.server 8000

# Option B: Node.js (if installed)
npx serve .

# Option C: Rust (if cargo is available)
cargo install basic-http-server
basic-http-server .
```

### Step 2: Open in Browser

Navigate to:
```
http://localhost:8000/search_currents.html
```

You should see **Search Currents** with a flowing particle visualization!

### Step 3: Explore the Interface

#### Load Trends Data
1. Click **"🔄 Fetch Live Trends"** button
2. Watch the visualization regenerate with data-driven patterns
3. See top trends listed in the Data Source section

#### Play with Seeds
- **Next →**: Explore variation 12346
- **← Prev**: Go back to variation 12344
- **↻ Random**: Generate unexpected seed
- **Seed input**: Type any number (try: 42, 1337, 99999)

#### Adjust Parameters
Try these combinations:

**Chaotic Energy**
- Trend Influence: 2.5
- Particle Count: 12000
- Flow Speed: 2.0

**Meditative Flow**
- Noise Scale: 0.002
- Trail Memory: 25
- Flow Speed: 0.3

**High Contrast**
- Color Temperature: 1.8
- Particle Count: 8000
- Trend Influence: 1.5

#### Export Your Art
Click **"⬇ Download PNG"** to save the current frame with metadata timestamp.

## What You're Seeing

### Visual Elements
- **Flowing Lines**: Particles following electromagnetic field currents
- **Warm Colors** (Orange/Yellow): Rising search trends
- **Cool Colors** (Blue/Purple): Stable search trends
- **Red Tones**: Declining search trends
- **Dense Clusters**: High-volume trending searches
- **Sparse Regions**: Low search activity

### How Data Maps to Art
```
Google Trend → Visual Effect
─────────────────────────────
Search Volume → Particle density, field strength
Rising Trend  → Warm hues (yellows/oranges), faster particles
Falling Trend → Red hues, slower particles
Stable Trend  → Cool hues (blues/purples)
Query Text    → Position of field vortex
```

## Troubleshooting

### "Search Currents" doesn't load
- **Problem**: Blank white screen
- **Solution**: Check browser console (F12), ensure server is running

### Visualization is choppy
- **Problem**: Low frame rate
- **Solution**: Reduce particle count (try 3000)

### "Fetch Trends" doesn't work
- **Problem**: CORS errors in console
- **Current Status**: Using mock data (8 sample trends)
- **Future**: Will connect to real Google Trends RSS via WASM

## Next: Integrate Real Data

To connect real Google Trends (advanced):

1. The WASM module is already built in `trends-wasm/pkg/`
2. Edit `search_currents.html` to import WASM:
```javascript
// Add at top of <script> section
import init, { generate_mock_trends } from './trends-wasm/pkg/trends_wasm.js';
await init();

// In fetchTrendsData(), replace setTimeout with:
const wasmData = generate_mock_trends(15);
trendsData = JSON.parse(JSON.stringify(wasmData));
```

3. For live RSS data, handle CORS via proxy or server deployment

## Understanding the Algorithm

### Flow Field Technique
1. Generate Perlin noise field across canvas
2. For each trend, create vortex at hashed position
3. Vortex strength = search volume
4. Vortex rotation = trend velocity direction
5. Particles follow combined vector field
6. Trails fade over time (opacity decay)

### Color Theory
- **Hue**: Maps to trend velocity (-100 to +100)
  - Negative (falling): 0-15° (reds)
  - Positive (rising): 25-45° (yellows/oranges)
  - Neutral (stable): 200-240° (blues/purples)
- **Saturation**: Maps to search volume (0-100)
- **Brightness**: Maps to particle speed

### Reproducibility
- Same seed + same data = identical output
- Useful for creating variations or "editions"
- Art Blocks-style generative approach

## Keyboard Shortcuts (Future)
```
Space     - Pause/resume
R         - Regenerate (new seed)
E         - Export PNG
1-9       - Quick presets
```

## Tips for Beautiful Results

1. **Let it run**: Some seeds need 30+ seconds to develop
2. **Contrast is key**: High color temperature + varied particle count
3. **Seed hunting**: Try seeds in ranges (1000-2000, 42000-43000)
4. **Parameter combos**: Extreme values often create surprises
5. **Download early**: Good patterns can fade as particles converge

## What Makes This Special?

Unlike typical data visualization:
- **Generative**: Each seed produces unique aesthetic
- **Living**: Continuous motion, never static
- **Data-Driven**: Real search trends influence the algorithm
- **Reproducible**: Same inputs = same output
- **Museum-Quality**: Designed for print and exhibition

## Share Your Discoveries

Found a beautiful seed? Note it down:
```
Seed: _______
Trend Influence: _______
Particle Count: _______
Noise Scale: _______
Description: _______
```

## Further Reading

- `search_currents_philosophy.md` - The artistic vision
- `README.md` - Complete technical documentation
- `PROJECT_SUMMARY.md` - Implementation overview

---

**Ready to explore?** Fire up that server and dive into the currents of collective attention! 🌊
