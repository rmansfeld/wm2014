#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from operator import itemgetter
from random import choice
from collections import defaultdict

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .forms import TipForm, CommentForm
from .models import (Player, User, Tip, Round, Game, Country, GROUPS, Comment)
from .charts import make_chart



def get_user(request):
    if request.user.is_authenticated():
        return request.user
    else:
        return None

@login_required
def home(request):
    return render_to_response('tipgame/home/home.html',
                              {'user': get_user(request)})

@login_required
def rules(request):
    return render_to_response('tipgame/home/rules.html',
                              {'user': get_user(request)})

@login_required
def evaluation(request):
    return render_to_response('tipgame/home/evaluation.html',
                              {'rounds': Round.objects.order_by('id'),
                               'user': get_user(request)})


@login_required
def contact(request):
    return render_to_response('tipgame/home/contact.html',
                              {'user': get_user(request)})


@login_required
def comments(request):
    return render_to_response('tipgame/comments/info.html',
                              {'user': get_user(request)})

@login_required
def comments_today(request):
    start_date, end_date = _date_range(days_back=0)
    comments = Comment.objects.filter(date_time__range=(start_date, end_date)).order_by('-date_time')
    return render_to_response('tipgame/comments/read_comments.html',
                              {'comments': comments,
                               'user': get_user(request)})

@login_required
def comments_yesterday(request):
    start_date, end_date = _date_range(days_back=1)
    comments = Comment.objects.filter(date_time__range=(start_date, end_date)).order_by('-date_time')
    return render_to_response('tipgame/comments/read_comments.html',
                              {'comments': comments,
                               'user': get_user(request)})

@login_required
def comments_two_days_ago(request):
    start_date, end_date = _date_range(days_back=2)
    comments = Comment.objects.filter(date_time__range=(start_date, end_date)).order_by('-date_time')
    return render_to_response('tipgame/comments/read_comments.html',
                              {'comments': comments,
                               'user': get_user(request)})

def _date_range(days_back):
    current_date_time = datetime.datetime.today()

    year = current_date_time.year
    month = current_date_time.month
    day = current_date_time.day

    current_date = datetime.datetime(year, month, day, 0, 0)

    start_date = current_date - datetime.timedelta(days=days_back)
    end_date = start_date + datetime.timedelta(days=1)

    return start_date, end_date


@login_required
def comments_all(request):
    comments = Comment.objects.order_by('-date_time')
    return render_to_response('tipgame/comments/read_comments.html',
                              {'comments': comments,
                               'user': get_user(request)})


@login_required
def new_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            user = get_user(request)
            comment = Comment(user=user, text=text)
            comment.save()
            return HttpResponseRedirect('/Kommentare/Danke') # Redirect after POST
    else:
        form = CommentForm() # An unbound form

    return render_to_response('tipgame/comments/write_comment.html',
                              {'form': form,
                               'user': get_user(request)},
                               context_instance=RequestContext(request))

@login_required
def new_comment_thanks(request):
    return comments_today(request)


@login_required
def success(request, path):
    return render_to_response('tipgame/tips/success.html',
                              {'path': path, 'user': request.user})


@login_required
def games(request, group=None, round=None):
    if group is not None:
        games = Game.objects.filter(country1__group=group).order_by('date_time')
        chart = make_chart(games)
    else:
        games = Game.objects.filter(round__short_name__exact=round).order_by('date_time')
        chart = None
    round = games[0].round.name
    finished_tips = []
    open_tips = []

    for game in games:
        tip, _ = Tip.objects.get_or_create(participant=request.user, game=game)
        if game.has_begun():
            finished_tips.append(tip)
        else:
            open_tips.append(tip)

    if request.method == 'POST':
        guesses_1 = request.POST.getlist('guess1')
        guesses_2 = request.POST.getlist('guess2')
        forms = []
        all_valid = True
        for tip, guess_1, guess_2 in zip(open_tips, guesses_1, guesses_2):
            if tip.game.has_begun():
                all_valid = False
            else:
                req = request.POST.copy()
                req['guess1'] = guess_1
                req['guess2'] = guess_2
                form = TipForm(req, instance=tip, auto_id='id_%s_XXX')
                forms.append(form)
                if form.is_valid():
                    form.save()
                else:
                    assert False, "Hallo %s" % form
                    all_valid = False
        if all_valid:
            return HttpResponseRedirect('/success%s' % request.path)
    else:
        forms = [TipForm(instance=tip, auto_id='game{}_%s'.format(tip.game.id))
                     for tip in open_tips]

    return render_to_response('tipgame/tips/games.html',
                              {'group': group,
                               'round': round,
                               'finished_tips': finished_tips,
                               'tips_forms': zip(open_tips, forms),
                               'chart': chart,
                               'user': request.user},
                               context_instance=RequestContext(request))

