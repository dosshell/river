import schedule
import time
import argparse
from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address
from settings import config as cfg
import db


def mail_report() -> None:
    gmail_password = cfg['RiverGmailPassword']

    with SMTP("smtp.gmail.com:587") as smtp:
        print(smtp.noop())
        print(smtp.starttls())
        print(smtp.login('daemon.of.river.tam@gmail.com', gmail_password))
        msg = EmailMessage()
        msg['Subject'] = 'River Tam has daily news for you'
        msg['From'] = Address("River Tam", "River Tam",
                              "damon.of.river.tam@gmail.com")
        msg['To'] = (Address("Markus", "markus", "lindeloew.se"))
        msg.set_content("""\
            Two by two, hands of blue.
            """)
        print(smtp.send_message(msg))


def job() -> None:
    # Fetch all raw data
    db.update()

    # Process all indicators
    # Make suggestion
    # Insert suggestion in db
    # Make HTML report
    # Mail report
    print("Sending report")
    mail_report()


def main(args: argparse.Namespace) -> None:
    print("Unleashing the daemon of River Tam")

    if args.now:
        job()
    else:
        schedule.every().day.at("03:00").do(job)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is the Daemon of River Tam.')
    parser.add_argument('--now', action='store_true',
                        help='Do not wait for the right time, unleash the Daemon now!')
    args = parser.parse_args()
    main(args)
