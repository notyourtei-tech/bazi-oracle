with open(r'C:\Users\t\Desktop\bazi_app\core\comprehensive_analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining Chinese strings
fixes = [
    ('"保持平常心就好"', '"comp_events_neutral_2"'),
    ('"保持自我，不要随波逐流"', '"comp_do_self_1"'),
    ('"学习新技能，为未来做准备"', '"comp_do_drain_0"'),
    ('"comp_watch_neutral_0",\n            "comp_watch_neutral_2",\n            "comp_do_neutral_2"', '"comp_do_neutral_0",\n            "comp_do_neutral_1",\n            "comp_do_neutral_2"'),
]

for old, new in fixes:
    content = content.replace(old, new)

# Fix indentation issue on line 204
content = content.replace(
    '"comp_events_drain_0",\n"comp_events_drain_1",',
    '"comp_events_drain_0",\n            "comp_events_drain_1",'
)

with open(r'C:\Users\t\Desktop\bazi_app\core\comprehensive_analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done - fixed remaining Chinese strings')