@login_required
def preliminary_round(request):
    countries = Country.objects.filter(group__in=GROUPS)
    groups_lists = defaultdict(list)
    for country in countries:
        groups_lists[country.group].append(country.name)
    groups =[(group, sorted(members)) for group, members in sorted(groups_lists.iteritems())]

    return render_to_response('tipgame/tips/preliminary_round.html',
                              {'groups': groups,
                               'user': request.user})

@login_required
def main_round(request):
    # MAIN_ROUNDS = ROUNDS[1:]
    # rounds = [(Game.objects.filter(round=token), display)
    #              for (token, display) in MAIN_ROUNDS]
    return render_to_response('tipgame/tips/main_round.html',
                              {'user': request.user})

@login_required
def game_tips(request, game_id):
    game = Game.objects.get(pk=game_id)
    tips = Tip.objects.filter(game=game)
    ordered_tips = tips.order_by('-guess1', 'guess2')

    if game.has_result():
        return render_to_response('tipgame/tips/game_results.html',
                   {'game': game,
                    'points': _points_in_this_round(game),
                    'game_is_not_tie': not game.is_tie(),
                    'tips_kats': _create_point_categories(ordered_tips),
                    'user': request.user})
    else:
        return render_to_response('tipgame/tips/game_tips.html',
                   {'game': game,
                    'tips_kats': _create_tip_categories(ordered_tips),
                    'user': request.user})

@login_required
def game_tips_print(request, game_id):
    game = Game.objects.get(pk=game_id)
    tips = Tip.objects.filter(game=game)
    valid_tips = tips.exclude(guess1__isnull=True).exclude(guess2__isnull=True)
    ordered_tips = tips.order_by('-guess1', 'guess2')
    non_tippers = set(User.objects.all())
    if game.has_result():
        return render_to_response('tipgame/tips/game_results_print.html',
                   {'game': game,
                    'points': _points_in_this_round(game),
                    'game_is_not_tie': not game.is_tie(),
                    'tips_kats': _create_point_categories(ordered_tips),
                    'user': request.user})
    else:
        return render_to_response('tipgame/tips/game_tips_print.html',
                   {'game': game,
                    'tips_kats': _create_tip_categories(ordered_tips),
                    'user': request.user})

# def _points_in_this_round(game):
#     round_factor = game.round_factor()
#     points = {'result': 3 * round_factor,
#               'goal_difference': 2 * round_factor,
#               'tendency': 1 * round_factor}
#     return points

def _points_in_this_round(game):
    points = {'result': game.round.points_for_correct_result,
              'goal_difference': game.round.points_for_correct_goal_difference,
              'tendency': game.round.points_for_correct_tendency}
    return points

