# Search Currents - Testing Guide

## Test Suite Overview

Three HTML files for different testing scenarios:

1. **test_wasm.html** - WASM module unit tests
2. **search_currents.html** - Original version with mock data
3. **search_currents_wasm.html** - Full WASM integration

## Quick Test: Start Here

### Step 1: Start Local Server

```bash
# From /Users/bencium/eval-demo/
python3 -m http.server 8000
```

### Step 2: Test WASM Module (Unit Tests)

Open: `http://localhost:8000/test_wasm.html`

**Expected Results:**
- ✅ WASM module loads successfully
- ✅ Test 1 passes (mock trends generated)
- ✅ Test 2 passes (data processing works)
- ✅ Test 3 passes (visual params calculated)
- ❌ Test 4 fails (CORS expected - this is normal)

**What to Check:**
- Green "✅" messages in each test section
- JSON data structures displayed correctly
- Test 4 shows CORS error (expected behavior)

### Step 3: Test Original Visualization

Open: `http://localhost:8000/search_currents.html`

**Expected Results:**
- Flowing particle visualization appears
- Click "🔄 Fetch Live Trends" → Mock data loads
- Seed navigation works (Prev/Next/Random)
- Parameter sliders update visualization
- Download PNG creates file

**What to Check:**
- Particles flowing smoothly (~60fps)
- Colors change when clicking "Fetch Trends"
- Sliders respond in real-time
- No console errors

### Step 4: Test WASM Integration

Open: `http://localhost:8000/search_currents_wasm.html`

**Expected Results:**
- "✅ Rust+WASM module ready" shows at top
- Click "📊 Mock Data" → Trends load via WASM
- Click "🌐 Live RSS" → CORS error (expected)
- Visualization updates with WASM-generated data

**What to Check:**
- WASM status indicator shows green checkmark
- Mock data button works (trends appear)
- Live RSS button shows CORS error message
- Cached data persists across refreshes

## Detailed Test Scenarios

### Scenario 1: WASM Module Functions

**File:** `test_wasm.html`

#### Test 1.1: Mock Data Generation
```
Action: Click "Run Test" in Test 1
Expected: JSON array with 10 trend objects
Verify: Each trend has query, volume, velocity, category
```

#### Test 1.2: Data Processing
```
Action: Click "Run Test" in Test 2
Expected: Normalized volumes (0-100), sorted by volume
Verify: Highest volume trend appears first
```

#### Test 1.3: Visual Parameters
```
Action: Click "Run Test" in Test 3
Expected: Hue/saturation/brightness calculated for each case
Verify:
  - Rising trends → hue ~25-45 (warm)
  - Falling trends → hue ~0-15 (red)
  - Stable trends → hue ~200-240 (blue)
```

#### Test 1.4: Live RSS Fetch
```
Action: Click "Run Test" in Test 4
Expected: CORS error (unless using proxy)
Verify: Error message explains CORS and solutions
```

### Scenario 2: Visualization Basics

**File:** `search_currents.html`

#### Test 2.1: Initial Render
```
Setup: Open page
Expected:
  - Particles flowing in organic patterns
  - Default seed: 12345
  - 6000 particles visible
Verify:
  - Canvas is 1200x1200px
  - Smooth animation (~60fps)
  - No loading spinner
```

#### Test 2.2: Data Fetching
```
Action: Click "🔄 Fetch Live Trends"
Expected:
  - Status shows "Loaded 8 trends..."
  - 5 trends listed in UI
  - Visualization regenerates
Verify:
  - Particle colors shift
  - Flow field changes (vortices appear)
  - No console errors
```

#### Test 2.3: Seed Navigation
```
Actions:
  1. Click "Next →"
  2. Click "← Prev"
  3. Click "↻ Random"
  4. Type "42" in seed input
Expected:
  - Each action creates unique pattern
  - Seed number updates in input field
  - Same seed = identical output
Verify:
  - Seed 12345 → 12346 → 12345 looks same
  - Random creates unpredictable seed
  - Typed seed loads correctly
```

