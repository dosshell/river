import schedule
import time
import argparse
from smtplib import SMTP
from email.message import EmailMessage
from email.headerregistry import Address
import settings
import avanza
import totp

# import db


class Result(object):
    pass


def log(msg: str) -> None:
    print(msg)


def generate_report(res: Result) -> str:
    report = f"""
    Two by two, hands of blue.
    {res.own_capital}
    """
    return report


def mail_report(report: str, from_user: str, from_password: str, to_email: str) -> None:
    gmail_address = from_user
    gmail_password = from_password
    recipient_name = to_email.split('@')[0]
    recipient_domain = to_email.split('@')[1]

    with SMTP("smtp.gmail.com:587") as smtp:
        print(smtp.noop())
        print(smtp.starttls())
        print(smtp.login(gmail_address, gmail_password))
        msg = EmailMessage()
        msg['Subject'] = 'River Tam has daily news for you'
        msg['From'] = Address("River Tam", "River Tam", gmail_address)
        msg['To'] = (Address(recipient_name, recipient_name, recipient_domain))
        msg.set_content(report)
        print(smtp.send_message(msg))


def job(cfg: dict) -> None:
    # Fetch all raw data
    avanza_client = avanza.Avanza()
    totp_code = totp.totp(cfg['AvanzaPrivateKey'])
    if not avanza_client.login(cfg['AvanzaUsername'], cfg['AvanzaPassword'], totp_code):
        log("Could not sign in")
        exit(1)

    res = Result()
    res.own_capital = avanza_client.get_own_capital()

    # Update db
    pass

    # Process all indicators
    pass

    # Make suggestion
    pass

    # Insert suggestion in db
    pass

    # Make report
    log("Making report")
    report = generate_report(res)

    # Mail report
    log("Sending report")
    mail_report(report, cfg['RiverGmailUsername'], cfg['RiverGmailPassword'], cfg['UserEmail'])


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
        description="This is the Daemon of River Tam.")
    parser.add_argument('--now', action='store_true',
                        help="Do not wait for the right time, unleash the Daemon now!")
    parser.add_argument('-c', '--config', default='settings.json', help="Path to config file")
    parser.add_argument('-update-db', default=False, help="Update database")

    args = parser.parse_args()
    print(args)
    main(args)
