
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service  # Import Service for updated Selenium setup
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

        # Set up Chrome service for logging if enabled
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

    yield driver  # Return the driver to the test
    driver.quit()  # Teardown after test

@pytest.fixture()
def logger(request):
    level = request.config.getoption("--logger")
    print("[INFO] Logger: {}".format(level))
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger('main')
    log.setLevel(level=logging.getLevelName(level))
    return log

def get_chrome_options(caps=False):
    opts = webdriver.ChromeOptions()
    prefs = dict()
    prefs["download.default_directory"] = DOWNLOAD_DIR
    prefs["credentials_enable_service"] = False
    prefs["password_manager_enabled"] = False
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("disable-extensions")
    opts.add_argument("window-size=1440,900")

    opts.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    if caps:
        return opts.to_capabilities()
    else:
        return opts

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to take and embed screenshots in html report, whenever test fails.
    """

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if not REPORTS:
        return

    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = str(int(round(time.time() * 1000))) + ".png"
            full_path = os.path.join(report_directory, file_name)
            if item.funcargs.get('driver'):
                item.funcargs['driver'].get_screenshot_as_file(full_path)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" '                            'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))

                print("Console errors:")
                print(item.funcargs['driver'].get_log("browser"))
                print("Network requests (performance):")
                print(item.funcargs['driver'].get_log("performance"))

        report.extra = extra
