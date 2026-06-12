from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
from datetime import datetime
import random

app = Flask(__name__)

# 用新的 DB，别再碰你 sixyao.db 了
DB_PATH = "sixyao2.db"

LANGS = ["zh", "ja", "en", "vi"]

TEXTS = {
    "zh": {
        "app_title": "六爻占卜",
        "nav_home": "首页",
        "nav_history": "历史记录",
        "btn_start": "开始占卜",
        "method_coin": "摇卦（传统铜钱）",
        "method_time": "时间起卦",
        "method_number": "数字起卦",
        "method_label": "起卦方式",
        "number_placeholder": "请输入 0-999 的数字",
        "question_label": "问题 / 心中所想",
        "question_placeholder": "可写下你现在最在意的问题，也可以留空只看运势。",
        "result_title": "占卜结果",
        "hex_title_prefix": "第",
        "hex_title_suffix": "卦",
        "summary_notice": "此卦的具体含义需要结合问题本身、六亲、用神等综合判断，本页面提供的是日常生活向的大致参考。",
        "five_luck": "五大运势",
        "love": "恋爱 / 感情",
        "career": "工作 / 学业",
        "wealth": "金钱 / 财运",
        "health": "健康",
        "travel": "人际 / 出行",
        "now": "当前：",
        "future": "未来：",
        "advice": "建议：",
        "history_title": "占卜记录",
        "history_id": "ID",
        "history_method": "起卦方式",
        "history_question": "问题",
        "history_hex": "卦象",
        "history_time": "时间",
        "history_none": "目前还没有记录。",
        "method_name_coin": "摇卦",
        "method_name_time": "时间起卦",
        "method_name_number": "数字起卦",
    },
    "ja": {
        "app_title": "六爻占い",
        "nav_home": "トップ",
        "nav_history": "履歴",
        "btn_start": "占う",
        "method_coin": "揺卦（コイン法）",
        "method_time": "時間起卦",
        "method_number": "数字起卦",
        "method_label": "起卦方法",
        "number_placeholder": "0〜999 の数字を入力してください",
        "question_label": "占いたい内容・テーマ",
        "question_placeholder": "今一番気になっていることを書いてもいいし、空欄のまま運勢だけ見ても大丈夫です。",
        "result_title": "占い結果",
        "hex_title_prefix": "第",
        "hex_title_suffix": "卦",
        "summary_notice": "具体的な判断には質問内容・六親・用神などを総合して読む必要があります。このページでは日常生活向けの目安となる解説を表示しています。",
        "five_luck": "五大運勢",
        "love": "恋愛・感情",
        "career": "仕事・学業",
        "wealth": "金運・お金",
        "health": "健康",
        "travel": "人間関係・お出かけ",
        "now": "現在：",
        "future": "今後：",
        "advice": "アドバイス：",
        "history_title": "占い履歴",
        "history_id": "ID",
        "history_method": "方法",
        "history_question": "内容",
        "history_hex": "卦",
        "history_time": "時間",
        "history_none": "まだ履歴はありません。",
        "method_name_coin": "揺卦",
        "method_name_time": "時間起卦",
        "method_name_number": "数字起卦",
    },
    "en": {
        "app_title": "Six Yao Divination",
        "nav_home": "Home",
        "nav_history": "History",
        "btn_start": "Start",
        "method_coin": "Coin casting (traditional)",
        "method_time": "Time-based casting",
        "method_number": "Number casting",
        "method_label": "Casting method",
        "number_placeholder": "Enter a number from 0 to 999",
        "question_label": "Question / focus",
        "question_placeholder": "Write down what you care about most right now, or leave it blank to just see the general fortune.",
        "result_title": "Result",
        "hex_title_prefix": "Hexagram ",
        "hex_title_suffix": "",
        "summary_notice": "A precise reading requires combining the question, six relations and useful spirit. Here we show a practical, everyday-style summary.",
        "five_luck": "Five Aspects",
        "love": "Love / Relationship",
        "career": "Career / Study",
        "wealth": "Wealth / Money",
        "health": "Health",
        "travel": "People / Travel",
        "now": "Now:",
        "future": "Future:",
        "advice": "Advice:",
        "history_title": "History",
        "history_id": "ID",
        "history_method": "Method",
        "history_question": "Question",
        "history_hex": "Hexagram",
        "history_time": "Time",
        "history_none": "No records yet.",
        "method_name_coin": "Coin",
        "method_name_time": "Time",
        "method_name_number": "Number",
    },
    "vi": {
        "app_title": "Quẻ Lục Hào",
        "nav_home": "Trang chủ",
        "nav_history": "Lịch sử",
        "btn_start": "Bắt đầu bói",
        "method_coin": "Gieo quẻ bằng đồng xu",
        "method_time": "Lấy thời gian hiện tại",
        "method_number": "Nhập số để gieo quẻ",
        "method_label": "Cách gieo quẻ",
        "number_placeholder": "Nhập số từ 0 đến 999",
        "question_label": "Câu hỏi / điều đang nghĩ",
        "question_placeholder": "Bạn có thể viết điều mình băn khoăn nhất, hoặc để trống chỉ xem vận thế chung.",
        "result_title": "Kết quả",
        "hex_title_prefix": "Quẻ số ",
        "hex_title_suffix": "",
        "summary_notice": "Để luận quẻ chính xác cần kết hợp nội dung câu hỏi, Lục Thân và Dụng thần. Trang này chỉ đưa ra phần giải thích mang tính tham khảo cho đời sống hằng ngày.",
        "five_luck": "Năm phương diện",
        "love": "Tình cảm / Yêu đương",
        "career": "Công việc / Học tập",
        "wealth": "Tiền bạc / Tài vận",
        "health": "Sức khỏe",
        "travel": "Quan hệ / Đi lại",
        "now": "Hiện tại:",
        "future": "Tương lai:",
        "advice": "Gợi ý:",
        "history_title": "Lịch sử gieo quẻ",
        "history_id": "ID",
        "history_method": "Cách gieo",
        "history_question": "Câu hỏi",
        "history_hex": "Quẻ",
        "history_time": "Thời gian",
        "history_none": "Chưa có dữ liệu.",
        "method_name_coin": "Đồng xu",
        "method_name_time": "Thời gian",
        "method_name_number": "Con số",
    },
}


