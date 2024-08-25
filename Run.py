try:
    import requests, time, os, re, random, string, sys, json
    from requests_toolbelt import MultipartEncoder
    from rich import print as printf
    from rich.panel import Panel
    from rich.console import Console
    from requests.exceptions import RequestException
except (ModuleNotFoundError) as e:
    __import__("sys").exit(f"Error: {str(e).capitalize()}!")

def TAMPILKAN_LOGO():
    os.system("cls" if os.name == "nt" else "clear")
    printf(
        Panel(
            """[bold red]   _____ _      ____       ____                       
  |  ___| |__  / ___|     / ___|_ __ ___  _   _ _ __  
  | |_  | '_ \| |   _____| |  _| '__/ _ \| | | | '_ \ 
  |  _| | |_) | |__|_____| |_| | | | (_) | |_| | |_) |
[bold white]  |_|   |_.__/ \____|     \____|_|  \___/ \__,_| .__/ 
                                               |_|    
            [underline green]Facebook Auto Comments Groups""",
            width=59,
            style="bold bright_white",
        )
    )  # Coded by Rozhak
    return True

SUKSES, GAGAL, LOOPING, POSTINGAN, GAMBAR = [], [], 0, [], {"STATUS": None}

if os.path.exists("Penyimpanan") == False:
    os.mkdir("Penyimpanan")

def DEFAULT_HEADERS(cookies):
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "max-age=0",
        "Cookie": "{}".format(cookies),
        "dpr": "1.5",
        "Connection": "keep-alive",
        "Host": "m.facebook.com",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+",
    }

class LOGIN:
    def __init__(self) -> None:
        pass

    def COOKIES(self):
        try:
            TAMPILKAN_LOGO()
            printf(
                Panel(
                    f"[italic white]Please fill in your Facebook cookies, make sure the account is not using\nfree mode and the account uses Indonesian!",
                    width=59,
                    style="bold bright_white",
                    title="[Login Cookies]",
                    subtitle="╭─────",
                    subtitle_align="left",
                )
            )
            self.YOUR_COOKIES = Console().input("[bold bright_white]   ╰─> ")
            self.VALIDASI(cookies=self.YOUR_COOKIES)
            printf(
                Panel(
                    f"[italic green]Congratulations, you have successfully logged in. We are saving your cookies and\nyou will be redirected to other features!",
                    width=59,
                    style="bold bright_white",
                    title="[Login Sukses]",
                )
            )
            time.sleep(3.5)
            with open("Penyimpanan/Cookie.json", "w+") as w:
                w.write(json.dumps({"Cookie": self.YOUR_COOKIES}))
            w.close()
            MENU()
        except (Exception) as e:
            printf(
                Panel(
                    f"[italic red]{str(e).capitalize()}!",
                    width=59,
                    style="bold bright_white",
                    title="[Error]",
                )
            )
            sys.exit()

    def VALIDASI(self, cookies):
        with requests.Session() as r:
            r.headers.update(DEFAULT_HEADERS(cookies))
            response = r.get("https://m.facebook.com/?hrc=1&paipv=0&eav=&_rdr")
            if 'id="mbasic_logout_button"' in str(response.text):
                return True
            else:
                printf(
                    Panel(
                        f"[italic red]Failed to log in, it's possible that your Facebook account has been hit by a\ncheckpoint, or your account is stuck in free mode!",
                        width=59,
                        style="bold bright_white",
                        title="[Login Gagal]",
                    )
                )
                time.sleep(4.5)
                self.COOKIES()


