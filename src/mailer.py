from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address
from typing import List
import logger


class Attachment:
    bin = None
    type = None
    ext = None
    cid = None


def send_html(html_code: str, text_msg: str, subject: str, attachments: List[Attachment], from_user: str, from_password: str, to_email: str) -> bool:
    gmail_address = from_user
    gmail_password = from_password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Address("River Tam", "River Tam", gmail_address)
    msg['To'] = (Address(to_email, to_email))

    if text_msg is not None:
        msg.set_content(text_msg)
    else:
        msg.set_content('This email contains a html message. Please use a email viewer that support html content')

    msg.add_alternative(html_code, subtype='html')

    if attachments is not None:
        for n in range(0, len(attachments)):
            a = attachments[n]
            msg.get_payload()[n + 1].add_related(a.bin, a.type, a.ext, cid='<' + a.cid + '>')

    with SMTP("smtp.gmail.com:587") as smtp:
        logger.log(smtp.noop())
        logger.log(smtp.starttls())
        logger.log(smtp.login(gmail_address, gmail_password))
        logger.log(smtp.send_message(msg))
        logger.log(smtp.quit())
        return True
    logger.error("SMTP error")
    return False


def send_text(message: str, subject: str, from_user: str, from_password: str, to_email: str) -> str:
    gmail_address = from_user
    gmail_password = from_password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Address("River Tam", "River Tam", gmail_address)
    msg['To'] = (Address(to_email, to_email))

    msg.set_content(message)

    with SMTP("smtp.gmail.com:587") as smtp:
        logger.log(smtp.noop())
        logger.log(smtp.starttls())
        logger.log(smtp.login(gmail_address, gmail_password))
        logger.log(smtp.send_message(msg))
        logger.log(smtp.quit())
        return True
    logger.error("SMTP error")
    return False
