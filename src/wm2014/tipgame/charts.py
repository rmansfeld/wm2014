from tipgame.models import Country, Game
from operator import itemgetter

def direct_game(country_1, country_2):
    group = country_1.group
    games = Game.objects.filter(country1__group=group)
    game = games.filter(country1=country_1, country2=country_2)
    if game:
        goals_1, goal_2 = game[0].result1, game[0].result2
    else:
        game = games.filter(country1=country_2, country2=country_1)
        if game:
            goals_1, goal_2 = game[0].result2, game[0].result1
        else:
            return 0
    return cmp(goals_1, goal_2)

##def chart_cmp(data_1, data_2):
##    if data_1[1:4] > data_2[1:4]:
##        return 1
##    elif data_1[1:4] < data_2[1:4]:
##        return -1
##    else:
##        dg = direct_game(data_1[0], data_2[0])
##        if dg:
##            return dg
##        else:
##            return cmp(data_1[2], data_2[2])

def chart_cmp(data_1, data_2):
    if data_1[1] > data_2[1]:
        return 1
    elif data_1[1] < data_2[1]:
        return -1
    else:
        dg = direct_game(data_1[0], data_2[0])
        if dg:
            return dg
        else:
            return cmp(data_1[2:4], data_2[2:4])

def make_chart(games):
    group = games[0].country1.group
    countries = Country.objects.filter(group=group)
    data = {}
    for country in countries:
        data[country] = dict(wins=0, losses=0,  ties=0,
                               goals_shot=0,  goals_got=0)
    for game in games:
        country1 = game.country1
        country2 = game.country2
        if game.has_result():
            result1 = game.result1
            result2 = game.result2
            if result1 > result2:
                data[country1]['wins'] += 1
                data[country2]['losses'] += 1
            elif result1 < result2:
                data[country1]['losses'] += 1
                data[country2]['wins'] += 1
            else:
                data[country1]['ties'] += 1
                data[country2]['ties'] += 1
            data[country1]['goals_shot'] += result1
            data[country2]['goals_shot'] += result2
            data[country1]['goals_got'] += result2
            data[country2]['goals_got'] += result1

    charts = []
    for country in countries:
        charts.append((country,
                       data[country]['wins']*3 + data[country]['ties'],
                       data[country]['goals_shot']-data[country]['goals_got'],
                       data[country]['goals_shot'],
                       data[country]['goals_got'],
                       data[country]['wins'] + data[country]['losses'] + data[country]['ties'],
                       data[country]['wins'],
                       data[country]['losses'], data[country]['ties']))
    charts.sort(cmp=chart_cmp, reverse=True)
    return charts

