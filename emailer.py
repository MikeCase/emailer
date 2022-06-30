from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from emailtemplate import TemplateFactory



class Emailer:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.server = None

    def __enter__(self):
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.starttls()
        self.server.login(user=self.username, password=self.password)
        return self

    def send_email(self, recipients: List[str], message: MIMEMultipart) -> None:
        """ Send an email to {recipient} with {message}
        recipients: List[str]
        message: str

        """
        if self.server:
            try:
                print(f'Sending email: {message=}')
                # self.server.sendmail(self.username, recipients, message.as_string())
            except Exception as e:
                print(f"Email not sent. {e}")
                return

            print(f"E-mail {message['Subject']=} Sent to {', '.join(recipients)}")

    def build_message(self, subject: str, recipients: List[str], message: str, msg_type: str="plain") -> MIMEMultipart:
        mime_message = MIMEMultipart()
        mime_message['Subject'] = subject
        mime_message['From'] = self.username
        mime_message['To'] = ",".join(recipients)

        msg = MIMEText(message, msg_type)
        mime_message.attach(msg)

        return mime_message

    # I don't like this method. It seems out of place.
    def gen_html_file(self, template_type, template_file, data=None, extra_data=None):
        template = TemplateFactory.build_email(template_type, template_file, output_file='email_output.html')
        template.output_html(data=data, extra_data=extra_data)
        return template.template

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.server.close()