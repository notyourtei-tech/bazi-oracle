import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import app

with app.test_client() as client:
    # Test all routes
    for path in ['/', '/login', '/register', '/explain', '/history']:
        try:
            r = client.get(path)
            print(f'GET {path}: {r.status_code}')
            if r.status_code != 200:
                html = r.data.decode('utf-8')
                print(f'  Content: {html[:300]}')
        except Exception as e:
            print(f'GET {path}: ERROR - {e}')
    
    # Test POST to index (simulating form submission)
    try:
        r = client.post('/', data={
            '_csrf_token': 'test',
            'birth_country': 'CN',
            'birth_date': '1990-01-15',
            'birth_time': '10:30',
            'gender': 'male',
            'name': 'test'
        })
        print(f'POST /: {r.status_code}')
        if r.status_code != 200:
            html = r.data.decode('utf-8')
            if 'Exception' in html or 'error' in html.lower():
                print(f'  Error detected in response')
    except Exception as e:
        print(f'POST /: ERROR - {type(e).__name__}: {e}')
