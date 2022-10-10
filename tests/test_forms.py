#!/usr/bin/env python

from pages.home import Home
from pages.demo import Demo
from pages.brochure import Brochure


def test_contact_us(driver, logger, url):

    home = Home(driver, logger)

    home.open_url(url)

    home.close_cookie_banner()

    home.select_i_am("a potential customer")

    home.enter_company_name("Xaicode")
    home.enter_first_name("Abdul")
    home.enter_last_name("Zainos")
    home.enter_job_title("Owner")
    home.enter_email("abdul@xaicode.com")
    home.enter_note("delete")
    home.click_submit()


def test_demo_request(driver, logger, url):

    demo = Demo(driver, logger)

    demo.open_url(url + "demo-request/")

    demo.close_cookie_banner()

    demo.switch_to_iframe()

    demo.enter_first_name("Abdul")
    demo.enter_last_name("Zainos")
    demo.enter_job_title("Owner")
    demo.enter_company_name("Xaicode")
    demo.enter_email("abdul@xaicode.com")
    demo.enter_country("United States")
    demo.enter_message("delete me")
    demo.click_submit()


def test_brochure(driver, logger, url):

    brochure = Brochure(driver, logger)

    brochure.open_url(url + "brochure/")

    brochure.close_cookie_banner()

    brochure.switch_to_iframe()

    brochure.enter_company_name("Xaicode")
    brochure.enter_first_name("Abdul")
    brochure.enter_last_name("Zainos")
    brochure.enter_job_title("Owner")
    brochure.enter_email("abdul@xaicode.com")
    brochure.click_download()