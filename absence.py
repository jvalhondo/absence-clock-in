import os
import requests
from datetime import datetime
from dateutil.parser import parse


class Absence:

    url = 'https://app.absence.io/api'

    def __init__(self):
        self._authentication = None

    @property
    def token(self) -> str:
        r = requests.post(
            url=f'{self.url}/auth/login',
            json={
                'email': os.environ['ABSENCE_EMAIL'],
                'password': os.environ['ABSENCE_PASS'],
                'company': None,
                'trace': []
            },
            headers={
                'content-type': 'application/json'
            }
        )

        return r.json()['token']

    @property
    def authentication(self) -> dict:
        if self._authentication is None:
            r = requests.get(
                url=f'{self.url}/auth/{self.token}',
                headers={
                    'content-type': 'application/json'
                }
            )
            self._authentication = r.json()

        return self._authentication

    @property
    def user_id(self) -> str:
        return self.authentication['_id']

    def create_register(self, start: datetime, end: datetime):
        r = requests.post(
                url=f'{self.url}/v2/timespans/create',
                json={
                    'userId': self.user_id,
                    '_id': 'new',
                    'timezone': '+0000',
                    'timezoneName': 'hora de verano de Europa central',
                    'type': 'work',
                    'commentary': '',
                    'start': start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'end': end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'trace': []
                },
                headers={
                    'content-type': 'application/json',
                    'x-vacationtoken': self.token
                }
            )

        return r.status_code

        """
        TODO: pending this code section
        try:
            with urllib.request.urlopen(r):
                pass
        except urllib.error.URLError as e:
            message = e.read().decode('utf-8')
            if e.code == 412 and message == 'Los registros no se pueden solapar':
                print(f'Day {self.day} has register hours')
                return False
            else:
                print(f'Error code {e.code} with message {message}')
                raise
        return True
        """

    def get_absences_within_period(self, start: str, end: str) -> list:
        r = requests.post(
            url=f'{self.url}/v2/absences',
            json={
                'filter': {
                    'assignedToId': self.user_id,
                    'status': {'$in': [2]},
                    'start': {
                        '$gte': start,
                        '$lt': end
                    }
                },
                'sortBy': {
                    'start': 1
                }
            },
            headers={
                'content-type': 'application/json',
                'x-vacationtoken': self.token
            }
        )

        return [
            parse(day['date']).date()
            for absence in r.json()['data']
            for day in absence['days']
        ]
