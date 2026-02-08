# College Skill Marks Portal

A web application for students to upload certificates and earn skill marks for various academic and extracurricular activities.

## Features

- **Student Authentication**: Login system for students with usernames 24UCS001 to 24UCS190
- **Certificate Upload**: Upload certificates for different events
- **Automatic Analysis**: Basic certificate analysis to verify authenticity
- **Mark Allocation**: Automatic mark allocation based on certificate validation
- **Dashboard**: View total marks and uploaded certificates
- **Status Tracking**: Track certificate approval/rejection status

## Installation

1. **Install Python** (3.8 or higher)

2. **Clone or download** this project to your local machine

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## Login Credentials

- **Username**: 24UCS001 to 24UCS190
- **Password**: Same as username in lowercase
- **Example**: Username: 24UCS001, Password: 24ucs001

## Events and Marks

The system includes 18 different events with varying maximum marks:

1. Paper Presentation in Symposium - 2 marks
2. Tech Competitions Participation - 1 mark
3. Paper Presentation in NIT, IIT, etc. - 5 marks
4. Technical Competition Winning - 1 mark
5. Proposal Submission - 4 marks
6. NPTEL Online Certification Courses - 3 marks
7. Professional Chapter Registration - 1 mark
8. Paper Presentation & Conference - 3 marks
9. Tech Mag article publishing - 1 mark
10. National Design contest - 3 marks
11. Niral Thiruvizha / Industry project - 5 marks
12. Entrepreneurship / Patent / Journal - 5 marks
13. Approved Certification Courses - 3 marks
14. Sports Participation - 3 marks
15. Sports Winning / University team - 5 marks
16. Yoga / NCC / NSS / Clubs - 2 marks
17. SIH Participation - 2 marks
18. Internship through Placement - 3 marks

## Project Structure

```
skill mark web/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── login.html        # Login page
│   └── dashboard.html    # Student dashboard
├── uploads/              # Uploaded certificates storage
└── skill_marks.db        # SQLite database (created automatically)
```

## Certificate Analysis

The system includes basic certificate analysis functionality:

- **Keyword Matching**: Analyzes certificate filenames for relevant keywords
- **Event Validation**: Checks if certificate matches the selected event category
- **Status Assignment**: Marks certificates as approved or rejected based on analysis

**Note**: This is a basic implementation. For production use, consider implementing:
- OCR (Optical Character Recognition) for text extraction
- Machine learning models for better certificate validation
- Manual review process for disputed certificates

## Database Schema

The application uses SQLite with three main tables:

1. **Students**: Stores student information and total marks
2. **Events**: Contains event details and maximum marks
3. **Certificates**: Tracks uploaded certificates and their status

## Security Features

- Session-based authentication
- File upload validation
- SQL injection protection (via SQLAlchemy)
- CSRF protection (Flask-WTF can be added for enhanced security)

## Future Enhancements

- Admin panel for manual certificate review
- Advanced certificate analysis with AI/ML
- Email notifications for certificate status updates
- Export functionality for mark reports
- Integration with college ERP system

## Support

For any issues or questions, please contact the development team.

---

**Kamaraj College of Engineering and Technology**
*Skill Marks Management System*
