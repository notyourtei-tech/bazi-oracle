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

import json as _json
from xml.sax.saxutils import escape as xml_escape


def _load_i18n(lang="zh"):
    i18n_path = os.path.join(os.path.dirname(__file__), "..", "static", "i18n", f"{lang}.json")
    try:
        with open(i18n_path, "r", encoding="utf-8") as f:
            return _json.load(f)
    except Exception:
        return {}


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


def generate_pdf_report(result, output_path=None, lang="zh"):
    """
    Generate a professional PDF report for bazi analysis.
    
    Args:
        result: Bazi analysis result dict
        output_path: Output file path (if None, returns BytesIO)
        lang: Language code for i18n
    
    Returns:
        File path or BytesIO object
    """
    if not HAS_REPORTLAB:
        raise ImportError("reportlab is required for PDF generation")
    
    font_name = _register_chinese_font()
    t = _load_i18n(lang)
    
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
        # Validate output path to prevent path traversal
        abs_path = os.path.abspath(output_path)
        doc = SimpleDocTemplate(abs_path, pagesize=A4)
    else:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    story = []
    
    # Title
    story.append(Paragraph(t.get("pdf_title", "八字命盘分析报告"), title_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"{t.get('pdf_generated_time', '生成时间')}：{datetime.now().strftime('%Y-%m-%d %H:%M')}", small_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(t.get("pdf_pillar_heading", "四柱八字"), heading_style))
    
    bazi = result.get("bazi_detail", {})
    pillars_data = [
        [t.get("pdf_pillar_position", "柱位"), t.get("pdf_pillar_heavenly_stem", "天干"), t.get("pdf_pillar_earthly_branch", "地支"), t.get("pdf_pillar_nayin", "纳音")],
    ]
    
    pillar_names = {"year": t.get("pdf_pillar_year", "年柱"), "month": t.get("pdf_pillar_month", "月柱"), "day": t.get("pdf_pillar_day", "日柱"), "hour": t.get("pdf_pillar_hour", "时柱")}
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
    story.append(Paragraph(t.get("pdf_wuxing_heading", "五行强弱"), heading_style))
    
    wuxing = result.get("wuxing_strength", {})
    wx_names = {"wood": t.get("wuxing_wood", "木"), "fire": t.get("wuxing_fire", "火"), "earth": t.get("wuxing_earth", "土"), "metal": t.get("wuxing_metal", "金"), "water": t.get("wuxing_water", "水")}
    
    wx_data = [[t.get("pdf_wuxing_element", "五行"), t.get("pdf_wuxing_strength_label", "强度"), t.get("pdf_wuxing_status", "状态")]]
    for wx_key in ["wood", "fire", "earth", "metal", "water"]:
        score = wuxing.get(wx_key, 0)
        status = t.get("pdf_wuxing_strong", "旺") if score > 70 else (t.get("pdf_wuxing_weak", "弱") if score < 30 else t.get("pdf_wuxing_neutral", "中"))
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
    story.append(Paragraph(t.get("pdf_shensha_heading", "神煞信息"), heading_style))
    
    shensha = result.get("shensha", [])
    if shensha:
        for s in shensha:
            name_key = s.get("name_key", "")
            desc_key = s.get("desc_key", "")
            name = xml_escape(t.get(name_key, name_key.replace("shensha_", "").replace("_name", "")))
            desc = xml_escape(t.get(desc_key, desc_key))
            story.append(Paragraph(f"• {name}：{desc}", body_style))
    else:
        story.append(Paragraph(t.get("pdf_shensha_none", "无明显神煞"), body_style))
    
    story.append(Spacer(1, 20))
    
    # Personality
    story.append(Paragraph(t.get("pdf_personality_heading", "性格与用神"), heading_style))
    
    personality = result.get("personality", {})
    if personality:
        strength_key = personality.get("body_strength_key", "")
        strength = xml_escape(t.get(strength_key, strength_key.replace("body_", "")))
        story.append(Paragraph(f"{t.get('pdf_personality_strength', '身强身弱')}：{strength}", body_style))
        
        trait_key = personality.get("personality_key", "")
        trait = xml_escape(t.get(trait_key, trait_key))
        if trait:
            story.append(Paragraph(f"{t.get('pdf_personality_trait', '性格特征')}：{trait}", body_style))
        
        career_key = personality.get("career_advice_key", "")
        career = xml_escape(t.get(career_key, career_key))
        if career:
            story.append(Paragraph(f"{t.get('pdf_personality_career', '事业建议')}：{career}", body_style))
        
        relationship_key = personality.get("relationship_advice_key", "")
        relationship = xml_escape(t.get(relationship_key, relationship_key))
        if relationship:
            story.append(Paragraph(f"{t.get('pdf_personality_relationship', '感情建议')}：{relationship}", body_style))
    
    story.append(Spacer(1, 20))
    
    # Dayun
    story.append(Paragraph(t.get("pdf_dayun_heading", "大运分析"), heading_style))
    
    qiyun = result.get("qiyun", {})
    if qiyun:
        story.append(Paragraph(f"{t.get('pdf_dayun_qiyun_time', '起运时间')}：{qiyun.get('qiyun_time', t.get('pdf_dayun_unknown', '未知'))}", body_style))
        direction = t.get("pdf_dayun_forward", "顺行") if qiyun.get("direction") == "forward" else t.get("pdf_dayun_backward", "逆行")
        story.append(Paragraph(f"{t.get('pdf_dayun_direction', '起运方向')}：{direction}", body_style))
    
    dayun = result.get("dayun", [])
    if dayun:
        dayun_data = [[t.get("pdf_dayun_table_heading", "大运"), t.get("pdf_dayun_theme", "主题"), t.get("pdf_dayun_advice", "建议")]]
        for d in dayun[:4]:  # Show first 4 dayun periods
            theme_key = d.get("theme_key", "")
            advice_key = d.get("advice_key", "")
            theme = t.get(theme_key, theme_key.replace("dayun_", "").replace("_theme", ""))
            advice = t.get(advice_key, advice_key.replace("dayun_", "").replace("_advice", ""))
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
    story.append(Paragraph(t.get("pdf_footer_disclaimer", "本报告由八字排盘系统自动生成，仅供文化研究参考。"), small_style))
    story.append(Paragraph(t.get("pdf_footer_note", "命理分析属于传统文化范畴，不构成任何现实决策依据。"), small_style))
    
    # Build
    doc.build(story)
    
    if output_path:
        return abs_path
    else:
        buffer.seek(0)
        return buffer
