"""
Share Card Generator
Generates beautiful shareable images for bazi results
"""
import os
import math

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


WUXING_COLORS = {
    "wood": (143, 209, 158),
    "fire": (255, 130, 110),
    "earth": (224, 195, 107),
    "metal": (167, 199, 255),
    "water": (126, 200, 227),
}

GOLD = (201, 162, 63)
BG_COLOR = (11, 11, 11)
CARD_BG = (18, 18, 18)
TEXT_COLOR = (232, 230, 217)
MUTED = (160, 155, 140)


def _get_font(size, bold=False):
    """Get font, fallback to default if not available."""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # Microsoft YaHei
        "C:/Windows/Fonts/simhei.ttf",  # SimHei
        "C:/Windows/Fonts/simsun.ttc",  # SimSun
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_share_card(result, output_path="share_card.png"):
    """
    Generate a shareable bazi analysis card.
    
    Args:
        result: Bazi analysis result dict
        output_path: Output file path
    
    Returns:
        Path to generated image
    """
    if not HAS_PILLOW:
        raise ImportError("Pillow is required for share card generation")
    
    width, height = 800, 1200
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = _get_font(36, bold=True)
    subtitle_font = _get_font(24)
    body_font = _get_font(20)
    small_font = _get_font(16)
    big_font = _get_font(48, bold=True)
    
    y = 40
    
    # Header decorative line
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 20
    
    # Title
    draw.text((width // 2, y), "八字命盘", font=title_font, fill=GOLD, anchor="mt")
    y += 50
    
    # Decorative line
    draw.line([(100, y), (width - 100, y)], fill=(60, 60, 60), width=1)
    y += 20
    
    # Four Pillars
    bazi = result.get("bazi_detail", {})
    pillars = ["year", "month", "day", "hour"]
    pillar_names = ["年柱", "月柱", "日柱", "时柱"]
    
    pillar_width = (width - 120) // 4
    start_x = 60
    
    for i, (key, name) in enumerate(zip(pillars, pillar_names)):
        p = bazi.get(key, {})
        x = start_x + i * pillar_width + pillar_width // 2
        
        # Pillar background
        px = start_x + i * pillar_width + 5
        draw.rounded_rectangle(
            [px, y, px + pillar_width - 10, y + 180],
            radius=8,
            fill=CARD_BG,
            outline=(40, 40, 40)
        )
        
        # Pillar name
        draw.text((x, y + 10), name, font=small_font, fill=MUTED, anchor="mt")
        
        # Gan (Heavenly Stem)
        gan = p.get("gan", "-")
        gan_wx = p.get("gan_wx", "")
        gan_color = WUXING_COLORS.get(gan_wx, TEXT_COLOR)
        draw.text((x, y + 50), gan, font=big_font, fill=gan_color, anchor="mt")
        
        # Zhi (Earthly Branch)
        zhi = p.get("zhi", "-")
        zhi_wx = p.get("zhi_wx", "")
        zhi_color = WUXING_COLORS.get(zhi_wx, TEXT_COLOR)
        draw.text((x, y + 110), zhi, font=subtitle_font, fill=zhi_color, anchor="mt")
        
        # Nayin
        nayin_key = p.get("nayin_key", "")
        if nayin_key:
            draw.text((x, y + 150), nayin_key.replace("nayin_", ""), font=small_font, fill=MUTED, anchor="mt")
    
    y += 200
    
    # Separator
    draw.line([(60, y), (width - 60, y)], fill=(40, 40, 40), width=1)
    y += 20
    
    # Wuxing Strength as radar-like display
    draw.text((width // 2, y), "五行分布", font=subtitle_font, fill=GOLD, anchor="mt")
    y += 40
    
    wuxing = result.get("wuxing_strength", {})
    wx_names = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    
    bar_height = 16
    bar_max_width = width - 200
    
    for wx_key in ["wood", "fire", "earth", "metal", "water"]:
        score = wuxing.get(wx_key, 0)
        name = wx_names.get(wx_key, wx_key)
        color = WUXING_COLORS.get(wx_key, TEXT_COLOR)
        
        # Label
        draw.text((80, y + 2), name, font=body_font, fill=color, anchor="lt")
        
        # Bar background
        bar_x = 130
        draw.rounded_rectangle(
            [bar_x, y, bar_x + bar_max_width, y + bar_height],
            radius=8,
            fill=(30, 30, 30)
        )
        
        # Bar fill
        fill_width = int(bar_max_width * min(score / 100, 1.0))
        if fill_width > 0:
            draw.rounded_rectangle(
                [bar_x, y, bar_x + fill_width, y + bar_height],
                radius=8,
                fill=color
            )
        
        # Score
        draw.text((bar_x + bar_max_width + 10, y + 2), str(int(score)), font=small_font, fill=MUTED, anchor="lt")
        
        y += 30
    
    y += 20
    
    # Personality highlight
    personality = result.get("personality", {})
    if personality:
        draw.line([(60, y), (width - 60, y)], fill=(40, 40, 40), width=1)
        y += 20
        
        draw.text((width // 2, y), "性格特征", font=subtitle_font, fill=GOLD, anchor="mt")
        y += 40
        
        # Body strength
        strength_key = personality.get("body_strength_key", "")
        if strength_key:
            strength_text = strength_key.replace("body_", "").replace("_", " ")
            draw.text((80, y), f"身强身弱: {strength_text}", font=body_font, fill=TEXT_COLOR)
            y += 30
        
        # Personality trait
        trait_key = personality.get("personality_key", "")
        if trait_key:
            # Wrap text
            trait_text = trait_key
            lines = []
            while len(trait_text) > 25:
                lines.append(trait_text[:25])
                trait_text = trait_text[25:]
            lines.append(trait_text)
            
            for line in lines[:3]:
                draw.text((80, y), line, font=body_font, fill=TEXT_COLOR)
                y += 28
    
    # Footer
    y = height - 80
    draw.line([(60, y), (width - 60, y)], fill=GOLD, width=2)
    y += 15
    
    draw.text((width // 2, y), "由八字排盘系统生成", font=small_font, fill=MUTED, anchor="mt")
    y += 25
    draw.text((width // 2, y), "仅供文化研究参考", font=small_font, fill=(80, 80, 80), anchor="mt")
    
    # Save
    if output_path is None:
        import io
        buf = io.BytesIO()
        img.save(buf, 'PNG')
        buf.seek(0)
        return buf
    else:
        img.save(output_path, "PNG", quality=95)
        return output_path


def generate_share_card_base64(result):
    """Generate share card and return as base64 string."""
    import base64
    import io
    
    if not HAS_PILLOW:
        return None
    
    output = generate_share_card(result, output_path=None)
    
    if isinstance(output, io.BytesIO):
        return base64.b64encode(output.getvalue()).decode("utf-8")
    
    buffer = io.BytesIO()
    img = Image.open(output) if isinstance(output, str) else output
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
