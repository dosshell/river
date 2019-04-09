import schedule
import time
from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address


def mail_report():
    with SMTP("smtp.gmail.com:587") as smtp:
        print(smtp.noop())
        print(smtp.starttls())
        print(smtp.login('daemon.of.river.tam@gmail.com', r"""M#qZhyYctO0M%eoo5uN1*O*cQXvFMG1wf6LgxuGzLNliXaj6oGMYoGflUAa%O4^bQN!pp02iHJWAGTLw^6HU4OO8Oack5vs&osW"""))
        msg = EmailMessage()
        msg['Subject'] = 'River Tam has daily news for you'
        msg['From'] = Address("River Tam", "River Tam", "damon.of.river.tam@gmail.com")
        msg['To'] = (Address("Markus", "markus", "lindeloew.se"))
        msg.set_content("""\
            Two by two, hands of blue.
            """)
        print(smtp.send_message(msg))


def job():
    # Fetch all raw data
    # Process all indicators
    # Make suggestion
    # Insert suggestion in db
    # Make HTML report
    # Mail report
    print("Sending report")
    mail_report()


def main():
    print("Unleashing the daemon of River Tam")
    schedule.every().day.at("9:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
