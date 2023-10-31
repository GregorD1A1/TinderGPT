from selenium import webdriver
from os import path


def start_driver(head):
    print('Starting driver')
    options = webdriver.FirefoxOptions()
    if not head:
        options.add_argument('--headless')
    script_path = path.dirname(path.abspath(__file__))
    options.add_argument('-profile')
    options.add_argument(f'{script_path}/FirefoxProfile')
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    print('Driver activated')

    return driver