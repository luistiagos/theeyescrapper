import smtplib

from email.mime.text import MIMEText

msg = MIMEText('Testing some Mailgun awesomness')
msg['Subject'] = "Hello"
msg['From']    = "zutrix@gmail.com"
msg['To']      = "luistiago.andrighetto@gmail.com"

s = smtplib.SMTP('smtp.mailgun.org', 587)

s.login('postmaster@sandboxf63db4bd694b419fbdeaeeb68ef662c9.mailgun.org', '720aae5a23a7029cba3d803170ebbb53-a5d1a068-1a487204')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()