import concurrent
import math
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

THREADS = 6
WEBDRIVER_PATH = "C:/Users/Nick3214/Desktop/CourseRip/geckodriver.exe"
PROFILE_PATH = "C:/Users/Nick3214/AppData/Roaming/Mozilla/Firefox/Profiles/076ituj0.default-release"


class CourseRip:
    #If crashed after spawning drivers delete driver data at C:\Users\<User>\AppData\Local\Temp
    def __init__(self, links, name, driver, login, user, passwd):
        dict = [driver] * THREADS
        cnt = 0
        global is_running
        is_running = [0] * THREADS

        print("Files Will Download To: ", Fore.WHITE + os.getcwd() + "\\" + name)
        print(Fore.MAGENTA + str(THREADS) + " Threads - " + str(math.ceil(len(links) / THREADS)) + " Links Per Thread\n")
        print("Spawned Driver 1")
        if login == 'y' or login == 'Y':
            for n in range(THREADS - 1):
                dict[n + 1] = CourseRip.spawndriver_login(user, passwd)
                time.sleep(10)
                print("Spawned Driver " + str(n + 2))
        else:
            for n in range(THREADS - 1):
                dict[n + 1] = CourseRip.spawndriver_nologin()
                print("Spawned Driver " + str(n + 2))
        print("\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
            for lnk in links:
                cnt += 1
                thread = self.seek_ready()
                executor.submit(self.runthread, cnt, lnk, name, dict[thread], thread)
        CourseRip.close_drivers(dict)
        CourseRip.compress(name)
        CourseRip.killgecko()
        CourseRip.killfox()

    def seek_ready(self):
        while 1:
            for thread in range(THREADS):
                if is_running[thread] == 0:
                    is_running[thread] = 1
                    return thread
                else:
                    time.sleep(.5)

    def runthread(self, simplecnt, lnk, name, driver, thread):
        print("Spawned Instance " + str(simplecnt))
        driver.get('https://learn.acloud.guru/' + lnk)
        time.sleep(2)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/main/div/div/div/div[2]/div[1]/video")))
        except:
            return 0
        finally:
            time.sleep(2)
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
            is_running[thread] = 0
            return 0

    @staticmethod
    def spawndriver_login(user, passwd):
        options = Options()
        options.headless = True
        cap = webdriver.DesiredCapabilities.FIREFOX
        cap['marionette'] = True

        profile = webdriver.FirefoxProfile()
        preferences = (("general.useragent.override", 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'), ("dom.webdriver.enabled", False), ('useAutomationExtension', False))
        map(lambda x: profile.set_preference(x), preferences)

        driver = webdriver.Firefox(capabilities=cap, firefox_profile=profile, options=options)
        driver.execute_script("return navigator.userAgent")
        driver.get('https://learn.acloud.guru/login?')
        time.sleep(4)

        email = driver.find_element_by_xpath('//*[@id="1-email"]')
        email.send_keys(user)
        password = driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div/div/div/div/div[2]/div[2]/span/div/div/div/div/div/div/div/div/div[2]/div[3]/div[2]/div/div/input')
        password.send_keys(passwd)
        driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div/div/div/button/span').click()
        return driver

    @staticmethod
    def spawndriver_nologin():
        profile = webdriver.FirefoxProfile(PROFILE_PATH)
        options = Options()
        options.headless = True
        preferences = (("network.http.pipelining", True), ("network.http.proxy.pipelining", True), ("network.http.pipelining.maxrequests", 8), ("content.notify.interval", 500000),
                       ("content.notify.ontimer", True), ("content.switch.threshold", 250000), ("browser.cache.memory.capacity", 65536), ("browser.startup.homepage", "about:blank"),
                       ("reader.parse-on-load.enabled", False), ("browser.pocket.enabled", False), ("loop.enabled", False), ("browser.chrome.toolbar_style", 1),
                       ("browser.display.show_image_placeholders", False), ("browser.display.use_document_colors", False), ("browser.display.use_document_fonts", 0),
                       ("browser.display.use_system_colors", True), ("browser.formfill.enable", False), ("browser.helperApps.deleteTempFileOnExit", True), ("browser.shell.checkDefaultBrowser", False),
                       ("browser.startup.homepage", "about:blank"), ("browser.startup.page", 0), ("browser.tabs.forceHide", True), ("browser.urlbar.autoFill", False),
                       ("browser.urlbar.autocomplete.enabled", False), ("browser.urlbar.showPopup", False), ("browser.urlbar.showSearch", False), ("extensions.checkCompatibility", False),
                       ("extensions.checkUpdateSecurity", False), ("extensions.update.autoUpdateEnabled", False), ("extensions.update.enabled", False), ("general.startup.browser", False),
                       ("plugin.default_plugin_disabled", False), ("permissions.default.image", 2))
        arguments = ("start-maximized", "disable-infobars", "--disable-extensions", "--no-sandbox", "--disable-application-cache", "--disable-gpu", "--disable-dev-shm-usage")
        map(lambda x: profile.set_preference(x), preferences)
        map(lambda y: options.add_argument(y), arguments)
        return webdriver.Firefox(options=options, executable_path=WEBDRIVER_PATH, firefox_profile=profile)

    @staticmethod
    def close_drivers(drivers):
        for n in range(THREADS):
            drivers[n].close()
            drivers[n].quit()
            print("Killed Driver " + str(n + 1))

    @staticmethod
    def killgecko():
        os.system("START /wait taskkill /im geckodriver.exe /f")
        print(Fore.GREEN + "Killed Rogue Drivers :)")

    @staticmethod
    def killfox():
        os.system("START /wait taskkill /im firefox.exe /f")
        print("Killed Firefox :)\n")