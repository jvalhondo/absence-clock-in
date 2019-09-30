from .absence import Absence

from datetime import datetime


class ClockIn:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.absence = Absence(year, month)

    def one_day(self, day):
        self.absence.day = day
        entry_time = self.absence.get_entry_time()
        mealtime_start = self.absence.get_mealtime_start(entry_time)
        mealtime_end = mealtime_start + self.absence.TIME_TO_EAT
        time_work_on_morning = mealtime_start - entry_time
        departure_time = self.absence.get_departure_time(mealtime_end, time_work_on_morning)

        if entry_time.date() not in self.absence.holidays:
            self.absence.create_register(entry_time, mealtime_start)
            self.absence.create_register(mealtime_end, departure_time)
        else:
            print(f'You was on holiday at {entry_time.date()}')

    def one_month(self):
        for day in range(1, self.absence.max_day_of_month + 1):
            if datetime(year=self.year, month=self.month, day=day).weekday() < 5:
                self.one_day(day)
