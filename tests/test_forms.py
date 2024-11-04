#!/usr/bin/env python

from pages.contact_us import ContactUs
from pages.demo import Demo
from pages.brochure import Brochure

def test_contact_us_home(driver, logger, url):
    contact_us = ContactUs(driver, logger)
    contact_us.open_url(url)

    # Removed contact_us.close_cookie_banner() as it no longer exists

    contact_us.select_i_am("a potential customer")
    contact_us.enter_company_name("Xaicode")
    contact_us.enter_first_name("Abdul")
    contact_us.enter_last_name("Zainos")
    contact_us.enter_job_title("Owner")
    contact_us.enter_email("abdul@xaicode.com")
    contact_us.enter_note(f"delete: tested {url}")
    contact_us.click_submit()

# Uncomment and edit these tests as needed if you want to use them
# Be sure the `close_cookie_banner()` line is not needed anymore

# def test_contact_us(driver, logger, url):
#     contact_us = ContactUs(driver, logger)
#     contact_us.open_url(url + "contact/")
#
#     contact_us.select_i_am("a potential customer")
#     contact_us.enter_company_name("Xaicode")
#     contact_us.enter_first_name("Abdul")
#     contact_us.enter_last_name("Zainos")
#     contact_us.enter_job_title("Owner")
#     contact_us.enter_email("abdul@xaicode.com")
#     contact_us.enter_note(f"delete: tested {url}contact/")
#     contact_us.click_submit()

# def test_demo_request(driver, logger, url):
#     demo = Demo(driver, logger)
#     demo.open_url(url + "demo-request/")
#
#     demo.switch_to_iframe()
#     demo.enter_first_name("Abdul")
#     demo.enter_last_name("Zainos")
#     demo.enter_job_title("Owner")
#     demo.enter_company_name("Xaicode")
#     demo.enter_email("abdul@xaicode.com")
#     demo.enter_country("United States")
#     demo.enter_message("delete me")
#     demo.click_submit()

# def test_brochure(driver, logger, url):
#     brochure = Brochure(driver, logger)
#     brochure.open_url(url + "brochure/")
#
#     brochure.switch_to_iframe()
#     brochure.enter_company_name("Xaicode")
#     brochure.enter_first_name("Abdul")
#     brochure.enter_last_name("Zainos")
#     brochure.enter_job_title("Owner")
#     brochure.enter_email("abdul@xaicode.com")
#     brochure.click_download()
