from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.set_preference('profile', 'FirefoxProfile')
profile_ff = webdriver.FirefoxProfile('FirefoxProfile')
driver = webdriver.Firefox(options=options)
driver.get("https://love.com")
