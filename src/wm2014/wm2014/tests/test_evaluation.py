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

    @mock.patch('wm2014.tipgame.models.timezone', MockNow)
    def test_can_enter_tips_and_get_correct_points(self):

        # It's  June, 11th, 2014
        MockNow.set_now(2014, 6, 11, 10, 0)
        self.assertEqual(datetime.datetime(2014, 6, 11, 10, tzinfo=TZINFO),
                         wm2014.tipgame.models.timezone.now())

        # Edith has been giver a username and a password for the WM2014 tipgame.
        # She visits the homepage
        self.browser.get('http://localhost:8081')

        # and notices the page title is 'WM Tippspiel'
        self.assertIn('WM Tippspiel', self.browser.title)

        # She logs in
        input_username = self.browser.find_element_by_id("id_username")
        input_password = self.browser.find_element_by_id("id_password")

        input_username.send_keys("Edith")
        input_password.clear()
        input_password.send_keys("Rov4b")
        input_password.submit()

        # and is greeted with 'Hallo Edith'
        heading = self.browser.find_element_by_tag_name("h2")
        self.assertEqual("Hallo Edith,", heading.text)

        # She goes to the 'Tipps' page
        link = self.browser.find_element_by_link_text("Tipps")
        link.click()

        # and enters these tips for the first eight games:
        # Group A: 0:0, 0:1,  Group B: 1:0, 1:1,
        # Group C: 0:2, 2:0,  Group D: 1:2, 2:1,
        # and saves them
        tips = [("Gruppe A", [(1, (0, 0)), (2, (0, 1))]),
                ("Gruppe B", [(3, (1, 0)), (4, (1, 1))]),
                ("Gruppe C", [(5, (6, 7)), (6, (8, 9))]),
                ("Gruppe D", [(7, (1, 2)), (8, (2, 1))])]
        for group, games in tips:
            link = self.browser.find_element_by_link_text(group)
            link.click()
            for number, (guess_1, guess_2) in games:
                id_1 = "game{}_guess1".format(number)
                id_2 = "game{}_guess2".format(number)
                input_widget_1 = self.browser.find_element_by_id(id_1)
                input_widget_2 = self.browser.find_element_by_id(id_2)
                input_widget_1.send_keys(guess_1)
                input_widget_2.send_keys(guess_2)
            input_widget_2.submit()

        # She visits 'Alle (chrono.)' ...
        link = self.browser.find_element_by_link_text("Alle (chrono.)")
        link.click()

        # ... and checks that her tips are listed correctly
        inputs = self.browser.find_elements_by_tag_name("input")
        for guess, input_ in zip(guesses_list, inputs[1:]):
            self.assertEqual(str(guess), input_.get_attribute('value'))

        # She logs out
        link = self.browser.find_element_by_link_text("Abmelden")
        link.click()


        # the game results are:
        # Group A: 0:0, 0:1,  Group B: 2:1, 2:2,
        # Group C: 0:3, 3:0,  Group D: 2:1, 1:2,
    # games = Game.objects.all()
    # results = make_results()
    # for game, (result1, result2) in zip(games, results):
    #     game.result1 = result1
    #     game.result2 = result2
    #     game.save()


        # On the 16th of Edith she logs in again

        # and checks that she has got these points_
        # Group A: 6,  Group B: 4, Group C: 2,  Group 0,

        # She visits 'Spielstand' and sees that she is leading the ranking
        # table with 12 points

        # Satisfied, she logs out
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()