from datetime import datetime
from pytz import timezone
import requests


def fetch_decoded_json(link, params):
    try:
        return requests.get(link, params=params).json()
    except JSONDecodeError:
        return []


def get_attempts_lists(link):
    page = 1
    while True:
        decoded_json = fetch_decoded_json(link, {"page": page})
        yield decoded_json["records"]
        page += 1
        if decoded_json["page"] == decoded_json["number_of_pages"]:
            break


def is_midnighter(timestamp, time_zone):
    attempt_time = datetime.fromtimestamp(
        timestamp,
        tz=timezone(time_zone),
    )
    return 0 <= attempt_time.hour < 6


def print_midnighters(midnighters):
    print("=== Midnighters ===")
    print("\n".join(midnighters))


def main():
    link = "https://devman.org/api/challenges/solution_attempts/"
    attempts_lists = get_attempts_lists(link)
    midnighters = set()
    for attempts_list in attempts_lists:
        midnighters.update(
            [
                attempt["username"]
                for attempt in attempts_list
                if is_midnighter(attempt["timestamp"], attempt["timezone"])
            ]
        )
    print_midnighters(midnighters)


if __name__ == "__main__":
    main()
