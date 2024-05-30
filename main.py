import random
import string
import requests
import os
import platform
import concurrent.futures


xCookie = ""


class DiscordGiftChecker:
    def __init__(self):
        self.base_url = "https://discord.com/api/v10/entitlements/gift-codes/"
        self.headers = {
            "authority": "discord.com",
            "method": "GET",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": xCookie,
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
        self.username = os.getlogin()

    def generate_code(self):
        return "".join(random.choices(string.digits + string.ascii_letters, k=16))

    def check_code(self, C):
        url = f"{self.base_url}{C}?with_application=false&with_subscription_plan=true"
        r = requests.get(url, headers=self.headers, timeout=10)
        if r.status_code in range(200, 204):
            print(f"\033[1;32m    ╰──> [VALID]\033[0m discord.gift/{C}")
            return C, True
        else:
            print(f"\033[1;31m    ╰──> [INVALID]\033[0m discord.gift/{C}")
            return C, False


class TerminalTitleSetter:
    @staticmethod
    def set_title(title):
        if platform.system() == "Windows":
            import ctypes

            ctypes.windll.kernel32.SetConsoleTitleW(title)
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
        if os.path.exists(fn):
            with open(fn, "r") as f:
                for line in f:
                    codes.append(line.strip())
        return codes


if __name__ == "__main__":
    xdir = "data"
    if not os.path.exists(xdir):
        os.makedirs(xdir)

    vF = os.path.join(xdir, "valid.txt")
    invalid_file = os.path.join(xdir, "invalid.txt")
    codes_file = os.path.join(xdir, "codes.txt")

    checker = DiscordGiftChecker()
    TerminalTitleSetter.set_title("@0xnyxo Nitro | Checked: ???")
    print(f"\033[1;34m{' '*28}╰──> Logged in as: {checker.username}\033[0m\n")
    print(f"\033[1;36m{' '*30}_  _  _  _  _  _  _____ \033[0m")
    print(f"\033[1;36m{' '*30}( \\( )( \\/ )( \\/ )(  _  )\033[0m")
    print(f"\033[1;36m{' '*30})  (  \\  /  )  (  )(_)( \033[0m")
    print(f"\033[1;36m{' '*30}(_\\_) (__) (_/\\_)(_____)\033[0m\n\n")

    CA = int(input("    ╰──> Check > "))
    print("")
    TerminalTitleSetter.set_title(f"@0xnyxo Nitro | Checked: ???")

    checked_count = 0
    checked_codes = FileHandler.read(codes_file)
    vC = []
    iC = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_code = {executor.submit(checker.check_code, checker.generate_code()): checker.generate_code() for _ in range(CA)}
        for future in concurrent.futures.as_completed(future_to_code):
            C, result = future.result()
            if C in checked_codes:
                print(f"\033[1;33m    ╰──> [SKIPPED] {C} (C already checked)\033[0m")
                continue

            checked_codes.append(C)
            FileHandler.save(C, codes_file)

            checked_count += 1
            TerminalTitleSetter.set_title(f"@0xnyxo Nitro | Checked: {checked_count}")

            if result:
                vC.append(C)
                FileHandler.save(C, vF)
            else:
                iC.append(C)
                FileHandler.save(C, invalid_file)

    print("\n\033[1;32m    ╰──> Valid Codes:\033[0m")
    if vC:
        for C in vC:
            print(C)
    else:
        print("    ╰──> [None]")
