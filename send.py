import smtplib, os, config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

conf = config.get()
conf = conf['email']

def email(mail_subject, mail_body, mail_to, tech) :
    username = conf['username']
    password = os.environ.get('smtp_pwd')
    mail_from = conf['mail_from']
    mail_to = conf['mail_to'] # Test Email
    # mail_subject = "Test Subject"
    # mail_body = "This is a test message"

    html = f"""\
    <html>
    <head></head>
    <body>
        <p>Hi {tech.split()[0]},<br>
        Please assign all categories to the following tickets before the end of the month.</p>
        {mail_body}
        <p>beep boop</p>
    </body>
    </html>
    """

    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=mail_to
    # mimemsg['CC']= fields['mail_to']  # Test Email
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(html, 'html'))
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()