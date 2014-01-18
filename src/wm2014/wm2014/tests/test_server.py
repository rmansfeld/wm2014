#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import mock
from selenium import webdriver
from django.utils import unittest
from django.test import LiveServerTestCase

import wm2014.tipgame.models

from .mock_now import MockNow, TZINFO


class TestEvaluation(LiveServerTestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # pass
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()