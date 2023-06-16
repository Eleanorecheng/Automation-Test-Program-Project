import pytest
import requests

import os
from dotenv import load_dotenv

from api_objects.login_api import LoginAPI

if 'ENV_FILE' in os.environ:
    load_dotenv(os.environ['ENV_FILE'])
else:
    load_dotenv()

import logging
logger = logging.getLogger()

@pytest.fixture()
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture()
def default_api_login(session, worker_id):
    login_api = LoginAPI(session)

    worker_id = os.environ.get('PYTEST_XDIST_WORKER')
    if worker_id == 'gw0':
        email = os.environ.get('EMAIL_1')
        password = os.environ.get('PASSWORD_1')
    elif worker_id == 'gw1':
        email = os.environ.get('EMAIL_2')
        password = os.environ.get('PASSWORD_2')
    else:
        email = os.environ.get('EMAIL')
        password = os.environ.get('PASSWORD')

    request = login_api.login('native',email, password)
    assert request.response.status_code == 200

    session.headers["Authorization"] = f'Bearer {request.get_json("data")["access_token"]}'
    logger.info("Set token to header")

    return login_api.payload


