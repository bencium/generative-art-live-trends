use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use web_sys::{Request, RequestInit, RequestMode, Response};
use wasm_bindgen_futures::JsFuture;

/// Represents a single trending search query
#[derive(Debug, Clone, Serialize, Deserialize)]
#[wasm_bindgen]
pub struct Trend {
    #[wasm_bindgen(skip)]
    pub query: String,
    pub volume: u32,
    pub velocity: i32,  // Positive = rising, negative = falling
    #[wasm_bindgen(skip)]
    pub category: String,
}

#[wasm_bindgen]
impl Trend {
    #[wasm_bindgen(constructor)]
    pub fn new(query: String, volume: u32, velocity: i32, category: String) -> Trend {
        Trend {
            query,
            volume,
            velocity,
            category,
        }
    }

    #[wasm_bindgen(getter)]
    pub fn query(&self) -> String {
        self.query.clone()
    }

    #[wasm_bindgen(getter)]
    pub fn category(&self) -> String {
        self.category.clone()
    }
}

/// Container for all trends data
#[derive(Debug, Serialize, Deserialize)]
pub struct TrendsData {
    pub trends: Vec<Trend>,
    pub timestamp: String,
    pub region: String,
}

#[wasm_bindgen]
pub struct TrendsClient {
    region: String,
}

#[wasm_bindgen]
impl TrendsClient {
    #[wasm_bindgen(constructor)]
    pub fn new(region: Option<String>) -> TrendsClient {
        TrendsClient {
            region: region.unwrap_or_else(|| "US".to_string()),
        }
    }

    /// Fetch daily trending searches using Google Trends RSS feed
    /// Returns JsValue that can be parsed as TrendsData on JS side
    pub async fn fetch_daily_trends(&self) -> Result<JsValue, JsValue> {
        let window = web_sys::window().ok_or("No window object")?;

        // Google Trends RSS feed endpoint
        let url = format!(
            "https://trends.google.com/trends/trendingsearches/daily/rss?geo={}",
            self.region
        );

        // Create fetch request
        let mut opts = RequestInit::new();
        opts.method("GET");
        opts.mode(RequestMode::Cors);

        let request = Request::new_with_str_and_init(&url, &opts)?;

        request
            .headers()
            .set("Accept", "application/rss+xml, application/xml, text/xml")?;

        // Perform fetch
        let resp_value = JsFuture::from(window.fetch_with_request(&request)).await?;
        let resp: Response = resp_value.dyn_into()?;

        // Get response text
        let text = JsFuture::from(resp.text()?).await?;
        let xml_text = text.as_string().ok_or("Failed to get response text")?;

        // Parse XML and convert to trends data
        let trends_data = self.parse_rss_feed(&xml_text)?;

        // Serialize to JsValue
        Ok(serde_wasm_bindgen::to_value(&trends_data)?)
    }

    /// Parse RSS XML feed into structured trends data
    fn parse_rss_feed(&self, xml: &str) -> Result<TrendsData, JsValue> {
        // Simple XML parsing - extract trend items
        // In production, use a proper XML parser crate
        let mut trends = Vec::new();

        // Extract <title> tags (these contain the search queries)
        // This is a simplified parser - consider using xml-rs or quick-xml for production
        let mut in_item = false;
        let mut current_query = String::new();

        for line in xml.lines() {
            let trimmed = line.trim();

            if trimmed.starts_with("<item>") {
                in_item = true;
            } else if trimmed.starts_with("</item>") {
                if !current_query.is_empty() {
                    // Add trend with estimated metrics
                    // In real implementation, extract these from RSS data
                    trends.push(Trend {
                        query: current_query.clone(),
                        volume: 50 + (trends.len() as u32 * 7) % 50,  // Mock volume
                        velocity: ((trends.len() as i32 * 13) % 100) - 50,  // Mock velocity
                        category: "Trending".to_string(),
                    });
                    current_query.clear();
                }
                in_item = false;
            } else if in_item && trimmed.starts_with("<title>") {
                // Extract title text
                if let Some(start) = trimmed.find(">") {
                    if let Some(end) = trimmed.rfind("</title>") {
                        current_query = trimmed[start + 1..end].to_string();
                    }
                }
            }
        }

        Ok(TrendsData {
            trends: trends.into_iter().take(25).collect(),  // Top 25 trends
            timestamp: js_sys::Date::new_0().to_iso_string().into(),
            region: self.region.clone(),
        })
    }
}

