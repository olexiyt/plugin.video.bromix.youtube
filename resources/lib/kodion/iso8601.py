__author__ = 'bromix'

from datetime import date, datetime, timedelta, tzinfo
import re

from .exceptions import KodimonException


def parse(datetime_string):
    def _to_int(value):
        if value is None:
            return 0
        return int(value)

    # match date only '2014-11-08'
    date_only_match = re.match('^(?P<year>[0-9]{4})[-]?(?P<month>[0-9]{2})[-]?(?P<day>[0-9]{2})$', datetime_string)
    if date_only_match:
        return date(_to_int(date_only_match.group('year')),
                    _to_int(date_only_match.group('month')),
                    _to_int(date_only_match.group('day')))

    # full date time
    date_time_match = re.match(
        "^(?P<year>[0-9]{4})[-]?(?P<month>[0-9]{2})[-]?(?P<day>[0-9]{2})[' ''T'](?P<hour>[0-9]{2})[:]?(?P<minute>[0-9]{2})[:]?(?P<second>[0-9]{2})",
        datetime_string)
    if date_time_match:
        return datetime(_to_int(date_time_match.group('year')),
                        _to_int(date_time_match.group('month')),
                        _to_int(date_time_match.group('day')),
                        _to_int(date_time_match.group('hour')),
                        _to_int(date_time_match.group('minute')),
                        _to_int(date_time_match.group('second')))

    # period - at the moment we support only hours, minutes and seconds (e.g. videos and audio)
    period_match = re.match(
        'P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<days>\d+)D)?(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?)?',
        datetime_string)
    if period_match:
        return timedelta(hours=_to_int(period_match.group('hours')),
                         minutes=_to_int(period_match.group('minutes')),
                         seconds=_to_int(period_match.group('seconds')))

    raise KodimonException("Could not parse iso 8601 timestamp '%s'" % datetime_string)
