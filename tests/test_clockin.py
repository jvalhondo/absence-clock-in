import requests
import responses
from dateutil.parser import parse
from datetime import date, datetime

from project.clockin import ClockIn


class TestClockIn:

    YEAR: int = 2019
    MONTH: int = 8

    clockin = ClockIn(YEAR, MONTH)

    def test_randomize(self):
        assert ClockIn.randomize(self.clockin.lunch_hours_set) in self.clockin.lunch_hours_set

    def test_is_weekday(self):
        dt = parse('2019-08-02')
        assert ClockIn.is_weekday(dt)
        dt = parse('2019-08-03')
        assert not ClockIn.is_weekday(dt)

    def test_time_span(self):
        start, end = date(2019, 8, 1), date(2019, 9, 1)
        assert self.clockin.time_span == (start, end)

        clockin = ClockIn(self.YEAR, self.MONTH, 12)
        start, end = date(2019, 8, 12), date(2019, 8, 13)
        assert clockin.time_span == (start, end)

    def test_guess_lunch_break(self):
        clock_in = datetime(
            year=self.YEAR,
            month=self.MONTH,
            day=12,
            hour=9,
            minute=10
        )
        assert (
            (
                (self.clockin.guess_lunch_break(clock_in) - clock_in).total_seconds()
            ) < self.clockin.MAX_TIME_WORKING_BEFORE_LUNCH
        )

    def test_absences(
        self,
        login_response,
        authentication_response,
        absence_token,
        absences_response
    ):
        # token
        responses.add(
            responses.POST,
            f'{self.clockin.client.url}/auth/login',
            json=login_response,
            status=200
        )
        # authentication
        responses.add(
            responses.GET,
            f'{self.clockin.client.url}/auth/{absence_token}',
            json=authentication_response,
            status=200
        )
        # absences within period
        responses.add(
            responses.POST,
            f'{self.clockin.client.url}/v2/absences',
            json=absences_response,
            status=200
        )

        assert len(self.clockin.absences) == 2
