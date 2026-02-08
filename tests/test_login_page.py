import requests
from bs4 import BeautifulSoup

BASE = 'http://127.0.0.1:5000'

def check_login_page():
    """Verify student login page doesn't have Back/Admin links"""
    r = requests.get(BASE + '/login')
    print(f'✓ Login page: {r.status_code}')
    
    has_back_link = '← Back to Home' in r.text
    has_admin_link = 'Admin Login' in r.text
    has_separator = 'Back to Home | Admin Login' in r.text
    
    print('\n🔐 Login Page Elements:')
    print(f'  ✓ No "← Back to Home" link: {not has_back_link}')
    print(f'  ✓ No "Admin Login" link: {not has_admin_link}')
    print(f'  ✓ No separator pipe: {not has_separator}')
    
    all_good = not (has_back_link or has_admin_link or has_separator)
    
    return all_good

if __name__ == '__main__':
    print("=== Test 5: Student Login Page Verification ===\n")
    if check_login_page():
        print('\n✅ SUCCESS: Login page has no Back/Admin links')
    else:
        print('\n❌ FAILED: Login page still has unwanted links')
