"""
PDF Report Generator
Generates professional bazi analysis PDF reports
"""
import os
import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def _register_chinese_font():
    """Register Chinese font for PDF generation."""
    font_paths = [
        ("C:/Windows/Fonts/msyh.ttc", "MicrosoftYaHei"),
        ("C:/Windows/Fonts/simhei.ttf", "SimHei"),
        ("C:/Windows/Fonts/simsun.ttc", "SimSun"),
        ("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", "NotoSansCJK"),
    ]
    
    for path, name in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                return name
            except Exception:
                continue
    
    return "Helvetica"


def generate_pdf_report(result, output_path=None):
    """
    Generate a professional PDF report for bazi analysis.
    
    Args:
        result: Bazi analysis result dict
        output_path: Output file path (if None, returns BytesIO)
    
    Returns:
        File path or BytesIO object
    """
    if not HAS_REPORTLAB:
        raise ImportError("reportlab is required for PDF generation")
    
    font_name = _register_chinese_font()
    
    # Colors
    GOLD = HexColor("#c9a23f")
    DARK = HexColor("#0b0b0b")
    TEXT = HexColor("#333333")
    MUTED = HexColor("#666666")
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        textColor=GOLD,
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=16,
        textColor=GOLD,
        spaceBefore=15,
        spaceAfter=10,
        borderWidth=1,
        borderColor=GOLD,
        borderPadding=5,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        textColor=TEXT,
        spaceAfter=8,
        leading=16,
    )
    
    small_style = ParagraphStyle(
        'CustomSmall',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=9,
        textColor=MUTED,
        spaceAfter=4,
    )
    
    # Build document
    if output_path:
        doc = SimpleDocTemplate(output_path, pagesize=A4)
    else:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    story = []
    
    # Title
    story.append(Paragraph("八字命盘分析报告", title_style))
    story.append(Spacer(1, 10))
    
    # Generated time
    story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}", small_style))
    story.append(Spacer(1, 20))
    
    # Four Pillars
    story.append(Paragraph("四柱八字", heading_style))
    
    bazi = result.get("bazi_detail", {})
    pillars_data = [
        ["柱位", "天干", "地支", "纳音"],
    ]
    
    pillar_names = {"year": "年柱", "month": "月柱", "day": "日柱", "hour": "时柱"}
    for key in ["year", "month", "day", "hour"]:
        p = bazi.get(key, {})
        pillars_data.append([
            pillar_names.get(key, key),
            p.get("gan", "-"),
            p.get("zhi", "-"),
            p.get("nayin_key", "").replace("nayin_", ""),
        ])
    
    pillars_table = Table(pillars_data, colWidths=[80, 60, 60, 100])
    pillars_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GOLD),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(pillars_table)
    story.append(Spacer(1, 20))
    
    # Wuxing Strength
    story.append(Paragraph("五行强弱", heading_style))
    
    wuxing = result.get("wuxing_strength", {})
    wx_names = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
    
    wx_data = [["五行", "强度", "状态"]]
    for wx_key in ["wood", "fire", "earth", "metal", "water"]:
        score = wuxing.get(wx_key, 0)
        status = "旺" if score > 70 else ("弱" if score < 30 else "中")
        wx_data.append([wx_names.get(wx_key, wx_key), f"{int(score)}", status])
    
    wx_table = Table(wx_data, colWidths=[80, 80, 80])
    wx_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GOLD),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(wx_table)
    story.append(Spacer(1, 20))
    
    # Shensha
    story.append(Paragraph("神煞信息", heading_style))
    
    shensha = result.get("shensha", [])
    if shensha:
        for s in shensha:
            name = s.get("name_key", "").replace("shensha_", "").replace("_name", "")
            desc = s.get("desc_key", "")
            story.append(Paragraph(f"• {name}：{desc}", body_style))
    else:
        story.append(Paragraph("无明显神煞", body_style))
    
    story.append(Spacer(1, 20))
    
    # Personality
    story.append(Paragraph("性格与用神", heading_style))
    
    personality = result.get("personality", {})
    if personality:
        strength = personality.get("body_strength_key", "").replace("body_", "")
        story.append(Paragraph(f"身强身弱：{strength}", body_style))
        
        trait = personality.get("personality_key", "")
        if trait:
            story.append(Paragraph(f"性格特征：{trait}", body_style))
        
        career = personality.get("career_advice_key", "")
        if career:
            story.append(Paragraph(f"事业建议：{career}", body_style))
        
        relationship = personality.get("relationship_advice_key", "")
        if relationship:
            story.append(Paragraph(f"感情建议：{relationship}", body_style))
    
    story.append(Spacer(1, 20))
    
    # Dayun
    story.append(Paragraph("大运分析", heading_style))
    
    qiyun = result.get("qiyun", {})
    if qiyun:
        story.append(Paragraph(f"起运时间：{qiyun.get('qiyun_time', '未知')}", body_style))
        direction = "顺行" if qiyun.get("direction") == "forward" else "逆行"
        story.append(Paragraph(f"起运方向：{direction}", body_style))
    
    dayun = result.get("dayun", [])
    if dayun:
        dayun_data = [["大运", "主题", "建议"]]
        for d in dayun[:4]:  # Show first 4 dayun periods
            theme = d.get("theme_key", "").replace("dayun_", "").replace("_theme", "")
            advice = d.get("advice_key", "").replace("dayun_", "").replace("_advice", "")
            dayun_data.append([
                f"{d.get('start_year', '')}-{d.get('end_year', '')}",
                theme,
                advice[:30] + "..." if len(advice) > 30 else advice,
            ])
        
        dayun_table = Table(dayun_data, colWidths=[100, 100, 150])
        dayun_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), GOLD),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#ffffff")),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(dayun_table)
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("—" * 40, small_style))
    story.append(Paragraph("本报告由八字排盘系统自动生成，仅供文化研究参考。", small_style))
    story.append(Paragraph("命理分析属于传统文化范畴，不构成任何现实决策依据。", small_style))
    
    # Build
    doc.build(story)
    
    if output_path:
        return output_path
    else:
        buffer.seek(0)
        return buffer
