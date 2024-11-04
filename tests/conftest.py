import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service  # Import Service class
import os
from sys import platform
from config import *
import logging
import logging.config
import sys
import time

REPORTS = False

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser type: chrome, firefox.")
    parser.addoption("--logger", action="store", default="INFO", help="Logger level: INFO, DEBUG, WARNING ERROR.")
    parser.addoption("--service-args", action="store_true", default=False, help="to enable chrome driver logs")
    parser.addoption("--reports", action="store_true", default=False, help="generate html report")
    parser.addoption("--url", action="store", default="PLEASE PROVIDE URL", help="Url of the site")

@pytest.fixture()
def url(request):
    return request.config.getoption("--url")

@pytest.fixture()
def driver(request):
    global BROWSER
    BROWSER = request.config.getoption("--browser")
    enable_logs = request.config.getoption("--service-args")
    reports = request.config.getoption("--reports")

    if reports:
        global REPORTS
        REPORTS = True
        print("[INFO] Html reports")

    print("[INFO] +++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("[INFO] +++++++++++++++++++++ config ++++++++++++++++++++++++")
    print("[INFO] +++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("[INFO] Browser: {}".format(BROWSER))

    if BROWSER == 'chrome':
        chrome_options = get_chrome_options(False)

        # Set up Chrome service
        if enable_logs:
            chrome_logs = os.path.join(BASE_DIR, "chrome.log")
            service = Service(log_path=chrome_logs)
            print("[INFO] Logging enabled at:", chrome_logs)
        else:
            service = Service()

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'browser': 'ALL'}

        print("[INFO] chromeOptions: %s" % chrome_options.arguments)

        if platform in ('darwin', "linux", "linux2"):
            driver = webdriver.Chrome(options=chrome_options, service=service)
    else:
        print("[ERROR] unrecognized browser: {}".format(BROWSER))
        sys.exit(1)

    print("[INFO] resolution: %s" % driver.get_window_size())
    print("[INFO] +++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # Yield the driver to the test and quit after the test is done
    yield driver
    driver.quit()
