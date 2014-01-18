#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import unittest
from selenium import webdriver

URL = u'http://localhost:8000'


class TestMenus(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(URL)
        self.browser.implicitly_wait(3)
        self.login("Rainer", "dk2xwm")
        # self.browser.implicitly_wait(30)
        # self.assertEqual("Hallo Rainer,", self.browser.find_element_by_tag_name("h2").text)

    def tearDown(self):
        self.browser.quit()

    def test_main_menu(self):
        main_menu = self.browser.find_element_by_id("main-menu")
        main_menu_items = main_menu.find_elements_by_tag_name("a")

        expected = [("Home", "/"),
                    ("Tipps", "/Vorrunde"),
                    ("Spielstand", "/Spielstand"),
                    ("Kommentare", "/Kommentare")]

        self.assertEqual(len(expected), len(main_menu_items))
        for (title, link), menu_item in zip(expected, main_menu_items):
            self.assertEqual(title, menu_item.text)
            self.assertEqual(URL+link, menu_item.get_attribute("href"))

    def test_home_menu(self):
        link = self.browser.find_element_by_link_text("Home")
        link.click()

        home_menu = self.browser.find_element_by_id("home-menu")
        home_menu_items = home_menu.find_elements_by_tag_name("a")

        expected = [("Willkommen", "/"),
                    ("Regeln", "/Regeln"),
                    ("Wertung", "/Wertung"),
                    ("Kontakt", "/Kontakt")]

        self.assertEqual(len(expected), len(home_menu_items))
        for (title, link), menu_item in zip(expected, home_menu_items):
            self.assertEqual(title, menu_item.text)
            self.assertEqual(URL+link, menu_item.get_attribute("href"))

    def test_tips_menu(self):
        link = self.browser.find_element_by_link_text("Tipps")
        link.click()

        games_menu = self.browser.find_element_by_id("games-menu")
        games_menu_items = games_menu.find_elements_by_tag_name("a")

        expected = [("Vorrunde", "/Vorrunde"),
                    ("Gruppe A", "/GruppeA"),
                    ("Gruppe B", "/GruppeB"),
                    ("Gruppe C", "/GruppeC"),
                    ("Gruppe D", "/GruppeD"),
                    ("Gruppe E", "/GruppeE"),
                    ("Gruppe F", "/GruppeF"),
                    ("Gruppe G", "/GruppeG"),
                    ("Gruppe H", "/GruppeH"),
                    ("Alle (chrono.)", "/Alle"),
                    ("Hauptrunde", "/Hauptrunde"),
                    ("Achtelfinale", "/Achtelfinale"),
                    ("Viertelfinale", "/Viertelfinale"),
                    ("Halbfinale", "/Halbfinale"),
                    ("Spiel um Platz 3", "/SpielPlatz3"),
                    ("Finale", "/Finale")]

        self.assertEqual(len(expected), len(games_menu_items))
        for (title, link), menu_item in zip(expected, games_menu_items):
            self.assertEqual(title, menu_item.text)
            self.assertEqual(URL+link, menu_item.get_attribute("href"))

    def test_ranking_menu(self):
        link = self.browser.find_element_by_link_text("Spielstand")
        link.click()

        ranking_menu = self.browser.find_element_by_id("ranking-menu")
        ranking_menu_items = ranking_menu.find_elements_by_tag_name("a")

        expected = [("Alle", "/Spielstand"),
                    (u"Männer", "/Spielstand/Maenner"),
                    ("Frauen", "/Spielstand/Frauen"),
                    ("Jugendliche", "/Spielstand/Jugendliche"),
                    ("Erwachsene", "/Spielstand/Erwachsene"),
                    ("Vergessene Tipps", "/Spielstand/Vergessen"),
                    ("Nur Vorrunde", "/Spielstand/Punkte=1-0-0-0"),
                    ("Nur Hauptrunde", "/Spielstand/Punkte=0-4-7-10")]

        self.assertEqual(len(expected), len(ranking_menu_items))
        for (title, link), menu_item in zip(expected, ranking_menu_items):
            self.assertEqual(title, menu_item.text)
            self.assertEqual(URL+link, menu_item.get_attribute("href"))

    def test_comments_menu(self):
        link = self.browser.find_element_by_link_text("Kommentare")
        link.click()

        comments_menu = self.browser.find_element_by_id("comments-menu")
        comments_menu_items = comments_menu.find_elements_by_tag_name("a")

        expected = [("Info", "/Kommentare"),
                    ("Lesen", "/Kommentare/Heute"),
                    ("Heute", "/Kommentare/Heute"),
                    ("Gestern", "/Kommentare/Gestern"),
                    ("Vorgestern", "/Kommentare/Vorgestern"),
                    ("Alle", "/Kommentare/Alle"),
                    ("Schreiben", "/Kommentare/Schreiben")]

        self.assertEqual(len(expected), len(comments_menu_items))
        for (title, link), menu_item in zip(expected, comments_menu_items):
            self.assertEqual(title, menu_item.text)
            self.assertEqual(URL+link, menu_item.get_attribute("href"))

    def login(self, user_name, password):
        input_username = self.browser.find_element_by_id("id_username")
        input_password = self.browser.find_element_by_id("id_password")

        input_username.send_keys(user_name)
        input_password.clear()
        input_password.send_keys(password)
        input_password.submit()


if __name__ == '__main__':
    unittest.main()