def _create_point_categories(tips):
        point_categories = {'result': [], 'goal_difference': [],
                            'tendency': [], 'none': [], 'no_tip': []}

        non_tippers = set(User.objects.all())
        for tip in tips:
            if tip.is_valid():
                tip_tuple = (tip.participant.first_name, tip.guess1, tip.guess2)
                if tip.right_result():
                    point_categories['result'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
                elif tip.right_goal_difference():
                    point_categories['goal_difference'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
                elif tip.right_tendency():
                    point_categories['tendency'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
                else:
                    point_categories['none'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
        point_categories['result'].sort()
        point_categories['no_tip']= sorted(user.first_name for user in non_tippers)
        return point_categories

def _create_tip_categories(tips):
        tip_categories = {'win_1': [], 'win_2': [], 'tie': [], 'no_tip': []}

        non_tippers = set(User.objects.all())
        for tip in tips:
            if tip.is_valid():
                tip_tuple = (tip.participant.first_name, tip.guess1, tip.guess2)
                if tip.guess1 > tip.guess2:
                    tip_categories['win_1'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
                elif tip.guess1 < tip.guess2:
                    tip_categories['win_2'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
                else:
                    tip_categories['tie'].append(tip_tuple)
                    non_tippers.discard(tip.participant)
        tip_categories['no_tip'] = sorted(user.first_name for user in non_tippers)
        return tip_categories


SUB_HEADERS = {'Alle': '',
               'Maenner': 'Nur Männer',
               'Frauen': 'Nur Frauen',
               'Jugendliche': 'Nur Jugendliche',
               'Erwachsene': 'Nur Erwachsene'}

FILTERS = {'Alle': {},
           'Maenner': {'gender': 'M'},
           'Frauen': {'gender': 'F'},
           'Jugendliche': {'age_group': 'J'},
           'Erwachsene': {'age_group': 'N'}}

@login_required
def ranking(request, point_digits='1-4-7-10', group="Alle"):
    sub_header = SUB_HEADERS.get(group, '')
    group_filter = FILTERS.get(group, {})
    point_numbers = point_digits.split('-')
    base_points = dict(zip(('VR', 'VF', 'HF', 'F'),
                           (int(d) for d in point_numbers)))
    player_points = []
    for player in Player.objects.filter(**group_filter):
        points = sum(tip.points(base_points)
                        for tip in player.user.tip_set.all())
        player_points.append((str(player), points))
    player_points.sort(key=itemgetter(0))
    player_points.sort(key=itemgetter(1), reverse=True)
    number_games_played = sum(game.has_result() for game in Game.objects.all())
    return render_to_response('tipgame/ranking/ranking.html',
                              {'sub_header': sub_header,
                               'games_played': number_games_played,
                               'player_points': player_points,
                               'user': request.user})

@login_required
def missing_tips(request):
    all_games = Game.objects.all()
    games_played = all_games.filter(result1__isnull=False).filter(result2__isnull=False)
    missing_tips = Tip.objects.filter(game__result1__isnull=False,
                                      game__result2__isnull=False,
                                      guess1__isnull=True)
    missing_tips =  User.objects.filter(tip__game__result1__isnull=False,
                                        tip__game__result2__isnull=False,
                                        tip__guess1__isnull=True)
    tally = defaultdict(int)
    for user in missing_tips:
        tally[user] += 1
    player_points = list(tally.iteritems())
    player_points.sort(key=itemgetter(0))
    player_points.sort(key=itemgetter(1), reverse=True)
    number_games_played = sum(game.has_result() for game in Game.objects.all())
    return render_to_response('tipgame/ranking/ranking.html',
                              {'sub_header': 'Vergessene Tips ("Liste der Schande")',
                               'games_played': number_games_played,
                               'player_points': player_points,
                               'user': request.user})


def adjust_games():
    games = Game.objects.all()
    for game in games:
        if game.has_ended():
            if not game.has_result():
                game.result1 = random_result()
                game.result2 = random_result()
                game.save()
        else:
            if game.has_result():
                game.result1 = None
                game.result2 = None
                game.save()

goal_numbers = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2,  2, 2, 2, 3, 3, 3, 4, 4, 5)
def random_result():
    return choice(goal_numbers)


@login_required
def fail(request, second=False):
    games = Game.objects.order_by('date_time')
    open_games = [game for game in games if not game.has_begun()]
    if not open_games:
        return render_to_response('tipgame/fail.html',
                                  {'game': "Kein Spiel mehr offen",
                                   'good_players': [],
                                   'lazy_players': [],
                                   'user': get_user(request)})
    if second:
        if len(open_games) > 1:
            next_game = open_games[1]
        else:
            return render_to_response('tipgame/fail.html',
                                      {'game': "Nur noch ein Spiel",
                                       'good_players': [],
                                       'lazy_players': [],
                                       'user': get_user(request)})
    else:
        next_game = open_games[0]

    tips = Tip.objects.filter(game=next_game).exclude(guess1__isnull=True)

    all_users = User.objects.all()
    good_users = [tip.participant for tip in  tips]

    good_players = [user.get_profile() for user in  good_users]
    lazy_players = [user.get_profile() for user in  all_users
                    if user not in good_users]

    return render_to_response('tipgame/fail.html',
                              {'game': next_game,
                               'good_players': good_players,
                               'lazy_players': lazy_players,
                               'user': get_user(request)})