#### Test 2.4: Parameter Adjustments
```
Test each slider:

Trend Influence (0.1 → 3.0):
  - Low: Smooth, uniform flow
  - High: Strong vortices, chaotic

Noise Scale (0.001 → 0.015):
  - Low: Large patterns
  - High: Fine texture

Particle Count (1000 → 15000):
  - Low: Sparse, fast
  - High: Dense, may slow down

Trail Memory (1 → 30):
  - Low: Quick fade
  - High: Long trails

Flow Speed (0.1 → 3.0):
  - Low: Slow drift
  - High: Fast movement

Color Temperature (0.3 → 2.0):
  - Low: Muted colors
  - High: Vibrant, saturated
```

#### Test 2.5: Export Functionality
```
Action: Click "⬇ Download PNG"
Expected:
  - PNG file downloads
  - Filename: search-currents-YYYY-MM-DDTHHMM.png
  - Image size: 1200x1200px
Verify:
  - Image matches canvas
  - Timestamp in filename
  - No errors in console
```

### Scenario 3: WASM Integration

**File:** `search_currents_wasm.html`

#### Test 3.1: WASM Loading
```
Setup: Open page
Expected:
  - "⏳ Loading Rust+WASM module..." appears briefly
  - Changes to "✅ Rust+WASM module ready"
  - WASM status bar is green
Verify:
  - Console shows "✅ WASM module loaded successfully"
  - No JavaScript errors
  - Status updates within 1 second
```

#### Test 3.2: Mock Data via WASM
```
Action: Click "📊 Mock Data"
Expected:
  - Status: "Generating mock trends via WASM..."
  - Then: "✅ Loaded 12 mock trends via WASM"
  - 6 trends displayed with volume/velocity
  - Visualization regenerates
Verify:
  - Trend data shows Vol/Vel numbers
  - Particle colors reflect velocities
  - No JavaScript errors
```

#### Test 3.3: Live RSS Attempt
```
Action: Click "🌐 Live RSS"
Expected:
  - Status: "Fetching live Google Trends RSS..."
  - Error: "❌ CORS Error: Trying cached data..."
  - Falls back to cached or mock data
Verify:
  - CORS error is handled gracefully
  - User sees helpful error message
  - App doesn't crash
```

#### Test 3.4: Cache Persistence
```
Actions:
  1. Click "📊 Mock Data"
  2. Refresh page (F5 or Cmd+R)
Expected:
  - After reload: "📦 Loaded X cached trends"
  - Same trends reappear
  - Visualization continues from cached data
Verify:
  - localStorage contains "search_currents_cache"
  - Cached data survives refresh
  - Timestamp preserved
```

#### Test 3.5: Error Handling
```
Test 3.5a: WASM Load Failure
  Simulate: Rename trends-wasm/pkg/ folder
  Expected: "❌ WASM failed to load" message
  Verify: App doesn't crash, shows error

Test 3.5b: Network Timeout
  Action: Click "Live RSS" with network offline
  Expected: CORS error → cache fallback
  Verify: Graceful degradation

Test 3.5c: Invalid Seed
  Action: Type "-5" in seed input
  Expected: Reverts to previous valid seed
  Verify: No broken visualization
```

## Performance Testing

### Frame Rate Check
```
Tools: Chrome DevTools → Performance tab
Actions:
  1. Start recording
  2. Let visualization run for 10 seconds
  3. Stop recording
Expected:
  - ~60fps sustained
  - No major frame drops
  - CPU usage reasonable
Acceptable:
  - 30fps minimum (on older hardware)
  - Brief drops during parameter changes OK
Red Flags:
  - Constant <30fps
  - Freezing or stuttering
  - Memory leaks (increasing usage over time)
```

### Particle Count Scaling
```
Test different counts:
  - 1000 particles: Smooth even on mobile
  - 6000 particles: Default, should be ~60fps
  - 10000 particles: May drop to ~40fps on slower machines
  - 15000 particles: Expect ~20-30fps
```

### Memory Usage
```
Tools: Chrome DevTools → Memory tab
Action: Run for 5 minutes, monitoring memory
Expected:
  - Initial: ~50-100MB
  - Stable: No continuous growth
  - After 5min: <200MB
Red Flag:
  - Continuous increase (memory leak)
  - Crash after extended use
```

## Browser Compatibility

### Desktop Testing Matrix

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | 120+ | ✅ Primary | Best performance |
| Firefox | 120+ | ✅ Supported | Slightly slower |
| Safari | 17+ | ✅ Supported | M1 Macs perform well |
| Edge | 120+ | ✅ Supported | Chromium-based |

### Mobile Testing

