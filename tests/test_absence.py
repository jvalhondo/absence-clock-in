import responses
from datetime import datetime

from project.absence import Absence


class TestAbsence:

    absence = Absence()

    @responses.activate
    def test_token(self, login_response, absence_token):
        # token
        responses.add(
            responses.POST,
            f'{self.absence.url}/auth/login',
            json=login_response,
            status=200
        )

        assert self.absence.token == absence_token

    @responses.activate
    def test_user_id(
        self,
        login_response,
        authentication_response,
        absence_token,
        absence_user_id
    ):
        # token
        responses.add(
            responses.POST,
            f'{self.absence.url}/auth/login',
            json=login_response,
            status=200
        )
        # authentication
        responses.add(
            responses.GET,
            f'{self.absence.url}/auth/{absence_token}',
            json=authentication_response,
            status=200
        )

        assert self.absence.user_id == absence_user_id

    @responses.activate
    def test_create_register(
        self,
        login_response,
        authentication_response,
        absence_token
    ):
        # token
        responses.add(
            responses.POST,
            f'{self.absence.url}/auth/login',
            json=login_response,
            status=200
        )
        # authentication
        responses.add(
            responses.GET,
            f'{self.absence.url}/auth/{absence_token}',
            json=authentication_response,
            status=200
        )
        # create register
        responses.add(
            responses.POST,
            f'{self.absence.url}/v2/timespans/create',
            json={},
            status=200
        )

        start, end = datetime.now(), datetime.now()

        assert self.absence.create_register(start, end) == 200

    @responses.activate
    def test_get_absences_within_period(
        self,
        login_response,
        authentication_response,
        absence_token,
        absences_response
    ):
        # token
        responses.add(
            responses.POST,
            f'{self.absence.url}/auth/login',
            json=login_response,
            status=200
        )
        # authentication
        responses.add(
            responses.GET,
            f'{self.absence.url}/auth/{absence_token}',
            json=authentication_response,
            status=200
        )
        # absences within period
        responses.add(
            responses.POST,
            f'{self.absence.url}/v2/absences',
            json=absences_response,
            status=200
        )

        start, end = "2019-08-01T00:00:00.000Z", "2019-09-01T00:00:00.000Z",

        assert len(self.absence.get_absences_within_period(start, end)) == 2
