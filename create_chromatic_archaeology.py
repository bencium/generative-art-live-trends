#!/usr/bin/env python3
"""
Chromatic Archaeology - Visual Art
A museum-quality piece exploring stratification of time through color
"""

import random
from PIL import Image, ImageDraw, ImageFont
import math

# Canvas dimensions (high resolution for print quality)
WIDTH = 3000
HEIGHT = 4000

# Sophisticated color palette - earth tones, oxidized metals, archival blues
PALETTE = {
    'bg': (245, 242, 238),           # Warm off-white (archival paper)
    'strata_1': (168, 145, 128),     # Oxidized earth
    'strata_2': (201, 178, 156),     # Lighter sediment
    'strata_3': (88, 98, 108),       # Cool slate
    'strata_4': (142, 158, 171),     # Dusty blue
    'strata_5': (178, 152, 134),     # Terracotta
    'strata_6': (118, 112, 102),     # Dark earth
    'accent_warm': (188, 112, 88),   # Oxidized copper
    'accent_cool': (78, 108, 128),   # Prussian blue
    'text': (45, 42, 38),            # Near black
    'mark_light': (195, 185, 175),   # Light marks
    'mark_dark': (65, 62, 58),       # Dark marks
}

# Font paths
FONT_DIR = '/Users/bencium/.claude/plugins/marketplaces/anthropic-agent-skills/canvas-design/canvas-fonts/'
MONO_FONT = FONT_DIR + 'IBMPlexMono-Regular.ttf'
SANS_FONT = FONT_DIR + 'WorkSans-Regular.ttf'

def create_base_canvas():
    """Create the base canvas with subtle texture"""
    img = Image.new('RGB', (WIDTH, HEIGHT), PALETTE['bg'])
    draw = ImageDraw.Draw(img, 'RGBA')

    # Add very subtle paper texture with random noise
    random.seed(42)  # Reproducible
    for _ in range(8000):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 2)
        alpha = random.randint(3, 8)
        color = PALETTE['mark_light'] + (alpha,)
        draw.ellipse([x, y, x+size, y+size], fill=color)

    return img

def draw_stratified_layers(draw, start_y, num_layers=6):
    """
    Draw horizontal strata with varying thickness and color
    Each layer represents a temporal period
    """
    current_y = start_y
    layer_colors = [
        PALETTE['strata_1'],
        PALETTE['strata_2'],
        PALETTE['strata_3'],
        PALETTE['strata_4'],
        PALETTE['strata_5'],
        PALETTE['strata_6'],
    ]

    # Layer thicknesses (proportional system)
    thicknesses = [420, 380, 520, 340, 460, 380]

    layer_data = []

    for i, (color, thickness) in enumerate(zip(layer_colors, thicknesses)):
        # Draw main layer with subtle gradient effect
        for offset in range(thickness):
            # Subtle value shift for depth
            lightness_shift = int((offset / thickness) * 12) - 6
            adjusted_color = tuple(max(0, min(255, c + lightness_shift)) for c in color)

            draw.line(
                [(200, current_y + offset), (WIDTH - 200, current_y + offset)],
                fill=adjusted_color,
                width=1
            )

        # Store layer info for notation
        layer_data.append({
            'y': current_y,
            'height': thickness,
            'center_y': current_y + thickness // 2,
            'color': color,
            'index': i
        })

        current_y += thickness

    return layer_data

def draw_systematic_marks(draw, layer_data):
    """
    Add systematic mark-making - dots, lines, cross-hatches
    Like scientific observation points
    """
    random.seed(42)

    for layer in layer_data:
        y_top = layer['y']
        y_bottom = layer['y'] + layer['height']
        y_center = layer['center_y']

        # Density varies by layer (simulating different activity levels)
        density = [250, 180, 320, 150, 280, 200][layer['index']]

        # Small observation marks scattered throughout layer
        for _ in range(density):
            x = random.randint(250, WIDTH - 250)
            y = random.randint(y_top + 20, y_bottom - 20)

            mark_type = random.choice(['dot', 'dash', 'cross'])

            if mark_type == 'dot':
                # Small dot
                r = random.randint(2, 4)
                alpha = random.randint(40, 100)
                color = PALETTE['mark_dark'] + (alpha,)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

            elif mark_type == 'dash':
                # Short horizontal dash
                length = random.randint(8, 15)
                alpha = random.randint(35, 85)
                color = PALETTE['mark_dark'] + (alpha,)
                draw.line([(x, y), (x + length, y)], fill=color, width=1)

            elif mark_type == 'cross':
                # Small cross mark
                size = random.randint(5, 8)
                alpha = random.randint(30, 75)
                color = PALETTE['mark_dark'] + (alpha,)
                draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
                draw.line([(x, y - size), (x, y + size)], fill=color, width=1)

def draw_vertical_grid(draw, layer_data):
    """
    Add subtle vertical divisions creating a grid of observation points
    """
    # 5 vertical sections
    section_width = (WIDTH - 400) // 5

    for i in range(1, 5):
        x = 200 + (i * section_width)

        # Thin vertical line through all strata
        for y in range(layer_data[0]['y'], layer_data[-1]['y'] + layer_data[-1]['height']):
            if y % 3 == 0:  # Dotted line effect
                alpha = 25
                color = PALETTE['text'] + (alpha,)
                draw.point((x, y), fill=color)