class MENU:
    def __init__(self):
        global POSTINGAN
        try:
            TAMPILKAN_LOGO()
            with open("Penyimpanan/Cookie.json", "r") as f:
                self.COOKIES = json.loads(f.read())["Cookie"]
            LOGIN().VALIDASI(cookies=self.COOKIES)
        except (Exception) as e:
            printf(
                Panel(
                    f"[italic red]{str(e).capitalize()}!",
                    width=59,
                    style="bold bright_white",
                    title="[Error]",
                )
            )
            time.sleep(5.0)
            LOGIN().COOKIES()

        printf(
            Panel(
                f"[italic white]Please fill in the link of the Facebook group you want to comment on, for example:[italic green] https://m.facebook.com/groups/...?",
                width=59,
                style="bold bright_white",
                title="[Link Group]",
                subtitle="╭─────",
                subtitle_align="left",
            )
        )
        self.INPUT_GROUP_LINK = Console().input("[bold bright_white]   ╰─> ")
        self.GROUP_LINK = (
            f"https://m.facebook.com/{self.INPUT_GROUP_LINK.split('facebook.com/')[1]}"
        )

        printf(
            Panel(
                f"[italic white]Please fill in the image file you want to use as a comment, leave it blank if\nyou don't want to comment with an image!",
                width=59,
                style="bold bright_white",
                title="[File Gambar]",
                subtitle="╭─────",
                subtitle_align="left",
            )
        )
        self.IMAGE_PATH = Console().input("[bold bright_white]   ╰─> ")
        if os.path.exists(self.IMAGE_PATH) != False:
            GAMBAR.update({"STATUS": f"{self.IMAGE_PATH}"})
        else:
            GAMBAR.update({"STATUS": None})

        printf(
            Panel(
                f"[italic white]Please fill in the comment text, you can use commas for random comments and + for\nnew lines. For example:[italic green] Mantab Bang, Keren Bang",
                width=59,
                style="bold bright_white",
                title="[Teks Komentar]",
                subtitle="╭─────",
                subtitle_align="left",
            )
        )
        self.TEKS_KOMENTAR = (
            Console().input("[bold bright_white]   ╰─> ").replace("+", "\n").split(",")
        )

        printf(
            Panel(
                f"[italic white]Please fill in the comment gap, it is better to use a delay of more than[italic red] 60 seconds[italic white] to avoid being blocked!",
                width=59,
                style="bold bright_white",
                title="[Jeda Komentar]",
                subtitle="╭─────",
                subtitle_align="left",
            )
        )
        self.DELAY = int(Console().input("[bold bright_white]   ╰─> "))

        if os.path.exists("Penyimpanan/Sudah.txt") == False:
            open("Penyimpanan/Sudah.txt", "w+").write("")
        printf(
            Panel(
                f"[italic white]You can stop collecting posts by pressing[italic green] CTRL + C[italic white], and you can stop comments by using[italic red] CTRL + Z[italic white]!",
                width=59,
                style="bold bright_white",
                title="[Catatan]",
            )
        )
        while True:
            try:
                if len(POSTINGAN) == 0:
                    EKSEKUSI().KUMPULKAN_POSTINGAN(self.COOKIES, self.GROUP_LINK)
                    continue
                else:
                    for LINK in POSTINGAN:
                        try:
                            self.PERMALINK = re.search(
                                r"permalink/(\d+)/", str(LINK)
                            ).group(1)
                        except (AttributeError):
                            self.PERMALINK = None
                        if (
                            str(self.PERMALINK)
                            not in open("Penyimpanan/Sudah.txt", "r")
                            .read()
                            .splitlines()
                        ):
                            EKSEKUSI().KOMENTARI(self.COOKIES, LINK, self.TEKS_KOMENTAR)
                            for sleep in range(self.DELAY, 0, -1):
                                time.sleep(1)
                                printf(
                                    f"[bold bright_white]   ──>[bold white] TUNGGU[bold green] {self.DELAY}[bold white]/[bold red]{sleep}[bold white]/[bold green]{len(POSTINGAN)}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}[bold white]    ",
                                    end="\r",
                                )
                            continue
                        else:
                            printf(
                                f"[bold bright_white]   ──>[bold red] SUDAH DIKOMENTARI SEBELUMNYA!     ",
                                end="\r",
                            )
                            time.sleep(2.5)
                            continue
                    printf(
                        f"[bold bright_white]   ──>[bold green] BERHASIL MENGOMENTARI SEMUA POSTINGAN!     ",
                        end="\r",
                    )
                    time.sleep(5.0)
                    POSTINGAN.clear()
                    continue
            except (RequestException):
                printf(
                    f"[bold bright_white]   ──>[bold red] KONEKSI ANDA BERMASALAH!   ",
                    end="\r",
                )
                time.sleep(4.5)
                continue

