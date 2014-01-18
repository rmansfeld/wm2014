from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Country, City, Round, Game, Tip, Player, Comment, Message


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Round)


class GameAdmin(admin.ModelAdmin):
    fieldsets = (('Spiel', {'fields': [('country1', 'country2')]}),
                 ('Details', {'fields': ['round', 'date_time', 'city'],
                              'classes': ['collapse']}),
                 ('Ergebnis', {'fields': [('result1', 'result2')]}))

    readonly_fields = ('date_time', 'city', 'round', 'country1', 'country2')

    list_filter = ('round', 'country1__group')


admin.site.register(Game, GameAdmin)


class TipAdmin(admin.ModelAdmin):
    fieldsets = (('Mitspieler', {'fields': ['participant']}),
                 ('Spiel', {'fields': ['game']}),
                 ('Tipp', {'fields': [('guess1', 'guess2')]}))

    readonly_fields = ('participant', 'game')

    list_filter = ('game__country1__group', 'participant')


admin.site.register(Tip, TipAdmin)


class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'Mitspieler'


class UserAdminWithPlayer(UserAdmin):
    inlines = (PlayerInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdminWithPlayer)

admin.site.register(Comment)
admin.site.register(Message)
