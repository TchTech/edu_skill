import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, email, password, smtp_server='smtp.gmail.com', smtp_port=587):
        self.email = email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.server = None

    def login(self):
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.email, self.password)
            print('Logged in successfully.')
        except Exception as e:
            print(f'Error: Could not login to the email server.\n{e}')

    def send_email(self, to_addr, subject, body):
        if self.server is None:
            self.login()
        from_addr = self.email
        message = MIMEMultipart()
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        try:
            self.server.sendmail(from_addr, to_addr, message.as_string())
            print(f'Sent email to {to_addr} with subject "{subject}" and message: {body}')
        except Exception as e:
            print(f'Error: Could not send email.\n{e}')


if __name__ == '__main__':
    email_sender = EmailSender ("leha.bondar.05@mail.ru", "Sstrelo4gGvip")
    email_sender.send_email ("leha.bondar.05@mail.ru", "Test message", "Test text...")