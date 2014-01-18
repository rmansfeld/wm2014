#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
# from django.utils.timezone import now, get_default_timezone
from django.utils import timezone

# NOW_FOR_TESTS = datetime(2014, 6, 20, 20, 0, tzinfo=timezone.get_default_timezone())


# class Test(models.Model):
#     test_time = models.DateTimeField()
#
#     def __unicode__(self):
#         return unicode(self.test_time)


GROUPS = list('ABCDEFGH')
GROUP_CHOICES = [(char, 'Gruppe ' + char) for char in GROUPS + ['N']]


class Country(models.Model):
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES, verbose_name='Gruppe')

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = "Land"
        verbose_name_plural = u"Länder"


class City(models.Model):
    name = models.CharField(max_length=50)
    stadium = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%5s, %s" % (self.stadium, self.name)

    class Meta:
        verbose_name = "Spielort"
        verbose_name_plural = "Spielorte"


ROUNDS = (('VR', 'Vorrunde'), ('AF', 'Achtelfinale'), ('VF', 'Viertelfinale'),
          ('HF', 'Halbfinale'), ('S3', 'Spiel um Platz 3'), ('F', 'Finale'))
BASE_POINTS = {'VR': 1, 'VF': 4, 'HF': 7, 'F': 10}
POINTS = {'VR': 1, 'VF': 4, 'HF': 7, 'F': 10}


class Round(models.Model):
    name = models.CharField(max_length=20, editable=True)
    short_name = models.CharField(max_length=2, choices=ROUNDS, editable=True)
    points_for_correct_result = models.SmallIntegerField(editable=True)
    points_for_correct_goal_difference = models.SmallIntegerField(editable=True)
    points_for_correct_tendency = models.SmallIntegerField(editable=True)

    def __unicode__(self):
        return u"%s" % (self.name)

    def points_in_this_round(self, game):
        points = {'result': self.points_for_correct_result,
                  'goal_difference': self.points_for_correct_goal_difference,
                  'tendency': self.points_for_correct_tendency}
        return points

    def number_of_games(self):
        return Game.objects.filter(round__exact=self.id).count()

    def maximum_points(self):
        return self.number_of_games() * self.points_for_correct_result

    @classmethod
    def maximum_total_points(cls):
        return sum(round.maximum_points() for round in cls.objects.all())


class Game(models.Model):
    date_time = models.DateTimeField(verbose_name='Datum', editable=True)
    city = models.ForeignKey(City, verbose_name='Spielort', editable=True)
    round = models.ForeignKey(Round, verbose_name='Runde', editable=True)
    country1 = models.ForeignKey(Country, related_name='countryA',
                                 verbose_name='Land 1', editable=True)
    country2 = models.ForeignKey(Country, related_name='countryB',
                                 verbose_name='Land 2', editable=True)
    result1 = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Ergebnis 1', editable=True)
    result2 = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Ergebnis 2', editable=True)

    def __unicode__(self):
        if self.result1 is None or self.result2 is None:
            result = ''
        else:
            result = u"(%s:%s)" % (self.result1, self.result2)
        return u"%5s - %s %s" % (self.country1, self.country2, result)

    def has_begun(self):
##        return self.date_time < Test.objects.get(pk=1).test_time
        return self.date_time - timedelta(minutes=15) < _current_time()

    def has_ended(self):
        return self.date_time + timedelta(hours=1, minutes=45) < _current_time()

    def has_result(self):
        return self.result1 is not None and self.result2 is not None

    def is_tie(self):
        if self.has_result():
            return self.result1 == self.result2
        else:
            raise ValueError

    def round_factor(self, points=BASE_POINTS):
        return points[self.round]

    class Meta:
        ordering = ["date_time"]
        verbose_name = "Spiel"
        verbose_name_plural = "Spiele"


def _current_time():
    try:
        return NOW_FOR_TESTS
    except NameError:
        return timezone.now()


def sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0


class Tip(models.Model):
    participant = models.ForeignKey(User, verbose_name='Mitspieler', editable=False)
    game = models.ForeignKey(Game, verbose_name='Spiel', editable=False)
    guess1 = models.PositiveIntegerField(verbose_name='Tipp 1', null=True, blank=True)
    guess2 = models.PositiveIntegerField(verbose_name='Tipp 2', null=True, blank=True)

    def __unicode__(self):
        if self.is_valid():
            return u"%5s: %s - %s %s:%s" % (self.participant.username,
                                            self.game.country1, self.game.country2,
                                            self.guess1, self.guess2)
        else:
            return u"%5s: %s - %s" % (self.participant.username,
                                            self.game.country1, self.game.country2)

    def is_valid(self):
        return self.guess1 is not None and self.guess2 is not None

    # def points(self, base_points=BASE_POINTS):
    #     points = 0
    #     if self.game.has_result() and self.is_valid():
    #         goal_diff_guess = self.guess1 - self.guess2
    #         goal_diff_result= self.game.result1 - self.game.result2
    #         if self.right_tendency():
    #             points += 1
    #             if self.right_goal_difference():
    #                 points += 1
    #                 if self.right_result():
    #                     points += 1
    #     return points * self.game.round_factor(base_points)

    def points(self, base_points=BASE_POINTS):
        if self.game.has_result() and self.is_valid():
            if self.right_result():
                return self.game.round.points_for_correct_result
            elif self.right_goal_difference():
                return self.game.round.points_for_correct_goal_difference
            elif self.right_tendency():
                return self.game.round.points_for_correct_tendency

        return 0

    def right_tendency(self):
        return sign(self.guess1 - self.guess2) == \
               sign(self.game.result1 - self.game.result2)

    def right_goal_difference(self):
        return self.guess1 - self.guess2 == \
               self.game.result1 - self.game.result2

    def right_result(self):
        return self.guess1 == self.game.result1 and \
               self.guess2 == self.game.result2

    class Meta:
        ordering = ["game", "participant", ]
        unique_together = ("participant", "game")
        verbose_name = "Tipp"


class Player(models.Model):
    GENDER_CHOICES = (('M', 'Mann'), ('F', 'Frau'))
    AGE_GROUP_CHOICES = (('J', 'Jugendlicher'), ('N', 'Erwachsener'))
    user = models.OneToOneField(User, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=1, choices=AGE_GROUP_CHOICES)

    def __unicode__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "Mitspieler"
        verbose_name_plural = "Mitspieler"


class Comment(models.Model):
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
        time_stamp = self.date_time.strftime("%d.%m.%y um %H:%M:%S Uhr")
        return "Kommentar von %s am %s" % (self.user.first_name, time_stamp)

    class Meta:
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"


class Message(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return u"Letzte Meldung: %s" % unicode(self.text)
