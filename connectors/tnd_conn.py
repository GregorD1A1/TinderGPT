from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random


class TinderConnector():
    def __init__(self, driver):
        self.driver = driver
        # xpathes
        self.message_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/button[1]"
        self.match_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]"
        self.new_msg_flag_xpath = "//a[1]/div[1]/div[1]/div[2]"
        self.icons_xpath = "//div[1]/div[1]/div[3]/div[1]/ul[1]/li['.']/a[1]/div[1]/div[1]"
        self.messages_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div['.']/div[1]/div[2]"
        self.written_girl_bio_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.unwritten_girl_bio_xpath = "//div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.written_girl_name_age_xpath = "//div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]"
        self.main_page_element_for_wait = "//div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.text_area_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/form[1]/textarea[1]"
        self.return_to_main_page_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/button[1]/*"

    def load_main_page(self):
        self.driver.get("https://tinder.com")
        print('Waiting for the main page to load')
        Wait(self.driver, random.uniform(85, 100)).until(
            ExpCon.presence_of_element_located((By.XPATH, self.main_page_element_for_wait)))
        time.sleep(random.uniform(1, 3))

    def close_app(self):
        print('Closing Tinder')
        self.driver.get("about:blank")

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
        numbered_girl_xpath = f"//div[1]/div[1]/div[3]/div[2]/div[3]/ul[1]/li[{girl_nr}]"
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
        print('poczekałem 3s')
        Wait(self.driver, 45).until(ExpCon.presence_of_element_located((By.XPATH, name_xpath)))
        name = self.driver.find_element('xpath', name_xpath).text
        try:
            bio = self.driver.find_element('xpath', self.unwritten_girl_bio_xpath).text
        except NoSuchElementException:
            bio = ''
        return name, bio
