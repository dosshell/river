import schedule
import time
import argparse
import settings
import avanza
import totp
import logger
import traceback
import json
import mailer
import plotter
import os


class Result(object):
    pass


def dump(data: dict, file: str) -> None:
    with open(file, 'w') as f:
        json.dump(data, f)


def pretty_int(number: int) -> str:
    return '{:,}'.format(number).replace(',', ' ')


def generate_report_email(res: Result) -> str:
    report = {}
    report['attachments'] = []
    report['msg'] = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <p>
            Own capital: {pretty_int(res.own_capital)}<br/>
            In the mattress: {pretty_int(res.value_in_the_mattress)}<br/>
            On the table: {pretty_int(res.value_on_the_table)}<br/>
            Current investment: {pretty_int(res.current_investment)}<br/>
            Profit: {pretty_int(res.profit)}<br/>
        </p>
        <img alt="hej" src="cid:1" />
        <p>
            Two by two. Hands of blue.<br />
            // River Daemon
        </p>
    </body>
    </html>
    """

    a = mailer.Attachment
    a.bin = plotter.example_plot(res.chart_data['date'], res.chart_data['value'])
    a.type = 'image'
    a.ext = 'png'
    a.cid = '1'
    report['attachments'].append(a)

    return report


def job_wrapper(cfg: settings.Settings) -> None:
    '''Mostly a logger and error handle wrapper for the job function'''

    logger.flush()
    logger.log("Job started")

    try:
        was_successful = job(cfg)
    except Exception:
        logger.error(traceback.format_exc())
        was_successful = False

    logger.log("Job stopped")
    if was_successful:
        logger.log("Job was probably successful")
    else:
        logger.error("Job returned atleast one error")

    if logger.has_error and cfg.email:
        logs = logger.flush()
        log = '\n'.join(logs)
        mailer.send_text(log, "Bad news everyone!", cfg.gmail_username, cfg.gmail_password,
                         cfg.email_to)
    logger.flush()


def job(cfg: settings.Settings) -> bool:
    # Fetch all raw data
    avanza_client = avanza.Avanza(cfg.cache_file)
    if cfg.fetch:
        avanza_client.fetch_all(cfg.blacklist)
    totp_code = totp.totp(cfg.avanza_private_key)
    if not avanza_client.login(cfg.avanza_username, cfg.avanza_password, totp_code):
        logger.error("Could not sign in")
        return False
    logger.log("Login succeeded")

    res = Result()
    res.own_capital = avanza_client.get_own_capital()
    res.current_investment = avanza_client.get_current_investment()
    res.value_in_the_mattress = avanza_client.get_value_in_the_mattress()
    res.value_on_the_table = res.own_capital - res.value_in_the_mattress
    res.profit = res.own_capital - res.current_investment - res.value_in_the_mattress

    res.chart_data = avanza_client.get_account_chart()

    # Process all indicators
    pass

    # Make suggestion
    pass

    # Insert suggestion in db
    pass

    # Make report
    logger.log("Making report")
    report = generate_report_email(res)

    # Print report
    if cfg.email:
        logger.log("Sending report")
        send_ok = mailer.send_html(report['msg'], None, "River Report", report['attachments'],
                                   cfg.gmail_username, cfg.gmail_password, cfg.email_to)
        if not send_ok:
            return False
    else:
        logger.log('Printing report')
        print('------------')
        print(report['msg'])
        print('------------')
    return True


def main(cfg: settings.Settings) -> None:
    logger.log("Unleashing the daemon of River Tam")

    if cfg.clear_cache:
        if cfg.cache_file is None or cfg.cache_file == ':memory:':
            logger.error("No cache-file to clear")
        else:
            if os.path.exists(cfg.cache_file):
                os.remove(cfg.cache_file)

    if not cfg.daemon:
        job_wrapper(cfg)
    else:
        schedule.every().day.at("03:00").do(job_wrapper, cfg)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="River Tam. You’ve got tools, something sharp. Don’t be scared. I’m right here.")
    parser.add_argument('--auth-file', default=None, help="File with authentication credentials")
    parser.add_argument('--blacklist', nargs='*', default=None, help="List of orderbook ids to block")
    parser.add_argument('--cache-file', help="Path to cache file")
    parser.add_argument('--clear-cache', action='store_true', default=None, help="Clear old market data")
    parser.add_argument('--clear-cache-off', action='store_false', dest='clear_cache',
                        help='Turn off clear-cache config')
    parser.add_argument('--config-file', '-c', default=None, help="Path to config file")
    parser.add_argument('--daemon', '-d', action='store_true', default=None, help="Unleash the Daemon")
    parser.add_argument('--daemon-off', action='store_false', dest='daemon', help='Turn off daemon config')
    parser.add_argument('--email', action='store_true', default=None, help="Send report with email")
    parser.add_argument('--email-off', action='store_false', help='Turn off email config')
    parser.add_argument('--email-to', nargs=1, default=None, help="Email address to send email to")
    parser.add_argument('--fetch', action='store_true', default=None, help="Update market data")
    parser.add_argument('--fetch-off', action='store_false', dest='fetch', help="Turn off fetch config")

    args = parser.parse_args()
    cfg = settings.Settings()
    cfg.read_args(args)
    logger.log("config: " + str(cfg))
    main(cfg)
