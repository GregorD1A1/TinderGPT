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
from os import path


class TinderConnector():
    def __init__(self):
        self.driver = None
        # xpathes
        self.message_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]"
        self.match_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"
        self.new_msg_flag_xpath = "//a[1]/div[1]/div[1]/div[2]"
        self.icons_xpath = "//div[2]/div[1]/ul[1]/li[.]/a[1]/div[1]/div[1]"
        self.messages_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div['.']/div[1]/div[2]"
        self.written_girl_bio_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.unwritten_girl_bio_xpath = "//div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.written_girl_name_age_xpath = "//div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]"
        self.main_page_element_for_wait = "//nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/ul[1]/li[1]/a[1]/div[1]/div[3]"
        self.text_area_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/form[1]/textarea[1]"
        self.return_to_main_page_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/button[1]/*"

    def start_driver(self):
        print('Starting driver')
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        #options.add_argument('-profile')
        #options.add_argument('FirefoxProfile')
        script_path = path.dirname(path.abspath(__file__))
        profile = webdriver.FirefoxProfile(f'{script_path}/FirefoxProfile')
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        self.driver.maximize_window()
        print('Driver activated')

    def load_main_page(self):
        self.driver.get("https://tinder.com")
        print('Waiting for the main page to load')
        Wait(self.driver, random.uniform(85, 100)).until(
            ExpCon.presence_of_element_located((By.XPATH, self.main_page_element_for_wait)))
        time.sleep(random.uniform(1, 3))

    def close_app(self):
        print('Closing Tinder')
        self.driver.close()

    def send_message(self, message, type_of_girl=None):
        text_field = self.driver.find_element('xpath', self.text_area_xpath)
        print('Thinking about what to write...')
        time.sleep(random.uniform(1, 4))
        text_field.send_keys(message)
        print('Typing...')
        time.sleep(random.uniform(4, 10))
        text_field.send_keys(Keys.RETURN)
        print('Message sent')
        time.sleep(random.uniform(1, 4))
        # return to main page
        self.driver.find_element('xpath', self.return_to_main_page_xpath).click()

    # girl_nr is number of girl from the top of the list of message history
    def get_msgs(self, girl_nr=None):
        print('trying to get messages')
        numbered_girl_xpath = f"//div[1]/div[1]/div[2]/div[2]/div[3]/ul[1]/li[{girl_nr}]"
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(0.5, 1))
        # entering message history based on number
        if girl_nr:
            self.driver.find_element('xpath', numbered_girl_xpath).click()
        else:
            self.driver.find_element('xpath', self.new_msg_flag_xpath).click()

        print('message history entered')
        # waiting to all message load
        Wait(self.driver, 30).until(ExpCon.presence_of_element_located((By.XPATH, self.written_girl_bio_xpath)))
        time.sleep(random.uniform(1.5, 4))
        messages = self.driver.find_elements('xpath', self.messages_xpath)
        print('messages found')
        # cut off last 5 messages
        messages = messages[-5:]

        message_prompt = ''
        for message in messages:
            message_prompt += '- ' + message.text + '\n'

        return message_prompt

    # gets name_age from opened written girl
    def get_name_age(self):
        return self.driver.find_element('xpath', self.written_girl_name_age_xpath).text

    def get_bio(self, girl_nr=None):
        print('get bio function')
        name_xpath = "//h1[@class='Typs(display-1-strong) Fxs(1) Fxw(w) Pend(8px) M(0) D(i)']"
        self.driver.find_element('xpath', self.match_tab_xpath).click()
        time.sleep(random.uniform(2, 4))
        icons = self.driver.find_elements('xpath', self.icons_xpath)
        if len(icons) == 1:
            print('No girls to start a conversation with')
            return
        # number in square brackets is a number of girl to write (from 1)
        icons[1].click()
        time.sleep(3)
        Wait(self.driver, 45).until(ExpCon.presence_of_element_located((By.XPATH, name_xpath)))
        name = self.driver.find_element('xpath', name_xpath).text
        try:
            bio = self.driver.find_element('xpath', self.unwritten_girl_bio_xpath).text
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
