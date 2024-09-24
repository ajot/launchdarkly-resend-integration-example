import sqlite3
import resend
from launchdarkly_setup import evaluate_flag
import os
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Set the Resend API key
resend.api_key = os.getenv('RESEND_API_KEY')

# Get the email sender address from environment variables
email_from = os.getenv('RESEND_EMAIL_FROM')

def fetch_users_from_db():
    """Connect to the SQLite database and fetch user data."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Fetch all users from the database
    cursor.execute('SELECT email, subscription_status, last_login_date, purchase_count FROM users')
    users = cursor.fetchall()

    # Close the database connection
    conn.close()
    return users

def get_email_content(show_premium_content_flag):
    """Determine the email content based on the feature flag evaluation."""

    if show_premium_content_flag:
        subject = "✨ Exclusive Offer Just for You, Premium Member! ✨"
        body = '''
        <h1>Hey, Premium Member! 🌟</h1>
        <p>As a valued premium member, we're thrilled to bring you an exclusive offer. Enjoy <strong>20% off</strong> on your next purchase!</p>
        <p>Use the code <strong>PREMIUM20</strong> at checkout to claim your discount. 🎁</p>
        <p>Thank you for being a part of our premium family. We appreciate you! 💖</p>
        '''
    else:
        subject = "👀 Peek Inside – We’ve Got Something New! 👀"
        body = '''
        <h1>Hello, Wonderful You! 🌟</h1>
        <p>Check out the latest updates. 🧐</p>
        '''
    return subject, body

def send_personalized_email(email_to, show_premium_content_flag):
    """Send a personalized email based on the user's subscription status and feature flag."""
    
    # Get the subject and body based on the flag evaluation
    subject, body = get_email_content(show_premium_content_flag)

    # Send the email using the Resend SDK
    try:
        response = resend.Emails.send({
            "from": email_from,
            "to": email_to,
            "subject": subject,
            "html": body
        })
        print(f"Email sent to {email_to} with subject: {subject}. Response: {response}")
    except Exception as e:
        print(f"Failed to send email to {email_to}. Error: {e}")

def process_and_send_emails():
    """Fetch user data, evaluate feature flags, and send the appropriate type of email."""
    users = fetch_users_from_db()

    for user in users:
        email_to, subscription_status, last_login_date, purchase_count = user
        print(f"Database: User '{email_to}' has a '{subscription_status}' subscription.")

        # Evaluate the feature flag using the user's subscription status and purchase count
        feature_flag_key = 'premium-content'
        flag_detail = evaluate_flag(
            os.getenv("LAUNCHDARKLY_API_KEY"), 
            feature_flag_key, 
            email_to, 
            subscription_status, 
            purchase_count
        )

        show_premium_content_flag = flag_detail.value

        # Send personalized email
        send_personalized_email(email_to, show_premium_content_flag)

# Run the process to determine email type and send emails
if __name__ == "__main__":
    process_and_send_emails()
