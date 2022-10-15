import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .page import Page
from selenium.webdriver.support.select import Select


class ContactUs(Page):

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger

    def select_i_am(self, value="a potential customer"):
        css = 'select[data-placeholder="Select an option"]'
        select = Select(self.get_element_by_css(css))
        select.select_by_visible_text(value)

    def enter_company_name(self, value):
        self.send_by_css("input[placeholder=\"your company name\"]", value)

    def enter_first_name(self, value):
        self.send_by_css("input[placeholder=\"your first name\"]", value)

    def enter_last_name(self, value):
        self.send_by_css("input[placeholder=\"your last name\"]", value)

    def enter_job_title(self, value):
        self.send_by_css("input[placeholder=\"your job title\"]", value)

    def enter_email(self, value):
        self.send_by_css("input[placeholder=\"your company email\"]", value)

    def enter_note(self, value):
        self.send_by_css("[placeholder=\"how can we help you?\"]", value)

    def click_submit(self, success=True):
        self.click_by_css(".forminator-button-submit")
        if success:
            xpath = '//h2[contains(.,"Thank you!")][contains(@class, "ct-headline")]'
            self.wait_for_element_by_xpath(xpath)
            self.logger.info("Thank you! -> Form submitted ok")