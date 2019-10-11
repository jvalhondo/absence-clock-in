import click

from clockin import ClockIn


@click.command()
@click.option("--year", prompt="Year", type=int)
@click.option("--month", prompt="Month", type=int)
@click.option("--day", prompt="Day (leave empty for entire month)", default=0, type=int)
def clockin(year, month, day):
    clock_in = ClockIn(year, month)
    if day == 0:
        clock_in.one_day(day)
    else:
        clock_in.one_month()


if __name__ == "__main__":
    clockin()
