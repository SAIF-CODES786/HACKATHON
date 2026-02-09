"""
Email Integration Module
Send notifications and candidate reports via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional
import os


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
    
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = False
    ) -> bool:
        """
        Send email with optional attachments
        """
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for filepath in attachments:
                    with open(filepath, 'rb') as f:
                        attachment = MIMEApplication(f.read())
                        attachment.add_header(
                            'Content-Disposition',
                            'attachment',
                            filename=os.path.basename(filepath)
                        )
                        msg.attach(attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def send_candidate_report(
        self,
        recipient: str,
        candidates: List[dict],
        job_title: str
    ) -> bool:
        """
        Send ranked candidate report to recruiter
        """
        subject = f"Candidate Rankings for {job_title}"
        
        # Create HTML body
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                .high-score {{ background-color: #d4edda; }}
                .medium-score {{ background-color: #fff3cd; }}
                .low-score {{ background-color: #f8d7da; }}
            </style>
        </head>
        <body>
            <h2>Top Candidates for {job_title}</h2>
            <p>Here are the top ranked candidates based on your job requirements:</p>
            
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Total Score</th>
                    <th>Skills</th>
                    <th>Experience</th>
                </tr>
        """
        
        for candidate in candidates[:10]:  # Top 10
            score = candidate.get('total_score', 0)
            score_class = 'high-score' if score >= 80 else 'medium-score' if score >= 60 else 'low-score'
            
            body += f"""
                <tr class="{score_class}">
                    <td>{candidate.get('rank', 'N/A')}</td>
                    <td>{candidate.get('name', 'Unknown')}</td>
                    <td>{candidate.get('email', 'N/A')}</td>
                    <td>{score:.1f}</td>
                    <td>{', '.join(candidate.get('skills', [])[:5])}</td>
                    <td>{candidate.get('years_of_experience', 0)} years</td>
                </tr>
            """
        
        body += """
            </table>
            <p>Login to the system to view detailed candidate profiles and analytics.</p>
        </body>
        </html>
        """
        
        return self.send_email(recipient, subject, body, html=True)
    
    def send_welcome_email(self, recipient: str, username: str) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to Resume Screening System"
        body = f"""
        Hello {username},
        
        Welcome to the Resume Screening System!
        
        You can now:
        - Upload and parse resumes
        - Score candidates using AI
        - View analytics and insights
        - Export results
        
        Login at: http://localhost:5173
        
        Best regards,
        Resume Screening Team
        """
        
        return self.send_email(recipient, subject, body)


# Singleton instance
email_service = EmailService()
