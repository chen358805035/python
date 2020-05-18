from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import asyncio
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),addr))

def send_email(user_name, content, name):
    from_addr = 'c18683346287@163.com'
    password = 'YPNYKMZURQNXXWOZ'
   

    to_addr = '358805035@qq.com'

    smtp_server = 'smtp.163.com'
    #with open('F:/python/webapp/awesome-python3-webapp/www/templates/blog.html', 'r', encoding='utf-8') as f:
        
        #msg = MIMEText(f.read(), 'html', 'utf-8')
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = _format_addr('%s <%s>' % (user_name, from_addr))
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('%s' % name, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()