#!/usr/bin/env python3
"""
Generate HTML mockup artifacts for all 10 Theme Factory themes
Shows how each theme looks when applied to actual presentation content
"""

# Theme definitions
themes = [
    {
        "name": "Ocean Depths",
        "description": "Professional and calming maritime theme",
        "colors": {
            "primary": "#1a2332",
            "accent": "#2d8b8b",
            "secondary": "#a8dadc",
            "light": "#f1faee"
        },
        "fonts": {
            "header": "Georgia, serif",  # Using web-safe fonts
            "body": "Arial, sans-serif"
        },
        "use_case": "Corporate Quarterly Review"
    },
    {
        "name": "Sunset Boulevard",
        "description": "Warm and vibrant sunset colors",
        "colors": {
            "primary": "#264653",
            "accent": "#e76f51",
            "secondary": "#f4a261",
            "light": "#e9c46a"
        },
        "fonts": {
            "header": "Georgia, serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Creative Campaign Pitch"
    },
    {
        "name": "Forest Canopy",
        "description": "Natural and grounded earth tones",
        "colors": {
            "primary": "#2d4a2b",
            "accent": "#7d8471",
            "secondary": "#a4ac86",
            "light": "#faf9f6"
        },
        "fonts": {
            "header": "Georgia, serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Sustainability Report 2024"
    },
    {
        "name": "Modern Minimalist",
        "description": "Clean and contemporary grayscale",
        "colors": {
            "primary": "#36454f",
            "accent": "#708090",
            "secondary": "#d3d3d3",
            "light": "#ffffff"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Product Design Portfolio"
    },
    {
        "name": "Golden Hour",
        "description": "Rich and warm autumnal palette",
        "colors": {
            "primary": "#4a403a",
            "accent": "#f4a900",
            "secondary": "#c1666b",
            "light": "#d4b896"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Artisan Coffee Brand"
    },
    {
        "name": "Arctic Frost",
        "description": "Cool and crisp winter-inspired theme",
        "colors": {
            "primary": "#4a6fa5",
            "accent": "#d4e4f7",
            "secondary": "#c0c0c0",
            "light": "#fafafa"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Healthcare Innovation"
    },
    {
        "name": "Desert Rose",
        "description": "Soft and sophisticated dusty tones",
        "colors": {
            "primary": "#5d2e46",
            "accent": "#d4a5a5",
            "secondary": "#b87d6d",
            "light": "#e8d5c4"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Fashion Collection Launch"
    },
    {
        "name": "Tech Innovation",
        "description": "Bold and modern tech aesthetic",
        "colors": {
            "primary": "#1e1e1e",
            "accent": "#0066ff",
            "secondary": "#00ffff",
            "light": "#ffffff"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "AI Platform Demo"
    },
    {
        "name": "Botanical Garden",
        "description": "Fresh and organic garden colors",
        "colors": {
            "primary": "#4a7c59",
            "accent": "#f9a620",
            "secondary": "#b7472a",
            "light": "#f5f3ed"
        },
        "fonts": {
            "header": "Georgia, serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Farm-to-Table Restaurant"
    },
    {
        "name": "Midnight Galaxy",
        "description": "Dramatic and cosmic deep tones",
        "colors": {
            "primary": "#2b1e3e",
            "accent": "#4a4e8f",
            "secondary": "#a490c2",
            "light": "#e6e6fa"
        },
        "fonts": {
            "header": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "use_case": "Gaming Platform Launch"
    }
]

def generate_mockup(theme):
    """Generate HTML mockup for a single theme"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{theme['name']} - Theme Mockup</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: {theme['fonts']['body']};
            background: {theme['colors']['light']};
            padding: 40px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        /* Slide 1: Title Slide */
        .slide {{
            background: {theme['colors']['primary']};
            color: {theme['colors']['light']};
            padding: 80px;
            margin-bottom: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 600px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .slide h1 {{
            font-family: {theme['fonts']['header']};
            font-size: 72px;
            font-weight: bold;
            margin-bottom: 20px;
            color: {theme['colors']['accent']};
        }}

        .slide h2 {{
            font-family: {theme['fonts']['header']};
            font-size: 36px;
            font-weight: normal;
            margin-bottom: 40px;
            color: {theme['colors']['secondary']};
        }}

        .slide p {{
            font-size: 20px;
            line-height: 1.6;
            color: {theme['colors']['light']};
        }}

        /* Slide 2: Content Slide */
        .slide.content {{
            background: {theme['colors']['light']};
            color: {theme['colors']['primary']};
        }}

        .slide.content h2 {{
            font-size: 48px;
            color: {theme['colors']['primary']};
            border-bottom: 4px solid {theme['colors']['accent']};
            padding-bottom: 20px;
            margin-bottom: 40px;
        }}

        .slide.content h3 {{
            font-size: 28px;
            color: {theme['colors']['accent']};
            margin-top: 30px;
            margin-bottom: 15px;
        }}

        .slide.content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .slide.content li {{
            font-size: 20px;
            line-height: 1.8;
            margin-bottom: 15px;
            padding-left: 30px;
            position: relative;
        }}

        .slide.content li:before {{
            content: "▸";
            position: absolute;
            left: 0;
            color: {theme['colors']['accent']};
            font-weight: bold;
        }}

        /* Slide 3: Data Slide */
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 40px;
        }}

        .stat-card {{
            background: {theme['colors']['secondary']};
            padding: 40px;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-number {{
            font-size: 64px;
            font-weight: bold;
            color: {theme['colors']['primary']};
            margin-bottom: 10px;
        }}

        .stat-label {{
            font-size: 18px;
            color: {theme['colors']['primary']};
            opacity: 0.8;
        }}

        .theme-info {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            margin-top: 40px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}

        .theme-info h3 {{
            font-family: {theme['fonts']['header']};
            color: {theme['colors']['primary']};
            margin-bottom: 20px;
        }}

        .color-palette {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}

        .color-swatch {{
            flex: 1;
            height: 100px;
            border-radius: 8px;
            display: flex;
            align-items: flex-end;
            padding: 10px;
            color: white;
            font-size: 12px;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Title Slide -->
        <div class="slide">
            <h1>{theme['use_case']}</h1>
            <h2>{theme['description']}</h2>
            <p>Demonstrating the <strong>{theme['name']}</strong> theme with professional presentation content</p>
        </div>

        <!-- Content Slide -->
        <div class="slide content">
            <h2>Key Objectives</h2>

            <h3>Strategic Priorities</h3>
            <ul>
                <li>Drive innovation and sustainable growth</li>
                <li>Enhance customer experience across all touchpoints</li>
                <li>Build high-performing teams with clear accountability</li>
                <li>Leverage data-driven insights for decision making</li>
            </ul>

            <h3>Success Metrics</h3>
            <ul>
                <li>Quarterly revenue growth targets exceeded</li>
                <li>Customer satisfaction scores above 90%</li>
                <li>Team engagement and retention rates improved</li>
            </ul>
        </div>

        <!-- Stats Slide -->
        <div class="slide content">
            <h2>Performance Highlights</h2>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">247%</div>
                    <div class="stat-label">Growth Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">15K+</div>
                    <div class="stat-label">Active Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">98%</div>
                    <div class="stat-label">Satisfaction</div>
                </div>
            </div>
        </div>

        <!-- Theme Info -->
        <div class="theme-info">
            <h3>{theme['name']} Theme Specifications</h3>
            <p><strong>Description:</strong> {theme['description']}</p>
            <p style="margin-top: 10px;"><strong>Header Font:</strong> {theme['fonts']['header']}</p>
            <p><strong>Body Font:</strong> {theme['fonts']['body']}</p>

            <div class="color-palette">
                <div class="color-swatch" style="background: {theme['colors']['primary']};">
                    {theme['colors']['primary']}
                </div>
                <div class="color-swatch" style="background: {theme['colors']['accent']};">
                    {theme['colors']['accent']}
                </div>
                <div class="color-swatch" style="background: {theme['colors']['secondary']};">
                    {theme['colors']['secondary']}
                </div>
                <div class="color-swatch" style="background: {theme['colors']['light']}; color: black;">
                    {theme['colors']['light']}
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    return html

# Generate all mockups
for theme in themes:
    filename = theme['name'].lower().replace(' ', '-')
    filepath = f'theme-mockup-{filename}.html'

    with open(filepath, 'w') as f:
        f.write(generate_mockup(theme))

    print(f"✓ Created: {filepath}")

print(f"\n✓ All {len(themes)} theme mockups generated successfully!")
print("Open any HTML file in a browser to see the theme in action.")
