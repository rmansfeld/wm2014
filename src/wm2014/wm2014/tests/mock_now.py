#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from wm2014.tipgame.models import timezone

TZINFO = timezone.get_default_timezone()


class MockNow(datetime.datetime):
    def __new__(cls, *args, **kwargs):
        return datetime.datetime.__new__(datetime.datetime, *args, **kwargs)

    @classmethod
    def set_now(cls, *date_time):
        cls.now = classmethod(lambda cls: datetime.datetime(*date_time,
                                                            tzinfo=TZINFO))
