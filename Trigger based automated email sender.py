import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

# ===== CONFIGURATION ===== (Replace these values)
EMAIL_CONFIG = {
    'imap_server': 'imap.gmail.com',
    'imap_port': 993,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'example.1@gmail.com',          # Your Gmail address
    'password': 'app password',          # Your app password (not regular password)
    'check_interval': 300,                    # Check every 5 minutes (seconds)
    'auto_reply_subject': 'Auto-reply: Thank you for your email',
    'auto_reply_body': '''Hello,

Thank you for your email. This is an automated response to let you know 
I've received your message and will get back to you as soon as possible.

Best regards,
Automated Response System'''
}

# ===== TRACK PROCESSED EMAILS =====
processed_emails = set()

def extract_clean_email(raw_email):
    """Extract just the email address from 'Name <email@domain.com>' format"""
    if '<' in raw_email and '>' in raw_email:
        return raw_email.split('<')[1].split('>')[0].strip()
    return raw_email.strip()

def check_new_emails():
    """Check for and process new emails"""
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(EMAIL_CONFIG['imap_server'], EMAIL_CONFIG['imap_port'])
        mail.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        mail.select('inbox')
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        if status == 'OK':
            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    message_id = msg['Message-ID']
                    from_email = extract_clean_email(msg['from'])
                    subject = msg['subject']
                    
                    if message_id and message_id not in processed_emails:
                        print(f"New email from {from_email}: {subject}")
                        send_auto_reply(from_email)
                        processed_emails.add(message_id)
        
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Error checking emails: {e}")

def send_auto_reply(to_email):
    """Send automatic response"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = to_email
        msg['Subject'] = EMAIL_CONFIG['auto_reply_subject']
        
        msg.attach(MIMEText(EMAIL_CONFIG['auto_reply_body'], 'plain'))
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.sendmail(EMAIL_CONFIG['email'], to_email, msg.as_string())
        
        print(f"Sent auto-reply to {to_email}")
    except Exception as e:
        print(f"Error sending reply: {e}")

def main():
    print("Starting email auto-responder...")
    print(f"Monitoring account: {EMAIL_CONFIG['email']}")
    print(f"Checking every {EMAIL_CONFIG['check_interval']} seconds")
    
    while True:
        check_new_emails()
        time.sleep(EMAIL_CONFIG['check_interval'])

if __name__ == "__main__":
    main()
