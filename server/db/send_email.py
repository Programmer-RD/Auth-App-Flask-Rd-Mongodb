import smtplib
import smtpd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(to_email, subject, body):
    try:
        for x in to_email:
            msg = MIMEMultipart()
            msg["From"] = "go2ranuga@gmail.com"
            msg["To"] = x
            msg["subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com")
                server.ehlo()
                server.login("go2ranuga@gmail.com", "ranuga d 2008")
                server.sendmail("go2ranuga@gmail.com", x, msg.as_string())
                server.close()
                return True
            except:
                server = smtplib.SMTP_SSL("smtp.gmail.com")
                server.ehlo()
                server.login("go2ranuga@gmail.com", "RANUGA D 2008")
                server.sendmail("go2ranuga@gmail.com", x, msg.as_string())
                server.close()
                return True
            else:
                return False
    except:
        msg = MIMEMultipart()
        msg["From"] = "go2ranuga@gmail.com"
        msg["To"] = to_email
        msg["subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com")
            server.ehlo()
            server.login("go2ranuga@gmail.com", "ranuga d 2008")
            server.sendmail("go2ranuga@gmail.com", to_email, msg.as_string())
            server.close()
            return True
        except:
            server = smtplib.SMTP_SSL("smtp.gmail.com")
            server.ehlo()
            server.login("go2ranuga@gmail.com", "RANUGA D 2008")
            server.sendmail("go2ranuga@gmail.com", to_email, msg.as_string())
            server.close()
            return True
        else:
            return False
