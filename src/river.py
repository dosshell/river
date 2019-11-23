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
    a.bin = plotter.example_plot(res.chart_data['dates'], res.chart_data['value'])
    a.type = 'image'
    a.ext = 'png'
    a.cid = '1'
    report['attachments'].append(a)

    return report


def job_wrapper(cfg: dict) -> None:
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

    if logger.has_error and cfg['mail']:
        logs = logger.flush()
        log = '\n'.join(logs)
        mailer.send_text(log, "Bad news everyone!", cfg['RiverGmailUsername'], cfg['RiverGmailPassword'],
                         cfg['UserEmail'])
    logger.flush()


def job(cfg: dict) -> bool:
    # Fetch all raw data
    avanza_client = avanza.Avanza('cache.db')
    totp_code = totp.totp(cfg['AvanzaPrivateKey'])
    if not avanza_client.login(cfg['AvanzaUsername'], cfg['AvanzaPassword'], totp_code):
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

    # Update db
    pass

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
    if cfg['mail']:
        logger.log("Sending report")
        send_ok = mailer.send_html(report['msg'], None, "River Report", report['attachments'],
                                   cfg['RiverGmailUsername'], cfg['RiverGmailPassword'], cfg['UserEmail'])
        if not send_ok:
            return False
    else:
        logger.log('Printing report')
        print('------------')
        print(report['msg'])
        print('------------')
    return True


def main(args: argparse.Namespace) -> None:
    logger.log("Unleashing the daemon of River Tam")
    cfg = settings.read_settings(args.config)
    cfg['mail'] = args.mail

    if not args.daemon:
        job_wrapper(cfg)
    else:
        schedule.every().day.at("03:00").do(job_wrapper, cfg)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="River Tam. You’ve got tools, something sharp. Don’t be scared. I’m right here.")
    parser.add_argument('-d', '--daemon', action='store_true', help="Unleash the Daemon")
    parser.add_argument('-c', '--config', default='settings.json', help="Path to config file")
    parser.add_argument('--test', default=False, action='store_true', help="Use test data")
    parser.add_argument('--mail', action='store_true', help="Send report with email")

    args = parser.parse_args()
    logger.log("called with " + str(args))
    main(args)
