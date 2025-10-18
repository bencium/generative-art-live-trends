#!/usr/bin/env python3
"""
Chromatic Archaeology - REFINED VERSION
Second pass for museum-quality perfection
"""

import random
from PIL import Image, ImageDraw, ImageFont
import math

# Canvas dimensions (high resolution for print quality)
WIDTH = 3000
HEIGHT = 4000

# Refined, more sophisticated palette - carefully calibrated
PALETTE = {
    'bg': (248, 245, 242),           # Warmer archival white
    'strata_1': (162, 142, 126),     # Refined oxidized earth
    'strata_2': (198, 182, 166),     # Lighter sediment
    'strata_3': (82, 92, 102),       # Deeper slate
    'strata_4': (138, 152, 166),     # More saturated dusty blue
    'strata_5': (172, 148, 132),     # Warmer terracotta
    'strata_6': (112, 106, 98),      # Richer dark earth
    'accent_warm': (182, 108, 86),   # More refined copper
    'accent_cool': (72, 102, 122),   # Deeper prussian
    'text': (38, 36, 34),            # Richer near-black
    'mark_light': (205, 198, 190),   # Lighter marks
    'mark_dark': (58, 54, 50),       # Deeper dark marks
}

FONT_DIR = '/Users/bencium/.claude/plugins/marketplaces/anthropic-agent-skills/canvas-design/canvas-fonts/'
MONO_FONT = FONT_DIR + 'IBMPlexMono-Regular.ttf'
SANS_FONT = FONT_DIR + 'WorkSans-Regular.ttf'

def create_refined_base():
    """Create base with more sophisticated subtle texture"""
    img = Image.new('RGB', (WIDTH, HEIGHT), PALETTE['bg'])
    draw = ImageDraw.Draw(img, 'RGBA')

    # More deliberate paper texture - clustered for organic feel
    random.seed(42)
    for _ in range(12000):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 2)
        # Vary alpha based on position for subtle depth
        alpha = random.randint(2, 6) if random.random() > 0.7 else random.randint(1, 3)
        color = PALETTE['mark_light'] + (alpha,)
        draw.ellipse([x, y, x+size, y+size], fill=color)

    return img

