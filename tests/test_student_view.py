import requests
from bs4 import BeautifulSoup

BASE = 'http://127.0.0.1:5000'

def check_student_dashboard():
    """Verify student dashboard shows approval/rejection messages"""
    s = requests.Session()
    
    # Login
    r = s.post(BASE + '/login', data={'username':'24UCS001','password':'24ucs001'})
    print(f'✓ Student login: {r.status_code}')
    
    # Get dashboard
    r = s.get(BASE + '/dashboard')
    print(f'✓ Dashboard: {r.status_code}')
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check for certificate sections
    has_certificates = 'Your Certificates' in r.text
    has_approved_status = 'Approved' in r.text
    has_rejected_status = 'Rejected' in r.text
    has_approval_msg = 'Approved by admin' in r.text
    has_rejection_msg = 'Rejected by admin' in r.text
    has_view_button = 'View Certificate' in r.text
    has_no_approve_reject = 'approve_certificate' not in r.text and 'reject_certificate' not in r.text
    
    print('\n📋 Student Dashboard Elements:')
    print(f'  ✓ "Your Certificates" section: {has_certificates}')
    print(f'  ✓ Approved status badge: {has_approved_status}')
    print(f'  ✓ Rejected status badge: {has_rejected_status}')
    print(f'  ✓ Approval message visible: {has_approval_msg}')
    print(f'  ✓ Rejection message visible: {has_rejection_msg}')
    print(f'  ✓ View Certificate button: {has_view_button}')
    print(f'  ✓ No Approve/Reject buttons: {has_no_approve_reject}')
    
    all_good = all([
        has_certificates,
        has_approved_status,
        has_rejected_status,
        has_approval_msg,
        has_rejection_msg,
        has_view_button,
        has_no_approve_reject
    ])
    
    return all_good

if __name__ == '__main__':
    print("=== Test 4: Student Dashboard Verification ===\n")
    if check_student_dashboard():
        print('\n✅ SUCCESS: Student dashboard shows all required elements')
    else:
        print('\n❌ FAILED: Some elements missing from student dashboard')
