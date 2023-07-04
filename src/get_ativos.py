import requests
from util import write_file, file_exists, read_json, delete_file
import json
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

tickers_file = os.getenv("TICKERS_FILE")
api_key = os.getenv("POLYGON_API_KEY")

base_url = "https://api.polygon.io"
tickers_endpoint = "/v3/reference/tickers"
daily_open_close_endpoint = (
    lambda ticker, year, month, day: f"/v1/open-close/{ticker}/{year}-{month}-{day}"
)


def get_tickers(cursor: str = None, market: str = None):
    url = base_url + tickers_endpoint
    f_name = tickers_file
    print("requesting " + url)
    res_json = None
    last_res_json = None

    make_req = True
    if file_exists(f_name):
        last_res_json = read_json(f_name)
        if cursor == last_res_json["last_cursor"]:
            print("skipping request, cursor is the same")
            make_req = False
            res_json = last_res_json

    if make_req:
        print(f"make req to {url}")

        params = {"apiKey": api_key, "active": "true"}
        if market is not None:
            params["market"] = market
        if cursor is not None:
            params["cursor"] = cursor
        res = requests.get(base_url + tickers_endpoint, params=params)
        print(f"res.status_code = {res.status_code}")
        res_json = res.json()
        if res_json["status"] == "ERROR":
            print(f"request failed! {res_json['error'][:100]}")
            return None, None

    res_json["last_cursor"] = cursor
    print("============ RES JSON ==============")
    print(res_json)

    if (
        file_exists(f_name)
        and last_res_json is not None
        and cursor != last_res_json["last_cursor"]
    ):
        rs = set([r["ticker"] for r in res_json["results"]])
        for ticker in last_res_json["results"]:
            if ticker["ticker"] not in rs:
                res_json["results"].append(ticker)
                res_json["count"] += 1

    write_file(tickers_file, json.dumps(res_json, indent=4), clear=True)

    cursor = None
    if res_json.get("next_url") is not None:
        cursor = res_json["next_url"].split("cursor=")[1]

    return res_json, cursor


def get_daily_open_close(tickers: list[str], year, month, day):
    all_res = []
    for ticker in tickers:
        url = base_url + daily_open_close_endpoint(ticker, year, month, day)
        f_name = (
            daily_open_close_endpoint(ticker, year, month, day)
            .replace("/", "-")
            .replace("-v1-", "")
        )
        f_name = f"sample_reqs/{f_name}.json"
        print("requesting " + url)
        if file_exists(f_name):
            print("skipping request, file already exists")
            continue
        res = requests.get(url, params={"adjusted": "true", "apiKey": api_key})
        res_json = res.json()

        if res_json["status"] != "OK":
            print(
                f"request failed! skipping. err: {res_json.get('status')} msg: {res_json.get('error')}"
            )
            continue

        write_file(
            f_name,
            json.dumps(res_json, indent=4),
        )
        all_res.append(res_json)

    return all_res


def clear_sample_reqs():
    files = str(subprocess.check_output("ls sample_reqs", shell=True), encoding="utf-8")
    for file in files.split("\n"):
        if "open-close" in file:
            read = read_json("sample_reqs/" + file)
            if read["status"] != "OK":
                print(f"deleting... {file}")
                delete_file("sample_reqs/" + file)


from time import sleep


def main():
    cursor = None
    if file_exists(tickers_file):
        read = read_json(tickers_file)
        if read.get("next_url"):
            cursor = read["next_url"].split("cursor=")[1]
    while True:
        analyse()
        sleep(0.4)
        print("cursor = ", cursor)
        ticker_req, new_cursor = get_tickers(cursor, market="crypto")
        print("new_cursor = ", new_cursor)
        cursor = new_cursor
        if ticker_req is None:
            continue

        # tickers = [ticker["ticker"] for ticker in ticker_req["results"]]
        # res = get_daily_open_close(tickers, "2023", "07", "03")
        # print(f"got results for {len(res)} tickers")


def analyse():
    f = read_json(tickers_file)
    ls = {}
    for ticker in f["results"]:
        if ticker["currency_symbol"] not in ls:
            ls[ticker["currency_symbol"]] = 0
        ls[ticker["currency_symbol"]] += 1
    print("currencies:", ls)


analyse()
# main()
