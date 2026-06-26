import sys, re, traceback
sys.stdout.reconfigure(encoding='utf-8')
from app import app

try:
    with app.test_client() as client:
        resp = client.get('/')
        with client.session_transaction() as sess:
            csrf = sess.get('_csrf_token', '')
        
        resp = client.post('/', data={
            '_csrf_token': csrf,
            'name': 'Test',
            'gender': 'male',
            'birth_country': 'CN',
            'birth_date': '1990-05-15',
            'birth_time': '10:30',
            'birth_city': 'Beijing'
        }, follow_redirects=True)
        
        print(f'Status: {resp.status_code}')
        html = resp.data.decode('utf-8')
        
        if 'Forbidden' in html or '403' in html:
            print('FORBIDDEN detected!')
        
        if 'life_advice' in html:
            print('life_advice: YES')
        else:
            print('life_advice: NO')
        
        if 'career_direction' in html:
            print('career_direction: YES')
        else:
            print('career_direction: NO')
        
        print(f'Page length: {len(html)}')
except Exception as e:
    traceback.print_exc()
