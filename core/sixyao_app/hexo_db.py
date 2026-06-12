# hexo_db.py
HEXAGRAMS = []

for i in range(64):
    n = i + 1
    HEXAGRAMS.append({
        "id": i,
        "name_zh": f"第{n}卦",
        "name_ja": f"第{n}卦",
        "name_en": f"Hexagram {n}",
        "name_vi": f"Quẻ số {n}",
        "summary_zh": f"第{n}卦的含义需要结合具体问题、六亲、用神与动爻进行综合判断。本系统中作为示例卦使用。",
        "summary_ja": f"第{n}卦の意味は、質問内容・六親・用神・動爻と合わせて総合的に判断する必要があります。本アプリでは学習用のサンプルとして扱います。",
        "summary_en": f"The meaning of hexagram {n} depends on question, six relations, useful spirit and moving lines. Used here as sample.",
        "summary_vi": f"Ý nghĩa của quẻ số {n} cần luận cùng câu hỏi, lục thân, dụng thần và hào động."
    })
