#!/usr/bin/env python3
"""
Stewie Griffin Evil Grin - Emoji GIF for Slack
Creates a 128x128 emoji GIF of Stewie transforming to his evil grin
"""

import sys
import math
from PIL import Image, ImageDraw

# Add the slack-gif-creator toolkit to path
sys.path.insert(0, '/Users/bencium/.claude/plugins/marketplaces/anthropic-agent-skills/slack-gif-creator')

from core.gif_builder import GIFBuilder
from core.validators import check_slack_size, validate_gif
from core.easing import interpolate

# Stewie color palette (simple, solid colors for compression)
COLORS = {
    'background': (245, 245, 250),  # Very light gray-blue
    'head': (255, 220, 190),         # Peach/beige for head
    'head_outline': (40, 40, 40),    # Dark outline
    'eyes': (255, 255, 255),         # White eyes
    'pupils': (30, 30, 30),          # Dark pupils
    'eyebrows': (40, 40, 40),        # Dark eyebrows
    'mouth': (200, 60, 60),          # Red grin
    'teeth': (255, 255, 255),        # White teeth
    'overalls': (200, 50, 50)        # Red overalls
}

def draw_stewie_head(draw, center_x, center_y, head_width, head_height):
    """Draw Stewie's iconic football-shaped head"""
    # Head (ellipse)
    left = center_x - head_width // 2
    top = center_y - head_height // 2
    right = center_x + head_width // 2
    bottom = center_y + head_height // 2

    # Fill head
    draw.ellipse([left, top, right, bottom], fill=COLORS['head'], outline=COLORS['head_outline'], width=2)

def draw_eyes(draw, center_x, center_y, eye_spacing, eye_width, eye_height, pupil_y_offset=0, squint=0):
    """Draw Stewie's eyes with optional squint effect"""
    left_eye_x = center_x - eye_spacing // 2
    right_eye_x = center_x + eye_spacing // 2
    eye_y = center_y - 8

    # Apply squint (reduces eye height)
    actual_eye_height = eye_height - squint

    # Left eye
    draw.ellipse([
        left_eye_x - eye_width // 2,
        eye_y - actual_eye_height // 2,
        left_eye_x + eye_width // 2,
        eye_y + actual_eye_height // 2
    ], fill=COLORS['eyes'], outline=COLORS['head_outline'], width=1)

    # Right eye
    draw.ellipse([
        right_eye_x - eye_width // 2,
        eye_y - actual_eye_height // 2,
        right_eye_x + eye_width // 2,
        eye_y + actual_eye_height // 2
    ], fill=COLORS['eyes'], outline=COLORS['head_outline'], width=1)

    # Pupils
    pupil_size = 6
    draw.ellipse([
        left_eye_x - pupil_size // 2,
        eye_y + pupil_y_offset - pupil_size // 2,
        left_eye_x + pupil_size // 2,
        eye_y + pupil_y_offset + pupil_size // 2
    ], fill=COLORS['pupils'])

    draw.ellipse([
        right_eye_x - pupil_size // 2,
        eye_y + pupil_y_offset - pupil_size // 2,
        right_eye_x + pupil_size // 2,
        eye_y + pupil_y_offset + pupil_size // 2
    ], fill=COLORS['pupils'])

