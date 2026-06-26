import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\t\Desktop\bazi_app'
for dp, dns, fns in os.walk(base):
    if any(x in dp for x in ['__pycache__', 'env', '.git', '.sixth']):
        continue
    for fn in fns:
        if not fn.endswith('.py'):
            continue
        fp = os.path.join(dp, fn)
        try:
            with open(fp, encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if re.search(r'[\u4e00-\u9fff]', line):
                        if 'safe_error_response' in line:
                            rel = os.path.relpath(fp, base)
                            print(f'{rel}:{i}: {line.strip()[:120]}')
        except:
            pass
