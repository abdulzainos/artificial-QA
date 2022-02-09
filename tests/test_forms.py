#!/usr/bin/env python

import sys
import os
import pytest

from pages.home import Home


def test_contact_us(driver, logger):

    home = Home(driver, logger)

    home.open_home_page()

    home.close_cookie_banner()

    home.select_i_am("a potential employee")

    home.enter_company_name("artificial")
    home.enter_first_name("tester")
    home.enter_last_name("automation")
    home.enter_job_title("QA")
    home.enter_email("autotester.%s@artificial.com" % home.random_number)
    home.click_submit()
