#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import unittest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission

from wm2014.tipgame.models import (Country, City, Round, Game, Tip, Player,
                                   Comment, Message)

ERROR_MSG = "Found {0} items for model {1}, expected {2}."


class TestInitialData(unittest.TestCase):

    fixtures = ['initial_data.json']

    def test_auth_users(self):
        expected = {ContentType: 14,
                    User: 19,
                    Permission: 42,
                    Country: 32 + 16 + 8 + 4 + 2 + 2,
                    City: 12,
                    Round: 6,
                    Game: 8*6 + 8 + 4 + 2 + 1 + 1,
                    Tip: 0,
                    Player: 19,
                    Comment: 0,
                    Message: 0}

        for model, number_of_items in expected.iteritems():
            items = model.objects.all()
            self.assertEqual(number_of_items, items.count(),
                             ERROR_MSG.format(items.count(), model,
                                              number_of_items))


if __name__ == '__main__':
    unittest.main()
