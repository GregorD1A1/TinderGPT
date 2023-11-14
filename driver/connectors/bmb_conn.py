from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random


class BumbleConnector():
    def __init__(self, driver):
        self.driver = driver
        # xpathes
        self.new_msg_flags_xpath = "//div[1]/section[2]/div[1]/div[1]/div[1]/div['.']/div[2]/div[1]/div[2]/div[1]"
        #self.first_icon_xpath = "//main[1]/div[1]/section[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]"
        #self.icons_xpath = "//main[1]/div[1]/section[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div['.']/div['.']"
        self.messages_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[1]/div[1]"
        #self.unwritten_girl_bio_xpath = "/html[1]/body[1]/div[3]/div[2]/main[1]/div[1]/div[1]/div[2]/div[3]/section[1]"
        self.written_girl_name_age_xpath = "//div[1]/div[1]/div[1]/aside[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]"
        #self.unwritten_girl_name_xpath = "//div[2]/main[1]/div[1]/div[1]/div[1]/header[1]/div[2]/div[1]/h1[1]/span[1]"
        self.main_page_element_for_wait = "//div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/span[1]"
        self.text_area_xpath = "//body[1]/div[1]/div[1]/div[1]/main[1]/div[3]/div[1]/div[1]/div[1]/div[1]/textarea[1]"
        #self.return_to_main_page_xpath = "//div[3]/aside[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/img[1]"

    def load_main_page(self):
        self.driver.get("https://bumble.com/app")
        print('Waiting for the main page to load')
        Wait(self.driver, random.uniform(85, 100)).until(
            ExpCon.presence_of_element_located((By.XPATH, self.main_page_element_for_wait)))
        time.sleep(random.uniform(1, 3))

    def close_app(self):
        print('Closing Bumble')
        self.driver.get("about:blank")

    def send_message(self, message, type_of_girl='unwritten'):
        text_field = self.driver.find_element('xpath', self.text_area_xpath)
        print('Thinking about what to write...')
        time.sleep(random.uniform(1, 4))
        text_field.send_keys(message)
        print('Typing...')
        time.sleep(random.uniform(4, 10))
        text_field.send_keys(Keys.RETURN)
        print('Message sent')

    # girl_nr is number of girl from the top of the list of message history
    def get_msgs(self, girl_nr=None):
        print('trying to get messages')
        numbered_girl_xpath = f"//div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[{girl_nr}]/div[2]/div[2]/div[1]"
        # entering message history based on number
        if girl_nr:
            self.driver.find_element('xpath', numbered_girl_xpath).click()
        else:
            new_msg_flags = self.driver.find_elements('xpath', self.new_msg_flags_xpath)
            new_msg_flags[0].click()

        print('message history entered')
        # waiting to all message load
        Wait(self.driver, 30).until(ExpCon.presence_of_element_located((By.XPATH, self.messages_xpath)))
        time.sleep(random.uniform(1.5, 4))
        messages = self.driver.find_element('xpath', self.messages_xpath)

        print('messages found')
        # cut off last 5 messages
        #messages = messages[-5:]

        #message_prompt = ''
        #for message in messages:
        #    message_prompt += '- ' + message.text + '\n'
        message_prompt = messages.text

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
