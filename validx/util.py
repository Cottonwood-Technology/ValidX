from datetime import timedelta, tzinfo


class UTCTimeZone(tzinfo):
    _offset = timedelta(0)

    def __repr__(self):
        return "<UTC>"

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return self._offset


UTC = UTCTimeZone()
