import schedule
import time


def job():
    print("Doing stuff")


def main():
    print("Unleashing the daemon of River Tam")
    schedule.every().day.at("9:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