def draw_measurement_marks(draw, layer_data):
    """
    Add measurement ticks and small notations like a scientific diagram
    """
    # Left margin measurement ticks
    for layer in layer_data:
        y_top = layer['y']
        y_bottom = layer['y'] + layer['height']

        # Top tick
        draw.line([(170, y_top), (190, y_top)], fill=PALETTE['text'], width=2)
        # Bottom tick
        draw.line([(170, y_bottom), (190, y_bottom)], fill=PALETTE['text'], width=2)

        # Small connecting line
        for y in range(y_top, y_bottom, 8):
            draw.point((180, y), fill=PALETTE['text'])

def draw_minimal_typography(draw, layer_data):
    """
    Add sparse, clinical typography - specimen labels and coordinates
    """
    try:
        # Small monospace for labels
        font_small = ImageFont.truetype(MONO_FONT, 24)
        font_tiny = ImageFont.truetype(MONO_FONT, 18)
        font_title = ImageFont.truetype(SANS_FONT, 36)

    except:
        # Fallback to default
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Title at top - minimal
    title_text = "TEMPORAL STRATIFICATION"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, 450), title_text, fill=PALETTE['text'], font=font_title)

    # Subtitle
    subtitle = "Cross-sectional analysis of creative states, 2024–2025"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_tiny)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (WIDTH - sub_width) // 2
    draw.text((sub_x, 510), subtitle, fill=PALETTE['text'], font=font_tiny)

    # Layer labels (sparse)
    layer_names = [
        "LAYER VI · INCUBATION",
        "LAYER V · IDEATION",
        "LAYER IV · ITERATION",
        "LAYER III · SYNTHESIS",
        "LAYER II · REFINEMENT",
        "LAYER I · COMPLETION"
    ]

    for i, (layer, name) in enumerate(zip(layer_data, layer_names)):
        y_pos = layer['center_y']

        # Left margin label
        draw.text((50, y_pos - 12), name, fill=PALETTE['text'], font=font_small)

        # Right margin - depth measurement
        depth_text = f"{(i+1) * 120}mm"
        draw.text((WIDTH - 150, y_pos - 10), depth_text, fill=PALETTE['text'], font=font_tiny)

    # Bottom notation
    notation = "Site: Neural Archive 47°N · Sample Method: Temporal Core Extraction · Scale: 1:1200"
    note_bbox = draw.textbbox((0, 0), notation, font=font_tiny)
    note_width = note_bbox[2] - note_bbox[0]
    note_x = (WIDTH - note_width) // 2
    draw.text((note_x, HEIGHT - 300), notation, fill=PALETTE['text'], font=font_tiny)

    # Grid coordinates at bottom
    section_width = (WIDTH - 400) // 5
    coord_font = ImageFont.truetype(MONO_FONT, 20)
    coords = ["A1", "A2", "A3", "A4", "A5"]

    for i, coord in enumerate(coords):
        x = 200 + (i * section_width) + (section_width // 2)
        coord_bbox = draw.textbbox((0, 0), coord, font=coord_font)
        coord_width = coord_bbox[2] - coord_bbox[0]
        draw.text((x - coord_width//2, HEIGHT - 250), coord, fill=PALETTE['text'], font=coord_font)

def add_accent_elements(draw, layer_data):
    """
    Add subtle accent marks - moments of intensity or disruption
    """
    random.seed(123)

    # A few small concentrated clusters of marks (intense creative moments)
    for _ in range(8):
        # Pick random layer
        layer = random.choice(layer_data)
        center_x = random.randint(400, WIDTH - 400)
        center_y = random.randint(layer['y'] + 50, layer['y'] + layer['height'] - 50)

        # Dense cluster of small marks
        for _ in range(60):
            offset_x = random.randint(-40, 40)
            offset_y = random.randint(-30, 30)
            x = center_x + offset_x
            y = center_y + offset_y

            # Use accent colors
            color_choice = random.choice([PALETTE['accent_warm'], PALETTE['accent_cool']])
            alpha = random.randint(50, 120)
            color = color_choice + (alpha,)

            r = random.randint(1, 3)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

def create_artwork():
    """
    Create the complete Chromatic Archaeology artwork
    """
    print("Creating Chromatic Archaeology artwork...")
    print("This may take a few moments to render at high resolution...")

    # Create base
    img = create_base_canvas()
    draw = ImageDraw.Draw(img, 'RGBA')

    print("✓ Base canvas created")

    # Draw stratified layers starting below title area
    layer_data = draw_stratified_layers(draw, start_y=650, num_layers=6)
    print("✓ Stratified layers drawn")

    # Add vertical grid
    draw_vertical_grid(draw, layer_data)
    print("✓ Vertical grid added")

    # Add systematic marks (this takes time - meticulously placed)
    draw_systematic_marks(draw, layer_data)
    print("✓ Systematic observation marks placed")

    # Add accent elements
    add_accent_elements(draw, layer_data)
    print("✓ Accent elements added")

    # Add measurement marks
    draw_measurement_marks(draw, layer_data)
    print("✓ Measurement marks drawn")

    # Add typography (minimal and precise)
    draw_minimal_typography(draw, layer_data)
    print("✓ Typography added")

    # Save at high quality
    output_path = 'chromatic_archaeology.png'
    img.save(output_path, 'PNG', quality=100, dpi=(300, 300))

    print(f"\n✓ Artwork saved: {output_path}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"  Resolution: 300 DPI (print quality)")
    print(f"  File format: PNG")

    return output_path

if __name__ == '__main__':
    create_artwork()
    print("\n✓ Chromatic Archaeology complete - a masterpiece of patient observation")
