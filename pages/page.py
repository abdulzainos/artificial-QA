import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException, UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import time
from config import SCREENSHOT_DIR
from config import DOWNLOAD_DIR
import datetime
import pytest
from os import listdir
from os.path import isfile, join


class Page(object):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.css = dict()
        self.css['example'] = "#example-id"

    @property
    def today_time(self):
        today = datetime.date.today()
        return today.strftime('%Y-%m-%d') + " " + datetime.datetime.now().strftime('%H-%M-%S')

    def take_screenshot(self, name, scroll=False):

        today = datetime.date.today()
        folder = today.strftime('%Y-%m-%d')
        file_name = datetime.datetime.now().strftime('%H-%M-%S') + "_" + name
        if not os.path.exists(os.path.join(SCREENSHOT_DIR, folder)):
            os.makedirs(os.path.join(SCREENSHOT_DIR, folder))

        p = os.path.join(SCREENSHOT_DIR, folder, file_name + ".png")
        self.driver.save_screenshot(p)
        self.logger.info("screenshot name: %s", p)

        if scroll:
            self.scroll_into_top()
            p = os.path.join(SCREENSHOT_DIR, folder, file_name + "_scroll.png")
            self.driver.save_screenshot(p)
            self.logger.info("screenshot scroll up name: %s", p)
        return p

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.logger.info("open: %s", url)
        except Exception as err:
            self.logger.error("%s error: %s", err.__class__.__name__, err)
            pytest.fail("open_url: failed: %s" % err)

    @property
    def window_title(self):
        return self.driver.title

    def browser_back(self):
        self.driver.back()

    def get_current_url(self):
        self.logger.info("get_current_url: %s", self.driver.current_url)
        return self.driver.current_url

    def wait_for_url_contains(self, value):
        WebDriverWait(self.driver, 30).until(EC.url_contains(value))
        self.logger.info("wait_for_url_contains: %s", value)

    def get_element_by_css(self, selector_css, time_out=30):

        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, selector_css)), 'get_element_by_css: element timed out: %s' % selector_css)
        except TimeoutException as e:
            pytest.fail("get_element_by_css: failed: %s" % e)

    def is_element_by_css(self, selector_css, time_out=30, visible=False, clickable=False, log=True):

        try:
            if not visible and not clickable:
                WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (presence): element timed out: %s' % selector_css)
            elif visible:
                WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (visibility): element timed out: %s' % selector_css)
            elif clickable:
                WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (clickable): element timed out: %s' % selector_css)
            return True
        except:
            if log:
                self.logger.info("is_element_by_css: [%s] false [%d sec]" % (selector_css, time_out))
            return None

    def is_any_element_visible_by_css(self, selector_css, time_out=30):

        try:
            WebDriverWait(self.driver, time_out).until(EC.visibility_of_any_elements_located((
                By.CSS_SELECTOR, selector_css)), 'is_any_element_visible_by_css: element timed out: %s' % selector_css)
            return True
        except:
            return False

    def is_not_element_by_css(self, selector_css, time_out=30, visible=False, clickable=False):

        try:
            if not visible and not clickable:
                WebDriverWait(self.driver, time_out).until_not(EC.presence_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_not_element_by_css (presence): element timed out: %s' % selector_css)
            elif visible:
                WebDriverWait(self.driver, time_out).until_not(EC.visibility_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_not_element_by_css (visibility): element timed out: %s' % selector_css)
            elif clickable:
                WebDriverWait(self.driver, time_out).until_not(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, selector_css)), 'is_not_element_by_css (clickable): element timed out: %s' % selector_css)
            return True
        except:
            return False

    def get_element_clickable_by_css(self, selector_css, time_out=30):

        try:
            return WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, selector_css)), 'get_element_clickable_by_css: element timed out: %s' % selector_css)
        except Exception as err:
            self.logger.error("get_element_clickable_by_css: %s", err)
            pytest.fail("get_element_clickable_by_css: %s" % err)

    def click_by_css(self, selector_css, settle=False):
        err = ""

        if settle:
            self.wait_until_element_settles(selector_css)

        for _ in range(3):
            try:
                self.get_element_clickable_by_css(selector_css).click()
                return
            except Exception as err:
                self.logger.warning("[%s] click_by_css failed: %s. Don't raise error yet!",
                                    err.__class__.__name__, selector_css)
                time.sleep(1)
        else:
            self.logger.error("click_by_css failed x3: \n%s", err)
            pytest.fail("click_by_css failed: see logs for more details, error: \n%s" % err)

    def click_by_idx(self, selector, idx):

        self.wait_for_element_by_css(selector)

        for _ in range(3):
            try:
                el = self.get_all_elements_by_css(selector)[idx]
                self.ensure_element_by_idx_settles(selector, idx)
                for _ in range(3):
                    if el.is_enabled() and el.is_displayed():
                        el.click()
                        return True
                    else:
                        self.logger.info("click_by_idx: element visible: %s, enabled: %s, selector: %s",
                                         el.is_displayed(), el.is_enabled(), selector)
                        time.sleep(1)
                else:
                    self.logger.error("click_by_idx failed on selector: %s", selector)
                    pytest.fail("click_by_idx: failed on is_enabled & is_displayed. see logs for more details")

            except (StaleElementReferenceException, WebDriverException) as error:
                self.logger.info('%s: click_by_idx on selector: %s. retry', error.__class__.__name__, selector)
                time.sleep(1)
            except Exception as error:
                self.logger.error("%s: click_by_idx failed on selector: %s", error.__class__.__name__, selector)
                pytest.fail("click_by_idx: failed: see logs for more details")
        else:
            self.logger.error("click_by_idx: consecutively failed")
            pytest.fail('Check logs for more details')

    def click_by_xpath(self, xpath):
        for _ in range(3):
            try:
                self.get_element_clickable_by_xpath(xpath).click()
                return
            except Exception as err:
                self.logger.warning("(%s) failed to click on: %s. No error yet!", err.__class__.__name__, xpath)
                time.sleep(1)
        else:
            self.logger.error("click_by_xpath failed x3")
            pytest.fail("click_by_xpath failed: see logs for more details")

    def send_by_css(self, selector_css, value):

        for _ in range(3):
            try:
                el = self.get_element_by_css(selector_css)
                el.clear()
                el.send_keys(value)
                self.logger.info("send_by_css: %s", value)
                return
            except Exception as err:
                self.logger.warning("(%s) failed on: %s", err.__class__.__name__, selector_css)
                time.sleep(1)
        else:
            self.logger.error("send_by_css failed x3")
            pytest.fail("send_by_css failed: see logs for more details")

    def get_element_by_xpath(self, selector_xpath, time_out=30):
        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                By.XPATH, selector_xpath)), 'get_element_by_xpath: element timed out: %s' % selector_xpath)
        except TimeoutException as e:
            self.logger.error("get_element_by_xpath failed")
            pytest.fail("get_element_by_xpath: failed: see logs for more details")

    def get_all_elements_by_css(self, selector_css, time_out=30, visible=False, all_visible=True):

        try:
            if not visible:
                return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, selector_css)), 'get_all_elements_by_css (presence): element timed out: %s' % selector_css)
            elif visible and all_visible:
                return WebDriverWait(self.driver, time_out).until(EC.visibility_of_all_elements_located((
                    By.CSS_SELECTOR, selector_css)), 'get_all_elements_by_css (visibility all): element timed out: %s' % selector_css)
            elif visible and not all_visible:
                return WebDriverWait(self.driver, time_out).until(EC.visibility_of_any_elements_located((
                    By.CSS_SELECTOR, selector_css)),
                    'get_all_elements_by_css (visibility any): element timed out: %s' % selector_css)
        except Exception as e:
            self.logger.error("%s: get_all_elements_by_css error: %s", e.__class__.__name__, e)
            pytest.fail("get_all_elements_by_css: failed: see logs for more details")

    def wait_for_element_by_css(self, selector_css, time_out=30, visible=False, clickable=False):

        try:
            if visible:
                WebDriverWait(self.driver, time_out).until\
                    (EC.visibility_of_element_located((By.CSS_SELECTOR, selector_css)),
                        'wait_for_element_by_css (visible): element timed out: %s' % selector_css)
            elif clickable:
                WebDriverWait(self.driver, time_out).\
                    until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_css)),
                          'wait_for_element_by_css (clickable): element timed out: %s' % selector_css)
            else:
                WebDriverWait(self.driver, time_out).\
                    until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_css)),
                          'wait_for_element_by_css: element timed out: %s' % selector_css)
            return True
        except Exception as e:
            self.logger.error("%s: wait_for_element_by_css: %s", e.__class__.__name__, e)
            pytest.fail("wait_for_element_by_css: failed: %s" % e)

    def wait_until_element_not_visible_by_css(self, selector_css, time_out=30):

        try:
            WebDriverWait(self.driver, time_out).until_not(EC.visibility_of_element_located((
                By.CSS_SELECTOR, selector_css)),
                'wait_until_element_not_visible_by_css: element timed out: %s' % selector_css)
        except Exception as e:
            self.logger.error("%s error: %s", e.__class__.__name__, e)
            pytest.fail("wait_until_element_not_visible_by_css: failed: %s" % e)

    def wait_for_element_by_xpath(self, selector_xpath, time_out=30, visible=False):

        try:
            if visible:
                WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located((
                    By.XPATH, selector_xpath)), 'wait_for_element_by_xpath: element timed out: %s' % selector_xpath)
            else:
                WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                    By.XPATH, selector_xpath)), 'wait_for_element_by_xpath: element timed out: %s' % selector_xpath)
        except Exception as e:
            self.logger.error("%s error: %s", e.__class__.__name__, e)
            pytest.fail("wait_for_element_by_xpath: wait fail.. see logs for more details")

    def wait_until_element_not_present_by_css(self, selector_css, time_out=10):

        try:
            WebDriverWait(self.driver, time_out).until_not(EC.presence_of_element_located((
                By.CSS_SELECTOR, selector_css)), '(not present) element timed out: %s' % selector_css)
        except Exception as e:
            self.logger.error("%s error: %s", e.__class__.__name__, e)
            pytest.fail("wait_until_element_not_present_by_css: see logs for more details")

    def wait_until_element_settles(self, selector, by="css selector"):

        store_location = {}
        for _ in range(30):
            try:
                el = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
                    by, selector)), 'wait_until_element_settles: element timed out: %s' % selector)
                current_location = el.location
                if store_location == current_location:
                    self.logger.info("element |%s| settled at: %s", selector, current_location)
                    return
                else:
                    time.sleep(1)
                    store_location = current_location
            except StaleElementReferenceException:
                self.logger.info("wait_until_element_settles: StaleElementReferenceException")
                time.sleep(1)
            except Exception as e:
                self.logger.error("%s: wait_until_element_settles error: %s", e.__class__.__name__, e)
                pytest.fail("wait_until_element_settles: failed. see logs for more details")
        else:
            pytest.fail('wait_until_element_settles: element has not settled')

    def wait_for_alert(self):
        WebDriverWait(self.driver, 60).until(EC.alert_is_present())

    def accept_alert_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass

    @staticmethod
    def is_alert_present():
        if EC.alert_is_present:
            return True

    def switch_to_iframe(self):
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])

    # random
    # *******

    @property
    def random_number(self):
        return random.randint(1, 10000)

    @property
    def random_quantity(self):
        return random.randint(2, 11)

    def get_random_number(self, range_min, range_max):
        return random.randint(range_min, range_max)

    def delete_browser_storage(self):

        try:
            self.driver.execute_script("window.sessionStorage.clear();")
            self.driver.execute_script("window.localStorage.clear();")
        except Exception as e:
            self.logger.error('delete_browser_storage: failed: %s' % str(e))

    def send_esc_keyboard_key(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ESCAPE).perform()

    def send_enter_keyboard_key(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER).perform()

    def trigger_blur(self, css):
        script = 'document.querySelector("' + css + '").blur()'
        self.driver.execute_script(script)
        self.logger.info("trigger_blur: %s", script)

    # window handlers
    # ------------------------------

    def wait_for_windows(self, windows_count):
        try:
            WebDriverWait(self.driver, 30).until(EC.number_of_windows_to_be(windows_count))
        except TimeoutException as e:
            pytest.fail("wait_for_windows: %s" % e)

    def get_all_window_handles(self):
        return len(self.driver.window_handles)

    def select_recent_open_window(self):
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[-1])
        self.logger.info("select_recent_open_window: title: |%s|, url: %s", self.window_title,
                         self.get_current_url())

    def close_window(self):
        self.driver.close()

    def select_main_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def scroll_into_element(self, element):

        try:
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)
            self.scroll_by()
        except Exception as e:
            pytest.fail("scroll_into_element: %s" % e)

    def scroll_into_top(self):
        try:
            self.logger.info("scroll into the top of the page")
            self.driver.execute_script("window.scrollTo(0, 0);")
        except Exception as err:
            self.logger.error("%s: scroll_into_top: failed: %s", err.__class__.__name__, err)

    def scroll_by(self, y=-100):
        self.driver.execute_script("window.scrollBy(0,%s)" % y)

    @property
    def time_in_ms(self):
        return int(round(time.time() * 1000))

    def browser_logs(self):
        self.logger.info("------------------------")
        self.logger.info("browser logs:")
        self.logger.info("------------------------")
        for entry in self.driver.get_log('browser'):
            self.logger.info(entry)
        self.logger.info("------------------------")

    def refresh_browser(self):
        self.driver.refresh()
        self.logger.info("refresh_browser: ok")

    # download
    def get_all_files(self, file_like=None):

        for _ in range(20):
            files = [f for f in listdir(DOWNLOAD_DIR) if isfile(join(DOWNLOAD_DIR, f))]

            if file_like:
                for f in files:
                    if f.count(file_like):
                        self.logger.info("get_all_files: found file: %s in %s", file_like, files)
                        return files
                self.logger.info("get_all_files: file: |%s| not in %s yet", file_like, files)
                time.sleep(3)
            elif not file_like:
                return files

    def delete_files(self):
        for the_file in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, the_file)
            try:
                if os.path.isfile(file_path) and not the_file == ".gitkeep":
                    os.unlink(file_path)
                    self.logger.info("deleted: %s", file_path)
            except Exception as e:
                self.logger.error("failed to delete files: %s", e)
                pytest.fail("delete_files: failed to delete files")

    # site functions

    def close_cookie_banner(self):
        css = "#hs-eu-cookie-confirmation"
        self.wait_for_element_by_css(css)
        self.click_by_css("#hs-eu-confirmation-button")
        self.wait_until_element_not_visible_by_css(css)
        self.logger.info("Cookie banner closed!")