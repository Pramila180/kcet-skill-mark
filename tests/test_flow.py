import requests
import sqlite3
import time
import os

BASE = 'http://127.0.0.1:5000'
DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'skill_marks.db')

def get_student_id(username):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT id FROM student WHERE username=?', (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_certificate_by_filename(filename):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT id, student_id, status, marks_allocated FROM certificate WHERE filename=? ORDER BY id DESC', (filename,))
    row = cur.fetchone()
    conn.close()
    return row


def student_upload(username, password, filename, event_id='1'):
    s = requests.Session()
    r = s.post(BASE + '/login', data={'username': username, 'password': password})
    print('Student login status:', r.status_code)
    with open(os.path.join('uploads', filename), 'rb') as f:
        files = {'certificate': (filename, f)}
        data = {'event_id': event_id}
        r = s.post(BASE + '/upload_certificate', files=files, data=data)
    print('Upload response code:', r.status_code)


def admin_approve(certificate_id):
    s = requests.Session()
    r = s.post(BASE + '/admin', data={'username':'facultycse','password':'facultycse123'})
    print('Admin login status:', r.status_code)
    r = s.get(BASE + f'/admin/approve/{certificate_id}')
    print('Approve response code:', r.status_code)


def admin_reject(certificate_id):
    s = requests.Session()
    r = s.post(BASE + '/admin', data={'username':'facultycse','password':'facultycse123'})
    print('Admin login status:', r.status_code)
    r = s.get(BASE + f'/admin/reject/{certificate_id}')
    print('Reject response code:', r.status_code)


if __name__ == '__main__':
    # ensure DB exists
    if not os.path.exists(DB):
        print('Database not found; ensure the Flask app has created it.')
        exit(1)

    student = '24UCS001'
    password = '24ucs001'

    # Upload and approve
    student_upload(student, password, 'dummy_cert2.txt', event_id='1')
    time.sleep(1)
    cert = get_certificate_by_filename('dummy_cert2.txt')
    if cert:
        print('Uploaded certificate (approve test):', cert)
        cert_id = cert[0]
        admin_approve(cert_id)
        time.sleep(1)
        cert = get_certificate_by_filename('dummy_cert2.txt')
        print('After approve:', cert)
    else:
        print('Certificate not found after upload (approve test)')

    # Upload and reject
    student_upload(student, password, 'dummy_cert_reject.txt', event_id='1')
    time.sleep(1)
    cert = get_certificate_by_filename('dummy_cert_reject.txt')
    if cert:
        print('Uploaded certificate (reject test):', cert)
        cert_id = cert[0]
        admin_reject(cert_id)
        time.sleep(1)
        cert = get_certificate_by_filename('dummy_cert_reject.txt')
        print('After reject:', cert)
    else:
        print('Certificate not found after upload (reject test)')