def get_lang():
    if request.method == "POST":
        lang = request.form.get("lang")
    else:
        lang = request.args.get("lang")
    if lang not in LANGS:
        lang = "zh"
    return lang


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT,
            question TEXT,
            hex_code INTEGER,
            lines TEXT,
            moving TEXT,
            liuchin TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# ========== 起卦相关 ==========

def roll_coin_line():
    # 三个“硬币”，0/1 取奇偶做阴阳，0 或 3 当动爻
    total = sum(random.randint(0, 1) for _ in range(3))
    yang = 1 if total % 2 == 1 else 0
    moving = 1 if total in (0, 3) else 0
    return yang, moving


def make_lines(method, number=None):
    lines = []
    moving = []

    if method == "coin":
        for i in range(6):
            v, mv = roll_coin_line()
            lines.append(v)
            if mv:
                moving.append(i + 1)  # 1-based

    elif method == "time":
        now = datetime.now()
        seed = now.hour * 3600 + now.minute * 60 + now.second
        random.seed(seed)
        for i in range(6):
            v = random.randint(0, 1)
            lines.append(v)
        moving = [3]

    elif method == "number" and number is not None:
        s = str(abs(number))
        if not s:
            s = "0"
        for i in range(6):
            d = int(s[i % len(s)])
            v = d % 2
            lines.append(v)
        idx = sum(lines) % 6
        moving = [idx if idx != 0 else 6]

    else:
        for i in range(6):
            v = random.randint(0, 1)
            lines.append(v)
        moving = []

    return lines, moving


