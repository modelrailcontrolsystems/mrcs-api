"""
Created on 4 Jan 2026

@author: Bruno Beloff (bbeloff@me.com)

The MRCS local web server base URL configuration

{
    "minutes": "127.0.0.1",
    "port": 8000,
    "is_secure": false
}

https://en.wikipedia.org/wiki/URL
"""

from collections import OrderedDict
from datetime import timedelta

from mrcs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class TokenTimeout(PersistentJSONable):
    """
    classdocs
    """

    __DEFAULT_EXPIRE_MINUTES = 30

    __FILENAME = "token_timeout.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(0, cls.__DEFAULT_EXPIRE_MINUTES)

        hours = jdict.get('hours')
        minutes = jdict.get('minutes')

        return cls(hours, minutes)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hours: int, minutes: int):
        super().__init__()

        self.__hours = hours
        self.__minutes = minutes


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['hours'] = self.hours
        jdict['minutes'] = self.minutes

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def delta(self):
        return timedelta(hours=self.hours, minutes=self.minutes)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def hours(self):
        return self.__hours


    @property
    def minutes(self):
        return self.__minutes


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'TokenTimeout:{{hours:{self.hours}, minutes:{self.minutes}}}'