class EKSEKUSI:
    def __init__(self) -> None:
        pass

    def KUMPULKAN_POSTINGAN(self, cookies, groups_link):
        global POSTINGAN
        try:
            with requests.Session() as r:
                r.headers.update(DEFAULT_HEADERS(cookies))
                response = r.get("{}".format(groups_link))

                self.FIND_ALL_POSTINGAN = re.findall(
                    re.compile(
                        r'(https://m\.facebook\.com/groups/\d+/permalink/\d+/.*?)"'
                    ),
                    str(response.text),
                )
                self.DECODED_MATCHES = [
                    re.sub(r"&amp;", "&", match) for match in self.FIND_ALL_POSTINGAN
                ]

                for LINK in self.DECODED_MATCHES:
                    if str(LINK) in POSTINGAN and not "https://" in str(LINK):
                        continue
                    else:
                        printf(
                            f"[bold bright_white]   ──>[bold white] MENGUMPULKAN[bold green] {len(POSTINGAN)}[bold white] POSTINGAN!         ",
                            end="\r",
                        )
                        time.sleep(0.07)
                        POSTINGAN.append(f"{LINK}")

                if "bacr=" in str(response.text):
                    printf(
                        f"[bold bright_white]   ──>[bold yellow] BERHASIL MENEMUKAN NEXT CURSOR!          ",
                        end="\r",
                    )
                    self.BACR = (
                        re.search(r'href="(/groups/\d+\?bacr=.*?)"', str(response.text))
                        .group(1)
                        .replace("amp;", "")
                    )
                    self.NEXT_GROUP_LINK = f"https://m.facebook.com/{self.BACR}"
                    time.sleep(2.5)
                    self.KUMPULKAN_POSTINGAN(cookies, groups_link=self.NEXT_GROUP_LINK)
                else:
                    if len(POSTINGAN) != 0:
                        printf(
                            f"[bold bright_white]   ──>[bold green] BERHASIL MENEMUKAN SEMUA POSTINGAN!   ",
                            end="\r",
                        )
                        time.sleep(3.5)
                        return True
                    else:
                        printf(
                            f"[bold bright_white]   ──>[bold red] TIDAK ADA POSTINGAN YANG DITEMUKAN!   ",
                            end="\r",
                        )
                        time.sleep(3.5)
                        return False
        except (KeyboardInterrupt):
            printf(f"[bold bright_white]                      ", end="\r")
            time.sleep(2.5)
            return True
        except (RequestException):
            printf(
                f"[bold bright_white]   ──>[bold red] KONEKSI ANDA BERMASALAH!   ",
                end="\r",
            )
            time.sleep(5.0)
            self.KUMPULKAN_POSTINGAN(cookies, groups_link)

    def KOMENTARI(self, cookies, link_postingan, teks_komentar):
        global SUKSES, GAGAL, LOOPING
        with requests.Session() as r:
            r.headers.update(DEFAULT_HEADERS(cookies))
            response = r.get(link_postingan)

            self.COMMENT_ADVANCED = (
                re.search(
                    r'href="(/mbasic/comment/advanced/[^"]+)"', str(response.text)
                )
                .group(1)
                .replace("amp;", "")
            )
            r.headers.update(
                {
                    "Referer": "https://m.facebook.com/",
                }
            )
            response2 = r.get("https://m.facebook.com{}".format(self.COMMENT_ADVANCED))

            self._MUPLOAD_ = (
                re.search(
                    r'action="(https://upload.facebook.com/_mupload_/ufi/mbasic/advanced/[^"]+)"',
                    str(response2.text),
                )
                .group(1)
                .replace("amp;", "")
            )
            self.FB_DTSG = re.search(
                r'name="fb_dtsg" value="([^"]+)"', str(response2.text)
            ).group(1)
            self.JAZOEST = re.search(
                r'name="jazoest" value="([^"]+)"', str(response2.text)
            ).group(1)

            BOUNDARY = "----WebKitFormBoundary" + "".join(
                random.sample(string.ascii_letters + string.digits, 16)
            )

            self.KOMENTAR = f"{random.choice(teks_komentar)}"
            if GAMBAR["STATUS"] != None:
                data = MultipartEncoder(
                    fields={
                        "fb_dtsg": "{}".format(self.FB_DTSG),
                        "jazoest": "{}".format(self.JAZOEST),
                        "photo": (
                            f"{str(int(time.time()))}.jpg",
                            open(GAMBAR["STATUS"], "rb"),
                            "image/jpeg",
                        ),
                        "comment_text": f"{self.KOMENTAR}",
                        "post": "Komentari",
                    },
                    boundary=BOUNDARY,
                )
            else:
                data = MultipartEncoder(
                    fields={
                        "fb_dtsg": "{}".format(self.FB_DTSG),
                        "jazoest": "{}".format(self.JAZOEST),
                        "comment_text": f"{self.KOMENTAR}",
                        "post": "Komentari",
                    },
                    boundary=BOUNDARY,
                )

            r.headers.update(
                {
                    "Content-Type": "multipart/form-data; boundary={}".format(BOUNDARY),
                    "Origin": "https://m.facebook.com",
                    "Connection": "keep-alive",
                    "Host": "upload.facebook.com",
                }
            )
            response3 = r.post("{}".format(self._MUPLOAD_), data=data)
            LOOPING += 1
            if "url=https://m.facebook.com/groups/" in str(response3.text):
                try:
                    self.PERMALINK = re.search(
                        r"permalink/(\d+)/", str(link_postingan)
                    ).group(1)
                    open("Penyimpanan/Sudah.txt", "a+").write(f"{self.PERMALINK}\n")
                except (Exception):
                    pass
                SUKSES.append(f"{link_postingan}")
                printf(
                    Panel(
                        f"""[bold white]Status :[bold green] Commented successfully!
[bold white]Link :[bold red] {str(link_postingan)[:200]}
[bold white]Komentar :[bold green] {self.KOMENTAR}""",
                        width=59,
                        style="bold bright_white",
                        title="[Sukses]",
                    )
                )
                time.sleep(2.0)
                return True
            else:
                GAGAL.append(f"{link_postingan}")
                printf(
                    Panel(
                        f"""[bold white]Status :[bold red] Failed to comment!
[bold white]Link :[bold yellow] {str(link_postingan)[:200]}
[bold white]Komentar :[bold red] {self.KOMENTAR}""",
                        width=59,
                        style="bold bright_white",
                        title="[Gagal]",
                    )
                )
                time.sleep(2.0)
                return False

if __name__ == "__main__":
    try:
        os.system("git pull")
        MENU()
    except (Exception) as e:
        printf(
            Panel(
                f"[italic red]{str(e).capitalize()}!",
                width=59,
                style="bold bright_white",
                title="[Error]",
            )
        )
        sys.exit()