# Search Currents - Live Google Trends Visualizer

> **Museum-quality algorithmic art visualization of collective attention**
> Transforming Google Trends data into living, breathing generative art using Rust + WebAssembly and p5.js

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Rust](https://img.shields.io/badge/rust-1.70+-orange.svg)
![WASM](https://img.shields.io/badge/wasm-ready-green.svg)

---

## ✨ Overview

Search Currents transforms billions of Google search queries into electromagnetic rivers of attention. Trending topics create vortices, rising trends generate heat, and the zeitgeist emerges as visible field lines in computational noise—all powered by real-time data and high-performance WebAssembly.

**Live Demo:** [Coming Soon]

---

## 🎯 Key Features

### Visual System
- **Flow Field Algorithm** - Perlin noise-based particle physics
- **6,000 Particles** - Following electromagnetic currents at 60fps
- **Data-Driven Vortices** - Trending searches create field attractors
- **HSB Color Mapping** - Rising trends = warm, falling = cool, stable = blue
- **Trail Rendering** - Ghostly histories with opacity fade
- **Seed-Based Reproducibility** - Same seed + data = identical artwork

### Interactive Controls
- **6 Parameter Sliders** - Fine-tune the visualization aesthetics
  - Trend Influence (field warping strength)
  - Noise Scale (texture granularity)
  - Particle Count (density control)
  - Trail Memory (fade rate)
  - Flow Speed (animation velocity)
  - Color Temperature (saturation)
- **Seed Navigation** - Previous/Next/Random exploration
- **Manual Seed Input** - Jump to specific variations
- **PNG Export** - Download 1200x1200px artwork with timestamp

### Rust + WebAssembly Backend
- **High Performance** - Near-native speed data processing
- **Type Safety** - Compile-time error checking
- **Zero Dependencies** - Runs entirely in browser
- **Optimized Binary** - <100KB WASM module
- **Four Core Functions:**
  - `generate_mock_trends()` - Test data generation
  - `process_trends()` - Normalization and sorting
  - `calculate_visual_params()` - Data → visual mapping
  - `TrendsClient` - Google Trends RSS fetching

### Smart Data Management
- **Mock Data** - Instant testing with generated trends
- **Live RSS Fetching** - Real Google Trends (CORS-aware)
- **LocalStorage Cache** - Persists across browser sessions
- **Graceful Fallbacks** - Handles network errors elegantly
- **Error Recovery** - Never crashes, always displays something

---

## 🚀 Quick Start

### Option 1: Instant Preview (Mock Data)

```bash
# Clone the repository
git clone https://github.com/bencium/generative-art-live-trends.git
cd generative-art-live-trends

# Start local server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000/search_currents.html
```

**Then:**
1. Click "🔄 Fetch Live Trends" → See flowing particles
2. Use Next/Prev to explore variations
3. Adjust sliders to customize aesthetics
4. Download PNG exports for printing

### Option 2: Full WASM Integration

```bash
# Install Rust and wasm-pack (one-time setup)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install wasm-pack

# Build WASM module
cd trends-wasm
wasm-pack build --target web --out-dir pkg
cd ..

# Start server and open
python3 -m http.server 8000
open http://localhost:8000/search_currents_wasm.html
```

**Advanced Features:**
- Click "📊 Mock Data" → WASM-generated trends
- Click "🌐 Live RSS" → Real Google Trends (may hit CORS)
- Data persists in cache across refreshes

### Option 3: Unit Testing

```bash
# Open WASM test console
open http://localhost:8000/test_wasm.html
```

Auto-runs 4 unit tests on the Rust module!

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│         User Interface (HTML)               │
│  ┌────────────┐  ┌─────────────────────┐  │
│  │  Controls  │  │   Canvas (p5.js)   │  │
│  │  Sliders   │  │   1200x1200px      │  │
│  │  Buttons   │  │   Particles        │  │
│  └────────────┘  └─────────────────────┘  │
└───────┬─────────────────────┬──────────────┘
        │                     │
        │                     │
    ┌───▼──────────┐    ┌────▼───────────┐
    │ WASM Module  │    │  P5.js Engine  │
    │ (Rust)       │    │  (JavaScript)  │
    ├──────────────┤    ├────────────────┤
    │ Fetch RSS    │    │ Flow Field     │
    │ Generate     │    │ Particles      │
    │ Process      │    │ Color Mapping  │
    │ Calculate    │    │ Rendering      │
    └──────┬───────┘    └────────────────┘
           │
    ┌──────▼───────────┐
    │  Google Trends   │
    │  RSS Feed        │
    │  (CORS aware)    │
    └──────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | p5.js | Generative visualization |
| Data Processing | Rust + WASM | High-performance trend handling |
| Styling | Custom CSS | Anthropic-inspired design |
| Build | wasm-pack | WASM compilation |
| Deployment | Static Hosting | Zero backend required |

---

## 📂 File Structure

```
generative-art-live-trends/
├── search_currents.html           # Standalone version (mock data)
├── search_currents_wasm.html      # Full WASM integration
├── test_wasm.html                 # Unit testing console
├── trends-wasm/                   # Rust WASM module
│   ├── src/
│   │   └── lib.rs                # Main Rust implementation
│   ├── Cargo.toml                # Dependencies
│   └── pkg/                      # Compiled WASM (after build)
│       ├── trends_wasm.js        # JS bindings
│       ├── trends_wasm_bg.wasm   # Binary module
│       └── trends_wasm.d.ts      # TypeScript definitions
├── search_currents_philosophy.md  # Algorithmic art manifesto
├── QUICKSTART.md                  # 2-minute test guide
├── TESTING_GUIDE.md               # Comprehensive QA procedures
├── PROJECT_SUMMARY.md             # Implementation overview
├── DELIVERABLES.md                # Complete file inventory
└── README.md                      # This file
```

---

## 🎨 How It Works

### Data → Visual Mapping

```
Google Trends Data          Visual Manifestation
───────────────────         ────────────────────
Search Volume (0-100)   →   Particle density, field strength
Trend Velocity (+/-)    →   Color hue (warm/cool/neutral)
Query Text              →   Vortex position (spatial hash)
Time Patterns           →   Noise field evolution
Sentiment               →   Saturation & brightness
```

### Color System (HSB)

| Trend State | Hue Range | Visual Effect |
|-------------|-----------|---------------|
| Rising Fast (+20 to +100) | 25-45° | Yellow-orange (heat) |
| Falling (-100 to -20) | 0-15° | Red (cooling) |
| Stable (-20 to +20) | 200-240° | Blue-purple (calm) |

**Saturation:** Based on search volume (higher volume = more saturated)
**Brightness:** Based on particle speed (faster = brighter)

### Flow Field Algorithm

1. Generate Perlin noise base layer across canvas
2. For each trending search:
   - Hash query text → field position
   - Create vortex at position (radius ∝ volume)
   - Rotation direction from velocity sign
3. Particles follow combined vector field
4. Trails fade via opacity decay
5. Edge wrapping (toroidal topology)

---

## 🎮 Usage Guide

### Suggested Parameter Combos

**Chaotic Energy:**
```
Trend Influence: 2.5
Particle Count: 12000
Flow Speed: 2.0
Color Temperature: 1.8
```

**Meditative Flow:**
```
Noise Scale: 0.002
Trail Memory: 25
Flow Speed: 0.3
Color Temperature: 0.8
```

**High Contrast:**
```
Color Temperature: 1.8
Particle Count: 8000
Trend Influence: 1.5
```

**Minimalist:**
```
Particle Count: 2000
Trail Memory: 5
Noise Scale: 0.01
```

### Seed Exploration Tips

1. **Start with ranges:** Try 1000-2000, 42000-43000
2. **Look for patterns:** Adjacent seeds often share aesthetics
3. **Document favorites:** Note seed + parameters for reproducibility
4. **Extreme values:** Sometimes the best art is at parameter limits
5. **Let it evolve:** Some seeds need 30+ seconds to develop fully

---

## 🛠️ Development

### Prerequisites

- **Rust** (1.70+): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- **wasm-pack**: `cargo install wasm-pack`
- **Modern Browser**: Chrome, Firefox, Safari, or Edge

### Building from Source

```bash
# Clone repository
git clone https://github.com/bencium/generative-art-live-trends.git
cd generative-art-live-trends

# Build WASM module
cd trends-wasm
wasm-pack build --target web --out-dir pkg
cd ..

# Test locally
python3 -m http.server 8000
```

### Modifying the Visualization

**Edit `search_currents.html`:**
```javascript
// Line ~420: Parameters
let params = {
    seed: 12345,
    trendInfluence: 1.0,
    particleCount: 6000,
    // ... customize defaults
};

// Line ~500+: Flow field generation
function generateFlowField() {
    // Modify noise algorithm
}

// Line ~600+: Particle class
class Particle {
    // Customize behavior
}
```

### Modifying the WASM Module

**Edit `trends-wasm/src/lib.rs`:**
```rust
// Add custom data source
impl TrendsClient {
    pub async fn fetch_custom_api(&self) -> Result<JsValue, JsValue> {
        // Your implementation
    }
}

// Modify visual mapping
pub fn calculate_visual_params(volume: u32, velocity: i32) -> JsValue {
    // Custom color/parameter logic
}
```

**Rebuild:**
```bash
cd trends-wasm
wasm-pack build --target web --out-dir pkg
```

---

## 🔌 API Reference

### WASM Module Functions

```javascript
import init, {
    TrendsClient,
    generate_mock_trends,
    process_trends,
    calculate_visual_params
} from './trends-wasm/pkg/trends_wasm.js';

// Initialize (required once)
await init();

// Generate mock data
const mockData = generate_mock_trends(15);
// Returns: { trends: [...], timestamp: "...", region: "GLOBAL" }

// Fetch live trends
const client = new TrendsClient("US");  // US, GB, DE, FR, JP, etc.
const liveData = await client.fetch_daily_trends();
// Returns: { trends: [...], timestamp: "...", region: "US" }

// Process and normalize
const processed = process_trends(rawData);
// Normalizes volumes to 0-100, sorts by volume

// Calculate visual parameters
const visual = calculate_visual_params(75, 30);
// Args: volume (0-100), velocity (-100 to +100)
// Returns: { hue, saturation, brightness, particle_density, field_strength }
```

### Trend Data Structure

```javascript
{
    "trends": [
        {
            "query": "AI developments",
            "volume": 85,          // Normalized 0-100
            "velocity": 42,        // -100 (falling) to +100 (rising)
            "category": "Technology"
        },
        // ... more trends
    ],
    "timestamp": "2025-10-18T15:30:00Z",
    "region": "US"
}
```

---

## 🧪 Testing

### Quick Test (2 minutes)

```bash
# 1. Start server
python3 -m http.server 8000

# 2. Test WASM module
open http://localhost:8000/test_wasm.html
# Should see: ✅ WASM module loaded successfully

# 3. Test visualization
open http://localhost:8000/search_currents.html
# Click "Fetch Live Trends" → particles flow

# 4. Test WASM integration
open http://localhost:8000/search_currents_wasm.html
# Click "Mock Data" → trends via WASM
```

### Automated Tests

See `TESTING_GUIDE.md` for:
- 25+ test scenarios
- Performance benchmarks
- Browser compatibility matrix
- Debugging common issues

---

## 🐛 Troubleshooting

### CORS Errors (Expected)

**Problem:** Google Trends RSS blocks cross-origin requests

**Solutions:**
1. ✅ Use mock data ("📊 Mock Data" button)
2. ✅ Deploy with CORS proxy
3. ✅ Load cached data (persists automatically)
4. ⚠️ Live RSS works only with proxy/same-origin deployment

**Note:** This is standard browser security, not a bug!

### WASM Not Loading

**Check:**
- [ ] Using local server (not `file://`)
- [ ] `trends-wasm/pkg/` directory exists
- [ ] No 404 errors in browser console

**Fix:**
```bash
cd trends-wasm
wasm-pack build --target web --out-dir pkg
```

### Slow Performance

**Optimize:**
- Reduce particle count (try 3000)
- Lower trail memory (< 10)
- Close other browser tabs
- Use Chrome (fastest p5.js performance)

**Performance Targets:**
- 6K particles: ~60fps (default)
- 10K particles: ~40fps
- 15K particles: ~20-30fps

### Cache Won't Clear

**Reset:**
```javascript
// In browser console:
localStorage.removeItem('search_currents_cache');
location.reload();
```

---

## 🎓 Use Cases

### Data Visualization
"Transform dry analytics into engaging art for presentations"

### Creative Coding Education
"Teach flow fields, Perlin noise, particle systems, and WASM"

### Rust + WASM Showcase
"Demonstrate WebAssembly in real-world creative application"

### Generative Art Exhibitions
"Create series of prints from trending data (300 DPI ready)"

### UX Design Case Study
"Example of data-driven, interactive, accessible visualization"

---

## 🌟 Algorithmic Philosophy

From `search_currents_philosophy.md`:

> In the digital cosmos, billions of human curiosities converge into electromagnetic rivers of attention. Every search query—from the mundane to the profound—adds its quantum of interest to vast currents flowing through informational space. These are not random eddies but organized fields of collective consciousness, where trending topics create powerful vortices that pull in surrounding attention, while fading interests dissipate like cooling plasma into the background radiation of the web.

**Core Principles:**
- **Emergence** - Complexity from simple rules
- **Data Honesty** - Direct mathematical mapping
- **Computational Craft** - Every parameter meticulously tuned
- **Reproducibility** - Seeded randomness enables variations
- **Living Systems** - Continuous evolution, never static

---

## 🤝 Contributing

Contributions welcome! This project showcases:
- Rust + WASM for creative coding
- Data-driven generative art
- Real-time API integration
- Museum-quality computational aesthetics

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions

- [ ] Additional data sources (Twitter, Reddit, etc.)
- [ ] 3D visualization mode (Three.js/WebGL)
- [ ] Video export (canvas → MP4)
- [ ] Mobile-optimized version
- [ ] Audio reactivity
- [ ] Gallery mode (grid of seeds)
- [ ] Social sharing integration
- [ ] Custom color palettes
- [ ] Performance optimizations

---

## 📜 License

**MIT License**

Copyright (c) 2025 Search Currents Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🙏 Acknowledgments

**Project Credits:**
- **Concept** - Inspired by Anthropic Claude Code skills cookbook
- **Architecture & Design** - Bence Csernak / [Bencium.io](https://bencium.io)

**Technology & Inspiration:**
- **Google Trends** - Data source and inspiration
- **p5.js Community** - Creative coding tools and examples
- **Rust + WASM Ecosystem** - Enabling high-performance web applications
- **Anthropic** - Design system inspiration
- **Processing Foundation** - Generative art pioneers
- **Art Blocks** - Seeded randomness methodology

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Total Files | 11 |
| Lines of Code | ~1,800 |
| Documentation Words | ~12,000 |
| WASM Compile Time | 90 seconds |
| Page Load Time | < 2 seconds |
| Default Frame Rate | ~60fps |
| Browser Support | 4 major browsers |
| License | MIT (100% open source) |

---

## 🔗 Links

- **Repository:** https://github.com/bencium/generative-art-live-trends
- **Issues:** https://github.com/bencium/generative-art-live-trends/issues
- **Documentation:** See `QUICKSTART.md`, `TESTING_GUIDE.md`, `PROJECT_SUMMARY.md`
- **Philosophy:** `search_currents_philosophy.md`

---

## 📧 Contact & Support

- **Questions?** Open an issue
- **Ideas?** Start a discussion
- **Bugs?** Report with browser console logs

---

**Built with Rust, WebAssembly, p5.js, creativity, and lots of parameter tuning** ✨

**Explore the currents of collective attention** 🌊
