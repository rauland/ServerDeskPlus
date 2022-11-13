import smtplib, os, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(mail_subject, mail_body, mail_to, tech):
    # if config.debug_flag:
        # mail_to = config.mail_to # Test Email

    html = f"""\
    <html>
    <head></head>
    <body>
        <p>Hi {tech.split()[0]},<br>
        {config.message}.</p>
        {mail_body}
        <p>beep boop</p>
    </body>
    </html>
    """

    mimemsg = MIMEMultipart()
    mimemsg['From']=config.mail_from
    mimemsg['To']=mail_to
    # mimemsg['CC']= fields['mail_to']  # Test Email
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(html, 'html'))
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(config.username,os.environ.get('smtp_pwd'))
    connection.send_message(mimemsg)
    connection.quit()