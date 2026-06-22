"""
AI Analysis Engine - OpenRouter Integration
Generates personalized bazi analysis using OpenRouter API
"""
import os
import json
import requests

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
# Use a model via OpenRouter (user must have credits)
AI_MODEL = "google/gemma-4-31b-it:free"


def build_bazi_context(result):
    """Build context string from bazi result for AI analysis."""
    bazi = result.get("bazi_detail", {})
    wuxing = result.get("wuxing_strength", {})
    personality = result.get("personality", {})
    qiyun = result.get("qiyun", {})
    shensha = result.get("shensha", [])

    pillars = []
    for key in ["year", "month", "day", "hour"]:
        p = bazi.get(key, {})
        pillars.append(f"{key}: {p.get('gan', '?')}{p.get('zhi', '?')}")

    wuxing_str = ", ".join(f"{k}: {v}%" for k, v in wuxing.items())
    shensha_str = ", ".join(s.get("name_key", "").replace("shensha_", "").replace("_name", "") for s in shensha)

    return f"""
Four Pillars (BaZi): {' | '.join(pillars)}
Five Elements: {wuxing_str}
Symbolic Stars: {shensha_str}
Body Strength: {personality.get('body_strength_key', '?')}
Day Master: {bazi.get('day', {}).get('gan', '?')}
Luck Pillar Start: {qiyun.get('qiyun_time', '?')} {qiyun.get('direction', '?')}
"""


PROMPTS = {
    "zh": """你是一位资深的八字命理师，擅长用现代语言解读传统命理。请根据以下八字信息，生成一段个性化的深度分析。

要求：
1. 用通俗易懂的语言，避免过于专业的术语
2. 分析要具体、有针对性，不要泛泛而谈
3. 涵盖：性格特点、事业方向、感情运势、健康提醒
4. 给出实用的建议，让用户觉得有收获
5. 语气温暖专业，像一位智慧的长者在交谈
6. 控制在 300-500 字

八字信息：
{context}

请生成分析：""",
    "en": """You are a master of Chinese Bazi (Four Pillars of Destiny) analysis. Generate a personalized, in-depth analysis based on the following bazi information.

Requirements:
1. Use modern, accessible language - avoid overly technical jargon
2. Be specific and targeted, not generic
3. Cover: personality traits, career direction, relationship fortune, health reminders
4. Give practical, actionable advice
5. Warm and professional tone, like a wise mentor
6. Keep it 300-500 words

Bazi Information:
{context}

Please generate the analysis:""",
    "ja": """あなたは中国の八字（四柱推命）の達人です。以下の八字情報に基づいて、個別化された詳細な分析を生成してください。

要件：
1. 現代的で分かりやすい言葉を使用
2. 具体的で的確な分析を行う
3. 性格、キャリア、恋愛運、健康について触れる
4. 実用的なアドバイスを提供
5. 温かく専門的な口調
6. 300〜500語に収める

八字情報：
{context}

分析を生成してください：""",
    "ko": """당신은 중국 사주팔자 분석의 대가입니다. 다음 사주 정보를 바탕으로 맞춤형 심층 분석을 생성하세요.

요구사항:
1. 현대적이고 이해하기 쉬운 언어 사용
2. 구체적이고 맞춤형 분석
3. 성격, 직업운, 연애운, 건강운 포함
4. 실용적이고 실행 가능한 조언
5. 따뜻하고 전문적인 어조
6. 300~500단어 내외

사주 정보:
{context}

분석을 생성하세요:""",
    "vi": """Bạn là một bậc thầy phân tích Tứ Trụ (Bát Tự). Hãy tạo ra một phân tích cá nhân hóa chi tiết dựa trên thông tin bát tự sau.

Yêu cầu:
1. Sử dụng ngôn ngữ hiện đại, dễ hiểu
2. Phân tích cụ thể, có trọng tâm
3. Bao gồm: tính cách, sự nghiệp, tình duyên, sức khỏe
4. Đưa ra lời khuyên thực tế, hữu ích
5. Giọng điệu ấm áp, chuyên nghiệp
6. Giới hạn 300-500 từ

Thông tin bát tự:
{context}

Hãy tạo phân tích:""",
}


def generate_ai_analysis(result, lang="zh"):
    """Call OpenRouter API to generate personalized bazi analysis."""
    if not OPENROUTER_API_KEY:
        return {"success": False, "error": "no_key"}

    context = build_bazi_context(result)
    prompt = PROMPTS.get(lang, PROMPTS["zh"]).format(context=context)

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.environ.get("APP_REFERER", "http://127.0.0.1:5000"),
                "X-Title": "BaZi Chart System",
            },
            json={
                "model": AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
                "temperature": 0.7,
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        analysis = data["choices"][0]["message"]["content"]
        return {"success": True, "analysis": analysis}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout"}
    except requests.exceptions.RequestException:
        return {"success": False, "error": "service_unavailable"}
    except (KeyError, IndexError):
        return {"success": False, "error": "invalid_response"}


def generate_ai_analysis_stream(result, lang="zh"):
    """Generator for streaming AI analysis via SSE."""
    if not OPENROUTER_API_KEY:
        yield f"data: {json.dumps({'error': 'no_key'})}\n\n"
        return

    context = build_bazi_context(result)
    prompt = PROMPTS.get(lang, PROMPTS["zh"]).format(context=context)

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.environ.get("APP_REFERER", "http://127.0.0.1:5000"),
                "X-Title": "BaZi Chart System",
            },
            json={
                "model": AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
                "temperature": 0.7,
                "stream": True,
            },
            timeout=60,
            stream=True,
        )
        response.raise_for_status()

        import time
        start_time = time.time()
        STREAM_TIMEOUT = 60

        for line in response.iter_lines():
            if time.time() - start_time > STREAM_TIMEOUT:
                break
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield f"data: {json.dumps({'content': content})}\n\n"
                    except json.JSONDecodeError:
                        continue
    except Exception:
        yield f"data: {json.dumps({'error': 'service_unavailable'})}\n\n"
