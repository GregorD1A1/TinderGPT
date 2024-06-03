from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from AI_logic.airtable import girls_to_rise, upsert_record
from AI_logic.misc import translate_rise_msg
import time
import random
import os
import sys


class TinderConnector():
    def __init__(self, driver):
        self.driver = driver
        # xpathes
        self.message_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/button[1]"
        self.match_tab_xpath = "//aside[1]/nav[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]"
        self.new_msg_flag_xpath = "//a[1]/div[1]/div[1]/div[2]"
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/aside[1]/nav[2]/div[1]/div[1]/div[1]/div[3]/div[2]/div[3]/ul[1]/li[1]/a[1]/div[1]/div[1]/div[2]"
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/aside[1]/nav[2]/div[1]/div[1]/div[1]/div[3]/div[2]/div[3]/ul[1]/li[2]/a[1]/div[1]/div[1]/div[2]"
        self.icons_xpath = "//div[1]/div[1]/div[3]/div[1]/ul[1]/li['.']/a[1]/div[1]/div[1]"
        self.messages_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div['.']/div[1]/div[2]"
        self.written_girl_bio_xpath = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.unwritten_girl_full_bio_xpath = "//div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]"
        self.unwritten_girl_short_bio_xpath = \
            "//div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]"
        self.written_girl_name_age_xpath = "//div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]"
        self.main_page_element_for_wait = "//main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]"
        self.text_area_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/form[1]/textarea[1]"
        self.return_to_main_page_xpath = "//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/a[1]/button[1]/*"
        self.name_xpath = "//h1[@class='Typs(display-1-strong) Fxs(1) Fxw(w) Pend(8px) M(0) D(i)']"
        self.close_tnd_gold_enforser_xpath = "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[3]/button[2]/span[1]"
        self.not_opened_girls_css_selector = 'ul > li.P\(8px\)'

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.project_dir = os.path.dirname(os.path.dirname(current_dir))

        self.translate_rise_msg_if_needed()

    def load_main_page(self):
        self.driver.get("https://tinder.com")
        print('Waiting for the main page to load')
        try:
            Wait(self.driver, 120).until(
                ExpCon.presence_of_element_located((By.XPATH, self.main_page_element_for_wait)))
        except TimeoutException:
            time.sleep(random.uniform(0, 10))

        # delay to let gold enforser to appear
        time.sleep(random.uniform(2, 3))
        if self.driver.find_elements('xpath', self.close_tnd_gold_enforser_xpath):
            self.driver.find_element('xpath', self.close_tnd_gold_enforser_xpath).click()
            print('Tinder gold enforcer closed')


    def close_app(self):
        print('Closing Tinder')
        self.driver.get("about:blank")

    def send_messages(self, messages):
        text_field = self.driver.find_element('xpath', self.text_area_xpath)
        for message in messages:
            print('Thinking about what to write...')
            time.sleep(random.uniform(3, 6))
            text_field.send_keys(message)
            print('Typing...')
            time.sleep(random.uniform(6, 11))
            text_field.send_keys(Keys.RETURN)
        print('Messages sent')
        time.sleep(random.uniform(1, 4))
        # return to main page
        self.driver.find_element('xpath', self.return_to_main_page_xpath).click()
        time.sleep(random.uniform(1, 4))

    # girl_nr is number of girl from the top of the list of message history
    def get_msgs(self, girl_nr=None):
        self.enter_messages(girl_nr)
        messages = self.driver.find_elements('xpath', self.messages_xpath)
        print('messages found')
        # cut off last 8 messages
        messages = messages[-8:]

        message_prompt = align_messages(messages)

        return message_prompt

    def enter_messages(self, girl_nr=None):
        print('trying to get messages')
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(1, 1.5))
        # entering message history based on number
        numbered_girl_xpath = f"//div[1]/div[1]/div[3]/div[2]/div[3]/ul[1]/li[{girl_nr}]"
        if girl_nr:
            self.driver.find_element('xpath', numbered_girl_xpath).click()
        else:
            self.driver.find_element('xpath', self.new_msg_flag_xpath).click()

        # waiting to all message load
        Wait(self.driver, 30).until(ExpCon.presence_of_element_located((By.XPATH, self.written_girl_bio_xpath)))
        print('message history entered')
        time.sleep(random.uniform(1.5, 4))

    def count_new_messages(self):
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(1, 2))

        return len(self.driver.find_elements('xpath', self.new_msg_flag_xpath))

    def count_not_opened_girls(self):
        self.driver.find_element('xpath', self.match_tab_xpath).click()
        time.sleep(random.uniform(2, 4))

        number_of_girls = self.driver.find_elements(By.CSS_SELECTOR, self.not_opened_girls_css_selector)
        number_of_girls = len(number_of_girls) - 2

        return number_of_girls

    # gets name_age from opened written girl
    def get_name_age(self):
        name_age = self.driver.find_element('xpath', self.written_girl_name_age_xpath).text
        print(f'Got name_age: {name_age}')
        return name_age

    def get_bio(self, girl_nr=1):
        print('get bio function')
        self.driver.find_element('xpath', self.match_tab_xpath).click()
        time.sleep(random.uniform(2, 4))
        icons = self.driver.find_elements('xpath', self.icons_xpath)
        if len(icons) == 1:
            print('No girls to start a conversation with')
            return
        # number in square brackets is a number of girl to write (from 1)
        icons[girl_nr].click()
        time.sleep(3)
        Wait(self.driver, 45).until(ExpCon.presence_of_element_located((By.XPATH, self.name_xpath)))
        name = self.driver.find_element('xpath', self.name_xpath).text
        # choose short or long bio dependant it short is long enough
        try:
            bio = self.driver.find_element('xpath', self.unwritten_girl_short_bio_xpath).text
        except NoSuchElementException:
            bio = self.driver.find_element('xpath', self.unwritten_girl_full_bio_xpath).text
        else:
            if len(bio) < 50:
                bio = self.driver.find_element('xpath', self.unwritten_girl_full_bio_xpath).text

        return name, bio

    def rise_girls(self):
        # open message tab
        self.driver.find_element('xpath', self.message_tab_xpath).click()
        time.sleep(random.uniform(1, 1.5))

        self.translate_rise_msg_if_needed()
        with open(f'{self.project_dir}/AI_logic/cached_messages/rise_msg.txt', 'r', encoding='utf-8') as file:
            rise_msg = file.read()
            print(rise_msg)

        to_rise = girls_to_rise()
        for girl_nr in range(11, 20):
            print(girl_nr)
            self.enter_messages(girl_nr)
            name_age = self.get_name_age()

            if name_age in to_rise:
                print(f'Rising {name_age}')
                self.send_messages([rise_msg])
                upsert_record(name_age, not_to_rise=True)
                time.sleep(random.uniform(1, 2))

        print("All girls rised")

    def translate_rise_msg_if_needed(self):
        if not os.path.isfile(f'{self.project_dir}/AI_logic/cached_messages/rise_msg.txt'):
            with open(f'{self.project_dir}/AI_logic/cached_messages/rise_msg_orig.txt', 'r', encoding='utf-8') as file:
                orig_rise_msg = file.read()
            rise_msg = translate_rise_msg(orig_rise_msg)
            with open(f'{self.project_dir}/AI_logic/cached_messages/rise_msg.txt', 'w', encoding='utf-8') as file:
                file.write(rise_msg)

# misc functions
def align_messages(messages):
    your_color = 'rgb(255, 255, 255)'
    her_color = 'rgb(33, 38, 46)'
    message_prompt = ''
    for message in messages:
        if message.value_of_css_property('color') == your_color:
            message_prompt += 'You: ' + message.text + '\n'
        elif message.value_of_css_property('color') == her_color:
            message_prompt += 'Girl: ' + message.text + '\n'

    return message_prompt