/// Utility function to generate mock trends data for testing
#[wasm_bindgen]
pub fn generate_mock_trends(count: usize) -> Result<JsValue, JsValue> {
    let queries = vec![
        ("AI developments", "Technology"),
        ("Climate summit 2025", "News"),
        ("Cryptocurrency markets", "Finance"),
        ("Space exploration", "Science"),
        ("Election results", "Politics"),
        ("Health guidelines", "Health"),
        ("Tech IPO news", "Business"),
        ("Gaming console launch", "Technology"),
        ("Scientific breakthrough", "Science"),
        ("Food trends 2025", "Lifestyle"),
        ("Travel destinations", "Travel"),
        ("Fashion week highlights", "Fashion"),
        ("Renewable energy breakthrough", "Science"),
        ("Global economic outlook", "Business"),
        ("Medical research advances", "Health"),
        ("Smart city initiatives", "Technology"),
        ("Humanitarian crisis response", "News"),
        ("Cybersecurity threats", "Technology"),
        ("Housing market trends", "Finance"),
        ("Educational reform debate", "Politics"),
        ("Autonomous vehicle testing", "Technology"),
        ("Wildfire season updates", "News"),
        ("Plant-based nutrition", "Lifestyle"),
        ("Arctic ice melt data", "Science"),
        ("Inflation rate changes", "Finance"),
    ];

    let trends: Vec<Trend> = queries
        .into_iter()
        .take(count)
        .enumerate()
        .map(|(i, (query, category))| {
            Trend {
                query: query.to_string(),
                volume: 100 - (i as u32 * 5),
                velocity: ((i as i32 * 17) % 100) - 50,
                category: category.to_string(),
            }
        })
        .collect();

    let trends_data = TrendsData {
        trends,
        timestamp: js_sys::Date::new_0().to_iso_string().into(),
        region: "GLOBAL".to_string(),
    };

    Ok(serde_wasm_bindgen::to_value(&trends_data)?)
}

/// Process and enrich trends data with computed metrics
#[wasm_bindgen]
pub fn process_trends(trends_json: JsValue) -> Result<JsValue, JsValue> {
    let mut data: TrendsData = serde_wasm_bindgen::from_value(trends_json)?;

    // Normalize volumes to 0-100 scale
    if let Some(max_volume) = data.trends.iter().map(|t| t.volume).max() {
        if max_volume > 0 {
            for trend in &mut data.trends {
                trend.volume = ((trend.volume as f32 / max_volume as f32) * 100.0) as u32;
            }
        }
    }

    // Sort by volume (descending)
    data.trends.sort_by(|a, b| b.volume.cmp(&a.volume));

    Ok(serde_wasm_bindgen::to_value(&data)?)
}

/// Calculate visual parameters for a trend
#[wasm_bindgen]
pub fn calculate_visual_params(volume: u32, velocity: i32) -> JsValue {
    #[derive(Serialize)]
    struct VisualParams {
        hue: f32,
        saturation: f32,
        brightness: f32,
        particle_density: f32,
        field_strength: f32,
    }

    let params = VisualParams {
        hue: if velocity > 20 {
            // Rising = warm (yellow-orange)
            25.0 + (velocity as f32 / 100.0) * 20.0
        } else if velocity < -20 {
            // Falling = red
            0.0 + ((velocity.abs() as f32 / 100.0) * 15.0)
        } else {
            // Stable = blue-purple
            200.0 + (velocity as f32 / 40.0) * 40.0
        },
        saturation: 30.0 + (volume as f32 / 100.0) * 60.0,
        brightness: 40.0 + (volume as f32 / 100.0) * 50.0,
        particle_density: (volume as f32 / 100.0),
        field_strength: (volume as f32 / 100.0) * (1.0 + velocity.abs() as f32 / 100.0),
    };

    serde_wasm_bindgen::to_value(&params).unwrap()
}

#[wasm_bindgen(start)]
pub fn main() {
    // Set panic hook for better error messages in console
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}
