import click
from datetime import datetime

from clockin import ClockIn


@click.command()
@click.option("--year", prompt="Year", type=int, default=datetime.now().year)
@click.option("--month", prompt="Month", type=int, default=datetime.now().month)
@click.option("--day", prompt="Day (leave empty for entire month)", default=0, type=int)
def clockin(year, month, day):
    clock_in = ClockIn(year, month)

    if day == 0:
        clock_in.one_month()
    else:
        clock_in.one_day(day)


if __name__ == "__main__":
    clockin()
