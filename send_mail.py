from flask_mail import Mail, Message

def configure_mail(app):
    mail = Mail(app)
    return mail

def send_bug_report_email(mail, sender_email, recipients, file_path):
    msg = Message('Bug Report', sender=sender_email, recipients=recipients)
    msg.body = "Please find the bug report attached."
    with open(file_path, 'rb') as fp:
        msg.attach('bug_report.xlsx',
                   'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', fp.read())
    mail.send(msg)