| Browser | OS | Expected |
|---------|-------|----------|
| Safari | iOS 17+ | Works, reduce particles to 3000 |
| Chrome | Android 13+ | Works, performance varies |
| Firefox | Android 13+ | Works, may be slower |

**Mobile-Specific Tests:**
- Touch controls for sliders
- Responsive layout (sidebar stacks)
- Performance with lower particle counts

## Debugging Common Issues

### Issue 1: WASM Not Loading
**Symptoms:** "WASM failed to load" error
**Checks:**
- [ ] File exists: `trends-wasm/pkg/trends_wasm.js`
- [ ] File exists: `trends-wasm/pkg/trends_wasm_bg.wasm`
- [ ] Using local server (not `file://`)
- [ ] No 404 errors in console

**Fix:**
```bash
cd trends-wasm
wasm-pack build --target web --out-dir pkg
```

### Issue 2: CORS Errors
**Symptoms:** "CORS blocked" when fetching RSS
**This is expected!** Google Trends blocks cross-origin requests.
**Solutions:**
- Use mock data ("📊 Mock Data" button)
- Deploy to production with CORS proxy
- Use cached data (persists across sessions)

### Issue 3: Slow Performance
**Symptoms:** Choppy animation, low FPS
**Checks:**
- [ ] Reduce particle count (< 6000)
- [ ] Close other tabs
- [ ] Check CPU usage
- [ ] Try different browser

**Optimizations:**
```javascript
// In search_currents_wasm.html, reduce defaults:
particleCount: 3000  // Was 6000
trailDecay: 15       // Was 8 (faster fade = less drawing)
```

### Issue 4: Cache Won't Clear
**Symptoms:** Old trends persist after refresh
**Fix:**
```javascript
// In browser console:
localStorage.removeItem('search_currents_cache');
// Then refresh page
```

### Issue 5: Blank Canvas
**Symptoms:** White rectangle, no particles
**Checks:**
- [ ] Console shows errors?
- [ ] p5.js loaded? (Check Network tab)
- [ ] `initializeSystem()` called?
- [ ] Particle count > 0?

**Debug:**
```javascript
// In browser console:
console.log('Particles:', particles.length);
console.log('Flow field:', flowField.length);
console.log('Params:', params);
```

## Automated Testing (Future)

### Unit Tests (Potential)
```javascript
// tests/wasm.test.js
describe('WASM Module', () => {
  test('generates mock trends', () => {
    const data = generate_mock_trends(10);
    expect(data.trends).toHaveLength(10);
  });

  test('processes trends correctly', () => {
    const mockData = generate_mock_trends(5);
    const processed = process_trends(mockData);
    expect(processed.trends[0].volume).toBeLessThanOrEqual(100);
  });
});
```

### Visual Regression Tests
```javascript
// tests/visual.test.js
// Compare screenshots for same seed
const seed12345 = screenshot({ seed: 12345 });
const seed12345Again = screenshot({ seed: 12345 });
expect(seed12345).toMatchImage(seed12345Again);
```

## Test Reporting Template

```
Test Date: __________
Tester: __________
Browser: __________ (version: _____)
OS: __________

✅ WASM module loads
✅ Mock data generation works
✅ Live RSS (CORS expected)
✅ Visualization renders
✅ Seed navigation
✅ Parameter controls
✅ Cache persistence
✅ Export PNG
✅ Performance (~60fps)
✅ No console errors

Issues Found:
1. ____________________
2. ____________________

Notes:
_______________________
_______________________
```

## Success Criteria

**Minimum Viable:**
- [ ] WASM module loads without errors
- [ ] Mock data generates and displays
- [ ] Visualization animates smoothly
- [ ] Parameters adjust in real-time
- [ ] Export PNG works

**Production Ready:**
- [ ] All above PLUS:
- [ ] Works in Chrome, Firefox, Safari
- [ ] Maintains 30+ FPS on average hardware
- [ ] Cache persists across sessions
- [ ] Graceful CORS error handling
- [ ] No memory leaks after 10min runtime

## Next Steps After Testing

1. **If tests pass:** Deploy to production server
2. **If WASM fails:** Check build process, file paths
3. **If performance issues:** Reduce default particle count
4. **If CORS blocks:** Add proxy server or use mock data only

---

**Ready to test?** Start with `test_wasm.html` to verify the foundation, then move to the full visualizations!
