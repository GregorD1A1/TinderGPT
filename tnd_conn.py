from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, \
    NoSuchElementException, ElementNotInteractableException
import time
from datetime import datetime, timedelta
import random
import re


class DatingAppConnector():
    def __init__(self):
        self.driver = None
        # xpathes
        self.message_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]"
        self.name_age_match_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/h1[1]"
        self.new_msg_flag_xpath = "//a[1]/div[1]/div[1]/div[2]"

    def open_tinder(self):
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')
        options.add_argument('-profile')
        options.add_argument('FirefoxProfile')
        self.driver = webdriver.Firefox(options=options)
        girl_card_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/ul[1]/li[1]/a[1]/div[1]/div[3]"
        self.load_main_page(girl_card_xpath)
        self.driver.maximize_window()
        print('Waiting for a while')
        time.sleep(random.uniform(1, 4))

    def load_main_page(self, girl_card_xpath):
        self.driver.get("https://tinder.com")
        print('Waiting for the main page to load')
        Wait(self.driver, random.uniform(85, 100)).until(
            ExpCon.presence_of_element_located((By.XPATH, girl_card_xpath)))

    def close_tinder(self):
        print('Closing Tinder')
        self.driver.close()

    def send_messages(self, messages):
        text_area_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/form[1]/textarea[1]"
        text_field = self.driver.find_element('xpath', text_area_xpath)
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        for message in messages:
            print('Thinking about what to write...')
            time.sleep(random.uniform(5, 10))
            text_field.send_keys(message)
            print('Typing...')
            time.sleep(random.uniform(6, 16))
            text_field.send_keys(Keys.RETURN)
            print('Sent the message')
            time.sleep(random.uniform(0.5, 1))
            time.sleep(random.uniform(2, 4))

    def match_tab_xpath(self):
        try:
            self.driver.find_element('xpath', '//div[contains(text(), "PIERWSZY MIESIĄC")]')
        except NoSuchElementException:
            return "//div[1]/aside[1]/nav[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"
        else:
            return "//div[1]/aside[1]/nav[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]"

    def icons_xpath(self):
        try:
            self.driver.find_element('xpath', '//div[contains(text(), "PIERWSZY MIESIĄC")]')
        except NoSuchElementException:
            return "//div[2]/div[1]/ul[1]/li[.]/a[1]/div[1]/div[1]"
        else:
            return "add the correct div here"

    def get_msgs(self):
        print('trying to get messages')
        messages_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div['.']/div[1]/div[2]"
        new_message_flags = self.driver.find_elements('xpath',
                                                 "//a['.']//div[1]//div[1]//div[2]")
        time.sleep(random.uniform(3, 5))
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(0.5, 1))
        # cleck on new message
        try:
            self.driver.find_element('xpath', self.new_msg_flag_xpath).click()
        except NoSuchElementException:
            pass

        first_girl_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/ul[1]/li[2]"
        self.driver.find_element('xpath', first_girl_xpath).click()
        # waiting to all message load
        time.sleep(3)
        messages = self.driver.find_elements('xpath', messages_xpath)

        message_prompt = ''
        for message in messages:
            message_prompt += '- ' + message.text + '\n'

        return message_prompt

    def get_first_match_bio(self):
        print('get bio function')
        name_xpath = "//h1[@class='Typs(display-1-strong) Fxs(1) Fxw(w) Pend(8px) M(0) D(i)']"
        #bio_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]"
        bio_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        time.sleep(random.uniform(1, 2))
        icons = self.driver.find_elements('xpath', self.icons_xpath())
        if len(icons) == 1:
            print('No girls to start a conversation with')
            return
        # number in square brackets is a number of girl to write (from 1)
        icons[1].click()
        time.sleep(3)
        Wait(self.driver, 30).until(ExpCon.presence_of_element_located((By.XPATH,
                                                                    name_xpath)))
        name = self.driver.find_element('xpath', name_xpath).text
        try:
            bio = self.driver.find_element('xpath', bio_xpath).text
        except NoSuchElementException:
            bio = ''
        return name, bio







def liking_tnd(ilosc_klikniec):
    # kliknięcie w pary (niepisane)
    like_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]"
    dislike_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]"
    wiek_xpath = "//div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/span[2]"
    iks_polubionej_dziewczyny_xpath = "//*[@class='Sq(24px) P(4px)']"
    wyjscie_z_wymuszacza_superlajka_xpath = "//span[contains(text(),'Nie, dziękuję')]"
    zdjęcie_3_xpath = "//div[3]/div[1]/div[1]/span[3]"
    liking(ilosc_klikniec, like_xpath, dislike_xpath, wiek_xpath,
        iks_polubionej_dziewczyny_xpath, wyjscie_z_wymuszacza_superlajka_xpath,
        zdjęcie_3_xpath)


def liking(ilosc_klikniec, like_xpath, dislike_xpath, wiek_xpath,
        iks_polubionej_dziewczyny_xpath, wyjscie_z_wymuszacza_superlajka_xpath,
        zdjęcie_3_xpath):
    for _ in range(ilosc_klikniec):
        Wait(driver, 90).until(ExpCon.presence_of_element_located((By.XPATH,
            wiek_xpath)))
        # udawanie człowieka
        time.sleep(random.uniform(0.5, 4))
        wiek = int(driver.find_element('xpath', wiek_xpath).text)
        # sprawdzanie, czy dziewczyna ma co najmniej 4 zdjęcia (zmniejszenie
        # ryzyka donosu poprzez klikanie bardziej rozbudowanych dziewczyn)
        try:
            driver.find_element('xpath', zdjęcie_3_xpath)
        except NoSuchElementException:
            # znielubić
            driver.find_element('xpath', dislike_xpath).click()
            print('znielubiłem')
            continue
        if wiek >= 20:
            # polubić
            driver.find_element('xpath', like_xpath).click()
            print('polubiłem')
        else:
            # znielubić
            driver.find_element('xpath', dislike_xpath).click()
            print('znielubiłem')
            continue
        # wyjście z pop-upu pary
        try:
            Wait(driver, 5).until(ExpCon.presence_of_element_located((By.XPATH,
                iks_polubionej_dziewczyny_xpath)))
            # udawanie człowieka
            time.sleep(random.uniform(1.5, 3))
            driver.find_element('xpath', iks_polubionej_dziewczyny_xpath).click()
        except TimeoutException:
            pass
        # wyjście z pop-upu wymuszacza superlajka
        try:
            Wait(driver, 1).until(ExpCon.presence_of_element_located((
                By.XPATH, wyjscie_z_wymuszacza_superlajka_xpath)))
            # udawanie człowieka
            time.sleep(random.uniform(1.5, 3))
            driver.find_element('xpath',
                wyjscie_z_wymuszacza_superlajka_xpath).click()
        except TimeoutException:
            pass
