#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import unittest
from selenium import webdriver

URL = u'http://localhost:8000'


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        self.browser.get(URL)
        self.login("Rainer", "dk2xwm")

        caption = self.get_caption()
        self.assertEqual("Hallo Rainer,", caption)

    def test_logout(self):
        self.browser.get(URL)
        self.login("Rainer", "dk2xwm")
        self.logout()

        caption = self.get_caption()
        self.assertEqual("Herzlich Willkommen!", caption)

    def login(self, user_name, password):
        input_username = self.browser.find_element_by_id("id_username")
        input_password = self.browser.find_element_by_id("id_password")

        input_username.send_keys(user_name)
        input_password.clear()
        input_password.send_keys(password)
        input_password.submit()

    def logout(self):
        logout_link = self.browser.find_element_by_link_text("Abmelden")
        logout_link.click()

    def get_caption(self):
        heading = self.browser.find_element_by_tag_name("h2")
        return heading.text


if __name__ == '__main__':
    unittest.main()
