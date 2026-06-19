import urllib.request, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Test the result page
r = urllib.request.urlopen('http://127.0.0.1:5000/?load=15')
html = r.read().decode('utf-8')
print('Page length:', len(html))

# Check lang buttons
import re
btns = re.findall(r'onclick="loadLang\(\'(\w+)\'\)"', html)
print('Lang buttons:', btns)

# Check if loadLang function exists
print('loadLang defined:', 'function loadLang' in html)
print('applyI18N defined:', 'function applyI18N' in html)

# Check for any obvious JS errors
if 'SyntaxError' in html:
    print('SYNTAX ERROR in page!')
if 'Uncaught' in html:
    print('Uncaught error in page!')

# Try fetching ja.json
try:
    r2 = urllib.request.urlopen('http://127.0.0.1:5000/static/i18n/ja.json')
    data = r2.read()
    print('ja.json size:', len(data), 'bytes')
except Exception as e:
    print('ja.json FAILED:', e)
