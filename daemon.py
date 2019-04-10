import schedule
import time
import json
from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address


def mail_report(config):
    gmail_password = config['RiverGmailPassword']

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


def job():
    with open('/run/secrets/river_settings') as f:
        config = json.load(f)

    # Fetch all raw data
    # Process all indicators
    # Make suggestion
    # Insert suggestion in db
    # Make HTML report
    # Mail report
    print("Sending report")
    mail_report(config)


def main():
    print("Unleashing the daemon of River Tam")
    schedule.every().day.at("09:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
