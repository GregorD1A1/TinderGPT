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


class BadooConnector():
    def __init__(self):
        self.driver = None
        # xpathes
        self.message_tab_xpath = "//aside[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/nav[1]/a[3]"
        self.match_tab_xpath = "//aside[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/nav[1]/a[4]"
        self.new_msg_flag_xpath = "//section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]"
        self.first_icon_xpath = "//main[1]/div[1]/section[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]"
        self.icons_xpath = "//main[1]/div[1]/section[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div['.']/div['.']"
        self.messages_xpath = "//div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div['.']/div[1]/div[1]/div[1]"
        self.unwritten_girl_bio_xpath = "/html[1]/body[1]/div[3]/div[2]/main[1]/div[1]/div[1]/div[2]/div[3]/section[1]"
        self.written_girl_name_age_xpath = "//div[1]/div[1]/div[2]/div[1]/header[1]/div[1]/div[1]/div[1]/div[1]/div[1]"
        self.unwritten_girl_name_xpath = "//div[2]/main[1]/div[1]/div[1]/div[1]/header[1]/div[2]/div[1]/h1[1]/span[1]"
        self.main_page_element_for_wait = "//div[2]/main[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]"
        self.unwritten_text_area_xpath = "//div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/input[1]"
        self.written_text_area_xpath = "//div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]"
        self.return_to_main_page_xpath = "//div[3]/aside[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/img[1]"

    def open_dating_app(self):
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')
        #options.add_argument('-profile')
        #options.add_argument('FirefoxProfile')
        script_path = path.dirname(path.abspath(__file__))
        profile = webdriver.FirefoxProfile(f'{script_path}/FirefoxProfile')
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        self.driver.maximize_window()

    def load_main_page(self):
        self.driver.get("https://badoo.com")
        print('Waiting for the main page to load')
        Wait(self.driver, random.uniform(85, 100)).until(
            ExpCon.presence_of_element_located((By.XPATH, self.main_page_element_for_wait)))
        time.sleep(random.uniform(1, 3))

    def close_app(self):
        print('Closing Badoo')
        self.driver.close()

    def send_message(self, message, type_of_girl='unwritten'):
        if type_of_girl == 'unwritten':
            text_field = self.driver.find_element('xpath', self.unwritten_text_area_xpath)
        elif type_of_girl == 'written':
            text_field = self.driver.find_element('xpath', self.written_text_area_xpath)

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
        numbered_girl_xpath = f"//div[1]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[{girl_nr}]"
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(1, 2))
        # entering message history based on number
        if girl_nr:
            self.driver.find_element('xpath', numbered_girl_xpath).click()
        else:
            try:
                self.driver.find_element('xpath', self.new_msg_flag_xpath).click()
            except:
                pass

        print('message history entered')
        # waiting to all message load
        Wait(self.driver, 30).until(ExpCon.presence_of_element_located((By.XPATH, self.written_text_area_xpath)))
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

    def get_bio(self, girl_nr):
        print('get bio function')
        self.driver.find_element('xpath', self.match_tab_xpath).click()
        time.sleep(random.uniform(2, 4))
        Wait(self.driver, 45).until(ExpCon.presence_of_element_located((By.XPATH, self.first_icon_xpath)))
        girl_icons = self.driver.find_elements('xpath', self.icons_xpath)
        girl_icons[girl_nr - 1].click()
        time.sleep(3)
        Wait(self.driver, 45).until(ExpCon.presence_of_element_located((By.XPATH, self.unwritten_girl_bio_xpath)))
        name = self.driver.find_element('xpath', self.unwritten_girl_name_xpath).text
        try:
            bio = self.driver.find_element('xpath', self.unwritten_girl_bio_xpath).text
        except NoSuchElementException:
            bio = ''
        return name, bio


if __name__ == '__main__':
    bdo_connector = DatingAppConnector()
    bdo_connector.open_badoo()
    print(bdo_connector.get_first_match_bio())