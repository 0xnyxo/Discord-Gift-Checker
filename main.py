import random                 as rdm
import string                 as str
import requests               as rq
import os                     as x
import platform               as ptfm
import concurrent.futures     as cf
import threading              as td
import time                   as t
from datetime import datetime as dt

class DiscordGiftChecker:
    def __init__(s, cookie):
        s.base_url = "https://discord.com/api/v10/entitlements/gift-codes/"
        s.headers = {
            "authority": "discord.com",
            "method": "GET",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": cookie,
            "Pragma": "no-cache",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        s.username = x.getlogin()

    def generate_code(s):
        return "".join(rdm.choices(str.digits + str.ascii_letters, k=16))

    def check_code(s, C):
        url = f"{s.base_url}{C}?with_application=false&with_subscription_plan=true"
        r = rq.get(url, headers=s.headers, timeout=10)
        if r.status_code in range(200, 204):
            print(f"\033[1;32m    [{dt.now().strftime('%H:%M')}] ╰──> [VALID]\033[0m discord.gift/{C}")
            return C, True
        else:
            print(f"\033[1;31m    [{dt.now().strftime('%H:%M')}] ╰──> [INVALID]\033[0m discord.gift/{C}")
            return C, False

class TerminalTitleSetter:
    @staticmethod
    def set_title(checked_count=None, elapsed_time=None):
        title = "By: @0xnyxo"
        if checked_count is not None:
            title += f" | Checked: {checked_count}"
        if elapsed_time:
            title += f" | Elapsed: {elapsed_time}"
        if ptfm.system() == "Windows":
            import ctypes as ct
            ct.windll.kernel32.SetConsoleTitleW(title)
        else:
            print(f"\033]0;{title}\007", end="", flush=True)

class FileHandler:
    @staticmethod
    def save(data, fn):
        with open(fn, "a") as f:
            f.write(data + "\n")

    @staticmethod
    def read(fn):
        codes = []
        if x.path.exists(fn):
            with open(fn, "r") as f:
                for line in f:
                    codes.append(line.strip())
        return codes

class CodeGenerator:
    @staticmethod
    def generate_amount(n):
        return ["".join(rdm.choices(str.digits + str.ascii_letters, k=16)) for _ in range(n)]

class GiftCheckerApp:
    def __init__(s, cookie):
        s.checker = DiscordGiftChecker(cookie)
        s.xdir = "data"
        s.vF = x.path.join(s.xdir, "valid.txt")
        s.invalid_file = x.path.join(s.xdir, "invalid.txt")
        s.codes_file = x.path.join(s.xdir, "codes.txt")
        s.checked_count = [0]
        s.checked_count_event = td.Event()
        s.start_time = t.time()

    def setup(s):
        if not x.path.exists(s.xdir):
            x.makedirs(s.xdir)
        TerminalTitleSetter.set_title(checked_count=0, elapsed_time="0:00")
        print(f"\033[1;34m{' '*7}╰──> Logged in as: {s.checker.username}\033[0m\n")
        print(f"\033[1;36m{' '*8}┌┐┌┬ ┬─┐ ┬┌─┐\033[0m")
        print(f"\033[1;36m{' '*8}│││└┬┘┌┴┬┘│ │\033[0m")
        print(f"\033[1;36m{' '*8}┘└┘ ┴ ┴ └─└─┘\033[0m\n")

    def update_counter(s):
        while True:
            elapsed_time = int(t.time() - s.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            elapsed_time_str = f"{minutes}:{seconds:02d}"
            TerminalTitleSetter.set_title(checked_count=s.checked_count[0], elapsed_time=elapsed_time_str)
            t.sleep(1)

    def check_codes(s, CA):
        td.Thread(target=s.update_counter, daemon=True).start()

        checked_codes = FileHandler.read(s.codes_file)
        vC = []
        iC = []

        with cf.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_code = {executor.submit(s.checker.check_code, s.checker.generate_code()): s.checker.generate_code() for _ in range(CA)}
            for future in cf.as_completed(future_to_code):
                C, result = future.result()

                if C in checked_codes:
                    print(f"\033[1;33m    [{dt.now().strftime('%H:%M')}] ╰──> [SKIPPED] {C} (Code already checked)\033[0m")
                    continue

                s.checked_count[0] += 1
                s.checked_count_event.set()

                FileHandler.save(C, s.codes_file)

                if result:
                    vC.append(C)
                    FileHandler.save(C, s.vF)
                else:
                    iC.append(C)
                    FileHandler.save(C, s.invalid_file)

        s.display_valid_codes(vC)

    @staticmethod
    def display_valid_codes(vC):
        print("\n\033[1;32m  ╰──> Valid Codes:\033[0m")
        if vC:
            for C in vC:
                print(C)
        else:
            print("  ╰──> [None]")

if __name__ == "__main__":
    cookie = ""  # Add your cookie here
    CA = 10000  # Number of codes to generate

    app = GiftCheckerApp(cookie)
    app.setup()
    app.check_codes(CA)