def lines_to_code(lines):
    code = 0
    for i, v in enumerate(lines):
        if v:
            code |= (1 << i)
    return code


def calc_liuchin(lines):
    # 简化版六亲，只是起个展示作用
    return ["父母", "兄弟", "妻财", "子孙", "官鬼", "父母"]


# ========== 运势解析 ==========

def build_analysis(lines, moving, liuchin):
    # 焦点爻：有动爻用第一个动爻，否则用三爻
    if moving:
        focus_idx = max(1, min(6, int(moving[0])))
    else:
        focus_idx = 3
    focus_kin = liuchin[focus_idx - 1] if 0 <= focus_idx - 1 < len(liuchin) else "用神"

    def pack(zh_now, zh_future, zh_adv,
             ja_now, ja_future, ja_adv,
             en_now, en_future, en_adv,
             vi_now, vi_future, vi_adv,
             title_zh, title_ja, title_en, title_vi):
        return {
            "title": {
                "zh": title_zh,
                "ja": title_ja,
                "en": title_en,
                "vi": title_vi,
            },
            "now": {
                "zh": zh_now,
                "ja": ja_now,
                "en": en_now,
                "vi": vi_now,
            },
            "future": {
                "zh": zh_future,
                "ja": ja_future,
                "en": en_future,
                "vi": vi_future,
            },
            "advice": {
                "zh": zh_adv,
                "ja": ja_adv,
                "en": en_adv,
                "vi": vi_adv,
            },
        }

    analysis = {}

    # 恋爱 / 感情
    analysis["love"] = pack(
        zh_now=f"感情整体气氛还算平稳，本卦的用神落在「{focus_kin}」位，说明情感状态和现实环境联系很深，需要多一点真诚的交流。",
        zh_future="未来一段时间有机会在原有基础上慢慢加深关系，但进展会比较缓慢，适合以朋友般的距离相处。",
        zh_adv="建议不要急着给结果，多观察对方的节奏和立场，用具体行动表达关心，比嘴上承诺更有效。",
        ja_now=f"恋愛の雰囲気は大きな波は少なく、用神は「{focus_kin}」にあり、気持ちと現実の状況が強く結び付いている状態です。素直なコミュニケーションが大事になります。",
        ja_future="しばらくはゆっくりと関係が深まっていく暗示です。急に形を決めるより、友達に近い距離感を保つほうがうまくいきやすいでしょう。",
        ja_adv="答えを急がず、相手のペースや立場をよく観察してください。言葉よりも、行動で思いやりを見せることが良い方向につながります。",
        en_now=f"The overall mood in love is relatively stable. The useful spirit sits on the “{focus_kin}” line, showing that feelings are closely tied to real-life conditions and need honest communication.",
        en_future="In the coming period the relationship can deepen step by step, but the pace is slow. It’s better to stay natural, almost like good friends, instead of forcing a clear label.",
        en_adv="Don’t rush for a conclusion. Pay attention to the other person’s rhythm and position. Concrete actions of care work better than grand promises.",
        vi_now=f"Bầu không khí tình cảm khá ổn định. Dụng thần rơi vào vị trí “{focus_kin}”, cho thấy cảm xúc gắn chặt với hoàn cảnh thực tế, cần giao tiếp chân thành hơn.",
        vi_future="Thời gian tới có cơ hội phát triển từ từ trên nền tảng hiện tại, nhưng tiến triển sẽ hơi chậm, phù hợp giữ khoảng cách tự nhiên như bạn bè thân.",
        vi_adv="Đừng vội ép phải có câu trả lời rõ ràng. Hãy quan sát nhịp độ và lập trường của đối phương, dùng hành động cụ thể để thể hiện quan tâm sẽ hiệu quả hơn lời nói.",
        title_zh="恋爱 / 感情",
        title_ja="恋愛・感情",
        title_en="Love / Relationship",
        title_vi="Tình cảm / Yêu đương",
    )

    # 工作 / 学业
    analysis["career"] = pack(
        zh_now=f"目前工作或学业压力存在，但大多仍在可控范围内，本卦用神所在的「{focus_kin}」位提示你要先站稳现在的位置。",
        zh_future="未来会有岗位调整或任务变化的可能，过程中可能出现一点反复，但也是累积经验的阶段。",
        zh_adv="建议把基础工作做好，再慢慢争取机会。与上司、老师的沟通要尽量具体，避免互相猜测。",
        ja_now=f"仕事・学業にはそれなりのプレッシャーがありますが、多くはまだコントロールできる範囲です。用神が「{focus_kin}」にあることから、まずは今いる立場をしっかり固めることが重要です。",
        ja_future="今後、担当やポジションが変わる可能性があります。多少の行きつ戻りつはありますが、その過程で経験が蓄積されていきます。",
        ja_adv="まずは基礎的な業務・勉強を丁寧にこなし、その上でチャンスを少しずつ取りに行きましょう。上司や先生とは、抽象的な言い方より具体的な相談を心がけてください。",
        en_now=f"There is some pressure in work or study, but it is still within a controllable range. With the useful spirit on the “{focus_kin}” line, you are asked to stabilise your current position first.",
        en_future="There may be changes in tasks or position in the future. The process can be two steps forward and one step back, but it is a period of gaining experience.",
        en_adv="Do the fundamentals carefully and then look for chances little by little. When talking to bosses or teachers, be concrete instead of vague to avoid misunderstandings.",
        vi_now=f"Công việc hoặc học tập hiện tại có áp lực, nhưng vẫn nằm trong phạm vi có thể kiểm soát. Dụng thần ở vị trí “{focus_kin}” nhắc bạn nên đứng vững chỗ hiện tại trước.",
        vi_future="Thời gian tới có khả năng thay đổi nhiệm vụ hoặc vị trí. Quá trình có thể hơi lặp đi lặp lại, nhưng cũng là giai đoạn tích lũy kinh nghiệm.",
        vi_adv="Hãy làm chắc phần nền tảng, sau đó từ từ tranh thủ cơ hội. Khi trao đổi với cấp trên hoặc thầy cô, nên nói rõ ràng, tránh mơ hồ khiến đôi bên hiểu lầm.",
        title_zh="工作 / 学业",
        title_ja="仕事・学業",
        title_en="Career / Study",
        title_vi="Công việc / Học tập",
    )

    # 金钱 / 财运
    analysis["wealth"] = pack(
        zh_now="近期财运整体比较平稳，适合踏实理财，不宜一次性投入太多冒险项目。",
        zh_future="未来有逐步改善的空间，但需要时间累积，偏向细水长流的收入模式。",
        zh_adv="建议做好收支记录，避免冲动消费和情绪化购物，把钱先留给真正重要的开支。",
        ja_now="最近の金運は大きな波は少なく、堅実なお金の管理に向いている時期です。一度に大きくリスクを取る投資は控えたほうがよいでしょう。",
        ja_future="今後はゆっくりと改善していく余地があります。どちらかというと、ドカンと一発よりも、コツコツ積み重ねるタイプの収入が育ちやすい時期です。",
        ja_adv="収支の記録をつけ、衝動買いやストレス発散の浪費を控えましょう。本当に必要な支出を優先し、それ以外は一度立ち止まって考えることが大切です。",
        en_now="Money luck is relatively stable right now. It is suitable for steady financial planning, not for throwing a big sum into high-risk projects.",
        en_future="There is room for gradual improvement in the future, but it will grow over time. The trend is more like a slow but steady stream rather than a sudden windfall.",
        en_adv="Keep track of income and expenses. Avoid impulse and emotional spending, and reserve money first for what is truly important.",
        vi_now="Tài vận gần đây khá ổn định, phù hợp quản lý tiền một cách chắc chắn, không nên dồn nhiều tiền vào dự án mạo hiểm.",
        vi_future="Tương lai có không gian cải thiện dần dần, cần thời gian tích lũy, thiên về dòng tiền ổn định lâu dài hơn là trúng đậm một lần.",
        vi_adv="Nên ghi chép thu chi, tránh mua sắm bốc đồng hay chi tiêu do cảm xúc. Hãy ưu tiên tiền cho những khoản thật sự quan trọng.",
        title_zh="金钱 / 财运",
        title_ja="金運・お金",
        title_en="Wealth / Money",
        title_vi="Tiền bạc / Tài vận",
    )

    # 健康
    analysis["health"] = pack(
        zh_now="身体状态可能有轻微疲劳或作息不规律的情况，需要让自己有真正休息的时间。",
        zh_future="如果能调整生活节奏，健康有望慢慢回到比较稳定的水平；若长期透支，则小毛病会反复出现。",
        zh_adv="建议适度运动、规律睡眠，少熬夜少久坐。有旧病史的人要按时复查，不要拖延。",
        ja_now="体調はやや疲れ気味、あるいは生活リズムの乱れが出やすい時期です。本当の意味で休める時間を意識的に確保する必要があります。",
        ja_future="生活リズムを整えれば、健康状態は少しずつ安定していくでしょう。逆に、長期間無理を続けると、小さな不調が何度もぶり返す暗示があります。",
        ja_adv="軽い運動と規則正しい睡眠を心がけ、徹夜や長時間の座りっぱなしを減らしましょう。持病がある人は、検査や通院を先延ばしにしないことが大切です。",
        en_now="Your body may feel slightly tired or your daily routine may be irregular. You need to deliberately secure real rest time for yourself.",
        en_future="If you can adjust your lifestyle, your condition is likely to return to a more stable level. If you keep overworking, small health issues may come and go repeatedly.",
        en_adv="Moderate exercise and regular sleep are recommended. Reduce staying up late and sitting for very long periods. If you have a chronic problem, don’t delay check-ups.",
        vi_now="Cơ thể có thể hơi mệt hoặc giờ giấc sinh hoạt không đều, cần chủ động dành thời gian nghỉ ngơi thật sự.",
        vi_future="Nếu điều chỉnh được nhịp sống, sức khỏe sẽ dần ổn định hơn. Nếu tiếp tục làm việc quá sức lâu dài, các triệu chứng lặt vặt sẽ lập đi lập lại.",
        vi_adv="Hãy vận động nhẹ nhàng, ngủ đúng giờ, hạn chế thức khuya và ngồi quá lâu. Ai có bệnh cũ thì nên tái khám đúng hẹn, đừng trì hoãn.",
        title_zh="健康",
        title_ja="健康",
        title_en="Health",
        title_vi="Sức khỏe",
    )

    # 人际 / 出行
    analysis["travel"] = pack(
        zh_now="人际关系整体还算顺畅，但偶尔会因为表达方式不同而产生误会，需要多一点耐心听对方说完。",
        zh_future="未来在出行、聚会或社交场合中，可能认识新的朋友或合作对象，对视野有拓展的帮助。",
        zh_adv="建议说话前先想一想对方的立场，必要时用更温和、具体的方式说明自己的想法。外出时注意时间与安全。",
        ja_now="人間関係は全体的に悪くはありませんが、表現の仕方の違いから誤解が生まれやすい時期です。相手の話を最後まで聞く姿勢が大切になります。",
        ja_future="今後、外出・イベント・交流の場で、新しい友人や協力相手と出会う可能性があります。視野が広がるきっかけにもなりそうです。",
        ja_adv="話す前に一度、相手の立場を想像してみてください。必要であれば、もう少し柔らかく・具体的に自分の考えを説明するとよいでしょう。外出時は時間と安全面の確認も忘れずに。",
        en_now="Relationships are generally smooth, but misunderstandings can arise from different ways of expressing things. It helps to patiently listen to others to the end.",
        en_future="In future trips, gatherings or social events, you may meet new friends or partners, which can broaden your horizon.",
        en_adv="Before speaking, think about the other person’s position and, when needed, explain your ideas in a gentler and more concrete way. Pay attention to time and safety when going out.",
        vi_now="Quan hệ với mọi người nhìn chung khá ổn, nhưng đôi khi dễ hiểu lầm do cách diễn đạt khác nhau, cần kiên nhẫn nghe đối phương nói hết.",
        vi_future="Trong các chuyến đi, buổi gặp gỡ hoặc hoạt động giao lưu sắp tới, bạn có thể quen thêm bạn mới hoặc đối tác hợp tác, giúp mở rộng tầm nhìn.",
        vi_adv="Trước khi nói hãy thử nghĩ từ góc độ của người khác, khi cần nên diễn đạt ý của mình mềm mại và cụ thể hơn. Khi ra ngoài nhớ chú ý thời gian và an toàn.",
        title_zh="人际 / 出行",
        title_ja="人間関係・お出かけ",
        title_en="People / Travel",
        title_vi="Quan hệ / Đi lại",
    )

    return analysis


