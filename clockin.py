import random
from datetime import datetime, timedelta, date
from dateutil.rrule import rrule, DAILY
from dateutil.relativedelta import relativedelta

from absence import Absence


class ClockIn:

    WORKDAY_HOURS = timedelta(hours=8)
    LUNCH_TIME_SPAN = timedelta(hours=1)
    MAX_TIME_WORKING_BEFORE_LUNCH = timedelta(hours=6).total_seconds()

    entry_hours_set = [8, 9]
    lunch_hours_set = [13, 14, 15]
    minutes_set = [0, 10, 20, 30, 40, 50]

    def __init__(self, year, month, day=None):
        self.year = year
        self.month = month
        self.day = day

        self._absences = None

        self.client = Absence()

    @classmethod
    def randomize(cls, items: list) -> int:
        return random.choice(items)

    @classmethod
    def is_weekday(cls, x: datetime) -> bool:
        return x.weekday() < 5

    @property
    def time_span(self):
        start = date(year=self.year, month=self.month, day=self.day or 1)
        if not self.day:
            return start, start + relativedelta(months=1)

        return start, start + relativedelta(days=1)

    def guess_lunch_break(self, clock_in: datetime):
        lunch_break = datetime(
            year=clock_in.year,
            month=clock_in.month,
            day=clock_in.day,
            hour=self.randomize(self.lunch_hours_set),
            minute=self.randomize(self.minutes_set)
        )
        if (lunch_break - clock_in).total_seconds() > self.MAX_TIME_WORKING_BEFORE_LUNCH:
            return self.guess_lunch_break(clock_in)

        return lunch_break

    @property
    def absences(self):
        if not self._absences:
            start, end = self.time_span
            self._absences = self.client.get_absences_within_period(start=str(start), end=str(end))

        return self._absences

    def one_day(self, day=None) -> None:
        if not date(self.year, self.month, day or self.day) in self.absences:
            clock_in = datetime(
                year=self.year,
                month=self.month,
                day=day or self.day,
                hour=self.randomize(self.entry_hours_set),
                minute=self.randomize(self.minutes_set)
            )
            lunch_break = self.guess_lunch_break(clock_in)
            lunch_stop = lunch_break + self.LUNCH_TIME_SPAN
            worked_hours = lunch_break - clock_in
            remaining_hours = self.WORKDAY_HOURS - worked_hours
            clock_out = lunch_stop + remaining_hours
            # First period (before lunch)
            print(clock_in, lunch_break, lunch_stop, clock_out)
            # self.absence.create_register(start=clock_in, end=lunch_break)
            # Second period (after lunch)
            # self.absence.create_register(start=lunch_stop, end=clock_out)

    def one_month(self) -> None:
        start, end = self.time_span
        for dt in list(rrule(DAILY, dtstart=start, until=end))[:-1]:
            if self.is_weekday(dt):
                self.one_day(day=dt.day)
