import requests
from bs4 import BeautifulSoup
import json
import re

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def parse_disconnections(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("div", id="fetched-data-container").find("table")
    rows = table.find_all("tr")


    data = {}
    current_date = None

    for row in rows:
        cells = row.find_all("td")



        if len(cells) > 0:
            first = cells[0].get_text(strip=True)
            if re.match(r"\d{2}\.\d{2}\.\d{4}", first):
                current_date = first
                data[current_date] = {}
                for idx, cell in enumerate(cells[1:], start=1):
                    times_raw = [p.get_text(strip=True) for p in cell.find_all("p")]
                    times = times_raw if times_raw else ([cell.get_text(strip=True)] if cell.get_text(strip=True) else [])

                    data[current_date][str(idx)] = times

    return data


def save_to_storage(parsed):
    with open("storage.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    cfg = load_config()
    url = cfg["cities"]["rivnenska"]

    parsed = parse_disconnections(url)
    save_to_storage(parsed)
