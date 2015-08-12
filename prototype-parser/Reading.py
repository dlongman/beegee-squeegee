import time
import datetime

class Reading(object):
    """
    Represents a single blood glucose reading
    """

    def unix_time(dt):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = dt - epoch
        return delta.total_seconds()

    def unix_time_millis(dt):
        return unix_time(dt) * 1000.0

    def __init__(self, d, t, result, unit):
        """
        Constructs a new instance of a blood glucose reading.

        @param d The date the reading was taken as a string (dd.mm.yyyy)
        @param t The time the reading was taken as a string (hh:mm)
        @param result The value of the blood glucose reading
        @param unit The unit the reading used as a string
        """
        self.datetime = time.strptime(d + t, "%d.%m.%Y%H:%M")
        self.result = result
        self.unit = unit

        self.key = "{0}{1}{2}{3}{4}{5}".format(self.datetime.tm_year, self.datetime.tm_mon, \
                                               self.datetime.tm_mday, self.datetime.tm_hour, \
                                               self.datetime.tm_min, self.datetime.tm_sec)

    def __str__(self):
        return "{0} {1} on {2}\\{3}\\{4} at {5}:{6} [{7}]".format(self.result, self.unit, \
                                               self.datetime.tm_mday, self.datetime.tm_mon, \
                                               self.datetime.tm_year, self.datetime.tm_hour, \
                                               self.datetime.tm_min, self.key)
