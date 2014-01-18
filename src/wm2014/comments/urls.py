from django.conf.urls import patterns, url


urlpatterns = patterns('wm2014.tipgame.views',
                        (r'^$', 'home'),
                        (r'^Regeln$', 'rules'),
                        (r'^Wertung$', 'evaluation'),
                        (r'^Kontakt$', 'contact'),

                        (r'^Kommentare$', 'comments'),
                        (r'^Kommentare/Heute$', 'comments_today'),
                        (r'^Kommentare/Gestern$', 'comments_yesterday'),
                        (r'^Kommentare/Vorgestern$', 'comments_two_days_ago'),
                        (r'^Kommentare/Alle$', 'comments_all'),
                        (r'^Kommentare/Schreiben$', 'new_comment'),
                        (r'^Kommentare/Danke$', 'new_comment_thanks'),

                        (r'^success/(.*)', 'success'),

                        (r'^Vorrunde$', 'preliminary_round'),
                        (r'^Gruppe([ABCDEFGH])$', 'games', {'round': 'VR'}),
                        (r'^Alle$', 'games', {'round': 'VR'}),
                        (r'^Hauptrunde$', 'main_round'),
                        (r'^Achtelfinale$', 'games', {'round': 'AF'}),
                        (r'^Viertelfinale$', 'games', {'round': 'VF'}),
                        (r'^Halbfinale$', 'games', {'round': 'HF'}),
                        (r'^SpielPlatz3$', 'games', {'round': 'S3'}),
                        (r'^Finale$', 'games', {'round': 'F'}),
                        (r'^Spiel/(\d\d?)/Druck$', 'game_tips_print', {}),
                        (r'^Spiel/(\d\d?)$', 'game_tips', {}),

                        (r'^Spielstand/Vergessen$', 'missing_tips'),
                        (r'^Spielstand/Punkte=(?P<point_digits>\d+\-\d+\-\d+\-\d+)$', 'ranking', {'group': 'Alle'}),
                        (r'^Spielstand/(?P<group>.*)$', 'ranking'),
                        (r'^Spielstand$', 'ranking'),
                        (r'^fail2$', 'fail', {'second': True}),
                        (r'^fail$', 'fail'),
                       )

# urlpatterns += patterns('',
#                         (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#                          {'document_root': 'F:/Python/EM2012/em2012/site_media'}),
#                        )