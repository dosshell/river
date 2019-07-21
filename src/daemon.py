import schedule
import time
import argparse
from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address
import settings
# import db


def mail_report(cfg: dict) -> None:
    gmail_password = cfg['RiverGmailPassword']
    gmail_address = cfg['RiverGmailUsername']
    recipient_name = cfg['UserEmail'].split('@')[0]
    recipient_domain = cfg['UserEmail'].split('@')[1]

    with SMTP("smtp.gmail.com:587") as smtp:
        print(smtp.noop())
        print(smtp.starttls())
        print(smtp.login(gmail_address, gmail_password))
        msg = EmailMessage()
        msg['Subject'] = 'River Tam has daily news for you'
        msg['From'] = Address("River Tam", "River Tam", gmail_address)
        msg['To'] = (Address(recipient_name, recipient_name, recipient_domain))
        msg.set_content("""\
            Two by two, hands of blue.
            """)
        print(smtp.send_message(msg))


def job(cfg: dict) -> None:
    # Fetch all raw data
    # db.update()

    # Process all indicators
    # Make suggestion
    # Insert suggestion in db
    # Make HTML report
    # Mail report
    print("Sending report")
    mail_report(cfg)


def main(args: argparse.Namespace) -> None:
    print("Unleashing the daemon of River Tam")
    cfg = settings.read_settings(args.config)
    if args.now:
        job(cfg)
    else:
        schedule.every().day.at("03:00").do(job, cfg)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is the Daemon of River Tam.')
    parser.add_argument('--now', action='store_true',
                        help='Do not wait for the right time, unleash the Daemon now!')
    parser.add_argument('-c', '--config', default='settings.json', help='Path to config file')

    args = parser.parse_args()
    print(args)
    main(args)
