#!/usr/bin/env python3
"""
Chromatic Archaeology - LIVE DATA VERSION
Museum-quality art visualization of social media trends
Accent clusters represent viral moments from Reddit and Hacker News
"""

import random
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime
from social_data_fetcher import SocialDataFetcher

# Canvas dimensions (high resolution for print quality)
WIDTH = 3000
HEIGHT = 4000

# Refined, sophisticated palette
PALETTE = {
    'bg': (248, 245, 242),
    'strata_1': (162, 142, 126),  # Reddit layer
    'strata_2': (198, 182, 166),
    'strata_3': (82, 92, 102),   # HN layer
    'strata_4': (138, 152, 166),
    'strata_5': (172, 148, 132),
    'strata_6': (112, 106, 98),
    'accent_positive': (88, 168, 128),    # Positive sentiment = green
    'accent_neutral': (182, 142, 108),    # Neutral = warm earth
    'accent_negative': (168, 88, 98),     # Negative = red
    'text': (38, 36, 34),
    'mark_light': (205, 198, 190),
    'mark_dark': (58, 54, 50),
}

FONT_DIR = '/Users/bencium/.claude/plugins/marketplaces/anthropic-agent-skills/canvas-design/canvas-fonts/'
MONO_FONT = FONT_DIR + 'IBMPlexMono-Regular.ttf'
SANS_FONT = FONT_DIR + 'WorkSans-Regular.ttf'

