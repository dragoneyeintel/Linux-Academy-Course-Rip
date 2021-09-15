# NOOT NOOT v2.5 Fixed Login :p + Cleaned Up a little + Auto-compress all vids larger than 100MB
import os
import sys
import re
import time
from colorama import Fore
from collections import OrderedDict
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.getcwd() + "/res/")
from Res import CourseRip
from Compress import Compress


class LinuxAcademy:
    def __init__(self):
        CourseRip.killgecko()
        CourseRip.killfox()

        # E.g. b74c026d-0a03-4d34-a641-e544cba4fd41
        name = input("Insert Course Name: ")
        login = input("Would you like to login (y / n): ")
        if login == 'y' or login == 'Y':
            user = input("Email: ")
            passwd = input("Password: ")
            self.driver = CourseRip.spawndriver_login(user, passwd)
        else:
            user = 'NULL'
            passwd = 'Null'
            print("Duplicating Firefox Profile")
            self.driver = CourseRip.spawndriver_nologin()
            print(Fore.MAGENTA + "\nSpawned Driver!")

        self.driver.get('https://learn.acloud.guru/course/' + name + '/dashboard')
        try:
            os.mkdir(name)
        except:
            print("Folder Already Exists :p")

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[1]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/a[1]/div/div[1]/span")))
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
            CourseRip(finallink, name, self.driver, login, user, passwd)
            Compress(name)


LinuxAcademy()
