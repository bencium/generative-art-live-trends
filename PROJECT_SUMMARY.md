# Search Currents - Project Summary

## What We Built

A live Google Trends visualizer that transforms search data into museum-quality generative art, combining Rust + WebAssembly with p5.js for high-performance data-driven visualization.

## Files Created

### Core Application
1. **search_currents.html** (9.8KB)
   - Interactive p5.js visualization
   - Anthropic-inspired UI design
   - Parameter controls for artistic tuning
   - Seed navigation for reproducibility
   - Currently uses mock data (WASM integration ready)

2. **search_currents_philosophy.md** (5.2KB)
   - Algorithmic philosophy document
   - "Search Currents" aesthetic manifesto
   - Computational expression guidelines
   - Parameter space definition

### Rust WASM Module
3. **trends-wasm/** directory
   - `src/lib.rs` - Google Trends API client + data structures
   - `Cargo.toml` - Rust dependencies configured for WASM
   - `pkg/` - Compiled WASM binary + JS bindings

Key Rust functions:
- `TrendsClient::fetch_daily_trends()` - Fetches from Google Trends RSS
- `generate_mock_trends()` - Testing data generator
- `process_trends()` - Data normalization and enrichment
- `calculate_visual_params()` - Trend → visual parameter mapping

### Documentation
4. **README.md** (6.3KB)
   - Complete setup instructions
   - Architecture overview
   - Usage guide
   - API reference
   - Troubleshooting section

5. **PROJECT_SUMMARY.md** (this file)
   - High-level overview
   - Implementation status
   - Next steps

## Current Status

### ✅ Completed
- [x] Algorithmic philosophy creation
- [x] Parameter space design
- [x] HTML viewer with Anthropic branding
- [x] Rust WASM project structure
- [x] Google Trends API client (RSS-based)
- [x] WASM build pipeline (successfully compiled)
- [x] P5.js core algorithm (flow fields)
- [x] Trend data → visual parameter mapping
- [x] Particle systems with trend affinity
- [x] Color mapping (velocity → temperature)
- [x] Seeded randomness (reproducible)
- [x] "Fetch Trends" UI button
- [x] Trends metadata display
- [x] Loading states
- [x] Parameter controls (6 sliders)
- [x] Seed navigation (prev/next/random)
- [x] Export to PNG functionality

### 🚧 In Progress
- [ ] WASM integration in HTML (mock data currently used)
- [ ] JavaScript interface bridging WASM ↔ p5.js
- [ ] CORS handling for Google Trends RSS

### 📋 Remaining Tasks
- [ ] Test WASM module independently
- [ ] Error handling for API failures
- [ ] Cache management for offline viewing
- [ ] WASM performance optimization
- [ ] Cross-browser compatibility testing

## How It Works

### Data Flow
```
Google Trends RSS
      ↓
Rust WASM (fetch + parse)
      ↓
JavaScript (trendsData object)
      ↓
P5.js Flow Field Generation
      ↓
Particle System (6000 agents)
      ↓
Visual Output (HSB color space)
```

### Visual Mapping
```
Search Volume   → Particle density, field strength, saturation
Trend Velocity  → Color hue (rising=warm, falling=cool, stable=blue)
Query Text      → Spatial hash → field attractor position
Categories      → Particle affinity groups
Time            → Noise field evolution (via seed)
```

### Key Algorithms

1. **Flow Field Generation**
   - Multi-octave Perlin noise base layer
   - Trend-driven vortices at hash positions
   - Influence radius based on search volume
   - Rotation direction from velocity sign

2. **Particle Behavior**
   - Follow local flow field vectors
   - Accumulate trails (opacity-based fade)
   - Wrap at canvas edges
   - Color updates per frame based on trend affinity

3. **Color System**
   - HSB color mode for intuitive mapping
   - Hue: 0-45° (reds/oranges) for falling/rising
   - Hue: 200-240° (blues/purples) for stable
   - Saturation/brightness from volume/speed

## Algorithmic Philosophy

From `search_currents_philosophy.md`:

> **Collective attention as electromagnetic fields.** Searches create gravitational influence, rising trends generate heat, particles reveal invisible force patterns. Every parameter was painstakingly tuned through countless iterations—the mark of master-level computational aesthetics.

## Technical Highlights

### Rust + WASM Benefits
- **Performance**: Near-native speed for data processing
- **Type Safety**: Compile-time error checking
- **Size**: Optimized WASM binary (~50KB)
- **Zero Dependencies**: Runs entirely in browser

### P5.js Integration
- **Seeded Randomness**: `randomSeed()` + `noiseSeed()` for reproducibility
- **HSB Color Mode**: Intuitive hue/saturation/brightness mapping
- **Persistent Canvas**: Fade overlay technique for trails
- **Responsive Design**: Scales to viewport size

## Using the System

### Quick Start (Mock Data)
```bash
# Serve the directory
python3 -m http.server 8000

# Open browser
open http://localhost:8000/search_currents.html

# Click interface buttons to explore
```

### With WASM Integration
```bash
# Build WASM (one-time)
cd trends-wasm && wasm-pack build --target web --out-dir pkg

# Update search_currents.html to load WASM
# Add at top of <script> section:
import init, { TrendsClient, generate_mock_trends } from './trends-wasm/pkg/trends_wasm.js';
await init();

# Replace fetchTrendsData() to use WASM
```

## Parameter Reference

| Parameter | Range | Effect |
|-----------|-------|--------|
| Trend Influence | 0.1-3.0 | Field warping strength |
| Noise Scale | 0.001-0.015 | Texture granularity |
| Particle Count | 1000-15000 | Density (↓ performance) |
| Trail Memory | 1-30 | Fade rate (30=slow) |
| Flow Speed | 0.1-3.0 | Particle velocity |
| Color Temperature | 0.3-2.0 | Hue/sat sensitivity |

## Next Steps

### Immediate
1. **Integrate WASM in HTML**
   - Import trends_wasm.js module
   - Replace mock fetchTrendsData() with actual WASM call
   - Handle CORS (proxy or same-origin deployment)

2. **Error Handling**
   - Try/catch around WASM calls
   - Fallback to mock data on failure
   - User-friendly error messages

3. **Testing**
   - Verify WASM loads correctly
   - Test on Chrome, Firefox, Safari
   - Mobile responsiveness check

### Future Enhancements
1. **Data Sources**
   - Official Google Trends API integration
   - Multiple regions (US, GB, JP, etc.)
   - Custom time ranges (hour, day, week)
   - Category filtering (tech, news, sports)

2. **Visualizations**
   - 3D flow fields (Three.js/WebGL)
   - Time-lapse mode (animate trend evolution)
   - Comparison view (two datasets side-by-side)
   - Audio reactivity (trend volume → sound)

3. **Export**
   - SVG export for vector editing
   - Video recording (canvas frames → MP4)
   - Metadata JSON sidecar files
   - Gallery mode (grid of seeds)

4. **Performance**
   - Web Workers for particle updates
   - OffscreenCanvas for background rendering
   - Progressive loading (start with low particle count)
   - GPU acceleration via WebGL

## Design Decisions

### Why Rust + WASM?
- **Performance**: Data processing without blocking UI
- **Learning**: Demonstrate Rust in creative coding
- **Modern Stack**: Cutting-edge web technology

### Why P5.js?
- **Accessibility**: Low barrier to creative coding
- **Community**: Massive ecosystem of examples
- **Simplicity**: Clear, readable code

### Why Flow Fields?
- **Organic**: Natural-looking motion
- **Data-Driven**: Parameters map intuitively to visuals
- **Scalable**: Works from 100 to 100,000 particles

### Why Mock Data Initially?
- **CORS Issues**: Google Trends RSS may block requests
- **Development Speed**: Iterate on visuals without API delays
- **Reliability**: Consistent data for testing parameters

## Credits & Inspiration

- **Chromatic Archaeology**: Original inspiration for data → art
- **Art Blocks**: Seeded randomness approach
- **Tyler Hobbs**: Flow field techniques
- **Perlin/Simplex Noise**: Foundation of organic motion
- **Anthropic Design**: UI aesthetic inspiration

## License

MIT License - Free to use, modify, and distribute

---

**Built with:** Rust, WebAssembly, p5.js, creativity, and lots of parameter tuning ✨
