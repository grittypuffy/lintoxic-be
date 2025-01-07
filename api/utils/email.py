import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api.config.environment import EnvVarConfig, get_env_config

env: EnvVarConfig = get_env_config()


def send_email(user_id: str, violations: str):
    # Email credentials and SMTP server details
    smtp_server = env.smtp_server
    smtp_port = 587  # For TLS
    sender_email = env.sender_email
    receiver_email = env.receiver_email
    sender_password = env.sender_pw

    # Compose the email
    subject = 'Violation of community guidelines'
    body = f'This is to inform that user with user ID: {
        user_id} has violated the community guidelines for {violations} times.'

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection with TLS

        # Login to your email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the server connection
        server.quit()
