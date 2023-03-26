import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Написано ChatGPT
class EmailSender:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def send_email(self, to_email: str, theme: str, text: str, attachment=None):
        """Отправляет сообщение на указанную почту."""
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = theme

        msg.attach(MIMEText(text, 'plain'))

        if attachment:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                part = MIMEApplication(file_data)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment}"')
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        text = msg.as_string()
        server.sendmail(self.email, to_email, text)
        server.quit()