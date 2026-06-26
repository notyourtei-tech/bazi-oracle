with open(r'C:\Users\t\Desktop\bazi_app\core\analysis.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace lines 202-213 (0-indexed: 201-212)
new_lines_202_213 = [
    '    if age < 18:\n',
    '        extra = "liunian_event_hint_child"\n',
    '    elif age < 28:\n',
    '        extra = "liunian_event_hint_youth"\n',
    '    elif age < 38:\n',
    '        extra = "liunian_event_hint_adult"\n',
    '    elif age < 48:\n',
    '        extra = "liunian_event_hint_middle"\n',
    '    elif age < 60:\n',
    '        extra = "liunian_event_hint_senior"\n',
    '    else:\n',
    '        extra = "liunian_event_hint_elderly"\n',
]

lines[201:213] = new_lines_202_213

with open(r'C:\Users\t\Desktop\bazi_app\core\analysis.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done - replaced liunian event hints')
