import email.message
import mimetypes
import os.path
import smtplib

def generate_email(sender, recipient, subject, body, attachment_path=''):
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if len(attachment_path) != 0:
        attachment_name = os.path.basename(attachment_path)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type, mime_subtype = mime_type.split('/',1)

        with open(attachment_path,'rb') as fh:
            message.add_attachment(fh.read(),
                                    maintype=mime_type,
                                    subtype=mime_subtype,
                                    filename=attachment_name)

    return message

def send_email(message,server_name='localhost'):
    mail_server = smtplib.SMTP(server_name)
    mail_server.send_message(message)
    mail_server.quit()
 