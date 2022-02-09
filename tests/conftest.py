import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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


@pytest.fixture()
def driver(request):

    global BROWSER
    BROWSER = request.config.getoption("--browser")
    service_args = request.config.getoption("--service-args")
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

        if service_args:
            chrome_logs = os.path.join(BASE_DIR, "chrome.log")
            service_args = ["--verbose", "--log-path=%s" % chrome_logs]
        else:
            service_args = []

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'browser': 'ALL'}

        print("[INFO] chromeOptions: %s" % chrome_options.arguments)

        if platform in ('darwin', "linux", "linux2"):
            d = webdriver.Chrome(options=chrome_options, service_args=service_args)
    else:
        print("[ERROR] unrecognized browser: {}".format(BROWSER))
        sys.exit(1)

    print("[INFO] +++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # d.maximize_window()
    yield driver
    #  teardown
    driver.quit()


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

    # https://www.rkengler.com/how-to-capture-network-traffic-when-scraping-with-selenium-and-python/
    # https://gist.github.com/rengler33/f8b9d3f26a518c08a414f6f86109863c
    # https://stackoverflow.com/questions/69930036/deprecationwarning-desired-capabilities-has-been-deprecated-please-pass-in-a-s
    opts.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

    # https://stackoverflow.com/questions/57298901/unable-to-hide-chrome-is-being-controlled-by-automated-software-infobar-within

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
    :param item:
    """

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if not REPORTS:
        return

    print("[INFO] report.when " + report.when)

    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = str(int(round(time.time() * 1000))) + ".png"
            full_path = os.path.join(report_directory, file_name)
            if item.funcargs.get('driver'):
                print("[INFO] screenshot: " + full_path)
                item.funcargs['driver'].get_screenshot_as_file(full_path)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))

                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("Console errors:")
                print(item.funcargs['driver'].get_log("browser"))
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("Network requests (performance):")
                print(item.funcargs['driver'].get_log("performance"))
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        report.extra = extra