import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime

def send_email():
    # Email configuration
    sender_email = "example.1@gmail.com"  # Replace with your email
    sender_password = "app password"      # Replace with your password or app password
    receiver_email = "yagyeshvijay017@gmail.com"  # Replace with recipient email
    subject = "Weekly Update - " + datetime.now().strftime("%Y-%m-%d")
    
    # Email content
    body = """
    <html>
        <body>
            <h1>Weekly Update</h1>
            <p>Hello,</p>
            <p>This is your automated weekly email sent every Monday morning.</p>
            <p>Current date: """ + datetime.now().strftime("%Y-%m-%d") + """</p>
            <p>Best regards,<br>Your Automated Email Sender</p>
        </body>
    </html>
    """
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    
    try:
        # Send email (for Gmail)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Schedule the email to be sent every Monday at 8:00 AM
schedule.every().monday.at("08:00").do(send_email)

print("Email scheduler started. Waiting for Monday 8:00 AM...")

# Keep the program running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