class LiveArtworkGenerator:
    """Generates artwork with live social media data"""

    def __init__(self, social_data):
        self.social_data = social_data
        self.events = social_data.get('events', [])
        self.timestamp = social_data.get('timestamp', datetime.now().isoformat())

    def create_base(self):
        """Create base with subtle texture"""
        img = Image.new('RGB', (WIDTH, HEIGHT), PALETTE['bg'])
        draw = ImageDraw.Draw(img, 'RGBA')

        random.seed(42)
        for _ in range(12000):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 2)
            alpha = random.randint(2, 6) if random.random() > 0.7 else random.randint(1, 3)
            color = PALETTE['mark_light'] + (alpha,)
            draw.ellipse([x, y, x+size, y+size], fill=color)

        return img

    def draw_strata(self, draw, start_y):
        """Draw stratified layers - platforms as geological strata"""
        current_y = start_y
        layer_colors = [
            PALETTE['strata_1'], PALETTE['strata_2'], PALETTE['strata_3'],
            PALETTE['strata_4'], PALETTE['strata_5'], PALETTE['strata_6'],
        ]
        thicknesses = [420, 380, 520, 340, 460, 380]
        layer_data = []

        for i, (base_color, thickness) in enumerate(zip(layer_colors, thicknesses)):
            for offset in range(thickness):
                t = offset / thickness
                ease = t * t * (3.0 - 2.0 * t)
                lightness_shift = int(math.sin(ease * math.pi) * 18) - 9
                band_variation = int(math.sin(offset * 0.08) * 4)
                total_shift = lightness_shift + band_variation
                adjusted_color = tuple(max(0, min(255, c + total_shift)) for c in base_color)

                draw.line(
                    [(200, current_y + offset), (WIDTH - 200, current_y + offset)],
                    fill=adjusted_color, width=1
                )

            layer_data.append({
                'y': current_y, 'height': thickness,
                'center_y': current_y + thickness // 2,
                'color': base_color, 'index': i,
                'platform': ['reddit', 'reddit', 'hackernews', 'hackernews', 'general', 'general'][i]
            })

            current_y += thickness

        return layer_data

    def map_event_to_position(self, event, layer_data):
        """Map social media event to canvas position"""
        # Find appropriate layer based on platform
        platform = event.get('platform', 'general')
        matching_layers = [l for l in layer_data if l['platform'] == platform]

        if not matching_layers:
            matching_layers = layer_data

        layer = random.choice(matching_layers)

        # X position: based on time of day (0-24 hours mapped to canvas width)
        created_utc = event.get('created_utc', 0)
        if created_utc > 0:
            dt = datetime.fromtimestamp(created_utc)
            hour = dt.hour + (dt.minute / 60.0)
            # Map 24 hours to canvas width (with margins)
            x = 250 + int((hour / 24.0) * (WIDTH - 500))
        else:
            x = random.randint(300, WIDTH - 300)

        # Y position: within the matched layer, slightly randomized
        y_min = layer['y'] + 60
        y_max = layer['y'] + layer['height'] - 60
        y = random.randint(y_min, y_max)

        return x, y, layer

    def get_sentiment_color(self, sentiment):
        """Map sentiment to color"""
        if sentiment > 0.3:
            return PALETTE['accent_positive']
        elif sentiment < -0.3:
            return PALETTE['accent_negative']
        else:
            return PALETTE['accent_neutral']

    def draw_data_driven_accents(self, draw, layer_data):
        """Draw accent clusters based on actual social media events"""
        print("\nMapping social media events to artwork...")

        # Take top events by significance
        significant_events = sorted(self.events, key=lambda x: x.get('significance', 0), reverse=True)[:30]

        for event in significant_events:
            significance = event.get('significance', 100)
            sentiment = event.get('sentiment', 0)

            # Map to position
            center_x, center_y, layer = self.map_event_to_position(event, layer_data)

            # Size based on significance (log scale for better visual balance)
            base_radius = 30 + int(math.log(max(significance, 10)) * 8)
            base_radius = min(base_radius, 100)  # Cap maximum size

            # Color based on sentiment
            accent_color = self.get_sentiment_color(sentiment)

            # Draw cluster
            num_marks = int(base_radius / 2)  # More marks for bigger events
            for _ in range(num_marks):
                angle = random.uniform(0, math.pi * 2)
                radius = random.uniform(base_radius * 0.3, base_radius)

                offset_x = int(radius * math.cos(angle))
                offset_y = int(radius * math.sin(angle) * 0.75)  # Slightly elliptical

                x = center_x + offset_x
                y = center_y + offset_y

                alpha = random.randint(50, 120)
                color = accent_color + (alpha,)

                r = random.randint(2, 5)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

        print(f"✓ Visualized {len(significant_events)} significant events as accent clusters")

    def draw_systematic_marks(self, draw, layer_data):
        """Base systematic marks (lighter than accent clusters)"""
        random.seed(42)

        for layer in layer_data:
            y_top = layer['y']
            y_bottom = layer['y'] + layer['height']

            # Sparse background marks
            for _ in range(100):
                x = random.randint(250, WIDTH - 250)
                y = random.randint(y_top + 20, y_bottom - 20)

                mark_type = random.choice(['dot', 'dash'])

                if mark_type == 'dot':
                    r = random.randint(1, 3)
                    alpha = random.randint(30, 60)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
                else:
                    length = random.randint(8, 14)
                    alpha = random.randint(25, 50)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.line([(x, y), (x + length, y)], fill=color, width=1)

    def draw_vertical_grid(self, draw, layer_data):
        """Vertical grid representing time divisions"""
        # 6 divisions = 4-hour blocks in 24-hour day
        num_divisions = 6
        section_width = (WIDTH - 400) // num_divisions

        for i in range(1, num_divisions):
            x = 200 + (i * section_width)

            y_start = layer_data[0]['y']
            y_end = layer_data[-1]['y'] + layer_data[-1]['height']

            for y in range(y_start, y_end, 4):
                alpha = 25
                color = PALETTE['text'] + (alpha,)
                draw.point((x, y), fill=color)
                draw.point((x+1, y), fill=color)

    def draw_measurement_marks(self, draw, layer_data):
        """Measurement system"""
        for layer in layer_data:
            y_top = layer['y']
            y_bottom = layer['y'] + layer['height']

            draw.line([(165, y_top), (195, y_top)], fill=PALETTE['text'], width=2)
            draw.line([(165, y_bottom), (195, y_bottom)], fill=PALETTE['text'], width=2)

            for y in range(y_top, y_bottom, 6):
                draw.point((180, y), fill=PALETTE['text'])
                draw.point((180, y+1), fill=PALETTE['text'])

    def draw_typography(self, draw, layer_data):
        """Typography with data metadata"""
        try:
            font_small = ImageFont.truetype(MONO_FONT, 26)
            font_tiny = ImageFont.truetype(MONO_FONT, 20)
            font_title = ImageFont.truetype(SANS_FONT, 40)
            font_subtitle = ImageFont.truetype(MONO_FONT, 22)
        except:
            font_small = ImageFont.load_default()
            font_tiny = ImageFont.load_default()
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()

        # Title
        title_text = "DIGITAL ARCHAEOLOGY"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (WIDTH - title_width) // 2
        draw.text((title_x, 420), title_text, fill=PALETTE['text'], font=font_title)

        # Subtitle with timestamp
        capture_date = datetime.fromisoformat(self.timestamp).strftime("%Y-%m-%d %H:%M UTC")
        subtitle = f"Snapshot of social media trends · {capture_date}"
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (WIDTH - sub_width) // 2
        draw.text((sub_x, 490), subtitle, fill=PALETTE['text'], font=font_subtitle)

        # Layer labels
        layer_names = [
            "REDDIT · r/all Top Posts",
            "REDDIT · Viral Content",
            "HACKER NEWS · Front Page",
            "HACKER NEWS · Top Stories",
            "GENERAL · Trending",
            "HISTORICAL · Archive"
        ]

        for i, (layer, name) in enumerate(zip(layer_data, layer_names)):
            y_pos = layer['center_y']
            draw.text((40, y_pos - 13), name, fill=PALETTE['text'], font=font_small)

            # Event count per layer
            layer_platform = layer['platform']
            count = len([e for e in self.events if e.get('platform') == layer_platform])
            count_text = f"{count} events"
            draw.text((WIDTH - 200, y_pos - 10), count_text, fill=PALETTE['text'], font=font_tiny)

        # Bottom notation
        total_events = len(self.events)
        reddit_count = self.social_data.get('reddit_count', 0)
        hn_count = self.social_data.get('hackernews_count', 0)

        notation = f"Data Sources: Reddit ({reddit_count}) · Hacker News ({hn_count}) · Total Events: {total_events}"
        note_bbox = draw.textbbox((0, 0), notation, font=font_tiny)
        note_width = note_bbox[2] - note_bbox[0]
        note_x = (WIDTH - note_width) // 2
        draw.text((note_x, HEIGHT - 280), notation, fill=PALETTE['text'], font=font_tiny)

        # Legend
        legend_y = HEIGHT - 220
        draw.text((250, legend_y), "SENTIMENT LEGEND:", fill=PALETTE['text'], font=font_tiny)

        # Positive
        draw.ellipse([250, legend_y + 30, 270, legend_y + 50], fill=PALETTE['accent_positive'])
        draw.text((280, legend_y + 32), "Positive/Uplifting", fill=PALETTE['text'], font=font_tiny)

        # Neutral
        draw.ellipse([500, legend_y + 30, 520, legend_y + 50], fill=PALETTE['accent_neutral'])
        draw.text((530, legend_y + 32), "Neutral/General", fill=PALETTE['text'], font=font_tiny)

        # Negative
        draw.ellipse([750, legend_y + 30, 770, legend_y + 50], fill=PALETTE['accent_negative'])
        draw.text((780, legend_y + 32), "Controversial", fill=PALETTE['text'], font=font_tiny)

    def generate(self, output_filename=None):
        """Generate the complete artwork"""
        if output_filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_filename = f'chromatic_archaeology_{date_str}.png'

        print("\n" + "="*60)
        print("GENERATING CHROMATIC ARCHAEOLOGY (LIVE DATA)")
        print("="*60 + "\n")

        img = self.create_base()
        draw = ImageDraw.Draw(img, 'RGBA')
        print("✓ Base canvas created")

        layer_data = self.draw_strata(draw, start_y=620)
        print("✓ Stratified layers drawn")

        self.draw_vertical_grid(draw, layer_data)
        print("✓ Temporal grid added")

        self.draw_systematic_marks(draw, layer_data)
        print("✓ Background marks placed")

        self.draw_data_driven_accents(draw, layer_data)
        # ^ This is where the magic happens - social data becomes art

        self.draw_measurement_marks(draw, layer_data)
        print("✓ Measurement system drawn")

        self.draw_typography(draw, layer_data)
        print("✓ Typography and metadata added")

        img.save(output_filename, 'PNG', quality=100, dpi=(300, 300))

        print(f"\n✓ Artwork saved: {output_filename}")
        print(f"  Dimensions: {WIDTH}x{HEIGHT}px @ 300 DPI")
        print(f"  Social events visualized: {len(self.events)}")
        print("="*60 + "\n")

        return output_filename


def main():
    """Main execution"""
    print("\nCHROMATIC ARCHAEOLOGY - LIVE DATA VERSION")
    print("Transforming social media trends into visual art")
    print("="*60 + "\n")

    # Fetch live data
    fetcher = SocialDataFetcher()
    social_data = fetcher.get_all_trends(reddit_limit=30, hn_limit=20)

    # Save cache
    fetcher.save_to_cache(social_data)

    # Generate artwork
    generator = LiveArtworkGenerator(social_data)
    output_file = generator.generate()

    print(f"✓ Process complete! Open {output_file} to see your digital archaeology.")
    return output_file


if __name__ == '__main__':
    main()
