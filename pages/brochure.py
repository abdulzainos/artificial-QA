import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .page import Page
from selenium.webdriver.support.select import Select


class Brochure(Page):

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger

    def enter_company_name(self, value):
        self.send_by_css("input[name=\"company\"]", value)

    def enter_first_name(self, value):
        self.send_by_css("input[name=\"firstname\"]", value)

    def enter_last_name(self, value):
        self.send_by_css("input[name=\"lastname\"]", value)

    def enter_job_title(self, value):
        self.send_by_css("input[name=\"jobtitle\"]", value)

    def enter_email(self, value):
        self.send_by_css("input[name=\"email\"]", value)

    def click_download(self, success=True):
        self.click_by_css("[value=\"Submit\"]")
        if success:
            self.select_main_window()
            self.wait_for_url_contains("Artificial-Product-Suite-Brochure.pdf")