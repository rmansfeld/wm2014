#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import test as djangotest
from django.http import HttpRequest
from django.utils import unittest
from django.core.urlresolvers import resolve, Resolver404
import django.contrib.auth.views

from wm2014.tipgame import views
from wm2014.tipgame.models import User, Round


class TestURLs(unittest.TestCase):

    def test_urls_resolve_to_correct_views(self):
        expected = {'/accounts/login/': (django.contrib.auth.views.login, (), {'template_name': 'tipgame/login.html'}),
                    '/accounts/logout/': (django.contrib.auth.views.logout_then_login, (),
                                          {'login_url': '/accounts/loggedout/?next=/'}),
                    '/accounts/loggedout/': (django.contrib.auth.views.login, (),
                                             {'template_name': 'tipgame/loggedout.html'}),

                    '/': (views.home, (), {}),
                    '/Regeln': (views.rules, (), {}),
                    '/Wertung': (views.evaluation, (), {}),
                    '/Kontakt': (views.contact, (), {}),

                    '/Kommentare': (views.comments, (), {}),
                    '/Kommentare/Heute': (views.comments_today, (), {}),
                    '/Kommentare/Gestern': (views.comments_yesterday, (), {}),
                    '/Kommentare/Vorgestern': (views.comments_two_days_ago, (), {}),
                    '/Kommentare/Alle': (views.comments_all, (), {}),
                    '/Kommentare/Schreiben': (views.new_comment, (), {}),
                    '/Kommentare/Danke': (views.new_comment_thanks, (), {}),

                    '/success/XYZ': (views.success, ('XYZ',), {}),

                    '/Vorrunde': (views.preliminary_round,  (), {}),
                    '/GruppeF': (views.games, ('F',), {'round': 'VR'}),
                    '/Alle': (views.games, (), {'round': 'VR'}),
                    '/Hauptrunde': (views.main_round, (), {}),
                    '/Achtelfinale': (views.games, (), {'round': 'AF'}),
                    '/Viertelfinale': (views.games, (), {'round': 'VF'}),
                    '/Halbfinale': (views.games, (), {'round': 'HF'}),
                    '/Finale': (views.games, (), {'round': 'F'}),
                    '/Spiel/42/Druck': (views.game_tips_print, ('42',), {}),
                    '/Spiel/17': (views.game_tips, ('17',), {}),

                    '/Spielstand/Vergessen': (views.missing_tips, (), {}),
                    '/Spielstand/Punkte=1-2-4-8': (views.ranking, (), {'point_digits': '1-2-4-8', 'group': 'Alle'}),
                    '/Spielstand/VR': (views.ranking, (), {'group': 'VR'}),
                    '/Spielstand': (views.ranking, (), {}),
                    '/fail2': (views.fail, (), {'second': True}),
                    '/fail': (views.fail, (), {})}

        for url, (expected_view, expected_args, expected_kwargs) in expected.iteritems():
            match = resolve(url)
            self.assertEqual(match.func, expected_view)
            self.assertEqual(match.args, expected_args)
            self.assertEqual(match.kwargs, expected_kwargs)

    def test_invalid_urls_raise_404(self):
        invalid_urls = ['/Irgendwas', '/Test',
                        '/Gruppe', '/GruppeX',
                        '/Kommentare/Morgen',
                        '/Spiel',
                        '/Spiel/',
                        '/Spiel/100',
                        '/Spiel/Druck']
        for invalid_url in invalid_urls:
            self.assertRaises(Resolver404, resolve, invalid_url)


class TestHome(djangotest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = User.objects.get(username="Heidi")

    def test_home_returns_correct_html(self):
        response_content = views.home(self.request).content
        self.assertIn('<h2>Hallo Heidi,</h2>', response_content)
        self.assertIn('herzlich Willkommen bei unserem kleinen WM-Spiel.', response_content)

    def test_rules_returns_correct_html(self):
        response_content = views.rules(self.request).content
        self.assertIn('<h2>Regeln</h2>', response_content)
        self.assertIn(u'Für die Teilnahme am Tipp-Spiel gelten folgende Regeln:'.encode("utf-8"), response_content)

    def test_evaluation_returns_correct_html(self):
        self.request.rounds = Round.objects.all()
        response_content = views.evaluation(self.request).content
        self.assertIn('<h2>Wertung</h2>', response_content)
        self.assertIn(u'Die Punkte pro getipptem Spiel werden nach folgendem Schlüssel verteilt:'.encode("utf-8"),
                      response_content)
        self.assertIn('<strong>285 Pkte.</strong>', response_content)

    def test_contact_returns_correct_html(self):
        response_content = views.contact(self.request).content
        self.assertIn('<h2>Kontakt</h2>', response_content)
        self.assertIn('ute.mansfeld@googlemail.com', response_content)
        self.assertIn('rainer@romulo.de', response_content)


class TestTips(djangotest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = User.objects.get(username="Heidi")

    def test_preliminary_round_returns_correct_html(self):
        response_content = views.preliminary_round(self.request).content
        self.assertIn('<h2>Vorrunde</h2>', response_content)
        self.assertIn('Brasilien, Kamerun, Kroatien, Mexiko', response_content)
        self.assertIn('Algerien, Belgien, Korea, Russland', response_content)

    def test_games_group_returns_correct_html(self):
        response_content = views.games(self.request, 'A', round='VR').content
        self.assertIn('<h2>Vorrunde</h2>', response_content)
        self.assertIn('Gruppe A', response_content)
        self.assertIn('Sao Paulo', response_content)
        self.assertIn('Kroatien - Mexiko', response_content)

    def test_games_all_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='VR').content
        self.assertIn('<h2>Vorrunde</h2>', response_content)
        self.assertIn('Brasilien - Kroatien', response_content)
        self.assertIn('Algerien - Russland', response_content)

    def test_main_round_returns_correct_html(self):
        response_content = views.main_round(self.request).content
        self.assertIn('<h2>Hauptrunde</h2>', response_content)
        self.assertIn('K.O-System', response_content)

    def test_games_eighth_final_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='AF').content
        self.assertIn('<h2>Achtelfinale</h2>', response_content)
        self.assertIn('28. Juni, 18:00 Uhr', response_content)
        self.assertIn('01. Juli, 22:00 Uhr', response_content)

    def test_games_quarter_final_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='VF').content
        self.assertIn('<h2>Viertelfinale</h2>', response_content)
        self.assertIn('04. Juli, 18:00 Uhr', response_content)
        self.assertIn('05. Juli, 22:00 Uhr', response_content)

    def test_games_semi_final_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='HF').content
        self.assertIn('<h2>Halbfinale</h2>', response_content)
        self.assertIn('08. Juli, 22:00 Uhr', response_content)
        self.assertIn('09. Juli, 22:00 Uhr', response_content)

    def test_games_third_place_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='S3').content
        self.assertIn('<h2>Spiel um Platz 3</h2>', response_content)
        self.assertIn('12. Juli, 22:00 Uhr', response_content)

    def test_games_final_returns_correct_html(self):
        response_content = views.games(self.request, group=None, round='F').content
        self.assertIn('<h2>Finale</h2>', response_content)
        self.assertIn('13. Juli, 22:00 Uhr', response_content)