# ========== 路由 ==========

@app.route("/")
def index():
    lang = get_lang()
    t = TEXTS[lang]
    lang_urls = {code: url_for("index", lang=code) for code in LANGS}
    return render_template("index.html", lang=lang, t=t, lang_urls=lang_urls)


@app.route("/result", methods=["POST"])
def result():
    lang = get_lang()
    t = TEXTS[lang]

    method = request.form.get("method", "coin")
    question = request.form.get("question", "").strip()
    number_raw = request.form.get("number", "").strip()

    number_val = None
    if method == "number":
        try:
            number_val = int(number_raw)
        except ValueError:
            number_val = 0

    lines, moving = make_lines(method, number_val)
    liuchin = calc_liuchin(lines)
    hex_code = lines_to_code(lines)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO history (method, question, hex_code, lines, moving, liuchin, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            method,
            question,
            hex_code,
            json.dumps(lines, ensure_ascii=False),
            json.dumps(moving, ensure_ascii=False),
            json.dumps(liuchin, ensure_ascii=False),
            created_at,
        ),
    )
    hid = cur.lastrowid
    conn.commit()
    conn.close()

    return redirect(url_for("view", hid=hid, lang=lang))


@app.route("/history")
def history():
    lang = get_lang()
    t = TEXTS[lang]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, method, question, hex_code, created_at FROM history ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    lang_urls = {code: url_for("history", lang=code) for code in LANGS}

    return render_template("history.html", lang=lang, t=t, rows=rows, lang_urls=lang_urls)


