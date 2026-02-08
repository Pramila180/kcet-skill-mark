import requests
from bs4 import BeautifulSoup

BASE = 'http://127.0.0.1:5000'

def check_student_dashboard_layout():
    """Verify new certificate layout matches screenshot"""
    s = requests.Session()
    
    # Login
    r = s.post(BASE + '/login', data={'username':'24UCS001','password':'24ucs001'})
    print(f'✓ Student login: {r.status_code}')
    
    # Get dashboard
    r = s.get(BASE + '/dashboard')
    print(f'✓ Dashboard: {r.status_code}')
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check for new layout elements
    certificates = soup.find_all('div', class_='certificate-item')
    print(f'\n📋 Found {len(certificates)} certificates on dashboard')
    
    if certificates:
        cert = certificates[0]
        
        # Check for left column
        cert_left = cert.find('div', class_='certificate-left')
        cert_title = cert.find('div', class_='certificate-title')
        cert_meta = cert.find('div', class_='certificate-meta')
        
        # Check for right column
        cert_right = cert.find('div', class_='certificate-right')
        status_badge = cert_right.find('span', class_=lambda x: x and 'status-' in x) if cert_right else None
        marks_badge = cert_right.find('span', class_='marks-badge') if cert_right else None
        cert_message = cert_right.find('div', class_='certificate-message') if cert_right else None
        view_btn = cert_right.find('a', class_='btn-view') if cert_right else None
        
        print('\n✅ New Layout Elements Found:')
        print(f'  - Left column (title + meta): {bool(cert_left and cert_title and cert_meta)}')
        print(f'  - Right column: {bool(cert_right)}')
        print(f'  - Status badge: {bool(status_badge)}')
        print(f'  - Marks badge: {bool(marks_badge)}')
        print(f'  - Admin message: {bool(cert_message)}')
        print(f'  - View button: {bool(view_btn)}')
        
        if cert_title:
            print(f'\n  Title: {cert_title.text.strip()}')
        if cert_meta:
            print(f'  Meta: {cert_meta.text.strip()[:80]}...')
        if cert_message:
            print(f'  Message: {cert_message.text.strip()}')
        
        all_good = all([cert_left, cert_title, cert_meta, cert_right, status_badge, marks_badge, view_btn])
        return all_good
    
    return False

if __name__ == '__main__':
    print("=== Testing Updated Certificate Layout ===\n")
    if check_student_dashboard_layout():
        print('\n✅ SUCCESS: New certificate layout matches screenshot!')
    else:
        print('\n❌ FAILED: Some layout elements missing')
