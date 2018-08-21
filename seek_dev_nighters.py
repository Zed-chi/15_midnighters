from datetime import datetime
import requests
import json
from pytz import timezone


def get_attempts_page(link, page):
    response = requests.get(link+"?page="+str(page))
    return json.loads(response.text)


def load_attempts(link):
    page = 1
    attempts_page = get_attempts_page(link, page)
    pages = attempts_page["number_of_pages"]
    att_list = attempts_page["records"]
    if pages > 1:
        for page in range(2, pages+1):
            att_list += get_attempts_page(link, page)["records"]
    return att_list


def is_midnight(stamp, time_zone):
    attempt_time = datetime.fromtimestamp(
        stamp,
        tz=timezone(time_zone),
    )
    if attempt_time.hour >= 0 and attempt_time.hour < 6:
        return True
    return False


def get_midnighters_names(attempts):
    midnighters = set()
    for attempt in attempts:
        if is_midnight(attempt["timestamp"], attempt['timezone']):
            midnighters.add(attempt["username"])
    return midnighters


def print_midnighters(midnighters):
    print("\n".join(midnighters))


def main():
    link = "https://devman.org/api/challenges/solution_attempts/"
    attempts = load_attempts(link)
    midnighters_names = get_midnighters_names(attempts)
    print_midnighters(midnighters_names)


if __name__ == '__main__':
    main()
