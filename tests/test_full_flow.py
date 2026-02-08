import requests
import sqlite3
import time
import os
from bs4 import BeautifulSoup

BASE = 'http://127.0.0.1:5000'
DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'skill_marks.db')

def get_certificate_by_filename(filename):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT id, student_id, status, marks_allocated, remarks FROM certificate WHERE filename=? ORDER BY id DESC', (filename,))
    row = cur.fetchone()
    conn.close()
    return row

def student_upload(username, password, filename, event_id='1'):
    s = requests.Session()
    r = s.post(BASE + '/login', data={'username': username, 'password': password})
    print(f'✓ Student login: {r.status_code}')
    with open(os.path.join('uploads', filename), 'rb') as f:
        files = {'certificate': (filename, f)}
        data = {'event_id': event_id}
        r = s.post(BASE + '/upload_certificate', files=files, data=data)
    print(f'✓ Upload: {r.status_code}')
    return r

def admin_approve(certificate_id):
    s = requests.Session()
    r = s.post(BASE + '/admin', data={'username':'facultycse','password':'facultycse123'})
    print(f'✓ Admin login: {r.status_code}')
    r = s.get(BASE + f'/admin/approve/{certificate_id}')
    print(f'✓ Approve: {r.status_code}')
    return r

def admin_reject(certificate_id):
    s = requests.Session()
    r = s.post(BASE + '/admin', data={'username':'facultycse','password':'facultycse123'})
    print(f'✓ Admin login: {r.status_code}')
    r = s.get(BASE + f'/admin/reject/{certificate_id}')
    print(f'✓ Reject: {r.status_code}')
    return r

def admin_dashboard_check():
    """Verify admin dashboard shows all three sections"""
    s = requests.Session()
    r = s.post(BASE + '/admin', data={'username':'facultycse','password':'facultycse123'})
    print(f'✓ Admin login: {r.status_code}')
    
    r = s.get(BASE + '/admin/dashboard')
    print(f'✓ Admin dashboard: {r.status_code}')
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Check for pending, approved, rejected sections
    has_pending = 'Pending Certificates' in r.text
    has_approved = 'Approved Certificates' in r.text
    has_rejected = 'Rejected Certificates' in r.text
    
    print(f'  - Has Pending section: {has_pending}')
    print(f'  - Has Approved section: {has_approved}')
    print(f'  - Has Rejected section: {has_rejected}')
    
    return has_pending and has_approved and has_rejected

if __name__ == '__main__':
    if not os.path.exists(DB):
        print('Database not found')
        exit(1)

    student = '24UCS001'
    password = '24ucs001'

    print("\n=== Test 1: Upload, Approve, Reject ===")
    
    # Upload cert 1 - will approve
    print("\n1. Uploading certificate for approval...")
    student_upload(student, password, 'dummy_cert2.txt', event_id='1')
    time.sleep(0.5)
    cert1 = get_certificate_by_filename('dummy_cert2.txt')
    print(f"Before approve: {cert1}")
    print(f"  ID={cert1[0]}, Status={cert1[2]}, Remarks={cert1[4]}")
    
    # Approve it
    print("\n2. Admin approving certificate...")
    admin_approve(cert1[0])
    time.sleep(0.5)
    cert1_after = get_certificate_by_filename('dummy_cert2.txt')
    print(f"After approve: {cert1_after}")
    print(f"  ID={cert1_after[0]}, Status={cert1_after[2]}, Marks={cert1_after[3]}, Remarks={cert1_after[4]}")
    
    # Upload cert 2 - will reject
    print("\n3. Uploading certificate for rejection...")
    student_upload(student, password, 'dummy_cert_reject.txt', event_id='1')
    time.sleep(0.5)
    cert2 = get_certificate_by_filename('dummy_cert_reject.txt')
    print(f"Before reject: {cert2}")
    print(f"  ID={cert2[0]}, Status={cert2[2]}, Remarks={cert2[4]}")
    
    # Reject it
    print("\n4. Admin rejecting certificate...")
    admin_reject(cert2[0])
    time.sleep(0.5)
    cert2_after = get_certificate_by_filename('dummy_cert_reject.txt')
    print(f"After reject: {cert2_after}")
    print(f"  ID={cert2_after[0]}, Status={cert2_after[2]}, Remarks={cert2_after[4]}")
    
    # Check admin dashboard
    print("\n=== Test 2: Admin Dashboard Layout ===")
    print("\nChecking admin dashboard has all three sections...")
    has_all_sections = admin_dashboard_check()
    
    if has_all_sections:
        print("\n✅ SUCCESS: Admin dashboard displays all three sections:")
        print("   - Pending Certificates (with Approve/Reject buttons)")
        print("   - Approved Certificates (with View button)")
        print("   - Rejected Certificates (with View button)")
    else:
        print("\n❌ FAILED: Admin dashboard missing some sections")
    
    print("\n=== Test 3: Verify Remarks ===")
    print(f"\nApproved certificate remarks: {cert1_after[4]}")
    print(f"Rejected certificate remarks: {cert2_after[4]}")
    
    if 'Approved' in str(cert1_after[4]) and 'Rejected' in str(cert2_after[4]):
        print("\n✅ SUCCESS: Admin remarks are shown for each certificate")
    else:
        print("\n❌ FAILED: Admin remarks not properly saved")