def draw_refined_strata(draw, start_y):
    """
    Refined stratified layers with more sophisticated color transitions
    Each layer has internal micro-variations
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

    thicknesses = [420, 380, 520, 340, 460, 380]
    layer_data = []

    for i, (base_color, thickness) in enumerate(zip(layer_colors, thicknesses)):
        # More sophisticated gradient with micro-variations
        for offset in range(thickness):
            t = offset / thickness

            # Subtle S-curve for more natural transition
            ease = t * t * (3.0 - 2.0 * t)

            # Base gradient
            lightness_shift = int(math.sin(ease * math.pi) * 18) - 9

            # Add subtle horizontal banding (geological micro-layers)
            band_variation = int(math.sin(offset * 0.08) * 4)

            # Combine
            total_shift = lightness_shift + band_variation
            adjusted_color = tuple(max(0, min(255, c + total_shift)) for c in base_color)

            draw.line(
                [(200, current_y + offset), (WIDTH - 200, current_y + offset)],
                fill=adjusted_color,
                width=1
            )

        layer_data.append({
            'y': current_y,
            'height': thickness,
            'center_y': current_y + thickness // 2,
            'color': base_color,
            'index': i
        })

        current_y += thickness

    return layer_data

def draw_refined_systematic_marks(draw, layer_data):
    """
    More deliberate, grid-based systematic marks
    Follows underlying structure more precisely
    """
    random.seed(42)

    section_width = (WIDTH - 400) // 5

    for layer in layer_data:
        y_top = layer['y']
        y_bottom = layer['y'] + layer['height']

        # Different mark strategies per layer (varied "research methods")
        mark_patterns = [
            'dense_grid',      # Layer VI
            'scattered',       # Layer V
            'horizontal_scan', # Layer IV
            'vertical_sample', # Layer III
            'cluster',         # Layer II
            'sparse_cross'     # Layer I
        ]

        pattern = mark_patterns[layer['index']]

        if pattern == 'dense_grid':
            # Systematic grid sampling
            for grid_x in range(5):
                for grid_y in range(8):
                    x = 250 + (grid_x * section_width) + random.randint(-30, 30)
                    y = y_top + 50 + (grid_y * (layer['height'] - 100) // 8) + random.randint(-15, 15)

                    # Precise small cross
                    size = 6
                    alpha = random.randint(60, 95)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
                    draw.line([(x, y - size), (x, y + size)], fill=color, width=1)

        elif pattern == 'horizontal_scan':
            # Horizontal scan lines
            num_scans = 12
            for scan in range(num_scans):
                y = y_top + (scan * layer['height'] // num_scans) + layer['height'] // (2 * num_scans)
                for x in range(250, WIDTH - 250, 35):
                    jitter = random.randint(-3, 3)
                    alpha = random.randint(50, 80)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.ellipse([x-2+jitter, y-2, x+2+jitter, y+2], fill=color)

        elif pattern == 'vertical_sample':
            # Vertical core samples
            for col in range(5):
                x = 250 + (col * section_width) + section_width // 2
                num_points = 18
                for pt in range(num_points):
                    y = y_top + (pt * layer['height'] // num_points) + random.randint(-8, 8)
                    alpha = random.randint(55, 90)
                    color = PALETTE['mark_dark'] + (alpha,)
                    r = random.randint(2, 3)
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

        elif pattern == 'cluster':
            # Clustered observation points
            num_clusters = 8
            for _ in range(num_clusters):
                cx = random.randint(350, WIDTH - 350)
                cy = random.randint(y_top + 60, y_bottom - 60)

                for _ in range(25):
                    offset_x = int(random.gauss(0, 25))
                    offset_y = int(random.gauss(0, 20))
                    x = cx + offset_x
                    y = cy + offset_y

                    alpha = random.randint(45, 85)
                    color = PALETTE['mark_dark'] + (alpha,)
                    r = random.randint(1, 3)
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

        elif pattern == 'sparse_cross':
            # Sparse systematic crosses
            num_marks = 35
            for _ in range(num_marks):
                x = random.randint(300, WIDTH - 300)
                y = random.randint(y_top + 30, y_bottom - 30)

                size = random.randint(7, 10)
                alpha = random.randint(55, 85)
                color = PALETTE['mark_dark'] + (alpha,)
                draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
                draw.line([(x, y - size), (x, y + size)], fill=color, width=1)

        else:  # scattered
            density = 200
            for _ in range(density):
                x = random.randint(250, WIDTH - 250)
                y = random.randint(y_top + 20, y_bottom - 20)

                mark_type = random.choice(['dot', 'dash'])

                if mark_type == 'dot':
                    r = random.randint(2, 4)
                    alpha = random.randint(50, 95)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
                else:
                    length = random.randint(10, 16)
                    alpha = random.randint(45, 80)
                    color = PALETTE['mark_dark'] + (alpha,)
                    draw.line([(x, y), (x + length, y)], fill=color, width=1)

def draw_refined_vertical_grid(draw, layer_data):
    """More refined vertical divisions"""
    section_width = (WIDTH - 400) // 5

    for i in range(1, 5):
        x = 200 + (i * section_width)

        # More deliberate dotted line
        y_start = layer_data[0]['y']
        y_end = layer_data[-1]['y'] + layer_data[-1]['height']

        for y in range(y_start, y_end, 4):
            alpha = 30
            color = PALETTE['text'] + (alpha,)
            draw.point((x, y), fill=color)
            draw.point((x+1, y), fill=color)  # Slightly thicker

def draw_refined_measurement_marks(draw, layer_data):
    """Refined measurement system with more precision"""
    # Left margin - main ticks
    for layer in layer_data:
        y_top = layer['y']
        y_bottom = layer['y'] + layer['height']

        # Top and bottom ticks
        draw.line([(165, y_top), (195, y_top)], fill=PALETTE['text'], width=2)
        draw.line([(165, y_bottom), (195, y_bottom)], fill=PALETTE['text'], width=2)

        # Connecting dotted line with precise spacing
        for y in range(y_top, y_bottom, 6):
            draw.point((180, y), fill=PALETTE['text'])
            draw.point((180, y+1), fill=PALETTE['text'])

    # Right margin - depth scale with smaller interval marks
    total_height = sum(l['height'] for l in layer_data)
    y_start = layer_data[0]['y']

    for i in range(0, 721, 40):  # Every 40mm
        y = y_start + int((i / 720) * total_height)
        if i % 120 == 0:  # Major marks
            draw.line([(WIDTH - 195, y), (WIDTH - 165, y)], fill=PALETTE['text'], width=2)
        else:  # Minor marks
            draw.line([(WIDTH - 185, y), (WIDTH - 175, y)], fill=PALETTE['text'], width=1)

def draw_refined_typography(draw, layer_data):
    """Refined typography with better spacing and hierarchy"""
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

    # Title with better spacing
    title_text = "TEMPORAL STRATIFICATION"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, 420), title_text, fill=PALETTE['text'], font=font_title)

    # Refined subtitle
    subtitle = "Cross-sectional analysis of creative states, 2024–2025"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (WIDTH - sub_width) // 2
    draw.text((sub_x, 490), subtitle, fill=PALETTE['text'], font=font_subtitle)

    # Layer labels with better positioning
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
        draw.text((40, y_pos - 13), name, fill=PALETTE['text'], font=font_small)

        # Right margin - depth with unit
        depth_text = f"{(i+1) * 120}mm"
        depth_bbox = draw.textbbox((0, 0), depth_text, font=font_tiny)
        depth_width = depth_bbox[2] - depth_bbox[0]
        draw.text((WIDTH - 40 - depth_width, y_pos - 10), depth_text, fill=PALETTE['text'], font=font_tiny)

    # Bottom notation - refined
    notation = "Site: Neural Archive 47°N · Sample Method: Temporal Core Extraction · Scale: 1:1200"
    note_bbox = draw.textbbox((0, 0), notation, font=font_tiny)
    note_width = note_bbox[2] - note_bbox[0]
    note_x = (WIDTH - note_width) // 2
    draw.text((note_x, HEIGHT - 280), notation, fill=PALETTE['text'], font=font_tiny)

    # Grid coordinates - better aligned
    section_width = (WIDTH - 400) // 5
    coord_font = ImageFont.truetype(MONO_FONT, 22)
    coords = ["A1", "A2", "A3", "A4", "A5"]

    for i, coord in enumerate(coords):
        x = 200 + (i * section_width) + (section_width // 2)
        coord_bbox = draw.textbbox((0, 0), coord, font=coord_font)
        coord_width = coord_bbox[2] - coord_bbox[0]
        draw.text((x - coord_width//2, HEIGHT - 230), coord, fill=PALETTE['text'], font=coord_font)

def add_refined_accents(draw, layer_data):
    """More deliberate accent placement"""
    random.seed(123)

    # Strategic accent clusters - moments of intensity
    accent_positions = [
        (1, 0.7),  # Layer index, position within layer (0-1)
        (2, 0.3),
        (3, 0.6),
        (4, 0.4),
    ]

    for layer_idx, position in accent_positions:
        layer = layer_data[layer_idx]

        # Calculate precise position
        center_x = 600 + (layer_idx * 450)
        center_y = layer['y'] + int(layer['height'] * position)

        # Use golden ratio for cluster sizing
        phi = 1.618
        base_radius = 50

        # Dense but organized cluster
        for angle_step in range(0, 360, 12):
            for radius_mult in [0.5, 0.8, 1.0, 1.2]:
                angle = math.radians(angle_step + random.uniform(-5, 5))
                radius = base_radius * radius_mult + random.uniform(-8, 8)

                x = center_x + int(radius * math.cos(angle))
                y = center_y + int(radius * math.sin(angle) * 0.8)  # Slightly elliptical

                # Alternate accent colors
                color_choice = PALETTE['accent_warm'] if layer_idx % 2 == 0 else PALETTE['accent_cool']
                alpha = random.randint(60, 110)
                color = color_choice + (alpha,)

                r = random.randint(2, 4)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

def create_refined_artwork():
    """Create the refined, museum-quality artwork"""
    print("Creating REFINED Chromatic Archaeology...")
    print("Applying museum-quality craftsmanship...")

    img = create_refined_base()
    draw = ImageDraw.Draw(img, 'RGBA')
    print("✓ Refined base created")

    layer_data = draw_refined_strata(draw, start_y=620)
    print("✓ Sophisticated stratified layers drawn")

    draw_refined_vertical_grid(draw, layer_data)
    print("✓ Refined vertical grid added")

    draw_refined_systematic_marks(draw, layer_data)
    print("✓ Deliberate systematic marks placed")

    add_refined_accents(draw, layer_data)
    print("✓ Strategic accent elements added")

    draw_refined_measurement_marks(draw, layer_data)
    print("✓ Precision measurement system drawn")

    draw_refined_typography(draw, layer_data)
    print("✓ Refined typography applied")

    output_path = 'chromatic_archaeology.png'
    img.save(output_path, 'PNG', quality=100, dpi=(300, 300))

    print(f"\n✓ REFINED artwork saved: {output_path}")
    print(f"  Museum-quality craftsmanship achieved")
    print(f"  Ready for exhibition")

    return output_path

if __name__ == '__main__':
    create_refined_artwork()
    print("\n✓ Chromatic Archaeology - MASTERPIECE COMPLETE")
