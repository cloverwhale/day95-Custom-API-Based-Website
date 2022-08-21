import os
import requests

URL = "https://api.fugle.tw/realtime/v0.3/intraday/"
TOKEN = os.getenv('TOKEN')
ENDPOINT_META = URL + "meta"
ENDPOINT_QUOTE = URL + "quote"
ENDPOINT_VOLUMES = URL + "volumes"


def search_request(endpoint, symbol_id):
    params = {
        "symbolId": f"{symbol_id}",
        "apiToken": TOKEN
    }
    response = requests.get(endpoint, params=params)
    status = response.status_code
    data = response.json()
    return status, data


def add_color(input_data, threshold):
    for item in input_data:
        if item["price"] > threshold:
            item["color"] = "r"
        elif item["price"] < threshold:
            item["color"] = "g"
        else:
            item["color"] = "b"
    return input_data


class Search:
    def __init__(self, symbol):
        self.symbol = symbol
        self.meta = search_request(ENDPOINT_META, self.symbol)
        self.quote = search_request(ENDPOINT_QUOTE, self.symbol)
        self.volumes = search_request(ENDPOINT_VOLUMES, self.symbol)
        self.display_data = self.get_display_data()

    def get_display_data(self):
        display_data = dict()
        if self.meta[0] == 200:
            try:
                display_data["is_suspended"] = self.meta[1]["data"]["meta"]["isSuspended"]
                display_data["is_terminated"] = self.meta[1]["data"]["meta"]["isTerminated"]
                display_data["symbol_id"] = self.meta[1]["data"]["info"]["symbolId"]
                display_data["name"] = self.meta[1]["data"]["meta"]["nameZhTw"]
                display_data["industry"] = self.meta[1]["data"]["meta"]["industryZhTw"]
                display_data["is_closed"] = self.quote[1]["data"]["quote"]["isClosed"]
                display_data["pre_closed"] = self.meta[1]["data"]["meta"]["previousClose"]
                display_data["order_at"] = self.quote[1]["data"]["quote"]["order"]["at"][:19].replace("T", " ")
                display_data["order"] = self.quote[1]["data"]["quote"]["order"]
                display_data["volumes_at"] = self.volumes[1]["data"]["info"]["lastUpdatedAt"][:19].replace("T", " ")
                display_data["volumes"] = self.volumes[1]["data"]["volumes"]

                display_data["order"]["bids"] = add_color(display_data["order"]["bids"], display_data["pre_closed"])
                display_data["order"]["asks"] = add_color(display_data["order"]["asks"], display_data["pre_closed"])
                display_data["volumes"] = add_color(display_data["volumes"], display_data["pre_closed"])
            except KeyError:
                display_data["error"] = "Cannot get specified symbol data."
        return display_data