def draw_eyebrows(draw, center_x, center_y, eye_spacing, eyebrow_angle=0, eyebrow_y_offset=0):
    """Draw Stewie's eyebrows with angle for expressions"""
    # Eyebrow positions
    left_brow_x = center_x - eye_spacing // 2
    right_brow_x = center_x + eye_spacing // 2
    brow_y = center_y - 20 + eyebrow_y_offset

    brow_width = 16
    brow_height = 3

    # Left eyebrow (angled)
    left_inner_y = brow_y - eyebrow_angle
    left_outer_y = brow_y + eyebrow_angle

    draw.line([
        (left_brow_x - brow_width // 2, left_outer_y),
        (left_brow_x + brow_width // 2, left_inner_y)
    ], fill=COLORS['eyebrows'], width=brow_height)

    # Right eyebrow (angled)
    right_inner_y = brow_y - eyebrow_angle
    right_outer_y = brow_y + eyebrow_angle

    draw.line([
        (right_brow_x - brow_width // 2, right_inner_y),
        (right_brow_x + brow_width // 2, right_outer_y)
    ], fill=COLORS['eyebrows'], width=brow_height)

def draw_mouth(draw, center_x, center_y, mouth_width, mouth_curve, show_grin=False):
    """Draw mouth - either neutral line or evil grin"""
    mouth_y = center_y + 15

    if not show_grin:
        # Neutral/frustrated mouth (straight line)
        draw.line([
            (center_x - mouth_width // 2, mouth_y),
            (center_x + mouth_width // 2, mouth_y)
        ], fill=COLORS['mouth'], width=2)
    else:
        # Evil grin (curved arc with teeth)
        # Draw grin arc
        grin_bbox = [
            center_x - mouth_width // 2,
            mouth_y - mouth_curve,
            center_x + mouth_width // 2,
            mouth_y + mouth_curve
        ]
        draw.arc(grin_bbox, start=0, end=180, fill=COLORS['mouth'], width=3)

        # Add teeth (small rectangles)
        num_teeth = 4
        tooth_width = mouth_width // (num_teeth + 1)
        tooth_height = 4

        for i in range(num_teeth):
            tooth_x = center_x - mouth_width // 2 + (i + 1) * tooth_width
            tooth_y = mouth_y - mouth_curve // 2
            draw.rectangle([
                tooth_x - 2,
                tooth_y,
                tooth_x + 2,
                tooth_y + tooth_height
            ], fill=COLORS['teeth'])

def draw_stewie_frame(frame_num, total_frames):
    """Draw a single frame of Stewie's animation"""
    img = Image.new('RGB', (128, 128), COLORS['background'])
    draw = ImageDraw.Draw(img)

    center_x = 64
    center_y = 58  # Slightly above center for head

    # Animation phases
    if frame_num < 5:
        # Phase 1: Neutral/frustrated (frames 0-4)
        t = frame_num / 4

        # Neutral expression
        draw_stewie_head(draw, center_x, center_y, 55, 65)
        draw_eyes(draw, center_x, center_y, eye_spacing=28, eye_width=14, eye_height=16)
        draw_eyebrows(draw, center_x, center_y, eye_spacing=28, eyebrow_angle=3, eyebrow_y_offset=0)
        draw_mouth(draw, center_x, center_y, mouth_width=20, mouth_curve=0, show_grin=False)

    elif frame_num < 9:
        # Phase 2: Transition to evil grin (frames 5-8)
        t = (frame_num - 5) / 3

        # Interpolate expressions
        eyebrow_angle = interpolate(3, -5, t, 'ease_out')  # Raise eyebrows (negative = raised)
        squint = int(interpolate(0, 4, t, 'ease_in'))       # Squint eyes
        mouth_curve = int(interpolate(0, 15, t, 'ease_out'))  # Curve mouth

        draw_stewie_head(draw, center_x, center_y, 55, 65)
        draw_eyes(draw, center_x, center_y, eye_spacing=28, eye_width=14, eye_height=16, squint=squint)
        draw_eyebrows(draw, center_x, center_y, eye_spacing=28, eyebrow_angle=int(eyebrow_angle), eyebrow_y_offset=-2)

        # Transition to grin
        if t > 0.5:
            draw_mouth(draw, center_x, center_y, mouth_width=30, mouth_curve=mouth_curve, show_grin=True)
        else:
            draw_mouth(draw, center_x, center_y, mouth_width=20, mouth_curve=0, show_grin=False)

    else:
        # Phase 3: Evil grin with pulse (frames 9-12)
        t = (frame_num - 9) / 3

        # Subtle pulse effect
        pulse = 1.0 + math.sin(t * math.pi * 2) * 0.03
        head_w = int(55 * pulse)
        head_h = int(65 * pulse)

        draw_stewie_head(draw, center_x, center_y, head_w, head_h)
        draw_eyes(draw, center_x, center_y, eye_spacing=28, eye_width=14, eye_height=16, squint=4)
        draw_eyebrows(draw, center_x, center_y, eye_spacing=28, eyebrow_angle=-5, eyebrow_y_offset=-2)
        draw_mouth(draw, center_x, center_y, mouth_width=30, mouth_curve=15, show_grin=True)

    # Add tiny overalls suggestion at bottom
    draw.rectangle([center_x - 15, 100, center_x + 15, 128], fill=COLORS['overalls'], outline=COLORS['head_outline'], width=1)

    return img

def main():
    """Create Stewie evil grin emoji GIF"""
    print("Creating Stewie evil grin emoji GIF...")

    # Create GIF builder (emoji specs)
    builder = GIFBuilder(width=128, height=128, fps=10)

    # Generate 12 frames
    total_frames = 12
    for i in range(total_frames):
        frame = draw_stewie_frame(i, total_frames)
        builder.add_frame(frame)
        print(f"Frame {i+1}/{total_frames} created")

    # Save with emoji optimization
    print("\nSaving GIF with emoji optimization...")
    output_file = 'stewie_evil_grin.gif'
    info = builder.save(output_file, num_colors=40, optimize_for_emoji=True)

    print(f"\nGIF saved: {output_file}")
    print(f"Size: {info['size_kb']:.2f} KB ({info['size_mb']:.3f} MB)")
    print(f"Frames: {info['frame_count']}")
    print(f"Duration: {info['duration_seconds']:.2f}s")

    # Validate for Slack emoji requirements
    print("\n" + "="*50)
    print("SLACK EMOJI VALIDATION")
    print("="*50)

    passes, size_info = check_slack_size(output_file, is_emoji=True)

    if passes:
        print("✓ GIF meets Slack emoji requirements!")
        print(f"  Size: {size_info['size_kb']:.2f} KB / 64 KB limit")
    else:
        print("✗ GIF exceeds Slack emoji size limit")
        print(f"  Size: {size_info['size_kb']:.2f} KB / 64 KB limit")
        print(f"  Needs reduction: {size_info['size_kb'] - 64:.2f} KB")
        print("\nOptimization suggestions:")
        print("  - Reduce to 10 frames (currently 12)")
        print("  - Reduce colors to 32 (currently 40)")
        print("  - Simplify background (use solid color)")

    # Run full validation
    all_pass, results = validate_gif(output_file, is_emoji=True)
    print("\nFull validation results:")
    for check, result in results.items():
        status = "✓" if result['passes'] else "✗"
        print(f"  {status} {check}: {result['message']}")

if __name__ == '__main__':
    main()
