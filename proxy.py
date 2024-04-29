from mitmproxy import http
from urllib.parse import urlparse
import requests
import threading
import logger
import yaml
import re
import socket
import time
import os

# import logging
# logging.basicConfig(level=logging.CRITICAL)

fonts = ["font/" + i.replace(".woff2", "") for i in os.listdir("./asset") if i.endswith(".woff2")]

with open("./rule.yml", "r") as confile:
    config = yaml.safe_load(confile)
    if "redirect" in config:
        original_redirects = config["redirect"]
        new_redirects = {}
        for source, destinations in original_redirects.items():
            for destination in destinations:
                new_redirects[destination] = source
        config["redirect"] = new_redirects

def request(flow: http.HTTPFlow) -> None:
    current_url = flow.request.pretty_url
    for pattern in config["blacklist"]:
        if re.search(pattern, current_url):
            return None

    for pattern, redirect in config["redirect"].items():
        if re.search(pattern, current_url):
            uri = urlparse(redirect)
            flow.request.host = uri.netloc.split(":")[0]
            if ":" in uri.netloc or uri.port is not None:
                flow.request.port = int(uri.port) if uri.port is not None else int(uri.netloc.split(":")[-1])
            flow.request.scheme = uri.scheme
            flow.request.headers["Host"] = uri.netloc
            if "/".join(current_url.split("/")[-2:]) not in fonts and current_url.split("/")[-1] != "icon":
                open("./data/" + socket.gethostbyname(socket.gethostname()) + ".log", "a", encoding="utf8").write(f"{time.time()*1000};{urlparse(current_url).netloc};{current_url}\n")

if __name__ == '__main__':
    threading.Thread(target=logger.start).start()
    os.system('mitmdump --quiet -s ' + __file__) # --certs=C:/Users/Game_K/.mitmproxy/mitmproxy-ca-cert.pem