@app.route("/view/<int:hid>")
def view(hid):
    lang = get_lang()
    t = TEXTS[lang]

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, method, question, hex_code, lines, moving, liuchin, created_at FROM history WHERE id=?",
        (hid,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return "Not Found", 404

    _, method, question, hex_code, lines_json, moving_json, liuchin_json, created_at = row

    try:
        lines = json.loads(lines_json)
    except Exception:
        lines = [0, 0, 0, 0, 0, 0]

    try:
        moving = json.loads(moving_json)
    except Exception:
        moving = []

    try:
        liuchin = json.loads(liuchin_json)
    except Exception:
        liuchin = calc_liuchin(lines)

    analysis = build_analysis(lines, moving, liuchin)
    hex_no = hex_code + 1

    lang_urls = {code: url_for("view", hid=hid, lang=code) for code in LANGS}

    return render_template(
        "result.html",
        lang=lang,
        t=t,
        lang_urls=lang_urls,
        hid=hid,
        method=method,
        question=question,
        created_at=created_at,
        hex_no=hex_no,
        lines=lines,
        moving=moving,
        liuchin=liuchin,
        analysis=analysis,
    )


if __name__ == "__main__":
    print("初始化数据库 sixyao2.db ...")
    init_db()
    print("启动: http://127.0.0.1:8888")
    app.run(debug=True, host="127.0.0.1", port=8888)
