import os
import json
import pytest


os.environ['ABSENCE_EMAIL'] = 'email@domain.com'
os.environ['ABSENCE_PASS'] = '1234asdf'


@pytest.fixture()
def login_response():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'fixtures/login_response.json'
        )
    ) as f:

        return json.loads(f.read())


@pytest.fixture()
def absence_token():
    return '1a1aa11aa1111a11a11aa111'


@pytest.fixture()
def authentication_response():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'fixtures/authentication_response.json'
        )
    ) as f:

        return json.loads(f.read())


@pytest.fixture(scope="class")
def absence_user_id():
    return '000zzz00z00z00000zz00000'


@pytest.fixture()
def absences_response():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'fixtures/absences_response.json'
        )
    ) as f:

        return json.loads(f.read())
