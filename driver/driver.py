from selenium import webdriver
from os import path


def start_driver():
    print('Starting driver')
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # options.add_argument('-profile')
    # options.add_argument('FirefoxProfile')
    script_path = path.dirname(path.abspath(__file__))
    profile = webdriver.FirefoxProfile(f'{script_path}/FirefoxProfile')
    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.maximize_window()
    print('Driver activated')

    return driver