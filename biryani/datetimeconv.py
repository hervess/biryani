# -*- coding: utf-8 -*-


# Biryani -- A conversion and validation toolbox
# By: Emmanuel Raviart <eraviart@easter-eggs.com>
#
# Copyright (C) 2009, 2010, 2011 Easter-eggs
# http://packages.python.org/Biryani/
#
# This file is part of Biryani.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Date and Time Related Converters

.. note:: Date & time converters are not in :mod:`biryani.baseconv`, because some of them depend from external
   libraries (``mx.DateTime`` & ``pytz``).
"""


import calendar
import datetime

import mx.DateTime

from .baseconv import cleanup_line, function, pipe
from . import states


__all__ = [
    'clean_iso8601_to_date',
    'clean_iso8601_to_datetime',
    'date_to_datetime',
    'date_to_iso8601',
    'date_to_timestamp',
    'datetime_to_date',
    'datetime_to_iso8601',
    'datetime_to_timestamp',
    'iso8601_to_date',
    'iso8601_to_datetime',
    'set_datetime_tzinfo',
    'timestamp_to_date',
    'timestamp_to_datetime',
    ]


# Level-1 Converters


def clean_iso8601_to_date(value, state = states.default_state):
    """Convert a clean string in ISO 8601 format to a date.

    .. note:: For a converter that doesn't require a clean string, see :func:`iso8601_to_date`.

    >>> clean_iso8601_to_date(u'2012-03-04')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'20120304')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04 05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04T05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04 05:06:07+01:00')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04 05:06:07-02:00')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04 05:06:07 +01:00')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'2012-03-04 05:06:07 -02:00')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'20120304 05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> clean_iso8601_to_date(u'today')
    (u'today', u'Value must be a date in ISO 8601 format')
    >>> clean_iso8601_to_date(u'')
    (u'', u'Value must be a date in ISO 8601 format')
    >>> clean_iso8601_to_date(None)
    (None, None)
    """
    if value is None:
        return value, None
    # mx.DateTime.ISO.ParseDateTimeUTC fails when time zone is preceded with a space. For example,
    # mx.DateTime.ISO.ParseDateTimeUTC'2011-03-17 14:46:03 +01:00') raises a"ValueError: wrong format,
    # use YYYY-MM-DD HH:MM:SS" while mx.DateTime.ISO.ParseDateTimeUTC'2011-03-17 14:46:03+01:00') works.
    # So we remove space before "+" and "-".
    while u' +' in value:
        value = value.replace(u' +', '+')
    while u' -' in value:
        value = value.replace(u' -', '-')
    try:
        return datetime.date.fromtimestamp(mx.DateTime.ISO.ParseDateTimeUTC(value)), None
    except ValueError:
        return value, state._(u'Value must be a date in ISO 8601 format')


def clean_iso8601_to_datetime(value, state = states.default_state):
    """Convert a clean string in ISO 8601 format to a datetime.

    .. note:: For a converter that doesn't require a clean string, see :func:`iso8601_to_datetime`.

    >>> clean_iso8601_to_datetime(u'2012-03-04')
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> clean_iso8601_to_datetime(u'20120304')
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04 05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04T05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04 05:06:07+01:00')
    (datetime.datetime(2012, 3, 4, 4, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04 05:06:07-02:00')
    (datetime.datetime(2012, 3, 4, 7, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04 05:06:07 +01:00')
    (datetime.datetime(2012, 3, 4, 4, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'2012-03-04 05:06:07 -02:00')
    (datetime.datetime(2012, 3, 4, 7, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'20120304 05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> clean_iso8601_to_datetime(u'now')
    (u'now', u'Value must be a date-time in ISO 8601 format')
    >>> clean_iso8601_to_datetime(u'')
    (u'', u'Value must be a date-time in ISO 8601 format')
    >>> clean_iso8601_to_datetime(None)
    (None, None)
    """
    if value is None:
        return value, None
    # mx.DateTime.ISO.ParseDateTimeUTC fails when time zone is preceded with a space. For example,
    # mx.DateTime.ISO.ParseDateTimeUTC'2011-03-17 14:46:03 +01:00') raises a"ValueError: wrong format,
    # use YYYY-MM-DD HH:MM:SS" while mx.DateTime.ISO.ParseDateTimeUTC'2011-03-17 14:46:03+01:00') works.
    # So we remove space before "+" and "-".
    while u' +' in value:
        value = value.replace(u' +', '+')
    while u' -' in value:
        value = value.replace(u' -', '-')
    try:
        return datetime.datetime.fromtimestamp(mx.DateTime.ISO.ParseDateTimeUTC(value)), None
    except ValueError:
        return value, state._(u'Value must be a date-time in ISO 8601 format')


def date_to_datetime(value, state = states.default_state):
    """Convert a date object to a datetime.

    >>> import datetime
    >>> date_to_datetime(datetime.date(2012, 3, 4))
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> date_to_datetime(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> date_to_datetime(None)
    (None, None)
    """
    if value is None:
        return value, None
    return datetime.datetime(value.year, value.month, value.day), None


def date_to_iso8601(value, state = states.default_state):
    """Convert a date to a string using ISO 8601 format.

    >>> date_to_iso8601(datetime.date(2012, 3, 4))
    (u'2012-03-04', None)
    >>> date_to_iso8601(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (u'2012-03-04', None)
    >>> date_to_iso8601(None)
    (None, None)
    """
    if value is None:
        return value, None
    return unicode(value.strftime('%Y-%m-%d')), None


def date_to_timestamp(value, state = states.default_state):
    """Convert a datetime to a JavaScript timestamp.

    >>> date_to_timestamp(datetime.date(2012, 3, 4))
    (1330819200000, None)
    >>> date_to_timestamp(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (1330837567000, None)
    >>> date_to_timestamp(None)
    (None, None)
    """
    if value is None:
        return value, None
    return int(calendar.timegm(value.timetuple()) * 1000), None


def datetime_to_date(value, state = states.default_state):
    """Convert a datetime object to a date.

    >>> datetime_to_date(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (datetime.date(2012, 3, 4), None)
    >>> datetime_to_date(datetime.date(2012, 3, 4))
    Traceback (most recent call last):
    AttributeError: 'datetime.date' object has no attribute 'date'
    >>> datetime_to_date(None)
    (None, None)
    """
    if value is None:
        return value, None
    return value.date(), None


def datetime_to_iso8601(value, state = states.default_state):
    """Convert a datetime to a string using ISO 8601 format.

    >>> datetime_to_iso8601(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (u'2012-03-04 05:06:07', None)
    >>> datetime_to_iso8601(datetime.date(2012, 3, 4))
    (u'2012-03-04 00:00:00', None)
    >>> datetime_to_iso8601(None)
    (None, None)
    """
    if value is None:
        return value, None
    return unicode(value.strftime('%Y-%m-%d %H:%M:%S')), None


def datetime_to_timestamp(value, state = states.default_state):
    """Convert a datetime to a JavaScript timestamp.

    >>> datetime_to_timestamp(datetime.datetime(2012, 3, 4, 5, 6, 7))
    (1330837567000, None)
    >>> datetime_to_timestamp(datetime.date(2012, 3, 4))
    (1330819200000, None)
    >>> datetime_to_timestamp(None)
    (None, None)
    """
    if not isinstance(value, datetime.datetime):
        return date_to_timestamp(value, state = state)
    utcoffset = value.utcoffset()
    if utcoffset is not None:
        value -= utcoffset
    return int(calendar.timegm(value.timetuple()) * 1000 + value.microsecond / 1000), None


def set_datetime_tzinfo(tzinfo = None):
    """Return a converter that sets or clears the field tzinfo of a datetime.

    >>> import datetime, pytz
    >>> set_datetime_tzinfo()(datetime.datetime(2011, 1, 2, 3, 4, 5))
    (datetime.datetime(2011, 1, 2, 3, 4, 5), None)
    >>> datetime.datetime(2011, 1, 2, 3, 4, 5, tzinfo = pytz.utc)
    datetime.datetime(2011, 1, 2, 3, 4, 5, tzinfo=<UTC>)
    >>> set_datetime_tzinfo()(datetime.datetime(2011, 1, 2, 3, 4, 5, tzinfo = pytz.utc))
    (datetime.datetime(2011, 1, 2, 3, 4, 5), None)
    >>> set_datetime_tzinfo(pytz.utc)(datetime.datetime(2011, 1, 2, 3, 4, 5))
    (datetime.datetime(2011, 1, 2, 3, 4, 5, tzinfo=<UTC>), None)
    """
    return function(lambda value: value.replace(tzinfo = tzinfo))


def timestamp_to_date(value, state = states.default_state):
    """Convert a JavaScript timestamp to a date.

    >>> timestamp_to_date(123456789.123)
    (datetime.date(1970, 1, 2), None)
    >>> timestamp_to_date(u'123456789.123')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for /: 'unicode' and 'int'
    >>> pipe(str_to_float, timestamp_to_date)(u'123456789.123')
    (datetime.date(1970, 1, 2), None)
    >>> timestamp_to_date(None)
    (None, None)
    """
    if value is None:
        return value, None
    try:
        return datetime.date.fromtimestamp(value / 1000), None
    except ValueError:
        return value, state._(u'Value must be a timestamp')


def timestamp_to_datetime(value, state = states.default_state):
    """Convert a JavaScript timestamp to a datetime.
    
    .. note:: Since a timestamp has no timezone, the generated datetime has no *tzinfo* attribute.
       Use :func:`set_datetime_tzinfo` to add one.

    >>> timestamp_to_datetime(123456789.123)
    (datetime.datetime(1970, 1, 2, 11, 17, 36, 789123), None)
    >>> import pytz
    >>> pipe(timestamp_to_datetime, set_datetime_tzinfo(pytz.utc))(123456789.123)
    (datetime.datetime(1970, 1, 2, 11, 17, 36, 789123, tzinfo=<UTC>), None)
    >>> timestamp_to_datetime(u'123456789.123')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for /: 'unicode' and 'int'
    >>> pipe(str_to_float, timestamp_to_datetime)(u'123456789.123')
    (datetime.datetime(1970, 1, 2, 11, 17, 36, 789123), None)
    >>> timestamp_to_datetime(None)
    (None, None)
    """
    if value is None:
        return value, None
    try:
        # Since a timestamp doesn't containe timezone information, the generated datetime has no timezone (ie naive
        # datetime), so we don't use pytz.utc.
        # return datetime.datetime.fromtimestamp(value / 1000, pytz.utc), None
        return datetime.datetime.fromtimestamp(value / 1000), None
    except ValueError:
        return value, state._(u'Value must be a timestamp')


# Level-2 Converters


iso8601_to_date = pipe(cleanup_line, clean_iso8601_to_date)
"""Convert a string in ISO 8601 format to a date.

    >>> iso8601_to_date(u'2012-03-04')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'20120304')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04 05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04T05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04 05:06:07+01:00')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04 05:06:07-02:00')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04 05:06:07 +01:00')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'2012-03-04 05:06:07 -02:00')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'20120304 05:06:07')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'   2012-03-04   ')
    (datetime.date(2012, 3, 4), None)
    >>> iso8601_to_date(u'today')
    (u'today', u'Value must be a date in ISO 8601 format')
    >>> iso8601_to_date(u'   ')
    (None, None)
    >>> iso8601_to_date(None)
    (None, None)
    """

iso8601_to_datetime = pipe(cleanup_line, clean_iso8601_to_datetime)
"""Convert a string in ISO 8601 format to a datetime.

    >>> iso8601_to_datetime(u'2012-03-04')
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> iso8601_to_datetime(u'20120304')
    (datetime.datetime(2012, 3, 4, 0, 0), None)
    >>> iso8601_to_datetime(u'2012-03-04 05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> iso8601_to_datetime(u'2012-03-04T05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> iso8601_to_datetime(u'2012-03-04 05:06:07+01:00')
    (datetime.datetime(2012, 3, 4, 4, 6, 7), None)
    >>> iso8601_to_datetime(u'2012-03-04 05:06:07-02:00')
    (datetime.datetime(2012, 3, 4, 7, 6, 7), None)
    >>> iso8601_to_datetime(u'2012-03-04 05:06:07 +01:00')
    (datetime.datetime(2012, 3, 4, 4, 6, 7), None)
    >>> iso8601_to_datetime(u'2012-03-04 05:06:07 -02:00')
    (datetime.datetime(2012, 3, 4, 7, 6, 7), None)
    >>> iso8601_to_datetime(u'20120304 05:06:07')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> iso8601_to_datetime(u'   2012-03-04 05:06:07   ')
    (datetime.datetime(2012, 3, 4, 5, 6, 7), None)
    >>> iso8601_to_datetime(u'now')
    (u'now', u'Value must be a date-time in ISO 8601 format')
    >>> iso8601_to_datetime(u'   ')
    (None, None)
    >>> iso8601_to_datetime(None)
    (None, None)
    """

