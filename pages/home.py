import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .page import Page
from selenium.webdriver.support.select import Select


class Home(Page):

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger

    def select_i_am(self, value="a potential customer"):
        css = 'select[data-placeholder="Select an option"]'
        select = Select(self.get_element_by_css(css))
        select.select_by_visible_text(value)

    def enter_company_name(self, value):
        self.send_by_css("#forminator-field-text-1", value)

    def enter_first_name(self, value):
        self.send_by_css("#forminator-field-first-name-1", value)

    def enter_last_name(self, value):
        self.send_by_css("#forminator-field-last-name-1", value)

    def enter_job_title(self, value):
        self.send_by_css("#forminator-field-text-2", value)

    def enter_email(self, value):
        self.send_by_css("#forminator-field-email-1", value)

    def enter_note(self, value):
        self.send_by_css("#forminator-field-textarea-1", value)

    def click_submit(self, success=True):
        self.click_by_css(".forminator-button-submit")
        if success:
            xpath = '//h2[contains(.,"Thank you!")][contains(@class, "ct-headline")]'
            self.wait_for_element_by_xpath(xpath)
            self.logger.info("Thank you! -> Form submitted ok")