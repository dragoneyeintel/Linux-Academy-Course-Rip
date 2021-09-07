# NOOT NOOT v2.3 Downloads Courses to Folder
# THREADS DO work in parallel now :)
import asyncio
import concurrent
import math
import os
import re
import threading
import time
from dataclasses import dataclass
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from colorama import Fore, Back, Style

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

THREADS = 2
WEBDRIVER_PATH = "C:/Users/Nick3214/Desktop/Courses/courseRip/geckodriver.exe"
PROFILE_PATH = "C:/Users/Nick3214/AppData/Roaming/Mozilla/Firefox/Profiles/076ituj0.default-release"


@dataclass
class f_class:
    f: asyncio.Future


def download(links, name, driver):
    dict = [driver] * THREADS
    cnt = 0
    global running
    running = [0] * THREADS
    future = [f_class] * THREADS

    print("Files Will Download To: ", )
    print(Fore.WHITE + os.getcwd() + "\\" + name)
    print(Fore.MAGENTA + str(THREADS) + " Threads - " + str(math.ceil(len(links) / THREADS)) + " Links Per Thread\n")
    print("Spawned Driver 1")
    for n in range(THREADS - 1):
        dict[n + 1] = spawndriver()
        print("Spawned Driver " + str(n + 2))
    print("\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        for lnk in links:
            cnt += 1
            future, running, thread = seek_ready(future)
            future[thread] = f_class(executor.submit(runthread, cnt, lnk, name, dict[thread], thread))
    close_drivers(dict)


def seek_ready(future):
    while 1 == 1:
        for thread in range(THREADS):
            if running[thread] == 0:
                running[thread] = 1
                return future, running, thread
            else:
                time.sleep(.5)
                thread += 1


def runthread(simplecnt, lnk, name, driver, thread):
    print("Spawned Instance " + str(simplecnt))
    driver.get('https://learn.acloud.guru/' + lnk)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div[2]/div/main/div/div/div/div[2]/div[1]/video"))
        )
    except:
        return 0
    finally:
        time.sleep(1)
        response = BeautifulSoup(driver.page_source, 'html.parser')
        URL_REGEX = re.compile("(https://content.acloud.guru/[^\"]*)")
        link = re.findall(URL_REGEX, str(response))
        link = link[0].replace(';', '&')
        print(str(link) + "\n")

        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(name + "/" + (str(simplecnt) + ".mp4"), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        running[thread] = 0


def spawndriver():
    profile = webdriver.FirefoxProfile(PROFILE_PATH)
    profile.set_preference("network.http.pipelining", True)
    profile.set_preference("network.http.proxy.pipelining", True)
    profile.set_preference("network.http.pipelining.maxrequests", 8)
    profile.set_preference("content.notify.interval", 500000)
    profile.set_preference("content.notify.ontimer", True)
    profile.set_preference("content.switch.threshold", 250000)
    profile.set_preference("browser.cache.memory.capacity", 65536)  # Increase the cache capacity.
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("reader.parse-on-load.enabled", False)  # Disable reader, we won't need that.
    profile.set_preference("browser.pocket.enabled", False)  # Duck pocket too!
    profile.set_preference("loop.enabled", False)
    profile.set_preference("browser.chrome.toolbar_style", 1)  # Text on Toolbar instead of icons
    profile.set_preference("browser.display.show_image_placeholders",
                           False)  # Don't show thumbnails on not loaded images.
    profile.set_preference("browser.display.use_document_colors", False)  # Don't show document colors.
    profile.set_preference("browser.display.use_document_fonts", 0)  # Don't load document fonts.
    profile.set_preference("browser.display.use_system_colors", True)  # Use system colors.
    profile.set_preference("browser.formfill.enable", False)  # Autofill on forms disabled.
    profile.set_preference("browser.helperApps.deleteTempFileOnExit", True)  # Delete temporary files.
    profile.set_preference("browser.shell.checkDefaultBrowser", False)
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("browser.startup.page", 0)  # blank
    profile.set_preference("browser.tabs.forceHide", True)  # Disable tabs, We won't need that.
    profile.set_preference("browser.urlbar.autoFill", False)  # Disable autofill on URL bar.
    profile.set_preference("browser.urlbar.autocomplete.enabled", False)  # Disable autocomplete on URL bar.
    profile.set_preference("browser.urlbar.showPopup", False)  # Disable list of URLs when typing on URL bar.
    profile.set_preference("browser.urlbar.showSearch", False)  # Disable search bar.
    profile.set_preference("extensions.checkCompatibility", False)  # Addon update disabled
    profile.set_preference("extensions.checkUpdateSecurity", False)
    profile.set_preference("extensions.update.autoUpdateEnabled", False)
    profile.set_preference("extensions.update.enabled", False)
    profile.set_preference("general.startup.browser", False)
    profile.set_preference("plugin.default_plugin_disabled", False)
    profile.set_preference("permissions.default.image", 2)  # Image load disabled again
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True
    return webdriver.Firefox(options=options, executable_path=WEBDRIVER_PATH, firefox_profile=profile)


def close_drivers(drivers):
    for n in range(THREADS):
        drivers[n].close()
        drivers[n].quit()
        print("Killed Driver " + str(n + 1))


def killgecko():
    os.system("START /wait taskkill /im geckodriver.exe /f")
    print(Fore.GREEN + "Killed Rogue Drivers :)")


def killfox():
    os.system("START /wait taskkill /im firefox.exe /f")
    print("Killed Firefox :)\n")


class LinuxAcademy:
    def __init__(self):
        # Eg. b74c026d-0a03-4d34-a641-e544cba4fd41
        name = input("Insert Course Name: ")

        self.driver = spawndriver()
        print(Fore.MAGENTA + "\nSpawned Driver!")
        self.driver.get('https://learn.acloud.guru/course/' + name + '/dashboard')
        try:
            os.mkdir(name)
        except:
            print("Folder Already Exists :p")

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[1]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/a[1]/div/div[1]/span"))
            )
        finally:
            time.sleep(5)
            response = BeautifulSoup(self.driver.page_source, 'html.parser')
            # print(response.prettify())
            URL_REGEX = re.compile("/(course/[^\"]*)")
            links = re.findall(URL_REGEX, str(response))

            # Remove Dup
            remdup = OrderedDict.fromkeys(links)
            finallink = []
            for lnk in remdup:
                if "watch" in lnk:
                    finallink.append(lnk)
            print("Crawled " + str(len(finallink)) + " Links!")
            download(finallink, name, self.driver)


killgecko()
killfox()
LinuxAcademy()
killgecko()
killfox()
