# absence-clock-in

Absence-clock-in is a tool to automate clock in hours of work on absence.

## Usage

### Configuration

Absence-clock-in need python 3.6 or superior. For other hand it need two enviroment variables to work.
They are:

`ABSENCE_EMAIL={your email on absence}`

`ABSENCE_PASS={your password on absence}`

### Clock in one day

Clock in one day, for example 2019-06-4

```python
from clockin import ClockIn


clock_in = ClockIn(2019, 6)
clock_in.one_day(4)
```

### Clock in one month

Clock in one month, It doesn't clock in on weekends, but It don't know your vacations. for example 2019-06:

```python
from clockin import ClockIn


clock_in = ClockIn(2019, 6)
clock_in.one_month()
```

### Using the command line

```bash
python project/commands.py
```

## FUTURE (on develop)

* Improve test
* Cron for clock in every day
* Funtion to clock in range
